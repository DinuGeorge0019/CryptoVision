

import jwt
import datetime
import base64
import time
import uuid
import os

import grpc
from protos.auth_proto import auth_pb2_grpc, auth_pb2
from grpc import StatusCode

from django_grpc_framework.services import Service
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction

from ._google_gmail_api import gmail_send_message
from ._google_drive_api import drive_upload_file, drive_download_file
from config.settings import TOKEN_EXPIRATION, JWT_SECRET, PROFILE_PICTURES_ROOT
from .models import UserPersonalData

# BLACKLIST set at the module level
BLACKLIST = set()

class AuthentificationService(Service):
    
    def __generate_token(self, user):
        # generate a token for the user and return it
        user_info = {
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'user_id': user.id
        }
      
        return jwt.encode(
            {
                'user_info': user_info,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRATION)
            }, 
            JWT_SECRET, 
            algorithm='HS256'
        )
    
    def Login(self, request, context):
        username = request.username
        password = request.password   

        # validate the username and password
        user = authenticate(username=username, password=password)
        if user is None:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid username or password')  

        # generate a token
        token = self.__generate_token(user) 

        return auth_pb2.LoginResponse(token=token)    

    def Logout(self, request, context):
        token = request.token

        # add the token to the blacklist
        BLACKLIST.add(token)

        return auth_pb2.LogoutResponse(message='User logged out successfully')
    
    def Register(self, request, context):
        username = request.username
        email = request.email
        password1 = request.password1
        password2 = request.password2

        # check if a user with the given username already exists
        if User.objects.filter(username=username).exists():
            context.abort(grpc.StatusCode.ALREADY_EXISTS, 'Username is already taken')

        # check if a user with the given email already exists
        if User.objects.filter(email=email).exists():
            context.abort(grpc.StatusCode.ALREADY_EXISTS, 'Email is already taken')

        # check if the passwords match
        if password1 != password2:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Passwords do not match')

        # create a new user
        try:
            with transaction.atomic():
                user = User.objects.create_user(username, email, password1)
                # create an empty UserPersonalData for the user
                UserPersonalData.objects.create(user=user, profile_picture_drive_url="1oSiU7E-CD8X9RkAc-4kQMcc8xvk6sxLf", wallet_security_stamp="xxxxx-xxxxx-xxxxx")
        except ValidationError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        
        context.set_code(StatusCode.OK)
        context.set_details('User registered successfully')
        return auth_pb2.RegisterResponse()


    def RequestPasswordReset(self, request, context):
        email = request.email
        user = get_user_model().objects.filter(email=email).first()
        print(email)
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User with the given email does not exist')

        # generate a password reset token
        token = self.__generate_token(user)

        print("//" + token + "//")
        
        gmail_send_message(
            subject='Password Reset Request',
            body=f'Here is your password reset token: {token}',
            to=email
        )
        
        return auth_pb2.RequestPasswordResetResponse(message='Password reset requested')

    def ResetPassword(self, request, context):
        token = request.token
        new_password = request.new_password
        
        # decode the token
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = payload['user_info']['user_id']
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid or expired token')
        
        user = get_user_model().objects.filter(pk=user_id).first()

        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User not found')

        # change the user's password
        user.set_password(new_password)
        user.save()

        return auth_pb2.ResetPasswordResponse(message='Password reset successfully')
    
    def GetUser(self, request, context):
        user_id = request.id

        # retrieve the user
        user = get_user_model().objects.filter(id=user_id).first()
        
        # retrieve the user's personal data
        user_personal_data = UserPersonalData.objects.filter(user__id=user_id).first()
        
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User not found')

        if not user_personal_data:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User personal data not found')
        
        # download the user's profile picture from Google Drive
        profile_picture_download_path = PROFILE_PICTURES_ROOT + f"{time.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}.png"
        drive_download_file(user_personal_data.profile_picture_drive_url, profile_picture_download_path)
        
        # encode the profile picture to base64
        with open(profile_picture_download_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # delete the temp file
        os.remove(profile_picture_download_path)
                
        # create the response
        response = auth_pb2.GetUserResponse(
            username=user.username,
            email=user.email,
            encoded_profile_picture=encoded_string,
            wallet_security_stamp=user_personal_data.wallet_security_stamp if user_personal_data.wallet_security_stamp else ''
        )

        return response

    
    def UpdateUser(self, request, context):
        # retrieve the user
        user = get_user_model().objects.filter(id=request.id).first()

        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User not found')

        # update the user's data
        user.username = request.username
        user.email = request.email
        user.save()

        # retrieve the user's personal data
        user_personal_data = UserPersonalData.objects.filter(user__id=user.id).first()

        if not user_personal_data:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User personal data not found')

        # update the user's wallet security stamp
        user_personal_data.wallet_security_stamp = request.wallet_security_stamp
        user_personal_data.save()

        # create the response
        response = auth_pb2.UpdateUserResponse(message='User data updated successfully')

        return response
    
    def UpdateProfilePicture(self, request, context):

        # decode the base64 string back to an image
        decoded_image = base64.b64decode(request.encoded_profile_picture)

        # generate a unique filename based on the current time and a random UUID
        filename = f"{time.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}.png"

        # save the decoded image to the media folder
        with open(PROFILE_PICTURES_ROOT + f"{filename}", "wb") as image_file:
            image_file.write(decoded_image)

        # retrieve the user's personal data
        user_personal_data = UserPersonalData.objects.filter(user__id=request.id).first()

        if not user_personal_data:
            context.abort(grpc.StatusCode.NOT_FOUND, 'User personal data not found')

        # update the user's profile picture with the file url from Google Drive
        user_personal_data.profile_picture_drive_url = drive_upload_file(PROFILE_PICTURES_ROOT + f"{filename}")
        user_personal_data.save()

        # delete the temp file
        os.remove(PROFILE_PICTURES_ROOT + f"{filename}")
        
        print("USER PROFILE ID: " + user_personal_data.profile_picture_drive_url)
        
        # create the response
        response = auth_pb2.UpdateProfilePictureResponse(message='Profile picture updated successfully')

        return response
