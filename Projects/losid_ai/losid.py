from googleapiclient.discovery import build
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

# Google Custom Search API key and CSE ID
api_key = 'YOUR_API_KEY'
cse_id = 'YOUR_CSE_ID'

# Create a service object for interacting with the API
service = build('customsearch', 'v1', developerKey=api_key)

def google_search(query):
    # Perform a Google search
    res = service.cse().list(q=query, cx=cse_id).execute()
    # Extract and return the snippet (description) from the first result
    return res['items'][0]['snippet']

def summarize_text(text, num_sentences=3):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the text into words
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    # Calculate word frequencies
    freq_dist = FreqDist(filtered_words)
    
    # Sort words by frequency
    sorted_words = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)
    
    # Get the most frequent words
    top_words = [word for word, freq in sorted_words[:10]]
    
    # Filter sentences containing the most frequent words
    summary_sentences = [sentence for sentence in sentences if any(word in sentence.lower() for word in top_words)]
    
    # Return the first 'num_sentences' summary sentences
    return ' '.join(summary_sentences[:num_sentences])

# Example usage
query = 'Artificial intelligence'
search_result = google_search(query)
summary = summarize_text(search_result)

print("Search Result:")
print(search_result)
print("\nSummary:")
print(summary)
