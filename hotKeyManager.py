from pynput.keyboard import Listener, Key, KeyCode
from dateController import dateToday

store = set()

HOT_KEYS = {
    'print_hello': set([Key.alt_l, KeyCode(char='1')]),
    'print_hello' : set([KeyCode(char='5')]),
    'print_today' : set([Key.ctrl_l,KeyCode(char='2')]),
    'dateToday' : set([KeyCode(char='2')])

}

def print_hello():
    print('hello, World!!!')

def print_today():
    print(dateToday())

def handleKeyPress(key):
    store.add(key)

    # for action, trigger in HOT_KEYS.items():
    #     CHECK = all([True if triggerKey in store else False for triggerKey in trigger])
    #
    #     if CHECK:
    #         # try:
    #         func = eval(action)
    #         if callable(func):
    #             func()
    #     # except NameError as err:
    #     # print(err)


def handleKeyRelease(key):
    for action, trigger in HOT_KEYS.items():
        CHECK = all([True if triggerKey in store else False for triggerKey in trigger])

        if CHECK:
            # try:
            func = eval(action)
            if callable(func):
                func()
        # except NameError as err:
        # print(err)

    if key in store:
        store.remove(key)

    # 종료
    if key == Key.esc:
        return False


def hotkeyStart():
    with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
        listener.join()

with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()