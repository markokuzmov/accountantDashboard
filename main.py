from dotenv import load_dotenv
import os

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

REDIRECT_URI = 'http://localhost:5000/auth/code'


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
    return render_template("index.html")

@app.route("/auth", methods=['GET'])
def auth():
    return redirect(auth_url)

@app.route("/auth/code", methods=['GET', 'POST'])
def get_token():
    code = request.args.get('code')
    realm_id = request.args.get('realmId')
    
    auth_client.get_bearer_token(auth_code=code, realm_id=realm_id)
    
    os.environ["ACCESS_TOKEN"] = auth_client.access_token
    os.environ["REFRESH_TOKEN"] = auth_client.refresh_token
    
    print(os.getenv('ACCESS_TOKEN'))
    print(os.getenv('REFRESH_TOKEN'))
    
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    
    
