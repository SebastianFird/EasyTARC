

class PasswordContainer:
    def __init__(self,):

        self.pw_id = 1
        self.request_password = 'Password_A'
        self.license_password = 'Password_B'
        self.db_password =      'Password_C'

    def get_request_password(self):
        return(self.request_password)
    
    def get_license_password(self):
        return(self.license_password)
    
    def get_db_password(self):
        return(self.db_password)
    
    def get_passwort_id(self):
        return(self.pw_id)