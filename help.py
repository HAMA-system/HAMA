def get_help(file, header):
    print('='*100)
    put = file.readline().strip()
    while put != "<"+header+">":
        put = file.readline().strip()
    while True:
        put = file.readline().strip()
        if put == "</"+header+">":
            break
        print(put)
    print('='*100)
    file.close()
    file = open("help.txt", 'r')
    return file

file = open("help.txt", 'r')
while True:
    put = file.readline().strip()
    if put == "</HELP>":
        break
    elif put == "<HELP>":
        continue
    print(put)
print('\n'*3)
file.close()

while True:
    file = open("help.txt", 'r')

    n = input()
    if n == '1':
        file = get_help(file,'LOOKUP')
    elif n == '2':
        file = get_help(file,'WRITE')
    elif n == '3':
        file = get_help(file,'MODIFY')
    elif n == '4':
        file = get_help(file,'DRAFT')
    elif n == '5':
        file = get_help(file,'HAMA')

    elif n == 'q':
        break


    print("\n[종료를 원하시면 'q'를 입력하시고 계속 하시려면 아무 거나 입력하세요]","\n"*3)
    m = input()
    if m=='q':
        break

    print('\n'*100)
    while True:
        put = file.readline().strip()
        if put == "</HELP>":
            break
        elif put == "<HELP>":
            continue
        print(put)
    print('\n'*3)
    file.close()

