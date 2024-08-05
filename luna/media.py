import tempfile
from typing import Union 

from pytubefix import YouTube
from pytubefix.cli import on_progress

from luna.base import BaseMediaReader


class YoutubeReader(BaseMediaReader): 
    def __init__(self, 
                lang:str='en',  # Get caption based on language
                to_local_dir: Union[str, None]=None, # Save to local dir
                transcript_mode:str="caption",        # There are 2 modes [caption, transcript]   
                **kwargs 
                ): 
        self.to_local_dir = to_local_dir
        self.lang = lang 
        self.transcript_mode = transcript_mode

    def get_audio(self, file):
        youtube = YouTube(url=file, on_progress_callback = on_progress)
        return youtube
    
    def get_transcript(self, file):
        return super().get_transcript(file)
    
    def lazy_read(self, file):
        if self.valid_url(file): 
            ...
        return super().lazy_read(file)()