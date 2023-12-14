import contextlib
from .imports import *
from . import _utils


def modul(self, absid):
    url = f"https://www.lectio.dk/lectio/{self.skoleId}/aktivitet/aktivitetforside2.aspx?absid={absid}"
    resp = self.session.get(url)
    if resp.url != url:
        raise Exception("lectio-cookie udløbet")
    soup = BeautifulSoup(resp.text, "html.parser")

    modulDetaljer = {
        "aktivitet": None,
        "note": "",
        "lektier": "",
        "præsentation": "",
        "grupper": {},
        "øvrigtIndhold": "",
    }

    with contextlib.suppress(Exception):
        modulDetaljer["note"] = soup.find(
            "textarea", {"class": "activity-note"}
        ).text.lstrip()
    modulContent = soup.find(
        "div", {"id": "s_m_Content_Content_tocAndToolbar_inlineHomeworkDiv"}
    )
    last = ""
    for div in modulContent.find_all("div"):
        if div.get("id") == None:
            if (
                divText := div.text.lstrip().rstrip()
            ) != "" and divText != "Vis fuld skærm":
                last = divText.lower().title().replace(" ", "")
                last = last[0].lower() + last[1:]
        else:
            article = div.find("article")
            if article.find("h1").text == "Groups":
                groupNames = list(map(lambda x: x.text, article.find_all("p")))
                groupParticipants = article.find_all("ul")
                for i, group in enumerate(groupNames):
                    modulDetaljer["grupper"][group] = list(
                        map(lambda x: x.text, groupParticipants[i].find_all("li"))
                    )
            else:
                for child in article.find_all(recursive=False):
                    modulDetaljer[last] += markdownify.markdownify(
                        str(child), bullets="-"
                    )

    modulDetaljer["aktivitet"] = _utils.skemaBrikExtract(
        soup.find("a", class_="s2skemabrik")
    )

    return modulDetaljer


def elevFeedback():
    pass
