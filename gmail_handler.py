'''
Created on Oct 22, 2016

@author: Mason Wong
'''

import quickstart as qs
import base64
import email
#from apiclient import errors
from bs4 import BeautifulSoup 
import re 
from builtins import str
from nltk.corpus import stopwords

'''run through the list of dictionaries in the names labels 
list and extract only the names
names = []
for index, row in enumerate(labels):
    names.append(row['name'])
    print(row['name'])'''

#Acquire inbox unread messages and their ids using getMessageInfo 
messages = qs.getMessageInfo('in: inbox is: unread')
print(messages)

#Create a message_id list to store all the ids from message info 
messages_id = []
for key in messages['messages']:
    messages_id.append(key['id'])
print(messages_id)

#Sample message pull
message_dict = {}
#This will be the list for all the relevant UNCLEAN text from the email
string_list = []

for key, row in enumerate(messages_id):
    #Key is the index of each message id in the list, row is the value at each index
    #Use the getMessage method to extract them message from the message_id (row)
    #Extract msg_str through the MIME message object and encoding it in ASCII
    mdict = qs.getMessage('me', row)
    msg_str = base64.urlsafe_b64decode(mdict['raw'].encode('ASCII'))
 
    #Extract the message and turn it into a email message
    messagetest4 = email.message_from_bytes(msg_str)
   
    #Walk through each part of the email message object and locate parts with html text
    for part in messagetest4.walk():
        if part.get_content_type() == 'text/html':
            #Store the part of the message with html into a variable
            message_text = part.get_payload()
            
            #Create a beautiful soup object to parse through the html text
            soup = BeautifulSoup(message_text, 'html.parser')
            
            #For every instance of the p tag, print out the text
            for tags in soup.find_all(re.compile("^div")):
                string_list.append(tags.find_all(text=True))   
                  
    
#Condense the formatting into a single list of strings
new_list = sum(string_list, [])
#Break it down further by splitting each word through the criteria of space
nlist = re.split(" ",str(new_list))
#Finally initiate the new list that will be CLEAN
finalwords = []

#Clean the list of words to remove unnecessary stuff
for strang in nlist:
    strang= re.sub("=?(\w|\W)+=(\w|\W)+","",strang)
    strang= strang.replace("=\\r\\n","")
    strang= strang.replace("\\n","")
    strang= re.sub("\\\\[a-z0-9]+","",strang)
    strang= re.sub("(\.|:|,|;|!|\||(-+))","",strang)
    strang= re.sub("^\W","",strang)
    strang= re.sub(">|<","",strang)
    strang= re.sub("']","", strang)
    strang= re.sub("^'|'$","", strang)
    strang= re.sub("^\"|\"$","", strang)
    strang = strang.lower()
    finalwords.append(strang)

#Filter out all the empty entries from filter
finalwords = list(filter(None, finalwords))
#Check if they are clean!
print(finalwords)

#List of stop words such as "the" to look out for
cachedStopWords = stopwords.words("english")

'''Simple loop to count the number of times a word surfaces 
that is not considered a stop word'''
finaldict = {}
for val in finalwords:
    if val in cachedStopWords:
        continue
    elif val in finaldict:
        finaldict[val] += 1
    else:
        finaldict[val] = 1

#CONGRATS PRINT THE BADBOY!
print(finaldict)
