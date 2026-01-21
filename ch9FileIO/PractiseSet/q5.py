# A file contains a word "Donkey" multiple Times.You need to write a program which replaces this word with  ##### by updating the same file
# BUT NOW DO IT FOR A LIST OF SUCH WORD TO BE CENSORED 


def replaceWord(list):
    f = open("donkeyFile.txt")
    content = f.read()
    replacedContent = content
    print("Your File Data: \n",content)
    print("Your File Data Ended: \n")
    f.close()
    for word in list:
        print("Word is :",word)
        if word.lower():
            replacedContent = replacedContent.replace(word, "#####")
            print(replacedContent)
    with open("donkeyFile.txt","w") as f:
        f.write(replacedContent)    



list = ["donkey","stupid","fool"]
replaceWord(list)
