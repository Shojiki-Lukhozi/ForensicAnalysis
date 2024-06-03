## change to your own credentials

in the emailStorage.py and send.pyfile

    pop3_address="pop3.mailtrap.io"
    pop3_port=1100
    username=""
    password =""
    mailserver = (pop3_address, pop3_port)



## Textblob polarity

This indicates in a text has a postive , negative or neutral sentiment polarity is [-1,1]

postive sentiment closer to 1
negative sentiment closer to -1
neutral sentiment close to 0


## ntlk and wordnet 

We use this to lemmatization and synonyms creations
We pattern match the synonyms in the email sent

# Demo discussions

## proof of some dev environment

show our github repository

https://github.com/Shojiki-Lukhozi/ForensicAnalysis

## extent to which we used our own code

we only used library framework that aided with semantic analysis 
- nltk which is a nlp library
- wordnet to generate synonyms to our keywords

The rest of the code is ours

70% our code and 30% library code

## contribution to digital forensics?

This demonstration has a huge potential to contributing to the DF world.
This demostration displays how time can be saved by using keyword search mechanism that doesn't just search those key words,
but expanding the search space into synonyms so even though the exact words were not used but search is able to detect similar words. 

furthermore the tool does semantic analysis , this helps outline the negative and positive sentiment of content, this can help save time for the investigator. The Investigator could use this tool to divide the search space and focus on the content they are interested in.

This can contribute you investigator having potential leads at an early stage of the investigation.

This tool has an extensive use case list,

The tool can be used for any text that needs to be categorised and searched for any investigation.

## Contribution AI makes to your project

AI is the baseline of the solution 

search is based on ai(NLP)
semantic analysis is based on ai (NLP)


## Capabilities of AI (please complete this point)


## Perform neccessary preprocessing off data for AI capability

- retrieve email from mail server
- convert data recieve to utf-8
- form the data into a text file 
- use AI to analyse the text files


## final output and presentation

- The output is a match to certain out or no match to the output
- html file has been created to display the output
