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

import hashlib
from easytarc_pw_container import PasswordContainer

def create_hash(username, password):
    
    hash_str = username + password

    # Using encode(enc)
    # convert string to byte
    hash_b = hash_str.encode('utf-8')

    h = hashlib.new('whirlpool')
    h.update(hash_b)

    return(h.hexdigest())

def create_license(hash_res):
    with open("EasyTARC_User_License.txt", "w") as file:
        file.write(hash_res)

def start():
    with open('Request_User_License.txt') as f:
        request_user_str = f.read()

    pw_container = PasswordContainer()

    license_hash_salt = pw_container.get_license_hash_salt()

    hash_res = create_hash(request_user_str,license_hash_salt)

    create_license(hash_res)
    

if __name__=='__main__':
    start()
