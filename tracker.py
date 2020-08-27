import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from dateutil import parser
from encoder import DateTimeEncoder

TRACKING_URL = "https://www.indiapost.gov.in/_layouts/15/DOP.Portal.Tracking/TrackConsignment.aspx"
ARTICLE_DETAILS_ID = "ctl00_PlaceHolderMain_ucNewLegacyControl_gvTrckMailArticleDtlsOER"


class Tracker:
    def __init__(self):
        self.POST_DATA = "ctl00%24ScriptManager=ctl00%24PlaceHolderMain%24ucNewLegacyControl%24upnlTrackConsignment%7Cctl00%24PlaceHolderMain%24ucNewLegacyControl%24btnSearch&ctl00%24UCLogin1%24hdnIsMobileSite=false&ctl00%24PlaceHolderMain%24ucNewLegacyControl%24hdnMobileSite=false&ctl00%24PlaceHolderMain%24ucNewLegacyControl%24txtOrignlPgTranNo=RK030174416IN&ctl00%24PlaceHolderMain%24ucNewLegacyControl%24ucCaptcha1%24txtCaptcha=4&__LASTFOCUS=&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=TKeRAvWL0As2I%2Fz6tYfo79zdstLww0Dr3adafHq%2FNh8%2FK%2FDnE9b%2BTD%2Fcr4rCPDc9RgzO061dszqJ6sk%2F7FlRnovX2aijpUg%2FVzqkGA5v7obRe11cKNKihqypyhyFmGgz0sdWRavsn2DFI%2F%2BrMAwl46SUk1bNGQXOrlOtxSUo1lpiYa%2BVphx7qYRtcxfzdqmzh6u2fzXDJzT%2BbrRPChmLIvc3sUyIW8kTsZRmYUOsLKGa4clvIAsuT3npsUfpmhfpg9E1TYJYXAqz9%2FVXqvaUHEZLS7KE545Ub8HnLIoB1mXA%2Ffp0xbJjXApZlRVGdsVFDjmmX3Dxa2%2BoSiN5r97hetFil2P%2FTqXaWqVgDwT4k6cMyVwDvVTxkHZPDPJiDFm5T4usEj%2Bm%2FCLbX%2BKf4JeYgxLnmf3rR9P4ZnOJaypJcPhi5wuSs1yTsv%2F%2F%2FT42FXZdiFMy5q%2BBaZZoQV04YhNmqyvJy5KhJJCdE1MyzwDA%2FIlMkzFNGEd2rGbXxm7%2FrlG%2BZCD6mHi1X2BU3x3Mw1UwBHjz%2FqjBJVMeuGYnS6IzIl7lsA2%2BxBu5nn09nzZO9awJ9xP0gC3mwMPWVAokLAyHCTAoH7XakWsNhyFQ482qUgGl1l11%2B%2FNKCZ3rlBi4CaM9rV29pfqHysCOeAMWU428Lt11ALN%2Fe%2BscllLHQbVTcUR%2BNyhnzZkLJckiLaPSzKVz0IpS%2FQE%2BhR2UxsGxbZild7DXJVCNp44LzxM3uQdF6i1DzquFG2pjYolKb3DHzVLW8B3OyfyzC23oj2EooSI6y%2FMuGvfdky0xjlPPytuNHjt%2BjJZG1ze6CCfRS%2B3qSI8s9sy5y8fuXu%2BBCtRnVbn9n6pG8l8h7o48sG3WqqDNQAOFIRgtezMWFTcBFxort98%2F%2B9qAgtG1lBorMvj1LJmaxUOAfu5aac3w06xP0iCai%2B%2FNxeJrx5k4ftvYQ8JekFDQQXskE5s4n%2BKrzrhFnpBEIg2NgH8UmPqtIU%2FZT5dA0%2FDQaoV6aMuam5i2YSJx2JM5hyiC4BqcQTg3PY7U3ev98hNRv92pX4jTs7si7S8rF%2BGTGVhGpof3QLByAQmc%2BOPlc7M5dO5bdKqHqi%2B3Lkf93joALbzT9Y0YrLudMRCLCWKU9LVfUlGRPFODOYrzwRKCvwTCIYjm2oQ5uImYdcFkTaUDhyq2U40ErqM0so1Cq7nciJaEzRQ7RDRpjFn8wCaKjRBXCXp4kKUZv7fS0rPfOSN0Q1WTZLZRE4mhjSaRJSQL%2BePpZfqb2M%2FDsrnDR9umlGHjRNQuqr8SQBphx78J2jGGbP02S8V0NtEyWtp2DPXEuWFYK7IT5KRM1EMqk6HCbqc1u1FfEYAHchBvrbAUsqoH7wxwHpeiUOkGk%2BRWPHIpBwfd6EYq39A7WTl7b%2FSHTHQHtF7kqEemkNHX0YcGnnwWotR9GTRQ5zynhudt9AzF8HsLxy%2BqCJpl6Gp7%2FN%2Ft%2BV9Bqe%2BwWtu0iaEd3%2FCFzHlR6l0eNCTzSzhxE6NPqdH59J4UEjHSf92vZBP3JFJHSIq3T5h5NiliBWOcUAhCohm8f9R5izMqSRtAkQwQFubZaMrAHhQfO8pi9l1ZghYoNNOHmMlncxuNDzya%2BfijHE08P5LZ0pjd4ffOuNqhSdTNa7HEEediaG794WwuAI4EAADEKKncvtsdvkEUk1HKTVr%2BnU%2Fe%2BTeBLdGYiyk8cYXDREJ63KF1jmbclZeH1wxiNU6s5WNIdOB%2FfXOHbFhnGAiLlx67aAz3RduFSMBB1rm0EsRuLZMUuPAKEH1Xk3JSfegXW6ErzW58gCgAnMvobVKMyMVuoWWL58I2xXzsxKwTl%2FYyhm50KK73QLSW%2BYnxXOXoQcM9zFfzlPb%2FxmZf7wdsuNw3l5aXQWZsjFMZ1w6acE0a01ischeguu9VUuvuQH3dulc94nVz8dDi7iK2tgmVSLPv78%2BvDOug4XyX%2F0pZ%2BIESiS34zxDB0zj1A9RFsMeo%2BukP9NoY5QeCRTlul6fzvcGk98z80oNKunAmrw0quem8F2tG42uH1nOUlRd8QhFIiXw4nvOy7VI1dIlwGfBJhPYAGcb9LmmhMEyyOa3W0QaveZCYcg8X4f%2BwsNYOc7%2BtsF3OnY28wuMRt9UAIQ%3D%3D&__VIEWSTATEGENERATOR=BA91C67B&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=sWLF5bKfqPIHkkFjPWxcRx6nV%2BMbMo%2FBPDPOsOUNTPi9OBrV9ZTJJjnBTVnQCSbeplt9AzBUONNcgAbrY%2FZUgjfa4c%2FbQRAj%2B6FPPbNJS%2BANjbIpnyKS6JwA%2B89%2BGpUxwKsfgFM7s%2BiKgst7EOvVivEQhgBKO2i5JkkjyS1Nkaev%2FI6%2BKiixqPVqcxG7My8ZtYwrrOh9DwQ46yBpoN9BQMd0dpbtEv7WAb%2B20G%2FYaffSTPghJLNbXB2ZH5d1r%2FC0DeUScVRRHbFG6XmwdsRMGg%3D%3D&MSOWebPartPage_PostbackSource=&MSOTlPn_SelectedWpId=&MSOTlPn_View=0&MSOTlPn_ShowSettings=False&MSOGallery_SelectedLibrary=&MSOGallery_FilterString=&MSOTlPn_Button=none&MSOSPWebPartManager_DisplayModeName=Browse&MSOSPWebPartManager_ExitingDesignMode=false&MSOWebPartPage_Shared=&MSOLayout_LayoutChanges=&MSOLayout_InDesignMode=&MSOSPWebPartManager_OldDisplayModeName=Browse&MSOSPWebPartManager_StartWebPartEditingName=false&MSOSPWebPartManager_EndWebPartEditing=false&__REQUESTDIGEST=0xBF89FAC5CB8E9CF0221C587BDFA11FD4E29D51EEFF006E9D5D394D89727FCFCB958FED456C2D3C5602FB98446D5ACCB45FD59DA1B5BE7FA45B65FF3700688BBE%2C27%20Aug%202020%2017%3A42%3A43%20-0000&__ASYNCPOST=true&ctl00%24PlaceHolderMain%24ucNewLegacyControl%24btnSearch=Search"

    def track(self, id):
        details = {}
        self.POST_DATA = self.POST_DATA.replace("RK030174416IN", id)
        headers = {
          "User-Agent": "Mozilla",
          "Referer": "https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx",
          "X-Requested-With": "XMLHttpRequest",
          'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.post(TRACKING_URL, data=self.POST_DATA, headers = headers)
        dom = BeautifulSoup(response.content, "html.parser")

        try:
            general_details = dom.find(id=ARTICLE_DETAILS_ID).findAll('td')
            details = {
                'id': id,
                'origin': general_details[0].text.strip(),
                'booking_date': parser.parse(general_details[1].text.strip()),
                'pincode': general_details[2].text.strip(),
                'tariff': general_details[3].text.strip(),
                'category': general_details[4].text.strip(),
                'destination': general_details[5].text.strip(),
            }
            if len(general_details) > 6:
                details['delivery_date'] = general_details[6].text.strip()
                details['delivered'] = details['delivery_date'] != 'Not Available'

            details['events'] = []

            events = dom.find(class_='responsivetable MailArticleEvntOER').findAll('tr')[1:]
            if events:
                for tr in events:
                    event = {}
                    data = tr.findAll('td')
                    event['date'] = parser.parse(data[0].text.strip() + ' ' + data[1].text.strip() + ' IST')
                    event['office'] = data[2].text.strip()
                    event['description'] = data[3].text.strip()
                    details['events'].append(event)

            return details
        except Exception as e:
            return None
