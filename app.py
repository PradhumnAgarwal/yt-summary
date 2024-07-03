from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)


@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('&')[0]
    video_id = video_id.split('=')[1]
    # print(video_id)
    transcript = get_transcript(video_id)
    summary = get_summary(transcript)
    return summary, 200

def get_transcript(video_id):
    # print("get_transcript is called")
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    print(transcript)
    return transcript

    
def get_summary(transcript):
    print("Starting get_summary")
    summariser = pipeline('summarization')
    # print("Summarizer pipeline created")
    summary = ''
    transcript_length = len(transcript)
    print(f"Transcript length: {transcript_length}")

    for i in range(0, (transcript_length // 1000) + 1):
        start_idx = i * 1000
        end_idx = (i + 1) * 1000
        # print(f"Processing transcript chunk from {start_idx} to {end_idx}")

        chunk = transcript[start_idx:end_idx]
        if chunk:  # Check if chunk is not empty
            try:
                summary_text = summariser(chunk)[0]['summary_text']
                summary += summary_text + ' '
                # print(f"Chunk summary: {summary_text}")
            except Exception as e:
                print(f"Error summarizing chunk: {e}")

    # print("Completed get_summary")
    return summary


if __name__ == '__main__':
    app.run()