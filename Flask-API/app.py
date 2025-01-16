from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, InvalidVideoId
from flask_cors import CORS
import openai
from config import API_KEY  # Ensure this contains your actual OpenAI API key

app = Flask(__name__)
CORS(app, resources={r"/summary": {"origins": "*"}})  # Allow all origins for now; restrict later if needed

# Set OpenAI API key
openai.api_key = API_KEY
openai.api_base = "http://localhost:3040/v1"  # Reverse proxy base URL for the ChatGPT API

@app.route('/summary', methods=['GET'])
def youtube_summarizer():
    """
    Endpoint to summarize a YouTube video using its transcript.
    """
    video_id = request.args.get('v')  # Extract video ID from query parameters
    if not video_id:
        return jsonify({"data": "Video ID is required", "error": True})  # Handle missing video ID

    try:
        transcript = get_transcript(video_id)  # Fetch the transcript
        print("Transcript fetched successfully.")  # Log success
        data = open_ai(transcript)  # Summarize using OpenAI API
        print("OpenAI response received:", data)  # Log API response

        # Check for valid API response
        if "choices" in data and data.choices:
            return jsonify({"data": data.choices[0].message.content, "error": False})
        else:
            return jsonify({"data": "Unexpected API response format", "error": True})

    except NoTranscriptFound:
        return jsonify({"data": "No English Subtitles found", "error": True})  # Handle missing subtitles
    except InvalidVideoId:
        return jsonify({"data": "Invalid Video ID", "error": True})  # Handle invalid video ID
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        return jsonify({"data": "Unable to Summarize the video", "error": True})  # Handle generic errors


def get_transcript(video_id):
    """
    Fetches the transcript of a YouTube video given its video ID.
    """
    try:
        transcript_response = YouTubeTranscriptApi.get_transcript(video_id)  # Get transcript
        transcript_list = [item['text'] for item in transcript_response]  # Extract text
        return ' '.join(transcript_list)  # Combine all transcript segments into a single string
    except NoTranscriptFound:
        raise NoTranscriptFound("No subtitles available for this video.")
    except InvalidVideoId:
        raise InvalidVideoId("The video ID provided is invalid.")
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")


def open_ai(transcript):
    """
    Uses OpenAI's API to summarize the transcript in 10 points.
    """
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You have to summarize a YouTube video using its transcript in 10 points."},
                {"role": "user", "content": transcript}
            ]
        )
        # Log the raw API response
        print("OpenAI Response:", completion)
        return completion
    except Exception as e:
        # Log any API-related errors
        raise Exception(f"Error with OpenAI API: {str(e)}")


# Run the Flask app (uncomment when running locally)
if __name__ == '__main__':
    app.run(debug=True)
