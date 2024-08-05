# Phylosohpy

- Keep it simple, stupid!
- Standing on the giants' shoudlers!

# Exercise 1

**Problem Statement:** Build a chabot that can handle videos allowing users search whatever they concern that related to those videos.

**Goal:**

- Enhance user's experience.

## Features

- [] Insights of the video. -> Text, Image, Time
- [] Search any specific moments in a video.

## Solutions

- Input as a (custom) .mp4 video(s) (or Youtube link(s)).
- Process videos: 
    - Shot boundaries => For searching similar image based on user's image-based input.
    - Transcripts => For retrieving based on user's text-based input.
- Using vector db for storing the processed information => structured format.

- Install `ffmeq` via `apt install ffmpeg`

## Resource

- https://github.com/JuanBindez/pytubefix.git
- https://github.com/openai/whisper.git

_Note:_ 

- Internal knowledge.
- The transcript may contain the name of characters within the video. For example, the Mr.Beast's video includes a transcript like "Mr.Beast: ...". In case the similarity search feature can not work properly, the image would be turned into the name of the character. The problem would be turned into "The timestamp(s) that the character is mentioned ... ".
- Get wrong information when using only the caption/transcript.


# Exercise 2

**Problem Statement:** Deploying an open-source LLM ((model BLOOMZ 1b1)[
https://huggingface.co/bigscience/bloomz-1b1]) while considering several factors: 

+ VRAM
+ Speed
+ Performance
+ Feature support: token completions, log proabilities, ...

**Goal:**

- Test LLM knowledge and deployment skills, ...