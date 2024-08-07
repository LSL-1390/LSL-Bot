import os
from dotenv import load_dotenv
from user_model import User
from transaction_model import Transaction

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

users = {}
transactions = []

def register_user(user_id, username, referred_by=None):
    if user_id not in users:
        users[user_id] = User(user_id, username, referred_by)
        if referred_by and referred_by in users:
            users[referred_by].add_referral(users[user_id])

def add_transaction(user_id, amount, description):
    transaction = Transaction(user_id, amount, description)
    transactions.append(transaction)
    users[user_id].add_balance(amount)
