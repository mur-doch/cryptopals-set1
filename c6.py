import base64, binascii
from c3 import decrypt_block_xor
from c5sol import repeating_key_xor

def b64_to_raw(b64_string):
    return base64.b64decode(b64_string)

def hamming_distance(byte1, byte2):
    x = byte1 ^ byte2
    set_bits = 0 

    while x > 0:
        set_bits += x & 1
        x = x >> 1
    
    return set_bits

def string_hamming_distance(byte_string1, byte_string2):
    # we're assuming for now that the strings are the same length
    dist = 0
    
    le = len(byte_string1)
    if len(byte_string1) > len(byte_string2):
        le = len(byte_string2)

    for i in range(le):
        dist += hamming_distance(byte_string1[i], byte_string2[i])

    return dist

def shift_list_left(l):
    if len(l) == 0:
        return []
    
    for i in range(len(l)-1, 0, -1):
        if (i-1) >= -1:
            l[i] = l[i-1]
    l[0] = 0
    return l

def score_vigenere_key_size(candidate_key_size, ciphertext):
    # as suggested in the instructions,
    # we take samples bigger than just one time the candidate key size
    slice_size = 2*candidate_key_size
    #slice_size = candidate_key_size

    # the number of samples we can make
    # given the ciphertext length
    nb_measurements = len(ciphertext) // slice_size - 1

    # the "score" will represent how likely it is
    # that the current candidate key size is the good one
    # (the lower the score the *more* likely)
    score = 0
    for i in range(nb_measurements):

        s = slice_size
        k = candidate_key_size
        # in python, "slices" objects are what you put in square brackets
        # to access elements in lists and other iterable objects.
        # see https://docs.python.org/3/library/functions.html#slice
        # here we build the slices separately
        # just to have a cleaner, easier to read code
        slice_1 = slice(i*s, i*s + k)
        slice_2 = slice(i*s + k, i*s + 2*k)
        
        # ADDED: I need to convert these two slices to byte strings to work
        # with the functions I've written.
        bytechunk1 = ciphertext[slice_1]
        bytechunk2 = ciphertext[slice_2]
        byte_string1 = b''
        byte_string2 = b''

        for b in bytechunk1:
            byte_string1 += bytes([b])

        for b in bytechunk2:
            byte_string2 += bytes([b])
        
        #score += string_hamming_distance(ciphertext[slice_1], ciphertext[slice_2])
        score += string_hamming_distance(byte_string1, byte_string2)
    
    # normalization: do not forget this
    # or there will be a strong biais towards long key sizes
    # and your code will not detect key size properly
    score /= candidate_key_size
    
    # some more normalization,
    # to make sure each candidate is evaluated in the same way
    score /= nb_measurements

    return score

def get_norm_dist(encrypted_bytes, keysize):
    # Split encrypted_bytes into chunks of size keysize.
    chunks = []
    for i in range(0, len(encrypted_bytes), keysize):
        chunks.append(encrypted_bytes[i:i+keysize])
    print(len(chunks[0]))
    # Sum the edit distances
    total_dist = 0
    count = 0
    for i in range(0, len(chunks)-1, 2):
        first_chunk = chunks[i]
        second_chunk = chunks[i+1]
        dist = string_hamming_distance(first_chunk, second_chunk)
        norm = dist / keysize
        total_dist += norm
        count += 2 # 1
    #return norm / count
    return total_dist / count

def get_blocks(byte_string, keysize):
    if len(byte_string) <= keysize:
        return [bytestring]
    
    output = []
    oindex = 0 
    counter = 0
    for i in range(len(byte_string)):
        if counter == 0:
            output.append(b'')
        # bytes([b[1]])
        output[oindex] += bytes([byte_string[i]])
        counter += 1
        if counter >= keysize:
            oindex += 1
            counter = 0

    return output

def get_transpose(blocks, keysize):
    output = []
    for k in range(keysize):
        output.append(b'')
        for i in range(len(blocks)):
            if len(blocks[i]) <= k:
                continue
            b = bytes([blocks[i][k]])
            output[k] += b
    return output

def main():
    # load data from 6.txt
    with open('6.txt', 'r') as file:
        data = file.read().replace('\n', '')

    encrypted_bytes = b64_to_raw(data)
    #encrypted_bytes = base64.b64decode(data).hex()
    #print(binascii.unhexlify(encrypted_bytes) == b64_to_raw(data))
    #priypnt(encrypted_bytes)

    # use keysizes from 2 to 40
    keysize_norms = []
    for keysize in range(2, 41):
        #first_chunk = encrypted_bytes[:keysize]
        #second_chunk = encrypted_bytes[keysize:keysize+keysize]
        #dist = string_hamming_distance(first_chunk, second_chunk)
        #norm = dist / keysize
        norm = get_norm_dist(encrypted_bytes, keysize)
        #norm = score_vigenere_key_size(keysize, encrypted_bytes)
        keysize_norms.append((keysize, norm))
    
    # Sort the list by norm.
    keysize_norms.sort(key=lambda tup: tup[1])
    # Get the top 3 most likely keysizes (smallest keysizes)
    keysizes = [keysize_norms[0][0], keysize_norms[1][0], keysize_norms[2][0]]
    print(keysize_norms)

    #keysizes = [29]

    for ki in range(len(keysizes)-2):
        # Now break the ciphertext into blocks of keysize length
        blocks = get_blocks(encrypted_bytes, keysizes[ki])
        # Transpose the blocks.
        transpose = get_transpose(blocks, keysizes[ki])

        # Now we want to solve each block as if it were a single-char xor.
        # From this we should get the single-byte xor for each block.
        # Put them together and we should have the repeating-key.
        repeating_key = b''
        for block in transpose:
            print(decrypt_block_xor(block))
            repeating_key += decrypt_block_xor(block)
        
        # Now with the repeating key, we want to try and get the message.
        # We can call our repeating key code from a previous challenge.
        decrypted_bytes = repeating_key_xor(encrypted_bytes, repeating_key)
        print(decrypted_bytes.decode('ascii'))

if __name__ == '__main__':
    main()
