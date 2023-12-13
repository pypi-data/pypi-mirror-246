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
            if div.find("article").find("h1").text == "Groups":
                article = div.find("article")
                groupNames = list(map(lambda x: x.text, article.find_all("p")))
                groupParticipants = article.find_all("ul")
                for i, group in enumerate(groupNames):
                    modulDetaljer["grupper"][group] = list(map(lambda x: x.text, groupParticipants[i].find_all("li")))
            else:
                for element in (
                    str(div)
                    .replace("\xa0", "\n")
                    .replace("<br/>", "\n")
                    .replace("</a>", "</a>\n")
                    .split("\n")
                ):
                    elementSoup = BeautifulSoup(element, "html.parser")
                    if elementSoup.text != "":
                        if (
                            elementWithHref := elementSoup.find("a", href=True)
                        ) is not None:
                            href = elementWithHref.get("href")
                            if href.startswith(f"/lectio/{self.skoleId}"):
                                href = "https://www.lectio.dk" + href
                            modulDetaljer[last] += unicodedata.normalize(
                                "NFKD", f"[{elementSoup.text.rstrip().lstrip()}]({href})\n"
                            )
                        else:
                            modulDetaljer[last] += unicodedata.normalize(
                                "NFKD",
                                elementSoup.text.rstrip().lstrip().replace("\xa0", " ")
                                + "\n",
                            )

    modulDetaljer["aktivitet"] = _utils.skemaBrikExtract(
        soup.find("a", class_="s2skemabrik")
    )

    return modulDetaljer


def elevFeedback():
    pass
