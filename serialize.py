#

import joblib


class Data:
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save_data(self, filename: str, value):
        filename = "./" + filename

        with open(filename, "wb") as f:
            joblib.dump(value, f, compress=3)

        print("save data!")

    def load_data(self, filename: str) -> object:
        filename = "./" + filename

        with open(filename, "rb") as f:
            value = joblib.load(f)
            return value
