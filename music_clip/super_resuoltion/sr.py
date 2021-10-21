import cv2
from ISR.models import RRDN, RDN
from ISR.predict import Predictor
import numpy as np
from PIL import Image


class SuperResolution:
    def __init__(self, model="edsr") -> None:
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        if model == "edsr":
            model_path = f"models/EDSR_x4.pb"
            self.sr.readModel(model_path)
            self.sr.setModel("edsr", 4)
        elif model == "fsrcnn":
            model_path = f"models/FSRCNN_x4.pb"
            self.sr.readModel(model_path)
            self.sr.setModel("fsrcnn", 4)

    def upscale(self, image):
        return self.sr.upsample(image)


class SuperReslutionV2:
    def __init__(self, model="RRDN", weights="gans") -> None:
        # self.model = RDN(weights="noise-cancel")
        self.model = RRDN(weights="gans")
        # self.model = RDN(weights="psnr-small")
        # self.model = RDN(weights="psnr-large")

    def upscale(self, image):

        sr_img = self.model.predict(np.array(image))
        return cv2.cvtColor(cv2.cvtColor(sr_img, cv2.COLOR_RGB2BGR), cv2.COLOR_RGB2BGR)

    def upscale_folder(self, folder_path):
        # predictor = Predictor(input_dir="data/input/test_images/")
        # predictor.get_predictions(model=self.model,)
        pass

