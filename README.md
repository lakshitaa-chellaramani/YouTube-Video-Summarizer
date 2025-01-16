
# YouTube Summarizer

This is a YouTube video summarizer that fetches video transcripts and generates a concise summary using OpenAI's GPT-3.5 model.

## Features
- Extracts video transcript using YouTube's API.
- Summarizes the transcript in 10 points using OpenAI's GPT-3.5 model.

## Prerequisites

To get this project up and running, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/lakshitaa-chellaramani/YouTube-Video-Summarizer.git
   cd YouTube-Summarizer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Replace the `API_KEY`**:
   - Open the `config.py` file.
   - Replace `your_openai_api_key_here` with your actual OpenAI API key.

   ```python
   API_KEY = 'your_openai_api_key_here'  # Replace with your OpenAI API key
   ```

   Without this step, the project will not work.

5. Run the application:
   ```bash
   python app.py
   ```

## Usage

- Access the application through your browser or API client (like Postman) at `http://127.0.0.1:5000/summary?v=VIDEO_ID`.
- Replace `VIDEO_ID` with the YouTube video ID you want to summarize.

Example:
```
http://127.0.0.1:5000/summary?v=giYejigUM9A
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

