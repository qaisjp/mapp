from flask.ext.login import UserMixin

class User(UserMixin):
    def __init__(self, login_token, attrs):
        self.login_token = login_token
        self.__dict__.update(attrs)

    def get_id(self):
        return self.login_token

    def get_username(self):
        return self.Principal

    def get_friend(self, friend_hash):
        import hashlib
        from config import CRYPTO_SECRET as secret
        from map import flask_redis
        
        all_friends = flask_redis.smembers(self.get_username()+'-friends')
        
        for friend in all_friends:
            hasher = hashlib.sha512()
            hasher.update(friend + str(secret))
            if hasher.hexdigest() == friend_hash:
                return friend
        return ""

    def has_friend(self, friend_hash):
        if self.get_friend(friend_hash) != "":
            return True
        return False

class BannedUser(User):
    def get_friend(self, hash):
        return ""

    def has_friend(self, hash):
        return False