words = {}

ParseWords()

def ParseWords():
    temp = ""
    with open('static/word_list.txt') as f:
        for i in range(len(f)):
            temp += f[i].strip()
            print(f[i].strip())


def RandomizeWord():
    return ["category", "word"]

#def DefineRoles(database, word):
