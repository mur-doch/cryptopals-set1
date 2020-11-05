from c1 import hex_to_raw

def main():
    # Read the lines into data
    with open('8.txt', 'r') as file:
        data = file.read().split('\n')
        data = data[:len(data)-1]
    
    # Go through each line in data
    potentially_ecb = []
    for line in data:
        # Convert the hex encoded line into bytes
        enc_bytes = hex_to_raw(line)
        
        # Split enc_bytes into 16 byte chunks
        n = 16 
        chunks = [enc_bytes[i:i+n] for i in range(0, len(enc_bytes), n)]

        # Score based on the total number of repeated chunks
        # and how many times each is repeated.
        prev_chunks = []
        score = 0
        for c in chunks:
            h = c.hex()
            if h in prev_chunks:
                score += 1
            prev_chunks.append(h)
        
        if score != 0:
            potentially_ecb.append(line)

    for line in potentially_ecb:
        print(line)

if __name__ == '__main__':
    main()
