import appJar
import string
import random
import copy



alphabet = { 
              'A' : 1, 'B': 2, 'C'  : 3, 'D' : 4,
              'E' : 5, 'F': 6, 'G'  : 7, 'H' : 8,
              'I' : 9, 'J': 10,'K'  : 11,'L' : 12,
              'M' : 13,'N': 14,'O'  : 15,'P' : 16,
              'Q' : 17,'R': 18,'S'  : 19,'T' : 20,
              'U' : 21,'V': 22,'W'  : 23,'X' : 24,
              'Y' : 25,'Z': 26 
            }
inv_alphabet = {v: k for k, v in alphabet.items()}







def buttonPress(button):

    if button == "Wczytaj tekst jawny z pliku":
        file = app.openBox("Otwórz",fileTypes=[('txt','*.txt')],asFile=True)
        fileString = file.read()
        tekstJawny = fileString
        app.clearTextArea("Tekst Jawny")
        app.setTextArea("Tekst Jawny",tekstJawny)

    if button == "Wczytaj tekst zaszyfrowany z pliku":
        file = app.openBox("Otwórz",fileTypes=[('txt','*.txt')],asFile=True)
        fileString = file.read()
        tekstZaszyfrowany = fileString
        app.clearTextArea("Tekst Szyfrowany")
        app.setTextArea("Tekst Szyfrowany",tekstZaszyfrowany)
    if button == "Zapisz Klucz do pliku":
        path = app.saveBox("Zapisz","Klucz",fileExt=".txt",fileTypes=[('txt',"*.txt")],asFile=True)
        stringToWrite = app.getEntry("Klucz")
        path.write(stringToWrite)
        path.close()
    if button == "Pobierz Klucz z pliku":
        file = app.openBox("Otwórz",fileTypes=[('txt','*.txt')],asFile=True)
        fileString = file.read()
        klucz = fileString
        app.clearEntry("Klucz")
        app.setEntry("Klucz",klucz)

    if button == "Zapisz tekst jawny do pliku":
        path = app.saveBox("Zapisz","Tekst Jawny",fileExt=".txt",fileTypes=[('txt',"*.txt")],asFile=True)
        stringToWrite = app.getTextArea("Tekst Jawny")
        path.write(stringToWrite)
        path.close()
    if button == "Zapisz tekst zaszyfrowany do pliku":
        path = app.saveBox("Zapisz","Zaszyfrowany Tekst",fileExt=".txt",fileTypes=[('txt',"*.txt")],asFile=True)
        stringToWrite = app.getTextArea("Tekst Szyfrowany")
        path.write(stringToWrite)
        path.close()
    if button == "Generuj klucz":
        matrix = convertStringToMatrix(app.getTextArea("Tekst Jawny"))
        length = len(matrix) - 1
        if checkIfMatrixIsValid(matrix) == False:
            app.warningBox("errorMatrix","Zły tekst jawny! Sprawdź INFO")
            return

        key = generateKey(length)
        app.clearEntry("Klucz")
        app.setEntry("Klucz",key)
    if button == "Szyfruj":
        key = app.getEntry("Klucz")
        matrix = convertStringToMatrix(app.getTextArea("Tekst Jawny"))
        if checkIfMatrixIsValid(matrix) == False:
            app.warningBox("errorMatrix","Zły tekst jawny! Sprawdź INFO")
            return
        if checkIfKeyMatchesMatrix(key,matrix) == False:
            app.warningBox("errorKey","Klucz nie pasuje do macierzy! Sprawdź INFO")
            return
        if checkIfKeyIsValid(key) == False:
            app.warningBox("errorKey","Błędny klucz! Sprawdź INFO")
            return
        cvtValues = convertStringToKeyValues(key)
        matrix = convertStringToMatrix(app.getTextArea("Tekst Jawny"))
        numberOfRows = len(matrix)
        numberOfColumns = numberOfRows - 1

        diagonal = []
        for off in cvtValues:
            lastIndex = 0
            offset = off - 1
            diagonal.append(matrix[-1][lastIndex + offset])

            for index in range(numberOfColumns - 1, -1 , -1):
                if (lastIndex + 1 + offset) == numberOfColumns:
                    lastIndex = 0
                    offset = 0
                else:
                    lastIndex = lastIndex + 1
                diagonal.append(matrix[index][lastIndex + offset])

        cipheredMessage = ''.join(diagonal)

        app.clearTextArea("Tekst Szyfrowany")
        app.setTextArea("Tekst Szyfrowany", cipheredMessage)
    if button == "Odszyfruj":
        key = app.getEntry("Klucz")
        cipheredMessage = app.getTextArea("Tekst Szyfrowany")
        if(not(checkIfCipheredMessageMatchesKey(key,cipheredMessage))):
            app.warningBox("errorCipher","Szyfrowany tekst nie pasuje do klucza! Sprawdź INFO")
            return
        if checkIfKeyIsValid(key) == False:
            app.warningBox("errorKey","Błędny klucz! Sprawdź INFO")
            return
        cvtValues = convertStringToKeyValues(key)

        wordLength = len(key) + 1
        cipheredWords = [cipheredMessage[i:i + wordLength] for i in range(0, len(cipheredMessage), wordLength)]
        decipheredMessage = [[0 for x in range(wordLength - 1)] for y in range(wordLength)] 
        for i,off in enumerate(cvtValues):
            currentCharacter = 0

            lastIndex = 0
            offset = off - 1
            currentWord = list(cipheredWords[i])
            decipheredMessage[-1][lastIndex + offset] = currentWord[currentCharacter]

            for index in range(wordLength - 2, -1 , -1):
                if (lastIndex + 1 + offset) == wordLength - 1:
                    lastIndex = 0
                    offset = 0
                    currentCharacter = currentCharacter + 1
                else:
                    lastIndex = lastIndex + 1
                    currentCharacter = currentCharacter + 1

                decipheredMessage[index][lastIndex + offset] = currentWord[currentCharacter]
        decipheredString = ''
        for i,row in enumerate(decipheredMessage):
            currentRowString = ''.join(row)
            if i != len(decipheredMessage) - 1:
                currentRowString = currentRowString + "\n"

            decipheredString = decipheredString + currentRowString
        app.clearTextArea("Tekst Jawny")
        app.setTextArea("Tekst Jawny", decipheredString)
    if button == "INFO":
        app.startSubWindow("Info", modal=True)
        app.addLabel("Info","Szyfr Przekątniowo-Kolumnowy\n\nTEKST JAWNY:\nTekst jawny jest w formie macierzy\nMacierz ta musi mieć określony stosunek rozmiarów\nWysokość macierzy musi być o 1 większa niż szerokość\n\nKLUCZ:\nDługość klucza musi być równa szerokości macierzy\nKlucz jest ciągiem znaków alfabetu(Duże litery)\nŻadna litera klucza nie może się powtórzyć\n\nTEKST SZYFROWANY:\nSą to odpowiednie przekątne oryginalnej macierzy\n\nSTOSUNEK KLUCZA DO TREŚCI SZYFROWANEJ:\nKażda litera klucza jest numerowana wg kolejności występowania w alfabecie\nTekst Szyfrowany dzielony jest na słowa o długości klucza+1\nWartość klucza jest odpowiednia dla każdego słowa\nWartość klucza jest numerem przekątnej która tworzy słowo")
        app.showSubWindow("Info")

