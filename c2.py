from c1 import hex_to_raw 

def raw_to_hex(byte_string):
    hex_string = ""
    for i in byte_string:
        h = hex(i)
        hs = h[2:]
        if len(hs) == 1:
            hs = '0' + hs
        hex_string += hs
    return hex_string

def fixed_xor(bytes1, bytes2):
    output = []
    for i in range(len(bytes1)):
        output.append(bytes1[i] ^ bytes2[i])
    return output


if __name__ == '__main__':
    hex_string1 = "1c0111001f010100061a024b53535009181c"
    hex_string2 = "686974207468652062756c6c277320657965"
    
    bytes1 = hex_to_raw(hex_string1)
    bytes2 = hex_to_raw(hex_string2)

    xor_val = fixed_xor(bytes1, bytes2)
    
    print(raw_to_hex(xor_val))
