from pathlib import Path
# from bs4 import BeautifulSoup
import re

def boardCategory(boardHTML):
    with open('./' + boardHTML + '/source.html', 'r', encoding='UTF-8') as html:
        # soup = BeautifulSoup(html, features="html.parser")
        source = html.read()
        pattern = r"(?<=, \"category\": )\"?\w+\"?"
        matches = re.findall(pattern, source)
        return matches[0]


def main():
    with open('./data-features/board_categories.txt', 'w') as categoryList:
        with open('./data-paths/valid_boards.txt', 'r') as v_boards:
            for board in v_boards:
                category = boardCategory(board.rstrip())
                # boardCategory(board.rstrip())
                categoryList.write("%s\n" % category)


if __name__ == "__main__":
    main()