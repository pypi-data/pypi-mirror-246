import mouse
import keyboard
import requests
from bs4 import BeautifulSoup
import time
from googletrans import Translator
from langdetect import detect
import os
import json


# global defs
def wait(wait_time = 1):
    time.sleep(wait_time)

def clear():
    os.system("cls")

def oss():
    return os

def detect_lang(text: str, detectOrSrc: int = 0):
    try:
        if detectOrSrc == 0: return detect(text)
        else: return Translator().translate(text).src
    except:
        return 404

def saveJson(data: dict, file_path: str, indent = 4, encoding = "utf-8"):
    with open(file_path, 'w', encoding=encoding) as output_file:
        json.dump(data, output_file, indent=indent, ensure_ascii=False)

def saveFile(data, file_path: str, encoding = "utf-8"):
    with open(file_path, 'w', encoding=encoding) as output_file:
        output_file.write(data)

def readFile(file_path: str, encoding = "utf-8"):
    data = 404
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            data = json.load(file)
            return data
    except:
        return 404


# arr defs
def equalArr(arr, dimensions = 1): # arr1 = arr2
    res = []

    i = 0
    while i < len(arr):
        if dimensions == 1:
            res.append(arr[i])
        else:
            res.append([])
            e = 0
            while e < len(arr[i]):
                if dimensions == 2:
                    res[i].append(arr[i][e])
                else:
                    res[i].append([])
                    f = 0
                    while f < len(arr[i][e]):
                        res[i][e].append(arr[i][e][f])
                        f += 1
                e += 1
        i += 1

    return res

def allIndexInArr(arr, item): # 1D arr=[10,20,30,40,30], item=30 ==> [2,4]
	allIndex = []
	
	i = 0
	while i < len(arr):
		if arr[i] == item:
			allIndex.append(i)
		i += 1
	
	return allIndex

def inArr(arr, item): # ==> True, False
	return item in arr

def onSide(arr, item, greater = 1, startFrom = 0): # 2D arr=[1,1,1,3,2,2,2,1,2,2], item=2, greater=1 ==> [ [4,5,6], [8,9] ] ==> [ indexArr ]
	finalArr = []
	onceArr = []
	
	i = startFrom
	while i < len(arr):
		if arr[i] == item:
			onceArr.append(i)
		else:
			if len(onceArr) > greater:
				finalArr.append(onceArr)
				
			onceArr = []
		i += 1
	
	if len(onceArr) > greater:
		finalArr.append(onceArr)
		onceArr = []
		
	return finalArr

def fillArr(arr, fill, fromNum = -1, toNum = -1): # arr=["⬜","⬜","⬜"], fill="🟩", from=0,to=1 ==> ["🟩","🟩","⬜"] #
	arr = equalArr(arr)
	
	if fromNum == -1:
		fromNum = 0
	if toNum == -1:
		toNum = len(arr)-1
	
	if fromNum < len(arr) and toNum < len(arr):
		i = fromNum
		while i < toNum+1:
			arr[i] = fill
			i += 1
	
	return arr

def removeFromArr(arr, index = -1, txt = "", minusOne = 0):
	newArr = []
	i = 0
	if (index > -1 and minusOne == 0) or (index <= -1 and minusOne != 0):
		while i < len(arr):
			if i != index%len(arr):
				newArr.append(arr[i])
			i += 1
	else:
		counter = 0
		while i < len(arr):
			if arr[i] != txt or (arr[i] == txt and counter == 1):
				newArr.append(arr[i])
		
			if counter == 0 and arr[i] == txt:
				counter = 1
			
			i += 1
		
	return newArr

