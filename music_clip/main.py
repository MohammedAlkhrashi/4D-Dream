from .lyrics import LyricsGenerator
from .music import MusicGenerator
from .video import VideoGenerator


def main():
    lyrics_gen = LyricsGenerator()
    lyrics = lyrics_gen()

    music_gen = MusicGenerator()
    music = music_gen()

    video_gen = VideoGenerator()
    video = video_gen()

    print("ok")

