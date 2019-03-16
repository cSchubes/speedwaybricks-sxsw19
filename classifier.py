from fastai.vision import *
import numpy as np
from PIL import Image as PILImage

class Classify(object):

    def __init__(self, artifact_path, fname):
        self._path = artifact_path
        self._learn = load_learner(self._path, fname=fname)

    def predict_numpy(self, image):
        pil = PILImage.fromarray(image)
        img = pil2tensor(pil, np.float32).div_(255)
        predImg = Image(img)
        return self._learn.predict(predImg)
        