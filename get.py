#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Spyder Editor

Script file for Pitchbook assessment
Author: Srinivas 
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen
from html.parser import HTMLParser
import argparse, re




# Parser class to handle HTML tags and 
class MyHTMLParser(HTMLParser):
    tags = ""
    links = ""
    dat = ""
    
    # Gets ALL links (internal and external) and start tags
    def handle_starttag(self, tag, attrs):
        self.tags = self.tags + '<' + str(tag) + '>'
        if tag == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    self.links = self.links + str(value) + "\n"
    
    # Handles end tags
    def handle_endtag(self, tag):
        self.tags = self.tags + '</' + str(tag) + '>'
    
    # Gets data
    def handle_data(self, data):
        self.dat = self.dat + str(data)
        
# Method to clean the HTML data

# Credits: this method has been sourced from user PeYoTlL
# http://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python        

def clean(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return (text)


# Basically appends the http://  (we assume all links are http)
def fixURL(url):
    if not url.startswith('http://'):
        url = 'http://' + url
    return str(url)



#Method to dump values to output
def writeToFile(value, fileName):
    file = open(fileName, 'a', encoding='utf-8')
    file.write(value)
    file.close()

#Method to dump values to log file
def writeToLog(value):
    file = 'log.txt'
    file = open(file, 'a', encoding='utf-8')
    file.write(value)
    file.close()
    
  
    
# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="URL")
parser.add_argument("op", type=str, help="Output file")
args = parser.parse_args();

#Defaults
url = "http://pitchbook.com"
fileName = "out.txt"

writeToLog(args.url)
writeToLog(args.op)

pattern = "^[\w,\s-]+\.[A-Za-z]{3}$"
result = re.match(pattern, args.op)

if result:
    fileName = args.op
else:
    print("Invalid Filename, defaulting to: out.txt")    

url = fixURL(args.url)
response = urlopen(url)

# We recieved valid response
if response.status == 200:
    
    string = response.read().decode('utf-8')
    parser = MyHTMLParser();
    parser.feed(string);

    #Write Links
    writeToFile("[links]\n",fileName)
    writeToFile(parser.links, fileName)
    writeToFile("\n",fileName)
    
    
    #Write Tags
    writeToFile("[HTML]\n",fileName)
    writeToFile(parser.tags, fileName)
    writeToFile("\n\n",fileName)
    
    #Process  [sequences]
    
    writeToFile("[sequences]\n",fileName)
    
    rawData = clean(url)

    sequence = ""
    finalSequence = ""
    wordCount = 0;
    
    for substr in rawData.split('\n'):
        #writeToLog(substr)
        for subsubstr in substr.split(" "):
            #writeToLog(subsubstr + '\n')
                if subsubstr[0].isupper():
                    sequence = sequence + subsubstr + " "
                    wordCount = wordCount + 1;
                    writeToLog(subsubstr + "\n" )
                if  subsubstr[0].islower() and wordCount >= 2:
                    finalSequence = sequence + '\n'
                    sequence = ""
                    wordCount = 0;
                    #print(finalSequence)
                    writeToFile(finalSequence,fileName)
                    finalSequence = ""
else:
    print("No valid Response from server!")