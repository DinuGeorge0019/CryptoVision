import grpc
from grpc._channel import _Rendezvous
from protos.auth_proto import auth_pb2, auth_pb2_grpc

from django.shortcuts import render, redirect
from django.contrib import messages

from concurrent.futures import ThreadPoolExecutor

from config._credentials import ROOT_CERTIFICATE
from config.settings import SERVER_ADDR_TEMPLATE, PORT
from config._jwt import check_jwt_token
from .interceptors import AuthClientInterceptor

from .forms import RegisterForm


def login_grpc_call(username, password):
    channel_credential = grpc.ssl_channel_credentials(
        ROOT_CERTIFICATE
    )
    
    channel = grpc.secure_channel(
        SERVER_ADDR_TEMPLATE % PORT, channel_credential
    )
    
    interceptors = [AuthClientInterceptor()]
    channel = grpc.intercept_channel(channel, *interceptors)

    stub = auth_pb2_grpc.AuthenticationStub(channel)
    request = auth_pb2.LoginRequest(username=username, password=password)
    response = stub.Login(request)
    return channel, response.token


def register_grpc_call(username, email, password1, password2):
    channel_credential = grpc.ssl_channel_credentials(
        ROOT_CERTIFICATE
    )
    
    channel = grpc.secure_channel(
        SERVER_ADDR_TEMPLATE % PORT, channel_credential
    )
    
    interceptors = [AuthClientInterceptor()]
    channel = grpc.intercept_channel(channel, *interceptors)

    stub = auth_pb2_grpc.AuthenticationStub(channel)
    request = auth_pb2.RegisterRequest(
        username=username, 
        email=email, 
        password1=password1, 
        password2=password2
    )
    response = stub.Register(request)
    return channel, response


def login_view(request):
    # Check if the user is already logged in
    if 'token' in request.session:
        return redirect('client_index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(login_grpc_call, username, password)
                channel, token = future.result()

            request.session['user_id'] = check_jwt_token(token)
            request.session['token'] = token
            
            channel.close()
    
            return redirect('client_index')
        except _Rendezvous as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'An error occurred')
                
    return render(request, 'registration/login.html')


def home_view(request):
    if 'token' in request.session:    
        return redirect('client_index')
    else:
        return render(request, 'main/home.html')


def register_view(request):
    if 'token' in request.session:
        return redirect('client_index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(register_grpc_call, username, email, password1, password2)
                    channel, _ = future.result()

                # Close the channel
                channel.close()

                # If the registration is successful, authenticate and login the user
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(login_grpc_call, username, password1)
                    channel, token = future.result()

                request.session['user_id'] = check_jwt_token(token)
                request.session['token'] = token
                                
                # Close the login channel
                channel.close()

                return redirect('client_index')

            except _Rendezvous as e:
                if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    form.add_error(None, 'Registration failed: ' + str(e.details()))
                else:
                    form.add_error(None, 'An error occurred')
        else:
            print("FORM: Is not valid")
    else:
        form = RegisterForm()
        
    return render(request, 'registration/register.html', {"form": form})

