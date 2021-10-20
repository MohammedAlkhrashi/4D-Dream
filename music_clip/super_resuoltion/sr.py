import cv2


class SR:
    def __init__(self, model="edsr") -> None:
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        if model == "edsr":
            model_path = f"../../models/EDSR_x4.pb"
            self.sr.readModel(model_path)
            self.sr.setModel("edsr", 4)
        elif model == "fsrcnn":
            model_path = f"../../models/FSRCNN_x4.pb"
            self.sr.readModel(model_path)
            self.sr.setModel("fsrcnn", 4)

    def upscale(self, image):
        return self.sr.upsample(image)

