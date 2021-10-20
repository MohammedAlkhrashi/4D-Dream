from .lyrics import LyricsGenerator
from .music import MusicGenerator
from .video import VideoGenerator

from .video.video_generator import merge_images_into_video


def main():
    lyrics_gen = LyricsGenerator()
    lyrics = lyrics_gen()

    music_gen = MusicGenerator()
    music = music_gen()

    # video_gen = VideoGenerator()
    # video_gen.generate_from_lyrics(lyrics)

    test_folder = "generated_videos/10-20_17-50-46"
    merge_images_into_video(test_folder)
