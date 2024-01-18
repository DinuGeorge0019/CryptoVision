
import numpy as np
import tensorflow as tf
from joblib import load as joblib_load
from datetime import datetime, timedelta

import json
import base64
import grpc
from protos.auth_proto import auth_pb2, auth_pb2_grpc

from django.shortcuts import render, redirect
from django.core.cache import cache

from config._jwt import check_jwt_token

from concurrent.futures import ThreadPoolExecutor

from config._credentials import ROOT_CERTIFICATE
from config.settings import SERVER_ADDR_TEMPLATE, PORT, CRYPTO_PREDICTION_MODEL_PATH, CRYPTO_SCALER_MODEL_PATH
from modules.main.interceptors import AuthClientInterceptor

from ._blockchain_bitquery_api import get_bitcoin_active_miners_and_value_from_this_week, get_bitcoin_transaction_count_from_this_week, get_bitcoin_mined_blocks_and_value_this_week, get_bitcoin_latest_transactions
from ._blockchain_binance_api import get_crypto_current_prices, get_btc_24hr_ticker, get_crypto_average_prices, get_crypto_hystorical_data, get_top_tokens
from ._blockchain_news_api import get_blockchain_news
from ._blockchain_gpt_api import request_gpt_crypto_analysis

def get_user_grpc_call(user_id):
    channel_credential = grpc.ssl_channel_credentials(
        ROOT_CERTIFICATE
    )
    
    channel = grpc.secure_channel(
        SERVER_ADDR_TEMPLATE % PORT, channel_credential
    )
    
    interceptors = [AuthClientInterceptor()]
    channel = grpc.intercept_channel(channel, *interceptors)

    stub = auth_pb2_grpc.AuthenticationStub(channel)
    request = auth_pb2.GetUserRequest(id=user_id)
    response = stub.GetUser(request)
    return channel, response

def update_user_grpc_call(user_id, username, email, wallet_security_stamp):
    channel_credential = grpc.ssl_channel_credentials(
        ROOT_CERTIFICATE
    )
    
    channel = grpc.secure_channel(
        SERVER_ADDR_TEMPLATE % PORT, channel_credential
    )
    
    interceptors = [AuthClientInterceptor()]
    channel = grpc.intercept_channel(channel, *interceptors)

    stub = auth_pb2_grpc.AuthenticationStub(channel)
    request = auth_pb2.UpdateUserRequest(id=user_id, username=username, email=email, wallet_security_stamp=wallet_security_stamp)
    response = stub.UpdateUser(request)
    return channel, response

def request_password_reset_grpc_call(email):
    channel_credential = grpc.ssl_channel_credentials(
        ROOT_CERTIFICATE
    )
    
    channel = grpc.secure_channel(
        SERVER_ADDR_TEMPLATE % PORT, channel_credential
    )
    
    interceptors = [AuthClientInterceptor()]
    channel = grpc.intercept_channel(channel, *interceptors)

    stub = auth_pb2_grpc.AuthenticationStub(channel)
    request = auth_pb2.RequestPasswordResetRequest(email=email)
    response = stub.RequestPasswordReset(request)
    return channel, response

def reset_password_grpc_call(token, new_password):
    channel_credential = grpc.ssl_channel_credentials(
        ROOT_CERTIFICATE
    )
    
    channel = grpc.secure_channel(
        SERVER_ADDR_TEMPLATE % PORT, channel_credential
    )
    
    interceptors = [AuthClientInterceptor()]
    channel = grpc.intercept_channel(channel, *interceptors)

    stub = auth_pb2_grpc.AuthenticationStub(channel)
    request = auth_pb2.ResetPasswordRequest(token=token, new_password=new_password)
    response = stub.ResetPassword(request)
    return channel, response

def change_user_profile_picture_grpc_call(user_id, encoded_profile_picture):
    channel_credential = grpc.ssl_channel_credentials(
        ROOT_CERTIFICATE
    )
    
    channel = grpc.secure_channel(
        SERVER_ADDR_TEMPLATE % PORT, channel_credential
    )
    
    interceptors = [AuthClientInterceptor()]
    channel = grpc.intercept_channel(channel, *interceptors)

    stub = auth_pb2_grpc.AuthenticationStub(channel)
    request = auth_pb2.UpdateProfilePictureRequest(id=user_id, encoded_profile_picture=encoded_profile_picture)
    response = stub.UpdateProfilePicture(request)
    return channel, response


