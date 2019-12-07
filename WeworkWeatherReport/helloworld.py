# -*- coding: utf8 -*-


def main_handler(event, context):
    print(str(event))
    return "hello world"

str = main_handler(None, None);
print(str)

if __name__ == '__main__':
    main_handler(None, None)