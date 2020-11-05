from c1 import hex_to_raw
import string

character_frequencies = {
    'e': 12.02,
    't': 9.10,
    'a': 8.12,
    'o': 7.68,
    'i': 7.31,
    'n': 6.95,
    's': 6.28, 
    'r': 6.02,
    'h': 5.92,
    'd': 4.32,
    'l': 3.98,
    'u': 2.88,
    'c': 2.71,
    'm': 2.61,
    'f': 2.30,
    'y': 2.11,
    'w': 2.09,
    'g': 2.03,
    'p': 1.82,
    'b': 1.49,
    'v': 1.11,
    'k': 0.69,
    'x': 0.17,
    'q': 0.11,
    'j': 0.10,
    'z': 0.07
}

def get_frequencies(text):
    # initialize the dictionary to have all chars
    odict = {}
    for c in string.ascii_lowercase:
        odict[c] = 0

    # Count the number of each character in the string.
    # we're counting punctuation here
    # I'm doing it separately because I want to guarantee that the chars
    # are in the dict, but the punctuation will be evaluated as all being
    # the same.
    for c in text:
        if c in odict.keys():
            odict[c] += 1
        else:
            odict[c] = 1
    
    # Calculate the frequencies of each character in the text.
    length = len(text)
    if length != 0:
        for c in odict.keys():
            odict[c] /= length
            odict[c] *= 100

    return odict


def score_english(text):
    frequencies = get_frequencies(text)
    # character_frequencies
    score = 0 
    for c in frequencies.keys():
        if c in character_frequencies.keys():
            score += abs(frequencies[c] - character_frequencies[c])
        elif c == ' ':
            score += 0
        elif c in "'\"!.?" or c in string.digits:
            score += 15
        else:
            score += 100
    return score

def bytes_to_string(byte_string):
    output = ""
    for i in byte_string:
        output += chr(i)
    return output

def xor(byte_string, key):
    output = b''
    key_val = key[0] # from key of type bytes to int
    for b in byte_string:
        output += bytes([b ^ key_val])
    return output

def decrypt_single_xor(hex_string):
    byte_string = hex_to_raw(hex_string)
    
    lowest_score = 100000
    lowest_string = ""
    
    for c in string.printable:
        xor_result = xor(byte_string, bytes([ord(c)]))
        xor_string = bytes_to_string(xor_result)
        score = score_english(xor_string)
        if score < lowest_score:
            lowest_score = score
            lowest_string = xor_string
    
    return lowest_string, c

def decrypt_block_xor(byte_string):
    lowest_score = 100000
    lowest_string = ""
    lowest_c = ""

    for c in string.printable:
        xor_result = xor(byte_string, bytes([ord(c)]))
        xor_string = bytes_to_string(xor_result)
        score = score_english(xor_string)
        if score < lowest_score:
            lowest_score = score
            lowest_string = xor_string
            lowest_c = c
    
    return bytes([ord(lowest_c)])

if __name__ == '__main__':
    b = b'\x3C'
    print(xor(b, (b'\x08'))[0])
    print(b[0] ^ (b'\x08')[0])
    hex_string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    #print(hex_to_raw(hex_string))
    print(decrypt_single_xor(hex_string))
