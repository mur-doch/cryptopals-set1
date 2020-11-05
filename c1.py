import base64, binascii

b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def hex_to_raw(hex_string):
    return binascii.unhexlify(hex_string)

def raw_to_b64(raw_bytes):
    # Taking a list of b64 index values, outputs a b64 encoded string
    output = ""
    for i in raw_bytes:
        output += b64_chars[i]
    return output

def hex_to_b64(hex_bytes):
    b64 = []
    for i in range(0, len(hex_bytes), 3):
        # where ls1 is the least significant b64 digit and ls4 is the most
        ls1 = hex_bytes[i+2] & 63
        ls2 = ((hex_bytes[i+2] & 192) >> 6) + ((hex_bytes[i+1] & 15) << 2)
        ls3 = ((hex_bytes[i+1] & 240) >> 4) + ((hex_bytes[i] & 3) << 4)
        ls4 = (hex_bytes[i] & 252) >> 2 
        b64.extend([ls4, ls3, ls2, ls1])

    return b64

if __name__ == '__main__':
    hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    hex_raw = hex_to_raw(hex_string)
    b64_raw = hex_to_b64(hex_raw)
    print(raw_to_b64(b64_raw))