def convertStringToMatrix(text):
    clearText = str.split(text,"\n")
    for index in range(len(clearText)):
        clearText[index] = list(clearText[index])
    return clearText    

def convertStringToKeyValues(key):
	charValues = []

	for character in key:
	  charValues.append(alphabet[character])
	  
	smallestNumber = 0
	convertedValues = copy.deepcopy(charValues)
	i = 1
	for index in range(len(charValues)):
	  smallestNumber = min(charValues,key=int)
	  position = charValues.index(smallestNumber)
	  charValues[position] = 100
	  convertedValues[position] = i
	  i = i + 1
	return convertedValues

def generateKey(length):
    key = random.sample(range(1,26),length)
    for index in range(len(key)):
        key[index] = inv_alphabet[key[index]]
    key = ''.join(key)
    return key


def checkIfMatrixIsValid(matrix):
    desiredWidth = len(matrix)
    if desiredWidth == 0 or desiredWidth == 1:
        return False
    for row in matrix:
        if len(row) != desiredWidth - 1:
            return False
    return True

def checkIfCipheredMessageMatchesKey(key,messageString):
    if len(key) == len(messageString) / (len(key) + 1):
        return True
    else:
        return False

def checkIfKeyMatchesMatrix(key,matrix):
    if len(key) != len(matrix) - 1:
        return False
    else:
        return True
def checkIfKeyIsValid(key):
    for char in key:
        if len(set([x for x in key if key.count(x) > 1])) > 0:
            return False
        else:
            return True
app = appJar.gui("Szyfr Przekątniowo-Kolumnowy","800x500")



app.addButton("Wczytaj tekst jawny z pliku",buttonPress,0,0)
app.addButton("Wczytaj tekst zaszyfrowany z pliku",buttonPress,0,2)

app.addButton("Zapisz tekst jawny do pliku",buttonPress,2,0)
app.addButton("Zapisz tekst zaszyfrowany do pliku",buttonPress,2,2)

app.addButton("Generuj klucz",buttonPress,2,1)
app.addButton("Szyfruj",buttonPress,4,1)
app.addButton("Odszyfruj",buttonPress,5,1)
app.addButton("Zapisz Klucz do pliku",buttonPress,0,1)
app.addButton("Pobierz Klucz z pliku",buttonPress,3,1)

app.addButton("INFO",buttonPress,6,1)


app.addTextArea("Tekst Jawny",1,0)
app.addTextArea("Tekst Szyfrowany",1,2)

app.addLabelEntry("Klucz",1,1)



app.go()