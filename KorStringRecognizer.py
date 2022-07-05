cho_start = 4352
jung_start = 4449
jong_start = 4520
jong_end = 4549
cho_list =[u"ㄱ",u"ㄲ",u"ㄴ",u"ㄷ",u"ㄸ",u"ㄹ",u"ㅁ",u"ㅂ",u"ㅃ",u"ㅅ",u"ㅆ",u"ㅇ",u"ㅈ",u"ㅉ",u"ㅊ",u"ㅋ",u"ㅌ",u"ㅍ",u"ㅎ"]
jung_list = [u"ㅏ",u"ㅐ",u"ㅑ",u"ㅒ",u"ㅓ",u"ㅔ",u"ㅕ",u"ㅖ",u"ㅗ",u"ㅘ",u"ㅙ",u"ㅚ",u"ㅛ"\
            ,u"ㅜ",u"ㅝ",u"ㅞ",u"ㅟ",u"ㅠ",u"ㅡ",u"ㅢ",u"ㅣ"]
jong_list = [u"",u"ㄱ",u"ㄲ",u"ㄳ",u"ㄴ",u"ㄵ",u"ㄶ",u"ㄷ",u"ㄹ",u"ㄺ",u"ㄻ",u"ㄼ",u"ㄽ",u"ㄾ"\
            ,u"ㄿ",u"ㅀ",u"ㅁ",u"ㅂ",u"ㅄ",u"ㅅ",u"ㅆ",u"ㅇ",u"ㅈ",u"ㅊ",u"ㅋ",u"ㅌ",u"ㅍ",u"ㅎ"]

def combine(cho,jung,jong):
    return chr((cho*21+jung)+jong)

def reorganizer(line):
    result = ""
    finish = False
    jong_index = 0 #종성은 없는 경우가 있기 때문에 먼저 정의해준다.
    for index,letter in enumerate(line):
        letter  = ord(letter)
        if letter>=cho_start and letter<jung_start:       #초성일경우
            print("dd")
        #첫번째가 아니고 초성이 돌아왔을 경우는 한글이 완성 되었기 때문에 결과값을 가져온다.
        if index != 0 and finish:
            result += combine(cho_index,jung_index,jong_index)
            cho_index = 0
            jung_index = 0
            jong_index = 0
            cho_index = letter-cho_start
            finish = True
        elif letter>=jung_start and letter<jong_start:    #중성일경우
            jung_index = letter-jung_start
        elif letter>=jong_start and letter<4549:          #종성일경우
            jong_index = letter-jong_start+1
        else:
            # 첫번째가 아니고 한글이 아닌 것이 왔을 경우 한글이 완성됬음으로 결과값을 가져온다.
            if index != 0 and finish:
                result += combine(cho_index,jung_index,jong_index)
                cho_index = 0
                jung_index = 0
                jong_index = 0
                finish = False
            letter = chr(letter)
            result += letter
    return result

if __name__ == '__main__':
    import os
    name = os.listdir()[2]  # 기차.txt
    print(name == '기차.txt')
    print(reorganizer(name) == '기차.txt')