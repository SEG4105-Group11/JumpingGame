import utils
import os
import json


def get_highscores():
    save_dir = utils.get_save_dir()
    savefile = os.path.join(save_dir, "highscores.json")

    if not os.path.exists(savefile):
        return {}

    with open(savefile, "r") as f:
        return json.load(f)
