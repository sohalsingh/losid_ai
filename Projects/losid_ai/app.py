import nltk
nltk.download('punkt')
nltk.download('stopwords')
from flask import Flask, render_template, request
from googleapiclient.discovery import build
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

app = Flask(__name__)

# Google Custom Search API key and CSE ID
api_key = 'YOUR_API_KEY'
cse_id = 'YOUR_CSE_ID'

# Create a service object for interacting with the API
service = build('customsearch', 'v1', developerKey=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    search_result = google_search(query)
    summary = summarize_text(search_result)
    return render_template('result.html', query=query, search_result=search_result, summary=summary)

def google_search(query):
    res = service.cse().list(q=query, cx=cse_id).execute()
    return res['items'][0]['snippet']

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    freq_dist = FreqDist(filtered_words)
    sorted_words = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)
    top_words = [word for word, freq in sorted_words[:10]]
    summary_sentences = [sentence for sentence in sentences if any(word in sentence.lower() for word in top_words)]
    return ' '.join(summary_sentences[:num_sentences])

if __name__ == '__main__':
    app.run(debug=True)
