import os
import uuid

import openai
import requests
import soundfile as sf

import config

openai.api_key = config.OPENAI_API_KEY


def chat_completion(messages: list[dict]) -> str:
    try:
        completion = openai.chat.completions.create(
            model=config.GPT_MODEL,
            messages=messages
        )

        return completion['choices'][0]['message']['content']
    except:
        return config.ERROR_MESSAGE


def transcript_audio(media_url: str) -> dict:
    try:
        ogg_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.ogg'
        data = requests.get(media_url)
        with open(ogg_file_path, 'wb') as file:
            file.write(data.content)
        audio_data, sample_rate = sf.read(ogg_file_path)
        mp3_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.mp3'
        sf.write(mp3_file_path, audio_data, sample_rate)
        audio_file = open(mp3_file_path, 'rb')
        os.unlink(ogg_file_path)
        os.unlink(mp3_file_path)
        transcript = openai.audio.transcriptions.create(
            model='whisper-1', file=audio_file, api_key=config.OPENAI_API_KEY, response_format='text')

        return {
            'status': 1,
            'transcript': transcript['text']
        }
    except Exception as e:
        print('Error at transcript_audio...')
        print(e)
        return {
            'status': 0,
            'transcript': ''
        }
