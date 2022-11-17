from label_studio_ml.model import LabelStudioMLBase


class MyModel(LabelStudioMLBase):
    def __init__(self):
        super().__init__()
        self.model = self._load_model()

    def predict(self, tasks, **kwargs):
        return self.model

    def fit(self, tasks, workdir=None, **kwargs):
        return {"checkpoints": ""}
