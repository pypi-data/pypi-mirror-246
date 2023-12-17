class DB:
    def __init__(self, path, title):
        self.title = title
        self.path = path
        with open(f"{self.path}.kkdb", "r+") as f:
            file = f.read()
            file = file.split("\n")
            file = [x for x in file if x]
            self.data = []
        for i in range(len(file)):
            self.data.append(file[i].split("=\data/="))
        f.close()

    def updateData(self):
        with open(f"{self.path}.kkdb", "r+") as f:
            file = f.read()
            file = file.split("\n")
            file = [x for x in file if x]
            self.data = []
        for i in range(len(file)):
            self.data.append(file[i].split("=\data/="))
        f.close()

    def printData(self):
        print(f"\ntitle: {self.title}"
              f"\nnames: ", end="")
        for i in range(len(self.data)):
            print(self.data[i][0] + ", ", end="")
        print(f"\nvalues: ", end="")
        for j in range(len(self.data)):
            print(self.data[j][1] + ", ", end="")
        print()

    def addData(self, name, value):
        with open(f"{self.path}.kkdb", "a+") as f1:
            f1.write(f"{name}=\data/={value}\n")
            f1.close()

    def setData(self, name, value):
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                with open(f"{self.path}.kkdb", 'r') as f:
                    old_data = f.read()
                new_data = old_data.replace(self.data[i][1], str(value))
                with open(f"{self.path}.kkdb", 'w') as f:
                    f.write(new_data)
            else:
                pass

    def getData(self, name, type):
        for i in range(len(self.data)):
            if name in self.data[i][0]:
                if type == "int":
                    return int(self.data[i][1])
                elif type == "float":
                    return float(self.data[i][1])
                elif type == "bool":
                    return bool(self.data[i][1])
                elif type == "str":
                    return self.data[i][1]
                elif type == "list":
                    return list(self.data[i][1][1:-1].split(","))
                elif type == "tuple":
                    return tuple(self.data[i][1][1:-1].split(","))





