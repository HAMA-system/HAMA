from linkData import 링크
import unicodedata



if __name__ == '__main__':
    import os
    print(os.listdir(링크[3] + "in/"))
    name = os.listdir(링크[3] + "in/")[3]  # 기차.txt
    print(name == '제2기숙사 경비 6월.pdf', name, '제2기숙사 경비 6월.pdf')
    name = unicodedata.normalize('NFC', name)
    print(name == '제2기숙사 경비 6월.pdf', name, '제2기숙사 경비 6월.pdf')
