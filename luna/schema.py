from typing import Dict
from langchain.pydantic_v1 import BaseModel, validator
from pytubefix.captions import Caption

class Media(BaseModel): 
    name: str

class YoutubeMedia(Media): 
    author: str
    description: str
    length: int             # in second
    thumbnail_url: str
    channel_url: str
    age_retricted: bool
    captions_lang: Dict[str, str]

    @validator('captions_lang',  pre=True)
    @classmethod
    def convert_to_dict(cls, caption_tracks: list[Caption]): 
        caption_lang = {}
        for caption in caption_tracks: 
            caption_lang[caption.name] = caption.code

        return caption_lang