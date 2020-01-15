#create User object
class User:
    def __init__(self, _id, username, password):
        self.id = _id # different from python keyword 'id' 
        self.username = username
        self.password = password
