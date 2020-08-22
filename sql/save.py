from datetime import date


def readFile():
    users = []
    battles = []
    dates = []
    file = open("fights.elbruto", "r") 
    for line in file.readlines():
        row = line.split(",")
        print(row)
        users.append(row[0])
        battles.append(row[1])
        dates.append(row[2])
    file.close() 
    return users, battles, dates

def nickExists(nick):
    file = open("fights.elbruto", "r") 
    for line in file.readlines():
        if(nick in line):
            file.close()
            return True
    file.close()
    return False

def updateFile(nick):
    file = open("fights.elbruto", "r") 
    for line in file.readlines():
        if(nick in line):
            file.close()
            return True
    file.close()
    return False

def saveInFile(nick):
    # ver si el nick existe
    if(nickExists(nick)):
        users, battles, dates = readFile()
        pos = 0
        for i in range(len(users)):
            if(users[i]==nick):
                pos = i
                break
        numberOfBattles = int(battles[pos])
        numberOfBattles += 1
        battles[pos] = str(numberOfBattles)
        file = open('fights.elbruto', 'w')
        line = ""
        for i in range(len(users)):
            line += users[i]+","+battles[i]+","+dates[i]
        file.write(line)
        file.close()
        #Funciona bien
    else:
        users, battles, dates = readFile()
        pos = 0
        file = open('fights.elbruto', 'w')
        line = ""
        for i in range(len(users)):
            line += users[i]+","+battles[i]+","+dates[i]
        line += "\n"+nick+",1,"+str(date.today())
        file.write(line)
        file.close()
        #Funciona bien



if __name__ == "__main__":
    #print(readFile())
    #saveInFile("fafs")
    #print("funciona")
    print(0)