'''
Created on 9 mar 2021

@author: Venturino
'''
import pytesseract
import cv2
import json
import os
from pytesseract import Output
import fileinput

global idx


def generateLabelmeData(labelmepath, elements, considerLabelme):
    # generate a compatible labelme json
    #removeNull(labelmepath)
    with open(labelmepath) as json_file:
        labelmeData = json.load(json_file)
    rectangles = labelmeData
    if not considerLabelme:
        rectangles['shapes'] = []
    for z in elements:
        elementCompatible = {
            'text': z['text'],
            'label': z['label'],
            'points': [[z['box'][0], z['box'][1]], [z['box'][2], z['box'][3]]],
            'shape_type': "rectangle",
            'flags': {},
            'group_id': z['id'],
            'link': [],
        }
        rectangles['shapes'].append(elementCompatible)
    return rectangles


'''def generateGroupID(path):
    removeNull(path)
    with open(path) as json_file:
        labelmeData = json.load(json_file)
    global idx
    for a in labelmeData['shapes']:
        idx += 1
        a.update({'group_id': idx})
    generateJson(imagepath, labelmeData, labelme)'''


'''def removeNull(filename):
    textToSearch = '"group_id": null,'
    textToReplace = ''
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(textToSearch, textToReplace), end='')'''


'''def adjuster(path):
    global idx
    # extract words from labelmeGiusti (the one adjusted by hand)
    with open(path) as json_file:
        labelmeGiusti = json.load(json_file)
    fields = labelmeGiusti['shapes']
    giustiRectangle = []
    for giusto in fields:
        giustoRectangle = {
            'text': giusto['text'],
            'box': [int(giusto['points'][0][0]), int(giusto['points'][0][1]), int(giusto['points'][1][0]),
                    int(giusto['points'][1][1])],
            'label': giusto['label'],
            'id': giusto['group_id'],
            'link': giusto['link'],
        }
        giustiRectangle.append(giustoRectangle)
    # update data
    aggiustati = []
    # check coordinates
    for w in giustiRectangle:
        if w['label'] == "word":
            if w['id'] is None:
                # found new word -> create
                idx += 1
                img = cv2.imread(imagepath)
                crop_img = img[w['box'][1]:w['box'][3], w['box'][0]:w['box'][2]] if w['box'][1] <= w['box'][3] else img[w['box'][3]:w['box'][1], w['box'][2]:w['box'][0]]
                #cv2.imshow("cropped", crop_img)
                parola = {
                    'box': w['box'],
                    'text': ''.join(pytesseract.image_to_data(crop_img, output_type=Output.DICT, lang='ita')['text']),
                    'id': str(idx),
                    'link': w['link'],
                    'label': w['label'],
                }
                #print("nuova parola trovata: " + parola['text'])
                #print("id: " + parola['id'])
                #cv2.waitKey(0)
                aggiustati.append(parola)
            for word in wordsRectangles:
                if word['label']=="word":
                    if word['id'] == w['id']:
                        if word['box'] != w['box']:
                            # has different coordinates -> update
                            word['box'] = w['box']
                            img = cv2.imread(imagepath)
                            crop_img = img[w['box'][1]:w['box'][3], w['box'][0]:w['box'][2]] if w['box'][1] <= w['box'][3] else img[w['box'][3]:w['box'][1], w['box'][2]:w['box'][0]]
                            # cv2.imshow("cropped", crop_img)
                            aggiusta = pytesseract.image_to_data(crop_img, output_type=Output.DICT, lang='ita')
                            # print('vecchia: ' + word['text'])
                            word['text'] = ''.join(aggiusta['text'])
                            # print('nuova: ' + word['text'])
                            # print('id: ' + word['id'])
                            # cv2.waitKey(0)
                        aggiustati.append(word)
    return aggiustati'''


def generateJson(fileName, elements, destinationpath):
    # code to get right path for json files
    namefileWithExtension = os.path.split(fileName)[1]  # file name with extension .png
    namefile = os.path.splitext(namefileWithExtension)[0]  # only file name
    annotationFileName = os.path.join(destinationpath, namefile + '.json')  # path destinationpath/nameFile.json
    with open(annotationFileName, 'w', encoding='utf8') as outfile:
        json.dump(elements, outfile, ensure_ascii=False, indent=4)
    print("generated: " + annotationFileName)


def infoWords(imageName):
    image = cv2.imread(imageName)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    image = threshold_img

    details = pytesseract.image_to_data(image, output_type=Output.DICT, lang='ita')

    # creating tuple with [coordinates], text OF SINGLE WORDS
    words = []  # contains ALL box + words + attributes
    idx = 0
    total_boxes = len(details['text'])
    for i in range(total_boxes):
        if int(details['conf'][i]) > 0 and str(details['text'][i]) != ' ':  # excluding low confidence and empty words
            #global idx
            idx += 1
            # coordinates format (left, top, left + width, top + height)
            coordinates = [details['left'][i], details['top'][i], details['width'][i] + details['left'][i],
                           details['height'][i] + details['top'][i]]
            # alternative coordinates format (left, top, width, height)
            # coordinateALT= [details['left'][i], details['top'][i], details['width'][i],  details['height'][i]]
            if details['text'][i].strip('.') != "" and details['text'][i].strip() != "" and details['text'][i].strip(
                    '_') != "":
                text = details['text'][i].strip('.')
                # creating single box + text
                word = {
                    'box': coordinates,
                    'text': text,
                    'id': str(idx),
                    'label': "word",
                }
                words.append(word)
    return words


