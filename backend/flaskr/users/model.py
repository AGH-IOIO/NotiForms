class UserD(object):
    def __init__(self):
        self._username = None
        self._email = None

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

    def __repr__(self):
        return "%s<%s>" % (self.username, self.email)
