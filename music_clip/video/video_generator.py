import os
from .big_sleep import BigSleepImagine
import contextlib
from datetime import datetime
from glob import glob

from music_clip.super_resuoltion.sr import SR

import cv2
from tqdm import tqdm


@contextlib.contextmanager
def cd_into_folder(folder_path):
    orignal_dir = os.getcwd()
    os.chdir(folder_path)
    yield
    os.chdir(orignal_dir)


# def morph_ffmpeg(paths, duration=10):
#     cur_image = "0idx_This_is_fire\\This_is_fire.best.png"
#     next_image = "1idx_Under_the_night's_sky\\Under_the_night's_sky.best.png"

#     commmand_one = []
#     command_two = []
#     for i, image_path in enumerate(paths):
#         commmand_one.append(f"-loop 1 -t 5 -i {image_path}")
#         command_two.append(
#             f"{i+1}format=yuva444p,fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+{4*(i+1)}/TB[f{i}]"
#         )

#     command = f'ffmpeg \
#         {" ".join(commmand_one)} \
#         -filter_complex \
#         "{";".join(command_two)} \
#         [0][f0]overlay[bg1];[bg1][f1]overlay[bg2];[bg2][f2]overlay[bg3]; \
#         [bg3][f3]overlay,format=yuv420p[v]" -map "[v]" -movflags +faststart out.mp4'
#     os.system(command)


def get_sort_key(path):
    image_num = path.split(".")[-2]
    folder_idx = path.split("idx")[0][-1]
    return int(str(1000 ** int(folder_idx)) + image_num)


def images_to_video_cv2(paths):
    img_array = []
    sr = SR()
    for filename in tqdm(sorted(paths, key=get_sort_key)[:]):
        try:
            # print(f"{filename}: {get_sort_key(filename)}")
            img = sr.upscale(cv2.imread(filename))
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        except Exception as e:
            print("error")
            print(e)

    out = cv2.VideoWriter("project.avi", cv2.VideoWriter_fourcc(*"DIVX"), 60, size)

    for image in img_array:
        out.write(image)
    out.release()


def merge_images_into_video(folder_path, duration=10):
    with cd_into_folder(folder_path):
        if not os.path.exists("video"):
            os.mkdir("video")

        images_folders = glob(f"./*idx*/")
        all_images_in_order = []
        last_generated_images = []
        best_generated_images = []
        for images_folder in images_folders:
            paths = glob(images_folder + "*")
            last_generated_images.append(paths[-1])
            best_generated_images.append(paths[-2])
            for image_path in paths[:-2]:
                all_images_in_order.append(image_path)

        # can try other morphing methods
        # morph_ffmpeg(last_generated_images)

        #
        images_to_video_cv2(all_images_in_order)


class VideoGenerator:
    def __init__(self) -> None:
        self.dream = BigSleepImagine(
            lr=7e-2,
            save_every=1,
            save_progress=True,
            iterations=750,
            epochs=1,
            save_best=True,
            open_folder=False,
            image_size=128,
        )

        self.folder_path = (
            f"generated_videos/{datetime.now().strftime('%m-%d_%H-%M-%S')}"
        )
        os.mkdir(self.folder_path)

    def generate_from_lyrics(self, lyrics):
        for idx, text in enumerate(lyrics):
            self.generate_images_from_text(text, idx)

        merge_images_into_video(self.folder_path)

    def generate_images_from_text(self, text, idx):
        text_images_folder = f"{self.folder_path}/{idx}idx_{text.replace(' ','_')}"
        os.makedirs(text_images_folder)
        with cd_into_folder(text_images_folder):
            # self.dream.reset()  # maybe not resting can give interesting results?
            self.dream.set_text(text)
            self.dream()

