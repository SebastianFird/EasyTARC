import hashlib
from easytarc_password_container import PasswordContainer

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

    license_password = pw_container.get_license_password()

    hash_res = create_hash(request_user_str,license_password)
    print(hash_res)

    create_license(hash_res)
    

if __name__=='__main__':
    start()
