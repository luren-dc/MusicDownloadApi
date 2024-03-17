#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import asyncio
import json
from random import choice

import aiohttp

from .utils import get_formated_data, parse_tx_song_info, random_searchID, random_string


class API:
    TXMUSIC_URL: str = "https://u.y.qq.com/cgi-bin/musicu.fcg"

    @staticmethod
    async def search_tx(keyword: str, num: int = 10, page: int = 0) -> list[dict]:
        """
        搜索歌曲

        Args:
            keyword: 关键词
            num: 单页数量
            page: 页码

        Returns:
            dict: 歌曲数据
        """

        async with aiohttp.ClientSession() as session:
            async with session.post(
                API.TXMUSIC_URL,
                data=get_formated_data(
                    {
                        "comm": {"ct": "19", "cv": "1859", "v": "1859"},
                        "request": {
                            "module": "music.search.SearchCgiService",
                            "method": "DoSearchForQQMusicDesktop",
                            "param": {
                                "search_id": random_searchID(),
                                "query": keyword,
                                "search_type": 0,
                                "num_per_page": num,
                                "page_num": page,
                                "page_id": page,
                                "grp": 1,
                            },
                        },
                    }
                ).encode("utf-8"),
                timeout=10,
            ) as resp:
                res = json.loads(await resp.text())
                song_data = res["request"]["data"]["body"]["song"]["list"]
                return [parse_tx_song_info(info) for info in song_data]

    @staticmethod
    async def get_tx_download(mid: list[str]) -> dict:
        """
        获取歌曲链接

        Args:
            mid: 歌曲mid

        Returns:
            dict: 对应mid的歌曲链接
        """
        mid_list = [mid[i : i + 100] for i in range(0, len(mid), 100)]
        urls = {}
        for mids in mid_list:
            # 构造请求参数
            param = {
                "filename": [f"M500{mid}{mid}.mp3" for mid in mids],
                "guid": random_string(32, "abcdef1234567890"),
                "songmid": mids,
                "songtype": [1 for i in range(len(mids))],
            }

            url = choice(
                [
                    "https://isure.stream.qqmusic.qq.com/",
                    "https://ws.stream.qqmusic.qq.com/",
                    # "https://dl.stream.qqmusic.qq.com/",
                ]
            )
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    API.TXMUSIC_URL,
                    data=get_formated_data(
                        {
                            "comm": {
                                "ct": "11",
                                "cv": "12060012",
                                "v": "12060012",
                                "QIMEI36": "0152e7226a03067b8904f60810001901730c",
                            },
                            "request": {
                                "module": "music.vkey.GetVkey",
                                "method": "UrlGetVkey",
                                "param": param,
                            },
                        }
                    ).encode("utf-8"),
                    timeout=10,
                ) as resp:
                    res = json.loads(await resp.text())
                    data = res["request"]["data"]["midurlinfo"]
                    urls.update(
                        {
                            info["songmid"]: (
                                url + info["wifiurl"] if info["wifiurl"] else ""
                            )
                            for info in data
                        }
                    )
        return urls
