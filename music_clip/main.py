from glob import glob
from textwrap import fill

from moviepy.video.VideoClip import TextClip
from .lyrics import LyricsGenerator

from .music import MusicGenerator
from .video import VideoGenerator

# from .video.video_generator import merge_images_into_video

from .super_resuoltion import SuperResolution, SuperReslutionV2
import cv2

import moviepy.editor as me
import os

import tempfile

IMAGEMAGICK_BINARY = os.getenv(
    "IMAGEMAGICK_BINARY", "C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"
)


def main():

    lyrics_gen = LyricsGenerator()
    lyrics = lyrics_gen()

    music_gen = MusicGenerator()
    music_gen.generate_initial_melody(lyrics)
    music_gen.harmonize_melody()

    super_resuoltion_model = SuperResolution("fsrcnn")
    video_gen = VideoGenerator(sr_model=super_resuoltion_model)
    video_gen.generate_from_lyrics(lyrics)

    # quick_testing()


def quick_testing():

    super_resuoltion_model = SuperResolution("fsrcnn")

    test_folder = "generated_videos/10-21_09-56-15"
    merge_images_into_video(test_folder, super_resuoltion_model)
    return

    return

    def get_sort_key(path):
        image_num = path.split(".")[-2]
        folder_idx = path.split("idx")[0][-1]
        return int(str(1000 ** int(folder_idx)) + image_num)

    from glob import glob

    folder_path = "generated_videos/10-21_15-36-33"
    images_folders = glob(f"{folder_path}/*idx*/")
    all_images_in_order = []
    last_generated_images = []
    best_generated_images = []
    for images_folder in images_folders:
        paths = glob(images_folder + "*")
        last_generated_images.append(paths[-1])
        best_generated_images.append(paths[-2])
        for image_path in paths[:-2]:
            all_images_in_order.append(image_path)

    all_images_in_order = sorted(all_images_in_order, key=get_sort_key)

    lyrics = [
        "In the middle of the trees",
        "From a day that was bight",
        "A dark hopeless night",
    ]
    durations = [4, 4, 3]
    create_lyrics(all_images_in_order, lyrics, durations)


def create_lyrics(frames, lyrics, durations, fps=120, max_line_length=10):
    final = None

    verses_count = len(lyrics)
    current_verse = 0
    frames_per_verse = len(frames) // verses_count

    fianls = []
    for txt, duration in zip(lyrics, durations):
        blackbg = (
            me.ColorClip((750, 512), (30, 30, 30))
            # .set_position("center")
            # .set_duration((duration))
        )
        start = current_verse * frames_per_verse
        end = (current_verse + 1) * (frames_per_verse)

        print(duration)
        print(len(frames))
        print(verses_count)
        print(duration / (len(frames) / verses_count))
        print(start, " ", end)

        clips = [
            me.ImageClip(m, duration=duration / (len(frames) / verses_count))
            for m in frames[start:end]
        ]
        concat_clip = me.concatenate_videoclips(clips, method="compose").set_position(
            "left"
        )
        words = txt.split()
        lines = []
        cur_length = 0
        cur_line = ""
        for word in words:
            cur_length += len(word)
            if cur_length <= max_line_length:
                cur_line += word + " "
            else:
                lines.append(cur_line)
                cur_line = ""
                cur_length = 0

                cur_line += word + " "
                cur_length += len(word)
        lines.append(cur_line)
        txt = "\n".join(lines)

        font_size = 20
        txt_width = blackbg.w // (1.36 + (1 / font_size))
        txt_height = blackbg.h // 2.7
        text_dims = (txt_width, txt_height)
        txtClip = (
            me.TextClip(
                txt,
                color="white",
                fontsize=font_size,
                font="Garamond",
                method="caption",
            )
            .set_position(text_dims)
            .set_duration(duration)
        )
        # txtClips.append(txtClip)

        comp_list = [blackbg, concat_clip, txtClip]
        current_verse += 1
        final = me.CompositeVideoClip(comp_list).set_duration(duration)
        final.write_videofile(f"output/final{current_verse}.mp4", fps=fps)
        fianls.append(final)
        # with tempfile.NamedTemporaryFile() as video_tempfile:
        #     final.write_videofile(video_tempfile.name + ".mp4", fps=fps)
        #     video_tempfile.seek(0)

        #     for clip in clips:
        #         clip.close()
        #     for clip in comp_list:
        #         clip.close()
        # video_tempfile

        # concat_text_clip = me.concatenate_videoclips(
        #     txtClips, method="compose"
        # ).set_position("left")

    video_with_lyrics = me.concatenate_videoclips(fianls, method="chain").set_position(
        "cenetr"
    )
    # video_with_lyrics.audio = me.AudioClip('somepath')
    video_with_lyrics.write_videofile("output/video.mp4", fps=fps)

    # if not final:
    # else:
    #     final: me.VideoClip = me.CompositeVideoClip(
    #         final, me.CompositeVideoClip(comp_list).set_duration(duration)
    #     )

    # final.write_videofile(f"output/final.mp4", fps=fps)
    # for clip in clips:
    #     clip.close()
    # for clip in comp_list:
    #     clip.close()


"""
In the middle of the trees,
From a day that was bight,
A dark hopeless night,
A man to the right,
We all should fight,
The firey sun,
A bloody bird
"""

# filename = "generated_videos/10-20_17-50-46/3idx_Hopeless_the_raging_tempest_of_her_woe/Hopeless_the_raging_tempest_of_her_woe.png"
# img = cv2.imread(filename)

# resized = cv2.resize(img, dsize=None, fx=4, fy=4)

# sr = SuperReslutionV2()
# upscaled_image = sr.upscale(img)

# import matplotlib.pyplot as plt

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

