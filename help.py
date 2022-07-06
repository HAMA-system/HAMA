def get_help(file, header, k):
    print('='*k)
    put = file.readline().strip()
    while put != "<"+header+">":
        put = file.readline().strip()
    while True:
        put = file.readline().strip()
        if put == "</"+header+">":
            break
        print(put)
    print('='*k)
    file.close()
    file = open("help.txt", 'r')
    return file

def help():
    file = open("help.txt", 'r')
    file = get_help(file, 'HELP', 35)
    print('\n'*3)
    file.close()

    while True:
        file = open("help.txt", 'r')

        n = input()
        if n == '1':
            file = get_help(file,'LOOKUP',100)
        elif n == '2':
            file = get_help(file,'WRITE',100)
        elif n == '3':
            file = get_help(file,'MODIFY',100)
        elif n == '4':
            file = get_help(file,'DRAFT',100)
        elif n == '5':
            file = get_help(file,'HAMA',100)

        elif n == 'q':
            break

        print("\n[종료를 원하시면 'q'를 입력하시고 계속 하시려면 아무 거나 입력하세요]","\n"*3)
        m = input()
        if m=='q':
            break
        print('\n'*100)
        file = get_help(file, 'HELP', 35)
        print('\n'*15)
        file.close()


if __name__ == '__main__':
    help()
