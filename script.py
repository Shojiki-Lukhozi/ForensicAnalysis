import os
import nltk
from nltk.corpus import wordnet as wn
from textblob import TextBlob

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('wordnet')

def generate_html_results(results):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search Results</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Search Results</h1>
        <table>
            <tr>
                <th>File</th>
                <th>Match Percentage</th>
                <th>Sentiment</th>
            </tr>
    """

    for file, data in results.items():
        html_content += f"""
            <tr>
                <td>{file}</td>
                <td>{data['matches']}</td>
                <td>{data['sentiment']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open('search_results.html', 'w') as f:
        f.write(html_content)

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def analyze_file_sentiments(files):
    sentiments = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            sentiments[file] = get_sentiment(content)
    return sentiments

def search_files(files, query):

    words = nltk.word_tokenize(query)
    synonyms = {word: get_synonyms(word) for word in words}

    print(f"Query Synonyms: {synonyms}")

    results = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            content_sentiment = get_sentiment(content)
            matches = [word.lower() for word in words if word in content.lower()]
            for word, syns in synonyms.items():
                if any(syn in content.lower() for syn in syns):
                    matches.append(word)
            if matches:
                results[file] = {'matches': matches, 'sentiment': content_sentiment}
    return results

def main():
    # Gather all text files in the current directory
    text_files = [f for f in os.listdir('.') if f.endswith('.txt')]
  
    # Display initial sentiment analysis of each file
    sentiments = analyze_file_sentiments(text_files)
    for file, sentiment in sentiments.items():
        print(f"File: {file}, Sentiment: {sentiment}")
  
    # Prompt for search query
    query = input("Enter your search query: ")
  
    # Search files based on query and synonyms
    results = search_files(text_files, query)
  
    # Display results
    for file, data in results.items():
        print(f"File: {file}")
        print(f"  Matches: {data['matches']}")
        print(f"  Sentiment: {data['sentiment']}")
    
    generate_html_results(results)
      
if __name__ == "__main__":
    main()