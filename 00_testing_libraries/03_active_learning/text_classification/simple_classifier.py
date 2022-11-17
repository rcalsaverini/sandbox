import os
import numpy as np
import requests
import json
import pickle
from pprint import pprint
from uuid import uuid4

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import DATA_UNDEFINED_NAME, get_env


HOSTNAME = "http://localhost:8080"
API_KEY = "0896cff204660e66d4f9efca212000d1247c3a1d"
TOKEN_PATTERN = r"(?u)\b\w\w+\b|\w"  # type: ignore
MODEL_DIR = "model"


print("=> LABEL STUDIO HOSTNAME = ", HOSTNAME)
if not API_KEY:
    print("=> WARNING! API_KEY is not set")


def _get_target_field(label_configuration):
    """
    Get target field from label configuration
    """
    if len(label_configuration) == 1:
        return list(label_configuration.keys())[0]
    else:
        raise ValueError("Label configuration must contain only one target field")


def _get_input_fields(label_configuration, target_field):
    """
    Get input fields from label configuration
    """
    inputs = label_configuration[target_field]["inputs"]
    if len(inputs) == 1:
        if inputs[0]["type"] == "Text":
            return inputs[0]["value"]
        else:
            raise ValueError("Input field must be of type Text")
    else:
        raise ValueError("Label configuration must contain only one input field")


def _get_labels(label_configuration, target_field):
    """
    Get labels from label configuration
    """
    return label_configuration[target_field]["labels"]


class SimpleTextClassifier(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super(SimpleTextClassifier, self).__init__(**kwargs)
        self.target_field = _get_target_field(self.parsed_label_config)
        self.input_field = _get_input_fields(
            self.parsed_label_config, self.target_field
        )
        self.labels = _get_labels(self.parsed_label_config, self.target_field)
        if not self.train_output:
            self.reset_model()
        else:
            self.model_file = self.train_output["model_file"]
            with open(self.model_file, mode="rb") as f:
                self.model = pickle.load(f)

    def predict(self, tasks, **kwargs):
        print(self.model)
        inputs = [task["data"][self.input_field] for task in tasks]
        probabilities = self.model.predict_proba(inputs)
        predicted_labels = np.argmax(probabilities, axis=1)
        predicted_scores = probabilities[
            np.arange(len(predicted_labels)), predicted_labels
        ]

        return [
            {
                "result": [
                    {
                        "from_name": self.input_field,
                        "to_name": self.target_field,
                        "type": "choices",
                        "value": label,
                    }
                ],
                "score": score,
            }
            for label, score in zip(predicted_labels, predicted_scores)
        ]

    def fit(self, tasks, workdir=None, **kwargs):
        label_to_index = {label: index for index, label in enumerate(self.labels)}

        def _get_examples(task):
            annotation = task["annotations"][0]
            input = task["data"][self.input_field]
            for result in annotation["result"]:
                for label in result["value"]["choices"]:
                    yield (input, label)

        def _is_valid(task):
            annotations = task.get("annotations", [])
            if len(annotations) == 0:
                return False
            return not (
                annotations[0].get("skipped", False)
                or annotations[0].get("was_cancelled", False)
            )

        X = []
        y = []
        for task in tasks:
            print(task)
            if _is_valid(task):
                annotation = task["annotations"][0]
                input = task["data"][self.input_field]
                labels = annotation["result"][0]["value"]["choices"]
                for label in labels:
                    print(input, label)
                    X.append(input)
                    y.append(label_to_index[label])
        print(X)
        print(y)
        self.reset_model()
        self.model.fit(X, y)

        workdir = workdir or MODEL_DIR
        model_name = str(uuid4())[:8]
        if workdir:
            model_file = os.path.join(workdir, f"{model_name}.pkl")
        else:
            model_file = f"{model_name}.pkl"
        print(f"Save model to {model_file}")
        with open(model_file, mode="wb") as fout:
            pickle.dump(self.model, fout)

        return {"checkpoints": model_file}

    def reset_model(self):
        self.model = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 3)),
            LogisticRegression(C=10, verbose=True),
        )
