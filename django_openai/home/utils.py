import moviepy.editor as mp
from django.conf import settings
from pathlib import Path
from openai import OpenAI
import os


class Transcricao:
    def __init__(self, path_video):
        self.path_video = path_video
        self.video = mp.VideoFileClip(path_video)
        self.client = OpenAI(
            api_key = settings.SK_OPENAI

        )
    
    @property
    def path_audio(self):
        return f'{settings.BASE_DIR / "audio_file" / Path(self.path_video).stem}.mp3'
    
    def save_tempfile(self):
        self.video.audio.write_audiofile(self.path_audio)
    
    def transcrever(self):
        self.save_tempfile()

        try:
            with open(self.path_audio, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model='whisper-1',
                    file=audio_file,
                    response_format='text',

                )

        finally:
            os.remove(self.path_audio)

        return transcript


def gerar_resumo(texto):
    client = OpenAI(api_key=settings.SK_OPENAI)

    response = client.completions.create(
        model='gpt-3.5-turbo-instruct',
        prompt=f'Olá, boa tarde! Resuma esse textopor favor {texto}',

    )

    return response.choices[0].text
