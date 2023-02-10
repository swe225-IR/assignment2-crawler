
from collections import Counter
import pickle as pkl
import sys

def extract_word_num(path: str, order_number: int) -> list:
    f = open(path, 'rb')
    all_record = pkl.load(f)
    f.close()
    return all_record.most_common(order_number)

if __name__ == '__main__':
    print('Top 50 most common words are: \t', extract_word_num(sys.argv[1], 50))
    print('The longest page is: \t', extract_word_num(sys.argv[2], 1))