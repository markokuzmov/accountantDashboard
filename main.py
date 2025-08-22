from dotenv import load_dotenv
import os

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

from flask import Flask, render_template, redirect, url_for, request

import requests

from last_reconciled import get_last_reconciled_dates

app = Flask(__name__)

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

REDIRECT_URI = 'http://localhost:5000/auth/code'
BASE_URL = 'https://sandbox-quickbooks.api.intuit.com'


auth_client = AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    environment="sandbox",
)
   
scopes = [
    Scopes.ACCOUNTING,
]

auth_url = auth_client.get_authorization_url(scopes)


@app.route("/", methods=['GET'])
def index():
    logged_in = os.getenv('ACCESS_TOKEN') is not None
    accounts = []
    last_reconciled_dates = []
    
    if logged_in:
        accounts = get_accounts_list()
        last_reconciled_dates = get_last_reconciled_dates(get_account_id_list(accounts))
    
    return render_template("index.html", logged_in=logged_in, accounts=accounts, last_reconciled_dates=last_reconciled_dates)


@app.route("/auth", methods=['GET'])
def auth():
    return redirect(auth_url)


@app.route("/auth/code", methods=['GET', 'POST'])
def get_token():
    code = request.args.get('code')
    realm_id = request.args.get('realmId')
    os.environ["REALM_ID"] = realm_id
    
    auth_client.get_bearer_token(auth_code=code, realm_id=realm_id)
    
    os.environ["ACCESS_TOKEN"] = auth_client.access_token
    os.environ["REFRESH_TOKEN"] = auth_client.refresh_token
    
    return redirect(url_for('index'))


def get_accounts_list():
    access_token = os.getenv('ACCESS_TOKEN')
    realm_id = os.getenv('REALM_ID')
    
    url = BASE_URL + f'/v3/company/{realm_id}/query'
    query = "select Id, Name, AccountType, AccountSubType, Active from Account"
    
    response = requests.get(
        url,
        headers= {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        },
        params={
            "query": query
        }
    )

    data = response.json()
    accounts = data.get("QueryResponse", {}).get("Account", [])
    
    return accounts

def get_account_id_list(accounts):
    account_id_list = []
    for account in accounts:
        account_id_list.append(account["Id"])
    
    return account_id_list


if __name__ == "__main__":
    app.run(debug=True)
    
    
