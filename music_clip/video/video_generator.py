import os

from music_clip.common import cd_into_folder
from .big_sleep import BigSleepImagine
from datetime import datetime
from glob import glob


import cv2
from tqdm import tqdm


def get_sort_key(path):
    image_num = path.split(".")[-2]
    folder_idx = path.split("idx")[0][-1]
    return int(str(1000 ** int(folder_idx)) + image_num)


def images_to_video_cv2_morph(paths, sr_model):
    img_array = []
    for filename in tqdm(sorted(paths, key=get_sort_key)[:]):
        try:
            # print(f"{filename}: {get_sort_key(filename)}")
            img = sr_model.upscale(cv2.imread(filename))
            # img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        except Exception as e:
            print("error")
            print(e)

    out = cv2.VideoWriter("project.avi", cv2.VideoWriter_fourcc(*"DIVX"), 60, size)
    for image in tqdm(img_array):
        out.write(image)
    out.release()


def merge_images_into_video(folder_path, sr_model=None):
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
        images_to_video_cv2_morph(all_images_in_order, sr_model)


class VideoGenerator:
    def __init__(self, sr_model=None) -> None:
        self.dream = BigSleepImagine(
            lr=7e-2,
            save_every=1,
            save_progress=True,
            iterations=750,
            epochs=2,
            save_best=True,
            open_folder=False,
            image_size=512,
        )
        self.sr_model = sr_model
        self.folder_path = (
            f"generated_videos/{datetime.now().strftime('%m-%d_%H-%M-%S')}"
        )
        os.mkdir(self.folder_path)

    def generate_from_lyrics(self, lyrics):
        for idx, text in enumerate(lyrics):
            self.generate_images_from_text(text, idx)

        merge_images_into_video(self.folder_path, self.sr_model)

    def generate_images_from_text(self, text, idx):
        text_images_folder = f"{self.folder_path}/{idx}idx_{text.replace(' ','_')}"
        os.makedirs(text_images_folder)
        with cd_into_folder(text_images_folder):
            # self.dream.reset()  # maybe not resting can give interesting results?
            self.dream.set_text(text)
            self.dream()

