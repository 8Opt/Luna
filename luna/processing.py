import os
import cv2

import tempfile
from typing import Union 

from pytubefix import YouTube
from pytubefix.cli import on_progress

def get_youtube(url): 
    youtube = YouTube(url=url, on_progress_callback = on_progress)
    return youtube

def get_caption(youtube, 
                lang:str='en',  # Get caption based on language
                to_local_dir: Union[str, None]=None, # Save to local dir
                ) -> str:
    try: 
        
        if not lang in youtube.captions:
            return f"Your chosen language is not provided by the video. Please refer to {youtube.caption_tracks}"
        
        caption = youtube.captions.get_by_language_code(lang)
        caption = caption.generate_srt_captions()

        if to_local_dir != None:
            if not os.path.exists(to_local_dir): 
                os.makedirs(to_local_dir)
            caption.save_captions(to_local_dir)

        return caption
    except Exception as e: 
        raise e


def get_transcript(youtube, 
                   whisper_model:str="base", 
                   to_local_dir: Union[str, None]=None
                   ) -> str:
    try: 
        import whisper
        
        audio = youtube.streams.get_audio_only()

        # Let's load the base model. This is not the most accurate
        # model but it's fast.
        whisper_model = whisper.load_model(whisper_model)

        with tempfile.TemporaryDirectory() as tmpdir:
            file = audio.download(output_path=tmpdir)
            transcription = whisper_model.transcribe(file, fp16=False)["text"].strip()

            with open(to_local_dir, "w") as file:
                file.write(transcription)
                
        return transcription
    except Exception as e: 
        raise e


# Function to extract frames 
def get_frames_capturing(path_or_file, 
                         out_dir, 
                         selected_points:list[int],
                         time_interval=1, 
                         return_frames:bool=False,
                         ): 
  
    if not os.path.exists(out_dir): 
        os.makedirs(out_dir)
    frames = []
    points = selected_points

    # Path to video file 
    print("[INFO] Start capturing")
    cap = cv2.VideoCapture(path_or_file) 
  
    # Used as counter variable 
    count = 0

    while True:
        
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate the current timestamp (assuming FPS = 30)
        timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)

        # Check if the current timestamp matches the desired interval
        if timestamp % time_interval == 0:
            try: 
                now = points[0]
                if timestamp == now: 
                    frames.append(frame)
                    print(f'[INFO] Length of frames: {len(frames)}')
                    img_path = os.path.join(out_dir, f'frame_{count}.jpg')
                    cv2.imwrite(img_path, frame)
                    count  += 1
                    points.pop(0)
            except: 
                break
            
    # cap.release()
    
    if return_frames: 
        return frames
