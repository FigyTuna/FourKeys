#Not yet functional
def settings():

    done = False

    file = readFile("settings.txt")

    while not done:

        print("Option ([1]button assign, [2]reverse), [0]exit:")

        answer = input()

        if 1 == answer:

            for i in range(0, 6):

                print(str(i) + ": ")

                temp = int(input())

                if(temp >= 0 or temp < 40):
                    file[i] = temp

                else:
                    print("Value for (" + str(i) + ") not set.")

        elif 2 == answer:

            print("[0] not reversed, [1] reversed")

            temp = int(input())

            if(temp == 0 or temp == 1):
                file[6] = temp

        elif 3 == answer:
            break
        

def readFile(fileName, start = 0, end = 100):

    ret = []

    i = 0

    f = open(fileName, 'r')

    while True:

        line = f.readline()
        if not line:
            break

        if i >= start and i < 100:
            ret.append(int(line))

        i += 1

    return ret
