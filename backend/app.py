import requests
from bs4 import BeautifulSoup
import spacy
from gtts import gTTS
import speech_recognition as sr
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def get_website_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all paragraphs on the webpage
        paragraphs = soup.find_all(['p', 'ul', 'ol'])

        # Concatenate the text content of all paragraphs
        website_data = ' '.join(element.get_text() for element in paragraphs)
        return website_data.lower()  # Convert to lowercase
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the website: {e}")
        return None
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return None

def process_question(question):
    # Use spaCy for NLP processing
    doc = nlp(question)
    
    # Extract keywords (non-stop words)
    keywords = [token.text.lower() for token in doc if not token.is_stop]
    
    return keywords

def generate_response(processed_question, website_data, url):
    if not website_data:
        return f"I couldn't retrieve information from the website."

    # Convert both processed_question and website_data to lowercase for case-insensitive comparison
    processed_question_lower = [keyword.lower() for keyword in processed_question]
    website_data_lower = website_data.lower()

    # Check if any keyword is present in the website data
    matched_keywords = [keyword for keyword in processed_question_lower if keyword in website_data_lower]

    if matched_keywords:
        # Provide context for the matched keywords by finding sentences containing them
        context_sentences = []
        for sentence in website_data.split('. '):
            if any(keyword in sentence.lower() for keyword in matched_keywords):
                context_sentences.append(sentence)

        if context_sentences:
            context = '. '.join(context_sentences)
            response = f"The website mentions the following keywords: {', '.join(matched_keywords)}. Here is some context: {context}."
        else:
            response = f"The website mentions the following keywords: {', '.join(matched_keywords)}. No additional context found."
    else:
        response = f"I couldn't find specific information based on your question about {url}."

    return response

@app.route('/analyze_audio', methods=['POST'])
def analyze_audio():
    try:
        # Get the audio file from the request
        audio_file = request.files['audio_data']

        # Use SpeechRecognition to transcribe the audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        user_query = recognizer.recognize_google(audio_data)

        college_data = {
            "nri": ['https://www.nrigroupindia.com/'],
            "courses": ['https://www.nrigroupindia.com/courses/'],
            "inception": ['https://www.nrigroupindia.com/about-us/the-inception/'],
            "vision": ['https://www.nrigroupindia.com/about-us/the-inception/'],
            "mission": ['https://www.nrigroupindia.com/about-us/the-inception/'],
            "admission": ['https://www.nrigroupindia.com/admission-procedure/'],
            "computer science department": ['https://www.nrigroupindia.com/niist/computer-science-department/']
            # Add more keywords with their respective URLs
        }

        processed_question = process_question(user_query)
        response_text = "I couldn't find information based on your query."

        for keyword, urls in college_data.items():
            if keyword.lower() in processed_question:
                for url in urls:
                    website_data = get_website_data(url)
                    if website_data:
                        response_text = generate_response(processed_question, website_data, url)
                        break

        # Generate audio response
        tts = gTTS(text=response_text, lang='en')
        tts.save('response.mp3')

        # Send the audio file back to the frontend
        with open('response.mp3', 'rb') as audio_file:
            audio_data = audio_file.read()

        return audio_data, 200, {'Content-Type': 'audio/mpeg'}
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500

if __name__ == "__main__":
    app.run(debug=True)



