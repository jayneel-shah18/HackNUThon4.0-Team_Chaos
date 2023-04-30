import streamlit as st
import socks
import socket
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random
from urllib.request import urlopen
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('wordnet')
from nltk.tag import pos_tag
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import opinion_lexicon
nltk.download('opinion_lexicon')
nltk.download('stopwords')
import time


st.title("Cybercrime Detection - Team Chaos")

socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

df=pd.read_csv("C:\\Users\\jayne\\OneDrive\\Desktop\\globalterrorismdb_2021Jan-June_1222dist.csv",encoding='ISO-8859-1', dtype=None)
columns=list(df.columns)
substring=[]
for i in df['scite1']:
    index=i.find('"',1)
    substr=i[1:index]
    substring.append(substr)

filtered_sentences=[]

stop_words = set(stopwords.words('english'))

for i in substring:
    words = nltk.word_tokenize(i)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    filtered_sent = ' '.join(filtered_words)
    filtered_sentences.append(filtered_sent)

lemmatizer= WordNetLemmatizer()
lemmatized_sentences=[]
for i in filtered_sentences:
    lemma=lemmatizer.lemmatize(i)
    lemmatized_sentences.append(lemma)

final_sentence=[]
for i in filtered_sentences:
    tokens = word_tokenize(i)
    tags = pos_tag(tokens)
    result = [word for word, tag in tags if tag != 'NNP' and tag != 'NNPS']
    result_text = ' '.join(result)
    final_sentence.append(result_text)

dataset=[]
neg_words = set(opinion_lexicon.negative())
for i in final_sentence:
    words = nltk.word_tokenize(i)
    negative_words = [word for word in words if word in neg_words]
    
    if negative_words:
        dataset.append(negative_words)
    
dataset_1d = [item for sublist in dataset for item in sublist]
final_dataset=set(dataset_1d)

st.caption("Automatic Scrapper")
option = st.selectbox('Select the number of sites you wish to scrape:', ['50', '100', '200'])

final = []
if option == 50:
    for keyword in final_dataset[:25]:
        res = requests.get(f"https://ahmia.fi/search/?q={keyword}")
        soup = BeautifulSoup(res.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        links = list(filter(None, links)) 
        onion = []
        for l in links:
            if "onion" in l:
                onion.append(l)
        pref = "/search/search/redirect?search_term=&redirect_url="
        links = []
        n=len(pref) + len(keyword)
        for link in onion:
            res = ''
            for i in range(0, len(link)):
                if i >= n:
                    res = res + link[i]    
            links.append(res)
        links1 = []
        for link in links:
            if link.find("competition") == -1:
                links1.append(link)
        final.append(links1[:2])
elif option == 100:
    for keyword in final_dataset[:25]:
        res = requests.get(f"https://ahmia.fi/search/?q={keyword}")
        soup = BeautifulSoup(res.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        links = list(filter(None, links)) 
        onion = []
        for l in links:
            if "onion" in l:
                onion.append(l)
        pref = "/search/search/redirect?search_term=&redirect_url="
        links = []
        n=len(pref) + len(keyword)
        for link in onion:
            res = ''
            for i in range(0, len(link)):
                if i >= n:
                    res = res + link[i]    
            links.append(res)
        links1 = []
        for link in links:
            if link.find("competition") == -1:
                links1.append(link)
        final.append(links1[:4])
elif option == 200:
    for keyword in final_dataset[:30]:
        res = requests.get(f"https://ahmia.fi/search/?q={keyword}")
        soup = BeautifulSoup(res.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        links = list(filter(None, links)) 
        onion = []
        for l in links:
            if "onion" in l:
                onion.append(l)
        pref = "/search/search/redirect?search_term=&redirect_url="
        links = []
        n=len(pref) + len(keyword)
        for link in onion:
            res = ''
            for i in range(0, len(link)):
                if i >= n:
                    res = res + link[i]    
            links.append(res)
        links1 = []
        for link in links:
            if link.find("competition") == -1:
                links1.append(link)
        final.append(links1[:7])
        
final_list = [element for sublist in final for element in sublist]
st.write(final_list)


st.caption("Manual Scrapper")
keyword = st.text_input("Enter a keyword to identify malicious sites: ", 'Hitman')
res = requests.get(f"https://ahmia.fi/search/?q={keyword}")
soup = BeautifulSoup(res.content, 'html.parser')
links = [link.get('href') for link in soup.find_all('a')]
links = list(filter(None, links)) 

onion = []

for l in links:
    if "onion" in l:
        onion.append(l)

pref = "/search/search/redirect?search_term=&redirect_url="
links = []
n=len(pref) + len(keyword)
for link in onion:
    res = ''
    for i in range(0, len(link)):
        if i >= n:
            res = res + link[i]    
    links.append(res)

links1 = []
for link in links:
    if link.find("competition") == -1:
        links1.append(link)

final = []
start=time.time()
end=time.time()
sum=end-start
timeout=100
st.write("Fetching your links...")
try:
    for link in links1:
        start_time=time.time()
        try:
            temp_res = requests.get(link,timeout=5)
            temp_soup = BeautifulSoup(temp_res.content, "html.parser")
            tag = temp_soup.body
            temp_str = ''
            for string in tag.strings:
                temp_str += string
            count=0
            for i in final_dataset:
                if i in temp_str:
                    count+=1
            if(count>5):
                final.append(link)
            if(len(final)>=10 ):
                break
        except Exception:
            pass
        if(len(final)>=10):
            break
        end_time = time.time()
        elapsed_time = end_time - start_time
        sum=sum+elapsed_time
        if sum > timeout:
            raise TimeoutError("Execution time exceeded {} seconds".format(timeout))
            break
except TimeoutError as te:
    if(len(final)>0):
        for links in final:
            st.write(links)
    else:
        st.write(te)