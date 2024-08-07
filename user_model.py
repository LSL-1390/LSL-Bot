class User:
    def __init__(self, user_id, username, referred_by=None):
        self.user_id = user_id
        self.username = username
        self.referred_by = referred_by
        self.referrals = []
        self.balance = 0.0

    def add_referral(self, user):
        self.referrals.append(user)
        
    def add_balance(self, amount):
        self.balance += amount
