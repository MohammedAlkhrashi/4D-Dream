import cv2


class SR:
    def __init__(self, model) -> None:
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = "EDSR_x4.pb"
        sr.readModel(path)

    def __call__(self):
        pass
