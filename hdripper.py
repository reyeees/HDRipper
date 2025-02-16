from sys import executable as PYTHON
from os import system
from importlib.util import find_spec

# installing packages if user is 怠け者
missing = []
for package in ("requests", "bs4", "tqdm"):
    if find_spec(package) is None:
        missing.append(package)
if missing != []:
    system(f"\"{PYTHON}\" -m pip install {' '.join(missing)}")
del PYTHON, system, find_spec, missing

# actual code starts here.

from argparse import ArgumentParser
from lib import HDSession, HDParser, HDUtils, TUI, Choose, FDownloader


class HDRip:
    def __init__(self, url: str, num_threads: int = 4, res_mode: str = "best") -> None:
        self.url: str = url.split('#')[0] # cut #t:56-s:1-e:2 for example.
        self.domain: str = self.url.split('/')[2]
        self.id = self.url.split('/')[-1].split('-')[0]

        self.res_mode: str = res_mode if res_mode in ["best", "input"] else "best"
        self.num_threads: int = num_threads

        self.tui = TUI()
        self.term_w = 20 # self.tui.get_terminal_size()[0]

        self.session = HDSession(self.domain)
        self.parser = HDParser(self.id)
        self.utils = HDUtils

    def pick_voicelines(self) -> str:
        translators = self.parser.val_translations
        if type(translators) == int:
            return translators
        
        data = []
        for translate in translators:
            string = f"{translate['name']} | {translate['id']}"
            string = f"{string:<{self.term_w}}"
            data.append(string)

        # using dwm vertical if here's too much objects
        # im too lazy to fix dwm one-row problem 
        idx = self.tui.choose(data, Choose.dwm_vertical)
        return translators[idx]['id']
    
    def pick_subtitles(self, subtitles: list[str]) -> int:
        data = []
        for sub in subtitles:
            data.append(f'{sub.split("]")[0].replace("[", ""):<{self.term_w}}')
        
        return self.tui.choose(data, Choose.dwm_vertical)

    def pick_resolution(self, res: list[str]) -> int:
        data = []
        for quality in res:
            string = f"{quality.split(']')[0].replace('[', ''):<{self.term_w}}"
            data.append(string)

        return self.tui.choose(data, Choose.dwm_vertical)

    def _get_subtitles(self, fname: str, subtitles: list[str]) -> None:
        if self.parser.rip_csubtitles == None:
            self.parser.rip_csubtitles = self.pick_subtitles(subtitles)
        url = subtitles[self.parser.rip_csubtitles].split(']')[1]
        fname = f"{fname}.{url.split('.')[-1]}"

        with open(fname, "wb") as _file:
            _file.write(self.session.get(url).content)
            _file.close()

    def parse_data(self, data: dict[str, str], fname: str, goat: callable) -> None:
        fname = self.utils.clear_fname(fname).replace(" ", "_")

        if data["subtitle"]:
            self._get_subtitles(fname, data["subtitle"].split(","))

        url = self.utils.decode_url(data["url"], goat).split(',')

        if self.res_mode == "best":
            self.parser.rip_cresolution = -1
            url = url[-1].split(" or ")[-1]
        elif self.res_mode == "input":
            if self.parser.rip_cresolution == None:
                self.parser.rip_cresolution = self.pick_resolution(url)
            url = url[self.parser.rip_cresolution].split(" or ")[-1]
        
        print(url)
        fdown = FDownloader(url, f"{fname}.mp4", self.num_threads)
        fdown.download()
        print("Done")

    def _download_stream(self, sid: int, eid: str, fname: str) -> None:
        goat = lambda: self.session.get_stream(
            self.id, self.parser.rip_ctanslation,
            sid, eid, self.parser.rip_favs
        )
        data = goat()
        self.parse_data(data, fname, goat)

    def _download_movie(self, fname: str) -> None:
        goat = lambda: self.session.get_movie(
            self.id, self.parser.rip_ctanslation,
            self.parser.rip_favs
        )
        data = goat()
        self.parse_data(data, fname, goat)

    def download(self) -> None:
        if "series" in self.parser.rip_type:
            episodes = self.parser.val_episodes
            first_season = self.parser.rip_fseason_id

            for season_idx, season in enumerate(episodes, first_season):
                for episode in season:
                    if self.parser.val_titles != [[]]:
                        season_id = season_idx - first_season
                        episode_id = int(episode) - 1
                        title = self.parser.val_titles[season_id][episode_id].text
                        fname = f"{season_idx}_{episode}_{title}"
                    else:
                        fname = f"{season_idx}_{episode}"

                    self._download_stream(season_idx, episode, fname)
                    # sleep(0.5) # testing things
        elif "movie" in self.parser.rip_type:
            # self.doc.find("meta", {"property": "og:title"})["content"]
            fname = "_".join(self.url.split("/")[-1].split("-")[1:-1])
            self._download_movie(fname)
        else:
            exit(f"[Unknown type] {self.parser.rip_type} - {self.url}")

    def test(self) -> None:
        body = self.session.get(self.url).text
        self.parser.load_document(body)
        self.parser.rip_ctanslation = self.pick_voicelines()
        self.download()


if __name__ == "__main__":
    parser = ArgumentParser(description = 'HDRezka downloader tool by ReYeS')
    parser.add_argument("url", help = "Input link.", type = str, default = "")
    parser.add_argument("--mode", "-m", help = "Quality choose mode. (best/input)", dest = "mode", type = str, default = "input") # best
    parser.add_argument("--threads", "-t", help = "Maximum threads number been used in downloading.", dest = "threads", type = int, default = 8)
    args = parser.parse_args()
    del parser

    HDRip(args.url, args.threads, args.mode).test()
