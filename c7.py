import base64
from Crypto.Cipher import AES

def b64_to_raw(b64_string):
    return base64.b64decode(b64_string)

def main():
    # First let's get all of the b64 encoded data from the file 
    with open('7.txt', 'r') as file:
        data = file.read().replace('\n', '')
    
    # Decode the b64 encrypted data into bytes
    encrypted_bytes = b64_to_raw(data)

    # Now we want to decrypt this with aes-128 ecb
    key = b'YELLOW SUBMARINE'
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(encrypted_bytes)
    print(plaintext)


if __name__ == '__main__':
    main()
