import requests
import time
import os
import re
import xmodits


# in samples path, we include both wav and mod files
sample_dir = "samples/"


class MOD:
    def __init__(
        self,
        mod_id,
        downloads,
        favourited,
        md5,
        format,
        channels,
        uncompressed_size,
        genre,
    ):
        self.mod_id = mod_id
        self.downloads = downloads
        self.favourited = favourited
        self.md5 = md5
        self.format = format
        self.channels = channels
        self.uncompressed_size = uncompressed_size
        self.genre = genre

    def __str__(self):
        return f"MOD ID: {self.mod_id}\nDownloads: {self.downloads}\nFavourited: {self.favourited}\nMD5: {self.md5}\nFormat: {self.format}\nChannels: {self.channels}\nUncompressed Size: {self.uncompressed_size}\nGenre: {self.genre}"


def get_ptext():
    url = "https://modarchive.org/index.php?request=view_random"
    response = requests.get(url)
    return response.text


def extract_MOD(ptext: str) -> MOD:
    mod_id = re.search(r"Mod Archive ID: (\d+)", ptext).group(1)
    downloads = re.search(r"Downloads: (\d+)", ptext).group(1)
    favourited = re.search(r"Favourited: (\d+) times", ptext).group(1)
    md5 = re.search(r"MD5: ([a-f0-9]+)", ptext).group(1)
    format = re.search(r"Format: ([A-Z]+)", ptext).group(1)
    channels = re.search(r"Channels: (\d+)", ptext).group(1)
    uncompressed_size = re.search(r"Uncompressed Size: ([\d.]+[A-Z]+)", ptext).group(1)
    genre = re.search(r"Genre: ([a-zA-Z/]+)", ptext).group(1)

    return MOD(
        mod_id, downloads, favourited, md5, format, channels, uncompressed_size, genre
    )


def get_file(mod_id: str, save_filepath: str):
    url = f"https://api.modarchive.org/downloads.php?moduleid={mod_id}"
    response = requests.get(url, allow_redirects=True)
    with open(save_filepath, "wb") as f:
        f.write(response.content)


def get_random_mod():
    return extract_MOD(get_ptext())


def rip_random_mod_samples():
    mod = get_random_mod()
    # gen folder at samples/mod_id
    folder = sample_dir + mod.mod_id + "/"
    os.makedirs(folder, exist_ok=True)
    # download mod file
    mod_fp = folder + f"{mod.mod_id}.{mod.format.lower()}"
    get_file(mod.mod_id, mod_fp)
    # rip
    xmodits.dump(mod_fp, folder)
    return mod


while True:
    try:
        mod = rip_random_mod_samples()
        print(mod)
        print("*" * 100)
    except Exception as e:
        print(e)
        time.sleep(10)
