# -*- coding: utf8 -*-


#TODO fish
#FIXME LI

def main_handler(event, context):
    print(str(event))
    return "hello world"

str1 = main_handler(None, None);
print(str1)

if __name__ == '__main__':
    main_handler(None, None)
    print("Hello SCF")