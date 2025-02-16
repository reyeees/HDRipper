from bs4 import BeautifulSoup as BS

_TRANSLATORS = "ul#translators-list > li"
_EPISODES = "div#simple-episodes-tabs > ul"
_EPISODES_IDS = "ul#{} > li".format
_SCHEDULES = "div.b-post__schedule > " \
             "div.b-post__schedule_block > " \
             "div.b-post__schedule_list > " \
             "table.b-post__schedule_table > " \
             "tr > td.td-2 > b"
_SCHEDULES_F = "div.b-post__schedule_block_hidden > " \
                "div.b-post__schedule_block > " \
                "div.b-post__schedule_list > " \
                "table.b-post__schedule_table"
_SCHEDULES_S = "tr > td.td-2 > b"


class Ripped:
    def __init__(self) -> None:
        self.rip_fseason_id: int = None # season id
        self.val_episodes: list = None # episodes
        self.val_titles: list = None # series titles
        # ^- if type is not "series", these values are None
        self.val_translations: list = None # translations

        self.rip_id: str = None # media id
        self.rip_type: str = None # # video.tv_series video.movie
        self.rip_favs: str = None # uuid?

        self.rip_ctanslation: int = None # translation
        self.rip_csubtitles = None # subtitles
        self.rip_cresolution = None # quality


class HDParser(Ripped):
    def __init__(self, id: str) -> None:
        super().__init__()
        self.document: BS = None

        self.rip_id = id # self.url.split('/')[-1].split('-')[0]

    def parse_single_translated(self) -> int:
        if "series" in self.rip_type:
            cdnevent = "sof.tv.initCDNSeriesEvents("
        elif "movie" in self.rip_type:
            cdnevent = "sof.tv.initCDNMoviesEvents("
        
        idx = 0
        for element in self.document.select("script"):
            if cdnevent in element.text:
                data = element.text
                index = data.find(cdnevent) + len(cdnevent)
                idx = data[index:].split(',')[1].strip()
                break

        return idx

    def parse_translators(self) -> list[dict] | int:
        arr = []
        translators = self.document.select(_TRANSLATORS)

        if translators == []:
            return self.parse_single_translated()
        
        for element in translators:
            arr.append({
                "name": element.text,
                "id": element.get("data-translator_id")
            })

        return arr
    
    def parse_episodes(self) -> list[list[str]]:
        arr = []
        seasons = self.document.select(_EPISODES)
        self.rip_fseason_id = int(seasons[0].li["data-season_id"])

        for season in seasons: # _element.get('id')
            season_arr = []
            for episode in season.select(_EPISODES_IDS(season.get("id"))):
                season_arr.append(episode.get("data-episode_id"))
            arr.append(season_arr)
            
        return arr
    
    def parse_titles(self) -> list[str]:
        # schedules = [list(map(lambda x: x.text, self.document.select(_SCHEDULES)[::-1]))]
        schedules = [self.document.select(_SCHEDULES)[::-1]]

        for schedule in self.document.select(_SCHEDULES_F):
            schedules.append(schedule.select(_SCHEDULES_S)[::-1])

        return schedules
    
    def load_document(self, body: str) -> None:
        self.document = BS(body, "html.parser")

        # looking for type in html headlines
        self.rip_type = self.document.find("meta", {"property": "og:type"})["content"]
        # hidden uuid below player
        self.rip_favs = self.document.find("input", id = "ctrl_favs").get("value")
        self.val_translations = self.parse_translators()

        if "series" in self.rip_type:
            self.rip_fseason_id = 1
            self.val_episodes = self.parse_episodes()
            self.val_titles = self.parse_titles()[::-1]
