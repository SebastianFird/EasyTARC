'''
Copyright 2023 Sebastian Feiert

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
__author__ = 'Sebastian Feiert'

import getpass
import os
import hashlib

class Authorisation():

    def __init__(self,algorithm):
        self.algorithm = algorithm
        self.request_hash_complement= 'hash_complement_A'
        self.permission_hash_complement = 'hash_complement_B'
        self.user_db_hash_complement = 'hash_complement_X' #hash_complement_X

    def create_user_data_str(self,str_format):
        if str_format == 'u':
            user_data_str = str(getpass.getuser()).upper()
        elif str_format == 'l':
            user_data_str = str(getpass.getuser()).lower()
        else:
            None
        return(user_data_str)

    def create_hash(self,str_1, str_2):
        hash_str = str_1 + str_2
        hash_b = hash_str.encode('utf-8')
        h = hashlib.new(self.algorithm)
        h.update(hash_b)
        return(h.hexdigest())
    
    def create_user_request_hash(self,str_format):
        user_data_str = self.create_user_data_str(str_format)
        hash_res = 'req_' + self.create_hash(user_data_str,self.request_hash_complement)
        return(hash_res)
    
    def create_permission_hash(self,hash_res):
        permission_hash = self.create_hash(hash_res,self.permission_hash_complement)
        return(permission_hash)
    
    def create_user_permission_hash(self,str_format):
        hash_res = self.create_user_request_hash(str_format)
        permission_hash = self.create_hash(hash_res,self.permission_hash_complement)
        return(permission_hash)
    
    def create_user_db_password(self,str_format):
        user_data_str = self.create_user_data_str(str_format)
        user_db_password = self.create_hash(user_data_str,self.user_db_hash_complement)
        return(user_db_password)
    
    def create_salt(self):
        salt = os.urandom(16)
        salt = str(hashlib.sha256(salt).hexdigest())
        return(salt)
