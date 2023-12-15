import os


def get_model_dir():
    return os.path.join(os.path.dirname(__file__), "models_llps/")


def get_go_dir():
    return os.path.join(os.path.dirname(__file__), "go/")