def RemoveDuplicates(arr, removeOriginalItem = 0, spicificItem = -1, item = None):
	arr = equalArr(arr)
	
	i = 0
	continu = 1
	while i < len(arr) and (spicificItem == -1 or (spicificItem != -1 and continu == 1)):
		allInd = []
		if spicificItem == -1:
			allInd = allIndexInArr(arr, arr[i])
		else:
			allInd = allIndexInArr(arr, item)
		
		if len(allInd) > 1:
			e = len(allInd)-1
			while e > 0:
				arr = removeFromArr(arr, allInd[e])
				if spicificItem != -1:
					continu = 0
				e -= 1
					
			if removeOriginalItem > 0:
				arr = removeFromArr(arr, allInd[0])
				i -= 1
					
		i += 1
			
	return arr

def sumArr(arr, fromNum = -1, toNum = -1): # arr=[1,2,3], fromNum=0, toNum=1 ==> 1+2 = 3
	sum = 0
	if fromNum > -1 and toNum > -1:
		toNum += 1
	elif fromNum > -1 and toNum < 0:
		toNum = len(arr)
	elif fromNum < 0 and toNum < 0:
		fromNum = 0
		toNum = len(arr)
		
	while fromNum < toNum:
		sum += arr[fromNum]
		fromNum += 1
	
	return sum

def minusArr(arr): # [1,4,5,8,7] ==> [3,1,3,-1]
	res = []

	i = 1
	while i < len(arr):
		res.append(arr[i] - arr[i-1])
		i += 1
	
	return res

def makeColumnArr(arr, column = 0): # convert column in 2D arr to arr
	arrLen = len(arr)
	columnArr = []

	i = 0
	while i < arrLen:
		if column < len(arr[i]): columnArr.append(arr[i][column])
		i += 1

	return columnArr

def convertRowToCol(arr, columnArr, column = 0): # Col ==> column, columnArr ==> row
    i = 0
    while i < len(columnArr):
        arr[i][column] = columnArr[i]
        i += 1
    
    return arr

def addArr(fromArr, toArr): # fromArr=[4,5,6], toArr=[1,2,3] ==> [1,2,3,4,5,6]
	toArr = equalArr(toArr)
	for x in fromArr:
		toArr.append(x)

	return toArr

def delArr(smallArr, bigArr): # smallArr = [4,5,6], bigArr=[1,2,3,4,5,6] ==> [1,2,3]
	smallArr = equalArr(smallArr)
	bigArr = equalArr(bigArr)

	for x in smallArr:
		if inArr(bigArr, x):
			bigArr = removeFromArr(bigArr, -1, x)
	
	return bigArr

def sliceArr(arr, fromNum = 0, toNum = 0): # arr=[10,20,30,40,50], fromNum=1, toNum=3 ==> [20,30,40]
    newArr = []

    i = fromNum
    while i <= toNum:
        newArr.append(arr[i])
        i += 1
    
    return newArr

def reverseArr(arr): # arr=[1,2,3] ==> [3,2,1]
    return arr[::-1]

def search2D(arr, item, column = 0): # ==> [index]
	res = []

	i = 0
	while i < len(arr):
		if arr[i][column] == item:
			res.append(i)
		i += 1

	return res

def convert2D(arr): # ==> 1D, convert 2D to 1D, arr=[ [1,2,3], [4,5,6], [7,8,9] ] ==> [1,2,3,4,5,6,7,8,9]
	newArr = []
	
	i = 0
	while i < len(arr):
		e = 0
		while e < len(arr[i]):
			newArr.append(arr[i][e])
			e += 1
		i += 1
	
	return newArr

def rotate2DArr(arr, numR = 1): # numR ==> num of right turns
    arr = equalArr(arr, 2)
    
    a = 0
    while a < numR:
        res = []

        i = 0
        while i < len(arr[0]):
            res.append(makeColumnArr(arr, i)[::-1])
            i += 1
        
        arr = res
        a += 1
    
    return arr

def insertInArr(arr, itemToInsert, itemIndex = 0, isMultiItems = 0): # arr=[1,3,4], itemToInsert=2 ==> [1,2,3,4]
    arr = equalArr(arr)
    res = []

    i = 0
    while i < len(arr):
        if i == itemIndex:
            if isMultiItems == 0: res.append(itemToInsert)
            elif "list" in str(type(itemToInsert)):
                e = 0
                while e < len(itemToInsert):
                    res.append(itemToInsert[e])
                    e += 1
        res.append(arr[i])
        i += 1

    return res

