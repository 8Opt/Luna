from abc import ABC, abstractmethod

import requests

class BaseFoundationModel(ABC): 

    @staticmethod
    @abstractmethod
    def from_pretrained(provider, config): 
        ...

class BaseMediaReader(ABC): 
    SUPPORTED_FORMAT= {
        "URL": ["youtube"], 
        "MEDIA": ["mp4", "MP4"]
    }

    @abstractmethod
    def get_audio(self, file): 
        ...

    @abstractmethod
    def get_transcript(self, file): 
        ...

    @abstractmethod
    def lazy_read(self, file): 
        ...

    def valid_url(self, payload) -> bool: 
        url_patterns = self.SUPPORTED_FORMAT["URL"]
        for pattern in url_patterns: 
            if pattern in payload \
                and requests.get(url=payload).status_code == "200": 
                return True
            
        return False
    
    def valid_media(self, payload) -> bool: 
        media_patterns = self.SUPPORTED_FORMAT("MEDIA")
        file_type = payload.split('.')[-1]
        return True if file_type in media_patterns else False