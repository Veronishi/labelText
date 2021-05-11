'''
Created on 9 mar 2021

@author: Venturino
'''
import pytesseract
import cv2
from pytesseract import Output


def adjuster(imagepath, selected, idx):
    for item in selected:
        if item.label == "word":
            if item.group_id is None:
                idx += 1
                item.group_id = idx
            img = cv2.imread(imagepath)
            if item.points[0].y() <= item.points[1].y():
                crop_img = img[int(item.points[0].y()):int(item.points[1].y()), int(item.points[0].x()):int(item.points[1].x())]
            else:
                crop_img = img[int(item.points[1].y()):int(item.points[0].y()), int(item.points[1].x()):int(item.points[0].x())]
            #cv2.imshow('crop',crop_img)
            #cv2.waitKey(0)
            item.text = ''.join(pytesseract.image_to_data(crop_img, output_type=Output.DICT, lang='ita')['text'])

def infoWords(imageName, idx):
    image = cv2.imread(imageName)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    image = threshold_img

    details = pytesseract.image_to_data(image, output_type=Output.DICT, lang='ita')

    # creating tuple with [coordinates], text OF SINGLE WORDS
    words = []  # contains ALL box + words + attributes
    total_boxes = len(details['text'])
    for i in range(total_boxes):
        if int(details['conf'][i]) > 0 and str(details['text'][i]) != ' ':  # excluding low confidence and empty words
            # coordinates format (left, top, left + width, top + height)
            coordinates = [details['left'][i], details['top'][i], details['width'][i] + details['left'][i],
                           details['height'][i] + details['top'][i]]
            # alternative coordinates format (left, top, width, height)
            # coordinateALT= [details['left'][i], details['top'][i], details['width'][i],  details['height'][i]]
            if details['text'][i].strip('.') != "" and details['text'][i].strip() != "" and details['text'][i].strip(
                    '_') != "":
                text = details['text'][i].strip('.')
                # creating single box + text
                idx += 1
                word = {
                    'text': text,
                    'label': "word",
                    'points': [[coordinates[0], coordinates[1]], [coordinates[2], coordinates[3]]],  # [x1,y1][x2,y2]
                    'shape_type': "rectangle",
                    'group_id': idx,
                    'link': set(),
                    'flags': {},
                    'other_data': None,
                }
                words.append(word)
    return words


def infoSentences(rectangles, words, idx):
    for rectangle in rectangles:
        points = [rectangle.points[0].x(), rectangle.points[0].y(), rectangle.points[1].x(), rectangle.points[1].y()]
        if rectangle.group_id is None:
            idx += 1
            rectangle.group_id = idx
        sentence = ""
        wordSentence = []
        infoRectangle = {
            'text': rectangle.text,
            'box': [int(points[0]), int(points[1]), int(points[2]), int(points[3])] if int(points[0]) <= int(int(points[2]))
                else [int(points[2]), int(points[3]), int(points[0]), int(points[1])],
            'label': rectangle.label,
            'id': rectangle.group_id if rectangle.group_id is not None else idx,
            'link': rectangle.link,
            'words': wordSentence
        }
        # grouping words in sentences
        for word in words:
            w = {'box': [int(word.points[0].x()), int(word.points[0].y()), int(word.points[1].x()), int(word.points[1].y())]}
            if infoRectangle['box'][0] < w['box'][0] and infoRectangle['box'][1] < w['box'][1] and infoRectangle['box'][2] > w['box'][2] and infoRectangle['box'][3] > w['box'][3]:
                if (word.text != ""):
                    sentence += word.text + " "
                    wordSentence.append(word)
        if sentence != "" and sentence != ".":
            infoRectangle['text'] = sentence.strip()
            rectangle.text = sentence.strip()
        rectangle.setWords(wordSentence)

# TODO: code optimization and documentation