def convertTxt(text): # convert text to code, "5 + 7" ==> 12
    try:
        return eval(text)
    except Exception as e:
        print("حدث خطأ في التحويل:", e)
        return None

def searchIn_decodeNum(arr, search_key, equalOrContain = 0): # arr=["n1", "o1", "n2"], search_key="n" ==> [0, 2] => [index]
    arr = equalArr(arr)
    result = []
    
    newArr = []
    i = 0
    while i < len(arr):
        newArr.append(decodeNum(arr[i]))
        for index, item in enumerate(newArr[i]):
            newArr[i][index] = str(item)

        if (equalOrContain == 0 and search_key in newArr[i]) or (equalOrContain == 1 and search_key in "".join(newArr[i])):
            result.append(i)
        i += 1

    return result

# object {} defs
def equalObject(the_object, dimensions = 1): # the_object1 = the_object2
    res = {}
    for key in the_object:
        value = the_object[key]
        if dimensions == 1:
            res[key] = the_object[key]
        else:
            res[key] = {}
            for key_e in the_object[key]:
                if dimensions == 2:
                    res[key][key_e] = the_object[key][key_e]
                else:
                    res[key][key_e] = {}
                    for key_f in the_object[key][key_e]:
                        res[key][key_e][key_f] = the_object[key][key_e][key_f]

    return res

def getObjectKeys(the_object): # {"h1": "text", "h2": "text2"} ==> ["h1", "h2"]
    keys = []
    for key in the_object:
        keys.append(key)
    
    return keys

def addToObject(the_object, key, want_to_add): # {"name": "about"}, "name", "about" ==> {"name": "about", "name 2": "about"}
    the_object = equalObject(the_object)
    if len(searchIn_decodeNum(getObjectKeys(the_object), key, 1)) > 0:
        the_object[f"{key} {len(searchIn_decodeNum(getObjectKeys(the_object), key, 1))+1}"] = want_to_add
    else:
        the_object[key] = want_to_add

    return the_object

# text defs
def decodeNum(text): # r2 ==> ["r", 2]
    res = []
    tmp = ""
    nums = "0123456789"

    i = 0
    while i < len(text)-1:
        tmp += text[i]
        if text[i] not in nums:
            if text[i+1] in nums:
                res.append(tmp)
                tmp = ""
        else:
            if text[i+1] not in nums:
                res.append(int(tmp))
                tmp = ""
        i += 1

    tmp += text[i]
    if text[i] in nums: res.append(int(tmp))
    if text[i] not in nums: res.append(tmp)
    tmp = ""

    return res

def right(text, amount):
    return text[-amount:]

def left(text, amount):
    return text[:amount]

def mid(text, offset, amount):
    return text[offset:offset+amount]

def removeSpaces(text): # إلغاء   المسافات
    text = " ".join(RemoveDuplicates(text.split(" "), 1, ""))
    text = " ".join(removeFromArr(text.split(" "), -1, ""))
    return text.strip()

def replaceText(text, replArr): # text = "hello word!", replArr = [ ["word", "world"], ["!", "."] ] ==> "hello world."
    i = 0
    while i < len(replArr):
        text = text.replace(replArr[i][0], replArr[i][1])
        i += 1

    return text

