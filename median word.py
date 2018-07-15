
# Finding the median word length on a Rainforest QA webpage
# 
# Assumptions
# * All hyphenated words (e.g. humans-in-the-loop, data-related) counted as one word.
# * Instances of 100%, 75%, 401k, ‘e.g.’, QA and 3x were counted as one word
# * Title, apply here button, header, footer and location info ("San Francisco / United States ...") were **not** included in the word count.
# 

import pandas as pd
import numpy as np
import itertools as it

from bs4 import BeautifulSoup
import requests
from requests import get

# download source code using the det function from the requests package
page = requests.get('https://jobs.lever.co/rainforest/e7eab367-cae8-4e7b-8642-e7b66c4c00bb?ref=keyvalues')

# confirm successful download with a code '200' response
page

# great an object containing the source code and have a look
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

# the job description text has the class 'section page centered'; create a list of the items with that tag
body = soup.find_all('div', class_="section page-centered")

# loop through the list to get the just the text from each item
text = []
for i in range(0,len(body)):
    text.append(body[i].get_text())

# remove characters and add spacing where needed, put result in new list
words = []
for i in range(0, len(text)):
    words.append([''.join(v).strip() for k, v in it.groupby(text[i], lambda x: x in ('/()!:')) if not k])

# convert from a list of lists to a single list of strings
for i in range(0, len(words)):
    words[i] = ' '.join(words[i])

# put list into a single string containing the entire job description
word_block = ''
for i in range(0, len(words)):
    temp = ''.join(words[i])
    word_block += temp
    temp= ''

#insert space where a lowercase letter abuts an uppercase letter
import re
word_block = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', word_block)
word_block

# fix the rest of the random spacing problems that will affect word counting
word_block = word_block.replace('Py Datas', 'PyDatas')
word_block = word_block.replace('Py Torch', 'PyTorch')
word_block = word_block.replace('401 k', '401k')
word_block = word_block.replace('attendance3x', 'attendance 3x')
word_block = word_block.replace('options100%', 'options 100%')
word_block = word_block.replace('.', ' ')
word_block = word_block.replace('e g', 'e.g.')

# for ease of assessing word length, create a new list containing each word of word_block as an element and have a look at it
lets_count = []
lets_count = word_block.split()
lets_count

# how many words are in the job description?
len(lets_count)

# a total of 656 words in the list puts the median at the agerage length of word nos. 328 and 329 (python indices 327 and 328)
lengths = []
for i in range(0, len(lets_count)):
    lengths.append(len(lets_count[i]))
lengths = sorted(lengths)

# the answer is 4
lengths[327:329]

# for fun - the actual two words at the middle of the job discription (both loger than 4 letters!)
lets_count[327:329]

# more fun - a quick istogram of list lengths (not a surprise that it's right skewed)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(12,5))
plt.hist(lengths, bins=17, facecolor='green', edgecolor='black')
plt.xticks(np.arange(min(lengths), max(lengths)+1, 1.0))
plt.xlabel('Word Lengths')
plt.ylabel('Count')

