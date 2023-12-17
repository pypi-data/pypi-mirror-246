from .kkdb import *

class script():
    def __init__(self, path):
        with open(f"{path}.kks", "r") as f:
            file = f.read()
            file = file.split("\n")
            code = []

        file = [x for x in file if x]

        for i in range(len(file)):
            if file[i].startswith("var "):
                code.append(file[i].split("="))
                exec(f"{code[i][0][4:]} = {code[i][1]}")

            elif file[i].startswith("printLn"):
                code.append(file[i].split("="))
                exec(f"print({code[i][1]})")

            elif file[i].startswith("$use "):
                code.append(file[i].split("="))
                exec(f"import {code[i][0][5:]}"
                     f"\n{code[i][0][5:]}.{code[i][1]}")

            elif file[i].startswith("$kkdb=create"):
                code.append(file[i].split("."))
                exec(f"{code[i][4]} = kkdb.{code[i][1]}({code[i][2]},{code[i][3]})")

            elif file[i].startswith("$kkdb"):
                code.append(file[i].split("."))
                if code[i][1] == "printData" or code[i][1] == "updateData":
                    exec(f"{code[i][2]}.{code[i][1]}()")
                else:
                    exec(f"{code[i][4]}.{code[i][1]}({code[i][2]},{code[i][3]})")





