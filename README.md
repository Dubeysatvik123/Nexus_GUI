# College Information Audio Query Service

This repository contains a Flask-based web application that allows users to ask questions about a college by submitting an audio file. The application processes the audio query, retrieves relevant information from specified URLs, and responds with an audio message.

## Features

- **Audio Query Processing**: Users can submit questions as audio files.
- **Natural Language Processing**: Utilizes spaCy for keyword extraction and processing.
- **Web Scraping**: Retrieves data from specified college URLs using BeautifulSoup.
- **Text-to-Speech**: Generates an audio response using gTTS (Google Text-to-Speech).
- **REST API**: Provides an endpoint to handle audio queries and respond with audio answers.

## Requirements

- Python 3.x
- Flask
- requests
- BeautifulSoup4
- spaCy
- gTTS
- SpeechRecognition

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/college-info-audio-query.git
    cd college-info-audio-query
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Download spaCy language model**:
    ```sh
    python -m spacy download en_core_web_sm
    ```

## Usage

3. **Receive the audio response**:
    - The response will be an audio file (`response.mp3`) containing the answer to the query.

## Endpoints

### POST /analyze_audio

#### Request
- `audio_data`: The audio file containing the user's query.

#### Response
- `200 OK`: Returns an audio file with the response.
- `500 Internal Server Error`: Returns an error message if something goes wrong.

## Example

1. **Submit an audio file with a question**:
    - Question: "What courses are offered?"

2. **Process and retrieve data from specified URLs**:
    - The application will process the query, extract keywords, scrape the relevant URLs, and generate a response.

3. **Receive an audio response**:
    - The response might mention the courses offered and provide context.

## Adding New Keywords and URLs

You can add more keywords and their respective URLs in the `college_data` dictionary in `app.py`. This allows the application to handle a broader range of queries.

```python
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
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README to better fit your project's specifics and add any additional information that might be helpful for users or contributors.
