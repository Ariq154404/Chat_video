import sys
import os
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import io

class VideoTranscriber:
    def __init__(self, model_path = "models/vosk-model-small-en-us-0.15", interval_length=60):
        if not os.path.exists(model_path):
            raise FileNotFoundError("Vosk model path does not exist. Please provide a valid path.")
        
        self.model = Model(model_path)
        self.interval_length = interval_length
        

    @staticmethod
    def format_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:06.3f}".format(int(hours), int(minutes), seconds)

    def transcribe_video(self, video_data, output_text_path):
        # Convert video data to audio using in-memory buffer
        video_buffer = io.BytesIO(video_data)
        audio = AudioSegment.from_file(video_buffer)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        
        # Read audio data
        audio_data = io.BytesIO()
        audio.export(audio_data, format="wav")
        audio_data.seek(0)
        data = audio_data.read()
        duration = len(audio) / 1000  # Duration of audio in seconds
        
        # Prepare for transcription
        rec = KaldiRecognizer(self.model, 16000)
        results = []
        current_time = 0
        
        while current_time < duration:
            segment = data[int(16000 * 2 * current_time):int(16000 * 2 * (current_time + self.interval_length))] 
            if rec.AcceptWaveform(segment):
                results.append(rec.Result())
            current_time += self.interval_length
        
        # Finalize and get last part of transcription
        results.append(rec.FinalResult())

        # Save Transcript to Text File
        with open(output_text_path, 'w') as f:
            f.write("The following lines are transcript from a video with time intervals in parentheses followed by the sentences within that timestamp:\n\n")
            for i, result in enumerate(results):
                result_json = json.loads(result)
                if 'text' in result_json:
                    start_time = self.format_time(i * self.interval_length)
                    end_time = self.format_time((i + 1) * self.interval_length)
                    f.write(f"[{start_time} - {end_time}] {result_json['text']}\n")

        print(f"Transcript saved to {output_text_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <path_to_vosk_model> <output_text_path> <interval_length>")
    else:
        model_path = sys.argv[1]
        output_text_path = sys.argv[2]
        interval_length = float(sys.argv[3])

        # Example: Read video data from a file (you would replace this part with getting video data from other sources)
        with open("videos/Ancient Life as Old as the Universe.mp4", "rb") as video_file:
            video_data = video_file.read()
            print("TYYYYPEEEE",type(video_data))

        transcriber = VideoTranscriber(model_path, interval_length)
        transcriber.transcribe_video(video_data, output_text_path)
