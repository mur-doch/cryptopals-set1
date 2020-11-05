from c2 import raw_to_hex

def ascii_to_raw(msg):
    output = []
    for c in msg:
        output.append(ord(c))
    return output

def repeating_key_xor(byte_string, key):
    output = []
    kindex = 0
    
    for b in byte_string:
        output.append(b ^ key[kindex])
        
        kindex += 1
        if kindex >= len(key):
            kindex = 0
    
    return output

if __name__ == '__main__':
    msg = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE" 
    msg_bytes = ascii_to_raw(msg)
    key_bytes = ascii_to_raw(key)
    encrypted_msg = repeating_key_xor(msg_bytes, key_bytes)
    msg_hex = raw_to_hex(encrypted_msg)
    print(msg_hex)