def __get_crypto_hystorical_data_for_prediction():
            
    def create_series(data, lookback=7*48):  # 7 days, 48 intervals per day
        if len(data) >= lookback:
            return data[-lookback:]  # Return a 2D array
        else:
            print("Not enough data points. Need at least {} data points.".format(lookback))
            return []

    # get the last 7 days of crypto data
    crypto_history_df = get_crypto_hystorical_data('BTCUSDT', 9)

    # Load the scaler
    scaler = joblib_load(CRYPTO_SCALER_MODEL_PATH)

    # Normalize the 'close' column
    crypto_history_data = scaler.transform(crypto_history_df[['close']])

    # Create 7-day series
    crypto_history_data = create_series(crypto_history_data)
    
    return crypto_history_data

def __predict_crypto():

    # Try to get the data from the cache
    predictions = cache.get('crypto_predictions_data')
        
    # If the data is not in the cache, generate it and store it in the cache
    if predictions is None:

        crypto_history_data = __get_crypto_hystorical_data_for_prediction()

        # load the model from disk
        model = tf.keras.models.load_model(CRYPTO_PREDICTION_MODEL_PATH)
                
        # Assuming 'model' is your trained LSTM model
        predictions = []
        
        for _ in range(336):  # For each 30-minute interval of the last week
        # for _ in range(2):  # For each 30-minute interval of the last week
            # Use the last 336 instances to predict the next instance
            X_test = crypto_history_data[-336:]
            X_test = np.reshape(X_test, (1, X_test.shape[0], 1))  # Reshape to be 3-dimensional
            pred = model.predict(X_test)
            
            # Append the predictions to the 'predictions' list
            predictions.extend(pred[0])
            
            # Slide the window forward by 48 instances
            crypto_history_data = np.concatenate((crypto_history_data, pred))
                
        # Cache the data for 30 minutes
        cache.set('crypto_predictions_data', predictions, 1800)

    # Load the scaler
    scaler = joblib_load(CRYPTO_SCALER_MODEL_PATH)

    # Rescale the predictions
    rescaled_predictions = np.array(predictions).reshape(-1, 1)  # Reshape to 2D array
    rescaled_predictions = scaler.inverse_transform(rescaled_predictions)  # Rescale to original format
    rescaled_predictions = rescaled_predictions.flatten()

    # Convert numpy array to Python list
    rescaled_predictions = rescaled_predictions.tolist()

    return rescaled_predictions

def __get_crypto_profit_calculator_advices(current_price, crypto_predictions):
    
    dates = []
    now = datetime.now()
    
    for i in range(len(crypto_predictions)):
        new_date = now + timedelta(minutes=30 * i)
        dates.append(new_date)
    
    # Get the minimum price
    min_price = min(crypto_predictions)
    
    # Find the index of the lowest price
    min_price_index = crypto_predictions.index(min_price)

    # Get the date corresponding to the lowest price
    min_price_date = dates[min_price_index]
    
    # Get the maximum price
    max_price = max(crypto_predictions)

    # Find the index of the highest price
    max_price_index = crypto_predictions.index(max_price)

    # Get the date corresponding to the highest price
    max_price_date = dates[max_price_index]
    
    advices = {
        'when_to_buy_date': [min_price_date.strftime('%Y-%m-%d %H:%M')],
        'minimum_price': [min_price],
        'when_to_sell': [max_price_date.strftime('%Y-%m-%d %H:%M')],
        'maximum_price': [max_price],
        'possible_profit': [max_price - min_price],
        'possible_loss': [max(abs(current_price - min_price), abs(current_price - max_price))]
    }
    
    return advices
    
def __get_gpt35_crypto_advice(crypto_data):
    gpt_response = request_gpt_crypto_analysis(crypto_data)
    return gpt_response

def __encode_wallet_security_stamp():
    s = "'BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'SOLUSDT', 'SHIBUSDT'"
    encoded_s = base64.b64encode(s.encode())
    print(encoded_s)
    
def __decode_wallet_security_stamp(wallet_security_stamp):
    decoded_wallet_security_stamp = base64.b64decode(wallet_security_stamp).decode()
    return decoded_wallet_security_stamp

