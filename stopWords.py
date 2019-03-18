from nltk.corpus import stopwords
from pathlib import Path
import string
cachedStopWords = stopwords.words("english")

def main():
    with open('./data-features/pin_text.txt', 'w', encoding='utf-8') as pinWords:
        with open('./data-paths/valid_pins.txt', 'r') as v_pins:
            for pinDir in v_pins:
                p = Path(pinDir.rstrip())
                if list(p.glob('*.txt')):
                    keyWords = []
                    for archivo in list(p.glob('*.txt')):
                        file = open(archivo, 'rt', encoding='utf-8')
                        text = file.read()
                        file.close()
                        words = text.split()
                        # lowercase all words
                        words = [word.lower() for word in words]
                        # remove punctuation
                        table = str.maketrans('', '', string.punctuation)
                        words = [word.translate(table) for word in words]
                        # remove words that arent alphanumeric
                        words = [word for word in words if word.isalpha()]
                        # remove stopwords
                        words = [word for word in words if word not in cachedStopWords]
                        [keyWords.append(word) for word in words]
                    sentence = ' '.join(word for word in keyWords)
                    pinWords.write(sentence + '\n')
                else:
                    pinWords.write("\n")


if __name__ == "__main__":
    main()