import json
import os.path

from flask import Flask, request


class DataManager:
    PATH = "data.json"

    def __init__(self):
        self.__data: dict[str, int] = {}
        self.__load()

    def __load(self) -> None:
        if not os.path.isfile(self.PATH):
            self.__save()
        else:
            with open(self.PATH) as f:
                self.__data = json.load(f)

    def __save(self) -> None:
        with open(self.PATH, "w") as f:
            json.dump(self.__data, f, indent=4)

    def is_exist(self, key: str) -> bool:
        return key in self.__data

    def get(self, key: str) -> int:
        if self.is_exist(key):
            return self.__data.get(key)
        else:
            raise KeyError(f"Key {key} not found")

    def set(self, key: str, value: int) -> None:
        self.__data[key] = value
        self.__save()

    def increase(self, key: str) -> None:
        if self.is_exist(key):
            self.__data[key] += 1
            self.__save()
        else:
            raise KeyError(f"Key {key} not found")

    def decrease(self, key: str) -> None:
        if self.is_exist(key):
            if self.__data[key] == 0:
                raise ValueError(f"Key {key} is already 0")

            self.__data[key] -= 1
            self.__save()
        else:
            raise KeyError(f"Key {key} not found")

    @property
    def data(self) -> dict[str, int]:
        return self.__data


def check_header():
    return request.headers.get("Authorization") == "Bearer 123"


app = Flask(__name__)
data_manager = DataManager()


@app.route("/", methods=["GET"])
def get_all():
    # check authorization
    if not check_header():
        return "Unauthorized", 401

    return data_manager.data


@app.route("/<plugin>", methods=["GET"])
def get_plugin(plugin: str):
    # check authorization
    if not check_header():
        return "Unauthorized", 401

    # check exist
    if not data_manager.is_exist(plugin):
        return "Not found", 404

    return {"value": data_manager.get(plugin)}


@app.route("/<plugin>", methods=["POST"])
def post_plugin(plugin: str):
    # check authorization
    if not check_header():
        return "Unauthorized", 401

    # check exist
    if data_manager.is_exist(plugin):
        return "Conflict", 409

    data_manager.set(plugin, 0)
    return "OK"


@app.route("/<plugin>", methods=["PUT"])
def put_plugin(plugin: str):
    # check authorization
    if not check_header():
        return "Unauthorized", 401

    # check exist
    if not data_manager.is_exist(plugin):
        return "Not found", 404

    if request.json["operation"] == "increase":
        data_manager.increase(plugin)
        return "OK"
    elif request.json["operation"] == "decrease":
        try:
            data_manager.decrease(plugin)
            return "OK"
        except ValueError:
            return "Bad request", 400
    else:
        return "Bad request", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0")
