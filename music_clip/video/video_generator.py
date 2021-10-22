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
    img = cv2.imread(paths[0])
    height, width, _ = img.shape
    size = (width, height)
    out = cv2.VideoWriter("project.avi", cv2.VideoWriter_fourcc(*"DIVX"), 340, size)
    for filename in tqdm(sorted(paths, key=get_sort_key)[:]):
        try:
            # print(f"{filename}: {get_sort_key(filename)}")
            img = cv2.imread(filename)
            out.write(img)
            # img = cv2.imread(filename)
        except Exception as e:
            print("error")
            print(e)
    out.release()


def upscale_paths(paths, sr_model, every=1):
    os.mkdir("upscaled_images")
    upscaled_paths = []
    count = 1000000
    for i, path in enumerate(tqdm(paths)):
        if not i % every:
            continue
        img = sr_model.upscale(cv2.imread(path))
        image_path = f"upscaled_images/{count}.png"
        cv2.imwrite(image_path, img)
        upscaled_paths.append(image_path)
        count += 1
    return upscale_paths


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

        all_images_in_order = sorted(all_images_in_order, key=get_sort_key)
        if sr_model:
            if not os.path.exists("upscaled_images"):
                all_images_in_order = upscale_paths(all_images_in_order, sr_model)
            else:
                all_images_in_order = glob("./upscaled_images/*")

        images_to_video_cv2_morph(all_images_in_order, sr_model)


class VideoGenerator:
    def __init__(self, sr_model=None) -> None:
        self.dream = BigSleepImagine(
            lr=7e-2,
            save_every=1,
            save_progress=True,
            iterations=1000,
            epochs=5,
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

