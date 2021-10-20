from .lyrics import LyricsGenerator
from .music import MusicGenerator
from .video import VideoGenerator

from .video.video_generator import merge_images_into_video

from .super_resuoltion import SR
import cv2

import matplotlib.pyplot as plt


def main():
    lyrics_gen = LyricsGenerator()
    lyrics = lyrics_gen()

    music_gen = MusicGenerator()
    music = music_gen()

    video_gen = VideoGenerator()
    video_gen.generate_from_lyrics(lyrics)

    # test_folder = "generated_videos/10-20_17-50-46"
    # merge_images_into_video(test_folder)

    # filename = "generated_videos/10-20_17-50-46/3idx_Hopeless_the_raging_tempest_of_her_woe/Hopeless_the_raging_tempest_of_her_woe.png"
    # img = cv2.imread(filename)

    # resized = cv2.resize(img, dsize=None, fx=4, fy=4)

    # sr = SR()
    # upscaled_image = sr.upscale(img)

    # plt.figure(figsize=(12, 8))
    # plt.subplot(1, 3, 1)
    # # Original image
    # plt.imshow(img[:, :, ::-1])
    # plt.subplot(1, 3, 2)
    # # SR upscaled
    # plt.imshow(upscaled_image[:, :, ::-1])
    # plt.subplot(1, 3, 3)
    # # OpenCV upscaled
    # plt.imshow(resized[:, :, ::-1])
    # plt.show()
    # plt.waitforbuttonpress()

