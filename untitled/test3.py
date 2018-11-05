from pypinyin import pinyin, lazy_pinyin
import pypinyin


# 输入汉字，查询同音字
def samechr():
    in_chr = input("Please input a chiness character:")
    n = 0
    for i in range(0x4e00, 0x9fa6):
        if (pinyin(chr(i))[0][0] == pinyin(in_chr)[0][0]):
            print(chr(i), end=' ')
            n += 1
            if (n % 15 == 0):
                print()


# 输入拼音，查询同音字
def sametune():
    in_pinyin = input("Please input a PinYin(e.g. zhong1):")
    n = 0
    for i in range(0x4e00, 0x9fa6):
        print(pinyin(chr(i), style=pypinyin.TONE3)[0][0])
        if (pinyin(chr(i), style=pypinyin.TONE3)[0][0] == in_pinyin):
            print(chr(i), end=' ')
            n += 1
            if (n % 15 == 0):
                print(i)


# 输入字符串，注音
def stringtune():
    in_str = input("Please input your string:")
    py = lazy_pinyin(in_str, style=pypinyin.TONE)
    result = ''
    for i in range(len(in_str)):
        result = result + in_str[i] + py[i]
    print(result)


def main():
    while True:
        print()
        print("以字查字1；以音查字2；为字符串注音3；退出99")
        choice = input("Please input your choice:")
        if (choice == '1'):
            samechr()
        elif (choice == '2'):
            sametune()
        elif (choice == '3'):
            stringtune()
        elif (choice == '99'):
            break
        else:
            print("Please input right choice!!")


if __name__ == '__main__':
    sametune()
