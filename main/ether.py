import requests 
import sys
import os 
from dotenv import load_dotenv




''' 
    https://api.etherscan.io/api
    ?module=account
    &action=balance
    &address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
    &tag=latest
    &apikey=YourApiKeyToken
'''

'''
    https://api.etherscan.io/api
   ?module=account
   &action=txlist
   &address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   &startblock=0
   &endblock=99999999
   &page=1
   &offset=10
   &sort=asc
   &apikey=YourApiKeyToken
'''

env_path= os.path.join("env_var", ".env")

load_dotenv("env_path")

API_KEY = os.getenv("API_KEY")

BASE_URL = os.getenv("BASE_URL")

ETHER_VALUE = 10 ** 18

ADDRESS = input("Your wallet address: ")

def make_api_url(module, action ,address, *args, **kwargs):
    request_url = f'{BASE_URL}/api?module={module}&action={action}&address={address}&apikey={API_KEY}'
    
    for key,value in kwargs.items():
        request_url += f'&{key}={value}'

    return request_url

get_url = make_api_url('account', 'balance', ADDRESS, tag = 'latest')

# print(get_url)

def get_address_balance(url):

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise sys.exit(e)
    else:
        data = response.json()
        value = int(data['result'])/ETHER_VALUE
        return f"ETHER BALANCE: {value}"

get_balance = get_address_balance(get_url)
print(get_balance)

def get_transaction_type():
    tx_url =  make_api_url(
                            'account', 
                            'txlist', 
                            ADDRESS, 
                            startblock=0, 
                            endblock=99999999, 
                            page=1 ,
                            offset=10, 
                            sort='asc'
                        )
    try:
        response = requests.get(tx_url)
    except requests.exceptions.RequestException:
        raise sys.exit()
    else:
        data = response.json()

        tx_data = data['result']

        # return tx_data[0]

        from datetime import datetime

        for tx in tx_data:
            print('sender address: ', tx['from'])
            print('recepient address: ', tx['to'])
            print('amount: ', int((tx['value']))/ETHER_VALUE)
            print('date & time: ', datetime.fromtimestamp(int(tx['timeStamp'])))
            print('------------------------------')


tx_type = get_transaction_type()
print(tx_type)