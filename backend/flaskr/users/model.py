class UserD(object):
    def __init__(self):
        self._username = None
        self._email = None
        self._password = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_username):
        self._username = new_username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email

    @property
    def password(self):
        return self._email

    @password.setter
    def password(self, new_password):
        self._password = new_password

    def as_dict(self):
        return {
            "email": self.email,
            "username": self.username
        }
