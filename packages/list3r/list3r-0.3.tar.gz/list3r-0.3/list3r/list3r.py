#!/usr/bin/env python3

class List3r(object):

    def simple(a: str, b: str, __much: int):
        print("{:<{}} {:<}".format(a, __much, b))

    def liner(a: str, b: str, __much: int):
        print("{:<{}} {:<}".format(a, __much, b))
        x = __much +  len(b) + 2
        print("-"*x)

    def postive(a: str, b:str, __much: int):
        print("{:<{}} {:<}".format(a, __much, b))
        x = __much + len(b) + 2
        print("+"*x)

    def mul(a: str, b: str, __much: int):
        print("{:<{}} {:<}".format(a, __much, b))
        x = __much + len(b) + 2
        print("*"*x)

    def eql(a: str, b: str, __much: int):
        print("{:<{}} {}".format(a, __much, b))
        x = __much + len(b) + 2
        print("="*x)

    def hashtag(a: str, b: str, __much: int):
        print("{:<{}} {}".format(a, __much, b))
        x = __much + len(b) + 2
        print("#"*x)

    def formatter(a: str, b: str, __much: int):
        print("{:<{}} {}".format(a, __much, b))
        x1 = __much + len(b) + 2

        if x1 % 2 == 0:
            print("{}{}".format("{"*int(x1 / 2),"}"*int(x1 / 2)))

        else:
            print("{}{}".format("{"*int(x1 / 2 + 1),"}"*int(x1 / 2 + 1)))

    def formatterData(a: str, b: str, data: str, __much: int):
        print("{:<{}} {}".format(a, __much, b))
        x1 = __much + len(b) + 2

        if x1 % 2 == 0:
            print("{}{}{}".format("{"*int(x1 / 2), data, "}"*int(x1 / 2 - len(data) + 2)))

        else:
            print("{}{}{}".format("{"*int(x1 / 2 + 1), data, "}"*int(x1 / 2 - len(data) + 3)))