def client_index(request):
    if 'token' in request.session:
        _ = check_jwt_token(request.session['token'])
                
        with ThreadPoolExecutor(max_workers=11) as executor:
            future1 = executor.submit(get_user_grpc_call, request.session['user_id'])
            channel, user_data = future1.result()
            
            # Get the symbols from the wallet security stamp
            symbols = __decode_wallet_security_stamp(user_data.wallet_security_stamp)
            symbols = symbols.replace("'", "").split(", ")
            
            future2 = executor.submit(__predict_crypto)
            future3 = executor.submit(get_bitcoin_latest_transactions)
            future4 = executor.submit(get_bitcoin_transaction_count_from_this_week)
            future5 = executor.submit(get_bitcoin_active_miners_and_value_from_this_week)
            future6 = executor.submit(get_bitcoin_mined_blocks_and_value_this_week)
            future7 = executor.submit(get_crypto_average_prices, symbols)
            future8 = executor.submit(get_crypto_current_prices, symbols)
            future9 = executor.submit(get_btc_24hr_ticker, symbols)
            future10 = executor.submit(get_blockchain_news)
            future11 = executor.submit(get_top_tokens)

            crypto_predictions_result = future2.result()
            bitcoin_latest_transactions = future3.result()
            transactions_count_this_week = future4.result()
            active_miners_and_value_this_week = future5.result()
            mined_blocks_and_value_this_week = future6.result()
            crypto_average_prices = future7.result()
            crypto_current_prices = future8.result()
            crypto_24hr_ticker = future9.result()
            blockchain_news = future10.result()
            top_tokens = future11.result()
                        
            profit_calculator_advices = __get_crypto_profit_calculator_advices(float(crypto_average_prices['BTCUSDT']), crypto_predictions_result)
            gpt_crypto_advice = __get_gpt35_crypto_advice(profit_calculator_advices)
              
            crypto_data = []
            for symbol in symbols:
                crypto_data.append({
                    'symbol': symbol,
                    'average_price': "{:.6f}".format(float(crypto_average_prices[symbol])),
                    'current_price': "{:.6f}".format(float(crypto_current_prices[symbol])),
                })

            crypto_his_data = []
            for symbol in symbols:
                crypto_his_data.append({
                    'symbol': symbol,
                    'record': get_crypto_hystorical_data(symbol, 8).to_json(orient='records'),
                })
            crypto_his_data = json.dumps(crypto_his_data)
                        
            context = {
                'symbols': symbols,
                'user_data': user_data,
                'crypto_predictions_result': crypto_predictions_result,
                'profit_calculator_advices': profit_calculator_advices,
                'crypto_data': crypto_data,
                'crypto_24hr_ticker': crypto_24hr_ticker,
                'crypto_his_data': crypto_his_data,
                'top_tokens': top_tokens,
                'bitcoin_latest_transactions': bitcoin_latest_transactions['data']['bitcoin']['transactions'],
                'transaction_count_data': transactions_count_this_week['data']['bitcoin']['transactions'],
                'active_miners_and_value_data': active_miners_and_value_this_week['data']['bitcoin']['outputs'],
                'mined_blocks_and_value_data': mined_blocks_and_value_this_week['data']['bitcoin']['transactions'],
                'blockchain_news': blockchain_news,
                'gpt_crypto_advice': gpt_crypto_advice
            }

        channel.close()
        
        return render(request, 'client/client_index.html', context)
        
    else:
        return render(request, 'main/home.html')

def logout_view(request):
    if 'token' in request.session and request.method == 'POST':
        del request.session['token']
        del request.session['user_id']
        return render(request, 'main/home.html')
    else:
        return render(request, 'main/home.html')
    
def save_user_data_view(request):
    if 'token' in request.session and request.method == 'POST':
        _ = check_jwt_token(request.session['token'])

        username = request.POST.get('username')
        email = request.POST.get('email')
        wallet_security_stamp = request.POST.get('wallet_security_stamp')
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                update_user_grpc_call, 
                user_id = request.session['user_id'], 
                username = username, 
                email = email, 
                wallet_security_stamp = wallet_security_stamp
            )
            channel, _ = future.result()
            
        channel.close()
        
    return redirect('client_index')
    
def password_confirmation_view(request):
    if 'token' in request.session and request.method == 'POST':        
        _ = check_jwt_token(request.session['token'])
        
        password_reset_token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        
        print(new_password)
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(reset_password_grpc_call, password_reset_token, new_password)
            channel, _ = future.result()
        
        channel.close()
        
        del request.session['token']
        del request.session['user_id']

    return render(request, 'main/home.html')

def change_user_password_view(request):
    if 'token' in request.session and request.method == 'POST':        
        _ = check_jwt_token(request.session['token'])
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(get_user_grpc_call, request.session['user_id'])
            channel, user_data = future.result()
            
            context = {
                'user_data': user_data,
                'new_password': request.POST.get('new_password'),
            }
        
        channel.close()

        if request.POST.get('new_password') == request.POST.get('confirm_new_password'):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(request_password_reset_grpc_call, user_data.email)
                channel, user_data = future.result()
            channel.close()

        return render(request, 'client/password_confirmation.html', context)
    else:
        return render(request, 'main/home.html')

def change_profile_picture_view(request):
    if 'token' in request.session and request.method == 'POST':
        _ = check_jwt_token(request.session['token'])

        profile_picture_file = request.FILES.get('profile_picture_file')
                
        if profile_picture_file is not None:
            encoded_profile_picture = base64.b64encode(profile_picture_file.read()).decode()
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(change_user_profile_picture_grpc_call, request.session['user_id'], encoded_profile_picture)
                channel, _ = future.result()
            
            channel.close()
        else:
            print("No file was uploaded.")

    return redirect('client_index')