def infoSentences(labelmepath, elements):
    infoRectangles = []
    global idx

    #generateGroupID(labelmepath)
    with open(labelmepath) as json_file:
        labelmeData = json.load(json_file)
    fields = labelmeData['shapes']
    for x in fields:
        if x['group_id'] is None:
            idx += 1
        sentence = ""
        wordSentence = []
        infoRectangle = {
            'text': x['text'],
            'box': [int(x['points'][0][0]), int(x['points'][0][1]), int(x['points'][1][0]), int(x['points'][1][1])] if int(x['points'][0][0]) <= int(x['points'][1][0])
                else [int(x['points'][1][0]), int(x['points'][1][1]), int(x['points'][0][0]), int(x['points'][0][1])],
            'label': x['label'],
            'id': x['group_id'] if not x['group_id'] is None else idx,
            'link': x['link'],
            'words': wordSentence
        }
        # grouping words in sentences
        for i in elements:
            if infoRectangle['box'][0] < i['box'][0] and infoRectangle['box'][1] < i['box'][1] and infoRectangle['box'][2] > i['box'][2] and infoRectangle['box'][3] > i['box'][3]:
                if (i['text'] != ""):
                    sentence += i['text'] + " "
                    wordSentence.append(i)

        if sentence != "" and sentence != ".":
            infoRectangle['text'] = sentence.strip()
        if infoRectangle['label'] != "word":
            infoRectangles.append(infoRectangle)
    return infoRectangles


# main

'''dataset = "C:\\Users\\veron\\Downloads\\dataset1"  # put here your path to dataset
images = os.path.join(dataset, "images")  # "C:/Users/veron/Downloads/dataset1/images"
annotations = os.path.join(dataset, "annotations")  # "C:/Users/veron/Downloads/dataset1/annotations"
labelme = os.path.join(dataset, "labelme")  # "C:/Users/veron/Downloads/dataset1/labelme"
labelmeInput = os.path.join(dataset, "labelmeInput")  # "C:/Users/veron/Downloads/dataset1/labelmeInput"
labelmeWords = os.path.join(dataset, "labelmeWords")  # "C:/Users/veron/Downloads/dataset1/labelmeWords"
labelmeGiusto = os.path.join(dataset, "labelmeGiusto")  # "C:/Users/veron/Downloads/dataset1/labelmeGiusto"
labelmeInputOK = os.path.join(dataset, "labelmeInputOK")  # "C:/Users/veron/Downloads/dataset1/labelmeInputOK"
final = os.path.join(dataset, "final")  # "C:/Users/veron/Downloads/dataset1/final"

# processes all images in dataset/images
for imagename in os.listdir(images):
    #if True:
    #imagename = "003.png"
    idx = 0
    # create word dict
    imagepath = os.path.join(images, imagename)
    wordsRectangles = infoWords(imagepath)
    # create sentence dict
    labelmepath = os.path.splitext(os.path.join(labelme, imagename))[0] + ".json"
    sentencesRectangles = infoSentences(labelmepath, wordsRectangles)
    # create json compatible with labelme
    labelmeData = generateLabelmeData(labelmepath, sentencesRectangles + wordsRectangles, False)
    generateJson(imagepath, labelmeData, labelmeInput)

    # lebel me with only words from pytesseract
    # labelmeWordsRectangles = generateLabelmeData(labelmepath, wordsRectangles, False)
    # generateJson(imagepath, labelmeWordsRectangles, labelmeWords)

    # update data with adjustment by hand
    giustopath = os.path.splitext(os.path.join(labelmeGiusto, imagename))[0] + ".json"
    aggiustati = adjuster(giustopath)
    sentencesRectanglesOK = infoSentences(labelmepath, aggiustati)

    labelmeDataOK = generateLabelmeData(labelmepath, sentencesRectanglesOK + aggiustati, False)
    generateJson(imagepath, labelmeDataOK, labelmeInputOK)

    finalpath = os.path.splitext(os.path.join(final, imagename))[0] + ".json"

    finalwords= []
    with open(finalpath, encoding="utf-8") as json_file:
        labelmeGiusti = json.load(json_file)
    for giusto in labelmeGiusti['shapes']:
        if giusto['label']=="word":
            giustoRectangle = {
                'text': giusto['text'],
                'label': giusto['label'],
                'box': [int(giusto['points'][0][0]), int(giusto['points'][0][1]), int(giusto['points'][1][0]),
                        int(giusto['points'][1][1])],
            }
        else:
            giustoRectangle = {
                'text': giusto['text'],
                'label': giusto['label'],
                'box': [int(giusto['points'][0][0]), int(giusto['points'][0][1]), int(giusto['points'][1][0]),
                        int(giusto['points'][1][1])],
                'id': giusto['group_id'],
                'link': giusto['link'],
            }
        finalwords.append(giustoRectangle)
    sentencesRectanglesFinal = infoSentences(finalpath, finalwords)
    #generate Ground Truth
    generateJson(imagepath, sentencesRectanglesFinal, annotations)

print("\nDONE")'''

# TODO: code optimization and documentation