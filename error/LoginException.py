class LoginException(Exception):
    def __init__(self):
        super().__init__("Could not log in.")
