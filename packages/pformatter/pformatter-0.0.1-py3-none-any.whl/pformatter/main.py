import typing


class _password_formatter:
    def __new__(self, /, *, password: str, f: str | typing.Literal["s", "us"]) -> str:
        if f == "c":
            coded_p = ""
            for char in range(len(password)):
                # lowercase ascii
                if password[char] == "a":
                    coded_p += "~"
                elif password[char] == "b":
                    coded_p += "}"
                elif password[char] == "c":
                    coded_p += "|"
                elif password[char] == "d":
                    coded_p += "{"
                elif password[char] == "e":
                    coded_p += "`"
                elif password[char] == "f":
                    coded_p += "_"
                elif password[char] == "g":
                    coded_p += "^"
                elif password[char] == "h":
                    coded_p += "]"
                elif password[char] == "i":
                    coded_p += "\\"
                elif password[char] == "j":
                    coded_p += "["
                elif password[char] == "k":
                    coded_p += "@"
                elif password[char] == "l":
                    coded_p += "?"
                elif password[char] == "m":
                    coded_p += ">"
                elif password[char] == "n":
                    coded_p += "="
                elif password[char] == "o":
                    coded_p += "<"
                elif password[char] == "p":
                    coded_p += ";"
                elif password[char] == "q":
                    coded_p += ":"
                elif password[char] == "r":
                    coded_p += "/"
                elif password[char] == "s":
                    coded_p += "."
                elif password[char] == "t":
                    coded_p += "-"
                elif password[char] == "u":
                    coded_p += ","
                elif password[char] == "v":
                    coded_p += "+"
                elif password[char] == "w":
                    coded_p += "*"
                elif password[char] == "x":
                    coded_p += ")"
                elif password[char] == "y":
                    coded_p += "("
                elif password[char] == "z":
                    coded_p += "'"
                # uppercase ascii
                elif password[char] == "A":
                    coded_p += "&"
                elif password[char] == "B":
                    coded_p += "%"
                elif password[char] == "C":
                    coded_p += "$"
                elif password[char] == "D":
                    coded_p += "#"
                elif password[char] == "E":
                    coded_p += '"'
                elif password[char] == "F":
                    coded_p += "!"
                elif password[char] == "G":
                    coded_p += "9"
                elif password[char] == "H":
                    coded_p += "8"
                elif password[char] == "I":
                    coded_p += "7"
                elif password[char] == "J":
                    coded_p += "6"
                elif password[char] == "K":
                    coded_p += "5"
                elif password[char] == "L":
                    coded_p += "4"
                elif password[char] == "M":
                    coded_p += "3"
                elif password[char] == "N":
                    coded_p += "2"
                elif password[char] == "O":
                    coded_p += "1"
                elif password[char] == "P":
                    coded_p += "0"
                elif password[char] == "Q":
                    coded_p += "Z"
                elif password[char] == "R":
                    coded_p += "Y"
                elif password[char] == "S":
                    coded_p += "X"
                elif password[char] == "T":
                    coded_p += "W"
                elif password[char] == "U":
                    coded_p += "V"
                elif password[char] == "V":
                    coded_p += "U"
                elif password[char] == "W":
                    coded_p += "T"
                elif password[char] == "X":
                    coded_p += "S"
                elif password[char] == "Y":
                    coded_p += "R"
                elif password[char] == "Z":
                    coded_p += "Q"
                # digits
                elif password[char] == "0":
                    coded_p += "P"
                elif password[char] == "1":
                    coded_p += "O"
                elif password[char] == "2":
                    coded_p += "N"
                elif password[char] == "3":
                    coded_p += "M"
                elif password[char] == "4":
                    coded_p += "L"
                elif password[char] == "5":
                    coded_p += "K"
                elif password[char] == "6":
                    coded_p += "J"
                elif password[char] == "7":
                    coded_p += "I"
                elif password[char] == "8":
                    coded_p += "H"
                elif password[char] == "9":
                    coded_p += "G"
                # punctuation
                elif password[char] == "!":
                    coded_p += "F"
                elif password[char] == '"':
                    coded_p += "E"
                elif password[char] == "$":
                    coded_p += "D"
                elif password[char] == "%":
                    coded_p += "C"
                elif password[char] == "&":
                    coded_p += "B"
                elif password[char] == "'":
                    coded_p += "A"
                elif password[char] == "(":
                    coded_p += "z"
                elif password[char] == ")":
                    coded_p += "y"
                elif password[char] == "*":
                    coded_p += "x"
                elif password[char] == "+":
                    coded_p += "w"
                elif password[char] == ",":
                    coded_p += "v"
                elif password[char] == "-":
                    coded_p += "u"
                elif password[char] == ".":
                    coded_p += "t"
                elif password[char] == "/":
                    coded_p += "s"
                elif password[char] == ":":
                    coded_p += "r"
                elif password[char] == ";":
                    coded_p += "q"
                elif password[char] == "<":
                    coded_p += "p"
                elif password[char] == "=":
                    coded_p += "o"
                elif password[char] == ">":
                    coded_p += "n"
                elif password[char] == "?":
                    coded_p += "m"
                elif password[char] == "@":
                    coded_p += "l"
                elif password[char] == "[":
                    coded_p += "k"
                elif password[char] == "\\":
                    coded_p += "j"
                elif password[char] == "]":
                    coded_p += "i"
                elif password[char] == "^":
                    coded_p += "h"
                elif password[char] == "_":
                    coded_p += "g"
                elif password[char] == "`":
                    coded_p += "f"
                elif password[char] == "{":
                    coded_p += "e"
                elif password[char] == "|":
                    coded_p += "d"
                elif password[char] == "}":
                    coded_p += "c"
                elif password[char] == "~":
                    coded_p += "b"
            return coded_p
        if f == "dc":
            decoded_p = ""
            for char in range(len(password)):
                # lowercase ascii
                if password[char] == "~":
                    decoded_p += "a"
                elif password[char] == "}":
                    decoded_p += "b"
                elif password[char] == "|":
                    decoded_p += "c"
                elif password[char] == "{":
                    decoded_p += "d"
                elif password[char] == "`":
                    decoded_p += "e"
                elif password[char] == "_":
                    decoded_p += "f"
                elif password[char] == "^":
                    decoded_p += "g"
                elif password[char] == "]":
                    decoded_p += "h"
                elif password[char] == "\\":
                    decoded_p += "i"
                elif password[char] == "[":
                    decoded_p += "j"
                elif password[char] == "@":
                    decoded_p += "k"
                elif password[char] == "?":
                    decoded_p += "l"
                elif password[char] == ">":
                    decoded_p += "m"
                elif password[char] == "=":
                    decoded_p += "n"
                elif password[char] == "<":
                    decoded_p += "o"
                elif password[char] == ";":
                    decoded_p += "p"
                elif password[char] == ":":
                    decoded_p += "q"
                elif password[char] == "/":
                    decoded_p += "r"
                elif password[char] == ".":
                    decoded_p += "s"
                elif password[char] == "-":
                    decoded_p += "t"
                elif password[char] == ",":
                    decoded_p += "u"
                elif password[char] == "+":
                    decoded_p += "v"
                elif password[char] == "*":
                    decoded_p += "w"
                elif password[char] == ")":
                    decoded_p += "x"
                elif password[char] == "(":
                    decoded_p += "y"
                elif password[char] == "'":
                    decoded_p += "z"
                # Uppercase ascii
                elif password[char] == "&":
                    decoded_p += "A"
                elif password[char] == "%":
                    decoded_p += "B"
                elif password[char] == "$":
                    decoded_p += "C"
                elif password[char] == "#":
                    decoded_p += "D"
                elif password[char] == '"':
                    decoded_p += "E"
                elif password[char] == "!":
                    decoded_p += "F"
                elif password[char] == "9":
                    decoded_p += "G"
                elif password[char] == "8":
                    decoded_p += "H"
                elif password[char] == "7":
                    decoded_p += "I"
                elif password[char] == "6":
                    decoded_p += "J"
                elif password[char] == "5":
                    decoded_p += "K"
                elif password[char] == "4":
                    decoded_p += "L"
                elif password[char] == "3":
                    decoded_p += "M"
                elif password[char] == "2":
                    decoded_p += "N"
                elif password[char] == "1":
                    decoded_p += "O"
                elif password[char] == "0":
                    decoded_p += "P"
                elif password[char] == "Z":
                    decoded_p += "Q"
                elif password[char] == "Y":
                    decoded_p += "R"
                elif password[char] == "X":
                    decoded_p += "S"
                elif password[char] == "W":
                    decoded_p += "T"
                elif password[char] == "V":
                    decoded_p += "U"
                elif password[char] == "U":
                    decoded_p += "V"
                elif password[char] == "T":
                    decoded_p += "W"
                elif password[char] == "S":
                    decoded_p += "X"
                elif password[char] == "R":
                    decoded_p += "Y"
                elif password[char] == "Q":
                    decoded_p += "Z"
                # digits
                elif password[char] == "P":
                    decoded_p += "0"
                elif password[char] == "O":
                    decoded_p += "1"
                elif password[char] == "N":
                    decoded_p += "2"
                elif password[char] == "M":
                    decoded_p += "3"
                elif password[char] == "L":
                    decoded_p += "4"
                elif password[char] == "K":
                    decoded_p += "5"
                elif password[char] == "J":
                    decoded_p += "6"
                elif password[char] == "I":
                    decoded_p += "7"
                elif password[char] == "H":
                    decoded_p += "8"
                elif password[char] == "G":
                    decoded_p += "9"
                # punctuation
                elif password[char] == "F":
                    decoded_p += "!"
                elif password[char] == "E":
                    decoded_p += '"'
                elif password[char] == "D":
                    decoded_p += "$"
                elif password[char] == "C":
                    decoded_p += "%"
                elif password[char] == "B":
                    decoded_p += "&"
                elif password[char] == "A":
                    decoded_p += "'"
                elif password[char] == "z":
                    decoded_p += "("
                elif password[char] == "y":
                    decoded_p += ")"
                elif password[char] == "x":
                    decoded_p += "*"
                elif password[char] == "w":
                    decoded_p += "+"
                elif password[char] == "v":
                    decoded_p += ","
                elif password[char] == "u":
                    decoded_p += "-"
                elif password[char] == "t":
                    decoded_p += "."
                elif password[char] == "s":
                    decoded_p += "/"
                elif password[char] == "r":
                    decoded_p += ":"
                elif password[char] == "q":
                    decoded_p += ";"
                elif password[char] == "p":
                    decoded_p += "<"
                elif password[char] == "o":
                    decoded_p += "="
                elif password[char] == "n":
                    decoded_p += ">"
                elif password[char] == "m":
                    decoded_p += "?"
                elif password[char] == "l":
                    decoded_p += "@"
                elif password[char] == "k":
                    decoded_p += "["
                elif password[char] == "j":
                    decoded_p += "\\"
                elif password[char] == "i":
                    decoded_p += "]"
                elif password[char] == "h":
                    decoded_p += "^"
                elif password[char] == "g":
                    decoded_p += "_"
                elif password[char] == "f":
                    decoded_p += "`"
                elif password[char] == "e":
                    decoded_p += "{"
                elif password[char] == "d":
                    decoded_p += "|"
                elif password[char] == "c":
                    decoded_p += "}"
                elif password[char] == "b":
                    decoded_p += "~"
            return decoded_p
