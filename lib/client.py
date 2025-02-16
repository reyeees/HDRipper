from time import time
from requests import Session, Response


class HDSession:
    def __init__(self, domain: str) -> None:
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0'
        }
        self.domain: str = domain

        self.session: Session = Session()
        self.session.headers.update(self.headers)

    def get(self, url: str) -> Response:
        return self.session.get(url)
    
    def get_stream(self, id: str, tid: str, sid: int, eid: str, favs: str) -> dict:
        data = self.session.post(
            f"https://{self.domain}/ajax/get_cdn_series/?t={time() * 1000}",
            data = {
                "id": id,
                "translator_id": tid,
                "season": sid,
                "episode": eid,
                "favs": favs,
                "action": "get_stream"
            }
        )
        return data.json()

    def get_movie(self, id: str, tid: str, favs: str) -> dict:
        data = self.session.post(
            f"https://{self.domain}/ajax/get_cdn_series/?t={time() * 1000}",
            data = {
                "id": id,
                "translator_id": tid,
                "favs": favs,
                "action": "get_movie"
            }
        )
        return data.json()
