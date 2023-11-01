import sys
import os
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

class VideoTranscriber:
    def __init__(self, model_path, interval_length=5):
        if not os.path.exists(model_path):
            raise FileNotFoundError("Vosk model path does not exist. Please provide a valid path.")
        
        self.model = Model(model_path)
        self.interval_length = interval_length

    @staticmethod
    def format_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:06.3f}".format(int(hours), int(minutes), seconds)

    def transcribe_video(self, video_path, output_text_path):
        if not os.path.exists(video_path):
            raise FileNotFoundError("Video file not found. Please provide a valid video file path.")
        
        # Extract and convert audio from video
        audio_path = "audio.wav"
        audio = AudioSegment.from_file(video_path)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        audio.export(audio_path, format="wav")
        
        # Read audio data
        wf = open(audio_path, "rb")
        data = wf.read()
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
            for i, result in enumerate(results):
                result_json = json.loads(result)
                if 'text' in result_json:
                    start_time = self.format_time(i * self.interval_length)
                    end_time = self.format_time((i + 1) * self.interval_length)
                    f.write(f"[{start_time} - {end_time}] {result_json['text']}\n")

        print(f"Transcript saved to {output_text_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <path_to_video> <path_to_vosk_model> <output_text_path> <interval_length>")
    else:
        video_path = sys.argv[1]
        model_path = sys.argv[2]
        output_text_path = sys.argv[3]
        interval_length = float(sys.argv[4])

        transcriber = VideoTranscriber(model_path, interval_length)
        transcriber.transcribe_video(video_path, output_text_path)