# translate defs
def translate_text(text, target_language="en", not_langs=[], detectOrSrc = 0):
    translator = Translator()

    if not_langs == []:
        if text:
            textArr = []
            for i in text.split("\n"):
                if i != "":
                    tmp = ""
                    try:
                        tmp = translator.translate(i, dest=target_language)
                    except:
                        tmp = i
                    textArr.append(tmp.text)

            translation = "\n".join(textArr)
            return translation
    else:
        sentences = text.split(" ")
    
        fullArr = []
        fullArrInd = []
        tmpArr = []
        tmpInd = -1
        # ["hello", "اهلا"] ==> fullArr = [ ["hello"] ], fullArrInd = [ 0 ]
        detected_language = ""
        for i, item in enumerate(sentences):
            detected_language = detect_lang(item, detectOrSrc)
            if detected_language != 404:
                if detected_language not in not_langs:
                    tmpArr.append(item)
                    if tmpInd == -1: tmpInd = i
                elif i != 0 and len(tmpArr) > 0:
                    fullArr.append(tmpArr)
                    fullArrInd.append(tmpInd)
                    tmpArr = []
                    tmpInd = -1
            else:
                fullArr.append(item)
                fullArrInd.append(i)
                tmpArr = []
                tmpInd = -1
                detected_language = ""
        if detected_language not in not_langs and len(tmpArr) > 0:
            fullArr.append(tmpArr)
            fullArrInd.append(tmpInd)
            tmpArr = []
            tmpInd = -1
        
        for i, item in enumerate(fullArr):
            i = len(fullArr)-i-1
            for e in range(len(fullArr[i])):
                sentences = removeFromArr(sentences, fullArrInd[i])
            sentences.insert(fullArrInd[i], fullArr[i])

        for i, item in enumerate(sentences):
            if str(type(item)) == "<class 'list'>":
                tmpTransText = " ".join(item)
                tmpTrans = ""
                try: tmpTrans = translator.translate(tmpTransText, dest=target_language).text
                except: tmpTrans = tmpTransText
                sentences[i] = tmpTrans

        text = " ".join(sentences)
    
    return text

def translate_arr(arr, target_language="en", not_langs=[]):
    newArr = []
    for item in arr:
        if str(type(item)) == "<class 'str'>":
            newArr.append(translate_text(item, target_language, not_langs))
        elif str(type(item)) == "<class 'dict'>": # dict ==> {}
            newArr.append(translate_obj(item, target_language, not_langs))
        elif str(type(item)) == "<class 'list'>": # list ==> []
            newArr.append(translate_arr(item, target_language, not_langs))
        else:
            newArr.append(item)
        
    return newArr

def translate_obj(obj, target_language="en", not_langs=[]):
    new_obj = {}

    for i in obj:
        if str(type(obj[i])) == "<class 'str'>":
            new_obj[translate_text(i, target_language, not_langs)] = translate_text(obj[i], target_language, not_langs)
        elif str(type(obj[i])) == "<class 'dict'>": # dict ==> {}
            new_obj[translate_text(i, target_language, not_langs)] = translate_obj(obj[i], target_language, not_langs)
        elif str(type(obj[i])) == "<class 'list'>": # list ==> []
            new_obj[translate_text(i, target_language, not_langs)] = translate_arr(obj[i], target_language, not_langs)
        else:
            new_obj[translate_text(i, target_language, not_langs)] = obj[i]

    return new_obj

# mouse defs
def getMousePosition():
    return [mouse.get_position()[0], mouse.get_position()[1]]

def getMousePositions(saveKey="g", breakKey="0"):
    all = []

    while True:
        if keyboard.is_pressed(saveKey):
            item = input("what is it?\n")
            all.append([ item, getMousePosition() ])

        if keyboard.is_pressed(breakKey):
            break

    print(all)

# soup
def get_soup(link, wait=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    with requests.Session() as session:
        try:
            result = session.get(link, headers=headers, timeout=10)
            time.sleep(wait)
            result.raise_for_status()  # رفع استثناء إذا كان هناك خطأ في الاستجابة
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            return soup
        except requests.exceptions.RequestException as e:
            # print(f"Error: {e}")
            return None

def get_redirected_url(link): # bit.ly ==> link
    # إجراء طلب GET للحصول على الصفحة الأولى
    response = requests.get(link)

    # التحقق من وجود عملية تحويل
    if response.history:
        # الحصول على الرابط النهائي بعد التحويل
        final_url = response.url
        return final_url
    else:
        return link
