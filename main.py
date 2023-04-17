from windows import Window

import sys

def main():
    if len(sys.argv) == 1:
        window = Window()

    else:
        Window.message_box("info", "Tilte", "Text")

if __name__ == '__main__':
    main()