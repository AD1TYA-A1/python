# A file contains a word "Donkey" multiple Times.You need to write a program which replaces this word with  ##### by updating the same file

def replaceWord(word):
    f = open("donkeyFile.txt")
    content = f.read()
    f.close()
    if word.upper() in content or word.lower() in content:
        replacedContent = content.replace("donkey","#####") 
        print(replacedContent)
        f = open("donkeyFile.txt","w")
        f.write(replacedContent)
        f.close()

replaceWord("donkey")
