import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--cipher", dest="cipher_type")
parser.add_argument("action", type=str)
parser.add_argument("--key", dest="key")
parser.add_argument("--input-file", dest="input_path")
parser.add_argument("--output-file", dest="output_path")
parser.add_argument("--text-file", dest="text_file_path")
parser.add_argument("--model-file", dest="model_file_path")

args = parser.parse_args()


def Caesar(cmessage, key, mode):
    cnew_message = ""
    for letter in cmessage:
        if letter in [' ', '.', ',', '\n']:
            cnew_message += letter
            continue
        if mode == "encode":
            new_num = ord(letter) + key % 25
            if new_num > 122 or 90 < new_num < 97:
                new_num -= 26
        else:
            new_num = ord(letter) - key % 25
            if new_num < 65 or 90 < new_num < 97:
                new_num += 26
        cnew_message += chr(new_num)
    return cnew_message


def Vigenere(vmessage, word, mode):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    vnew_message = ""
    wordIdx = 0
    word = word.upper()

    def find(symbol):
        for i in range(26):
            if letters[i] == symbol:
                return i
        return -1

    for letter in vmessage:
        num = find(letter.upper())
        if num == -1:
            vnew_message += letter
            continue
        if mode == "encode":
            num = (find(letter.upper()) + find(word[wordIdx])) % 26
        else:
            num = (find(letter.upper()) - find(word[wordIdx])) % 26
        if letter.isupper():
            vnew_message += letters[num]
        elif letter.islower():
            vnew_message += letters[num].lower()

        wordIdx += 1
        if wordIdx == len(word):
            wordIdx = 0
    return vnew_message


def train(text1):
    frequency = {}
    for k in range(97, 123):
        frequency[chr(k)] = 0
    letter_counter = 0
    for k in text1.lower():
        if k in [',', '.', ' ', '\n']:
            continue
        frequency[k] += 1
        letter_counter += 1
    g = open(args.model_file_path, 'w')
    for k in range(97, 123):
        frequency[chr(k)] /= letter_counter * 0.01
        g.write('{}:{}\n'.format(chr(k), frequency[chr(k)]))
    g.close()


def hack(text2):
    enc_alph = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f',
                'g', 'y', 'p', 'b', 'v', 'k', 'x', 'j', 'q', 'z']
    stat = open(args.model_file_path, 'r')
    decode_dic = {}
    for line in stat:
        key, value = line.split(':')
        decode_dic[key] = float(value.strip())
    stat.close()
    decode_dic = dict(sorted(decode_dic.items(), key=lambda x: x[1], reverse=True))
    dec_alph = []
    for i in decode_dic.keys():
        dec_alph.append(i)
    dic = dict(zip(dec_alph, enc_alph))
    new_text = ""
    for i in text2:
        if i in [',', '.', '\n', ' ']:
            new_text += i
            continue
        new_text += str(dic.get(i))
    return new_text


if args.action == "decode" or args.action == "encode":
    if not args.input_path:
        message = input()
    else:
        f = open('args.input_path', 'r')
        message = f.read()
        f.close()
    if args.cipher_type == "Caesar":
        new_message = Caesar(message, int(args.key), args.action)
    else:
        new_message = Vigenere(message, str(args.key), args.action)
    if not args.output_path:
        print(new_message)
    else:
        f = open(args.output_path, 'w')
        f.write(new_message)
        f.close()

if args.action == "train":
    if not args.text_file_path:
        text = input()
    else:
        f = open(args.text_file_path, 'r')
        text = f.read()
        f.close()
    train(text)

if args.action == "hack":
    if not args.input_path:
        text = input()
    else:
        f = open(args.input_path, 'r')
        text = f.read()
        f.close()
    new_message = hack(text)
    if not args.output_path:
        print(new_message)
    else:
        f = open(args.output_path, 'w')
        f.write(new_message)
        f.close()
