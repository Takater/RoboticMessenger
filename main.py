import sys

from windows import Window
from script import send_messages

def main():
    if len(sys.argv) == 1:
        Window()

    else:
        send_messages()

if __name__ == '__main__':
    main()