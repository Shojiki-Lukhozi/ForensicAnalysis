## change to your own credentials

in the emailStorage.py and send.pyfile

    pop3_address="pop3.mailtrap.io"
    pop3_port=1100
    username=""
    password =""
    mailserver = (pop3_address, pop3_port)



## Textblob polarity

This indicates if a text has a postive, negative or neutral sentiment. Polarity is [-1,1]

Postive sentiment closer to 1
Negative sentiment closer to -1
Neutral sentiment close to 0


## ntlk and wordnet 

We use this for lemmatization and synonyms creations
We pattern match the synonyms in the email sent

# Demo discussions

## Proof of some dev environment

Show our github repository

https://github.com/Shojiki-Lukhozi/ForensicAnalysis

## Extent to which we used our own code

we only used library framework that aided with semantic analysis 
- nltk which is a nlp library
- wordnet to generate synonyms to our keywords

The rest of the code is ours

- 70% our code  
- 30% library code

## Contribution to digital forensics?

This demonstration has significant potential to contribute to the digital forensics field.
This demonstration displays how time can be saved by using keyword search mechanism that doesn't just search those key words,
but expanding the search space into synonyms so even though the exact words were not used but search is able to detect similar words. 

Furthermore, the tool performs semantic analysis, which helps outline the negative and positive sentiment of content. This can save time for the investigator by dividing the search space and allowing them to focus on the content of interest.

This can contribute you investigator having potential leads at an early stage of the investigation.

The tool has extensive use cases and can be used for any text that needs to be categorised and searched for investigation purposes.

## Contribution AI makes to your project

AI is the baseline of the solution 

The search is based on AI (NLP)
Semantic analysis is based on AI (NLP)


## Capabilities of AI (please complete this point)

AI enhances the ability to understand and process natural language, enabling:

- Advanced search mechanisms using NLP techniques
- Semantic analysis to gauge the sentiment of text
- Pattern matching to identify keywords and their synonyms

## Perform neccessary preprocessing off data for AI capability

- Retrieve email from mail server
- Convert data recieve to utf-8
- Form the data into a text file 
- Use AI to analyse the text files


## Final output and presentation

- The output is a match to certain out or no match to the output
- An HTML file has been created to display the output
