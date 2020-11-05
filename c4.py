import c3

if __name__ == '__main__':
    f = open('4.txt', 'r')
    
    lowest_score = 100000
    lowest_text = ""
    for line in f:
        text = c3.decrypt_single_xor(line.strip())
        score = c3.score_english(text)
        if score < lowest_score:
            lowest_text = text
            lowest_score = score

    print(lowest_score)
    print(lowest_text)
    
    f.close()
