from google.cloud import speech

class SpeechService:
    def __init__(self):
        self.client = speech.SpeechClient()

    async def transcribe_audio(self, audio_content: bytes) -> str:
        try:
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )

            response = self.client.recognize(config=config, audio=audio)
            
            transcription = ""
            for result in response.results:
                transcription += result.alternatives[0].transcript

            return transcription
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            raise 