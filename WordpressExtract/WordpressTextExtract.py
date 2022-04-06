import os
import xml.etree.ElementTree as ET
import re
from tqdm import tqdm

outputPath = './post/'
fileNameRule = "{}_{}.md"

template = '''---
title: "{}"
date: {}
draft: false
tags: {}
categories: {}
---
{}
'''

textPattern = r'[a-zA-z<>!/:="-; {}’]'
stripPattern = r'^\n'
onlyWordPattern = r'[]'
multiNewLinePattern = r'\n{2,}'
monthMap = {"january": "01", "jan": "01", "february": "02", "feb": "02", "march": "03", "mar": "03", "april": "04",
            "apr": "04", "may": "05", "june": "06", "jun": "06", "july": "07",
            "jul": "07", "august": "08", "aug": "08", "september": "09", "sep": "09", "october": "10", "oct": "10",
            "november": "11", "nov": "11", "december": "12", "dec": "12"}
categoryMap = {'essay': '文章', 'ci': '词', 'shi': '诗'}

ErrorList = []


class Post:
    title = None
    pubDate = None
    content = None
    tags = None
    category = None

    def __init__(self, title, pubDate, content, category, tags):
        self.title = title.replace("undefined", "")
        self.content = content.replace('\n', '\n\n').replace("undefined", "")
        self.tags = tags
        self.category = category
        if not pubDate is None:
            dateList = pubDate.split(',')[-1].split('+')[0][1:-1].split(' ')
            self.pubDate = DateTime(dateList[2], monthMap[dateList[1].lower()], dateList[0], dateList[3], "+08").toString()
        else:
            self.pubDate = "2018-01-09T16:22:25+08:00"
            ErrorList.append(self.title)

    def toMarkdown(self):
        return template.format(self.title, self.pubDate, self.tags, self.category, self.content)

    def toFile(self):
        filename = fileNameRule.format(self.pubDate.split('T')[0], self.title).replace(" ", "")
        with open(os.path.join(outputPath+filename), 'w') as f:
            f.write(self.toMarkdown())
        # print(f"File {self.title} is transformed.")


class DateTime:
    year = None
    month = None
    day = None
    time = None
    # hour = None
    # minute = None
    # second = None
    timeZone = None

    def __init__(self, year, month, day, time, timeZone):
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        # self.hour = hour
        # self.minute = minute
        # self.second = second
        self.timeZone = timeZone

    def toString(self):
        return "{}-{}-{}T{}{}:00".format(self.year, self.month, self.day, self.time, self.timeZone)


if __name__ == '__main__':
    tree = ET.ElementTree(file="WordPress.2021-08-24.xml")
    root = tree.getroot()
    itemList = root.find('channel').findall('item')
    postsList = []
    print('Processing...')
    for i in tqdm(itemList):
        title = i.find('title').text.replace("\n", '').strip()
        pubDate = i.find('pubDate').text
        content = i.find('contents').text.replace('<p', '\n').replace('<strong>', '\n')
        content = re.sub(textPattern, '', content)
        content = re.sub(multiNewLinePattern, '\n', content)
        content = re.sub(stripPattern, '', content)
        tags = []
        category = []
        for j in i.findall('category'):
            if j.attrib['domain'] == 'category':
                category.append(categoryMap[j.attrib['nicename']].replace("undefined", ""))
            elif j.attrib['domain'] == 'post_tag':
                tags.append(j.text.replace("\n", '').replace("undefined", "").strip())
        postsList.append(Post(title, pubDate, content, category, tags))
    print('Writing...')
    for i in tqdm(postsList):
        i.toFile()
    print(ErrorList)
