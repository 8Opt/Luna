"""
Objects in this file are in charge of reading video files. In detail, the reading function work as: 
    1. Extracting caption/transcript from video files. 
    2. Capturing frames from the video.
"""


import os
import tempfile

import cv2
import requests
import ffmpeg

from pytubefix import YouTube
from pytubefix.cli import on_progress

from luna.base import BaseMediaReader
from luna.schema import YoutubeMedia
from luna.utils import dict_to_pd, get_second


class YoutubeReader(BaseMediaReader): 
    def __init__(self, 
                transcript_mode:str="caption",        # There are 2 modes [caption, transcription]   
                **kwargs 
                ): 
        super().__init__()
        self.transcript_mode = transcript_mode      # youtube provides captions so the choice of using provided tools or extended tools to convert spoken words to written words is a choice of product developing. 

        # Check models for transcription
        if self.transcript_mode == "transcript": 
            if 'whisper_model' in kwargs: 
                self.whisper_model = kwargs['whisper_model']

    def get_audio(self, payload):
        is_valid = self.__valid_url(payload)
        if is_valid: 
            youtube = YouTube(url=payload, on_progress_callback = on_progress)
            return youtube
        return None
    
    def get_transcript(self, payload) -> str:

        match self.transcript_mode: 
            case "caption": 
                if self.lang in self.metadata.captions_lang.values(): 
                    caption = payload.captions.get_by_language_code(self.lang)
                    caption = caption.generate_srt_captions()

                    return caption
                return None
            
            case "transcription": 
                import whisper
                
                audio = payload.streams.get_audio_only()

                whisper_model = whisper.load_model(whisper_model)

                with tempfile.TemporaryDirectory() as tmpdir:
                    file = audio.download(output_path=tmpdir)
                    transcription = whisper_model.transcribe(file, fp16=False)["text"].strip()

                return transcription

    def lazy_read(self, payload):
        youtube = self.get_audio(payload)
        self.metadata = self.__get_metadata(youtube=youtube)

        if not self.lang in self.metadata.captions_lang.values():
            return f"Your chosen language is not provided by the video. Please refer to {self.metadata['captions_lang']}"
        document = self.get_transcript(youtube)

        # Main difference is the selected points from youtube's caption, for transcription, there is no timestamp provided by `whisper`.
        match self.transcript_mode: 
            case "caption":         
                # print("[INFO] Processing information to dictionary")
                content = document.split('\n\n')
                content_dict = {
                    'from': [], 
                    'to': [], 
                    'content': []
                }
                
                # Processing youtube's captions for cutting frames
                for c in content: 
                    c  = c.split('\n')
                    content_dict['content'].append(c[-1])               # Get content
                    timestamps = c[1].split(' --> ')                    # Time process

                    t_from = timestamps[0].split(',')[0]
                    content_dict['from'].append(get_second(t_from))

                    t_to = timestamps[1].split(',')[0]
                    content_dict['to'].append(get_second(t_to))


                # print("[INFO] Processing dict to pandas") : to get points easily
                content_df = dict_to_pd(content_dict)
                    
                # print("[INFO] Saving to .csv")    : for checking
                content_df.to_csv(f"{self.to_local_dir}/{self.metadata.name}.csv", encoding='utf-8')

                # print("[INFO] Downloading youtube video")
                with tempfile.TemporaryDirectory() as tmpdir: 
                    mp4_streams = youtube.streams.filter(file_extension='mp4')
                    for stream in mp4_streams:
                        if stream.type == 'video':
                            try:
                                # downloading the video
                                stream.download(output_path=tmpdir)
                                print('Video downloaded successfully!')

                                # Just get the first audio that is considered as video
                                break
                            except:
                                print("Some Error!")

                    print('[INFO] Cutting frames')
                    points = content_df['from'].to_list()
                    # print(points)
                    # print(os.listdir(tmpdir))
                    temp_yt_file = os.path.join(tmpdir, os.listdir(tmpdir)[0])
                    # print(temp_yt_file)
                    frames = self.get_frames(temp_yt_file, 
                                            selected_points=points, 
                                            )
            case "transcription": 
                with tempfile.TemporaryDirectory() as tmpdir: 
                    mp4_streams = youtube.streams.filter(file_extension='mp4')
                    for stream in mp4_streams:
                        if stream.type == 'video':
                            try:
                                # downloading the video
                                stream.download(output_path=tmpdir)
                                print('Video downloaded successfully!')

                                break
                            except:
                                print("Some Error!")

                    print('[INFO] Cutting frames')
                    points = content_df['from'].to_list()
                    temp_yt_file = os.path.join(tmpdir, os.listdir(tmpdir)[0])
                    frames = self.get_frames(temp_yt_file, 
                                            )


        if self.save_document: 
                file_path = os.path.join(self.to_local_dir, self.metadata.name + '.txt')
                with open(file_path, "w") as file:
                    file.write(document)


        if self.save_frames: 
            count = 0
            img_dir = os.path.join(self.to_local_dir, 'images') 
            if not os.path.exists(img_dir): 
                os.makedirs(img_dir)

            for frame in frames: 
                img_path = os.path.join(self.to_local_dir, "images", f'frame_{count}.jpg')
                cv2.imwrite(img_path, frame)
                count +=1

        return {
                    'document': document, 
                    'frames': frames
                }
    
    def __get_metadata(self, youtube) -> YoutubeMedia: 
        metadata = YoutubeMedia(name=youtube.title, 
                                author=youtube.author, 
                                description=youtube.description, 
                                length=youtube.length, 
                                thumbnail_url=youtube.thumbnail_url, 
                                channel_url=youtube.channel_url, 
                                age_retricted=youtube.age_restricted, 
                                captions_lang=youtube.captions)
        return metadata

    def __valid_url(self, payload) -> bool: 
        url_patterns = self.SUPPORTED_FORMAT["URL"]
        for pattern in url_patterns: 
            if pattern in payload \
                and requests.get(url=payload).status_code == 200: 
                return True
        return False
    


class MP4Reader(BaseMediaReader): 
    def __init__(self, 
                 lang, 
                 save_wav:bool): 
        super().__init__()
        ...

    def lazy_read(self, payload):
        return super().lazy_read(payload)
    
    def get_audio(self, payload):
        return super().get_audio(payload)
    
    def get_transcript(self, payload) -> str:
        return super().get_transcript(payload)
    
    def __convert_mp4_to_wav(self, input_file, output_file): 
        from ffmpeg import input, output
        """
            Libraries that support `speech to text`, most of them, utilize .wav file
        """
        ...


    def __valid_media(self, payload) -> bool: 
        media_patterns = self.SUPPORTED_FORMAT("MEDIA")
        file_type = payload.split('.')[-1]
        return True if file_type in media_patterns else False