#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import random
import re
import time


def get_formated_data(data: dict) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def random_string(length: int, chars: str) -> str:
    return "".join(random.choices(chars, k=length))


def random_searchID() -> str:
    e = random.randint(1, 20)
    t = e * 18014398509481984
    n = random.randint(0, 4194304) * 4294967296
    a = time.time()
    r = round(a * 1000) % (24 * 60 * 60 * 1000)
    return str(t + n + r)


def generate_random_user_agent():
    platforms = (
        "Windows NT 10.0; Win64; x64",
        "Windows NT 10.0; WOW64; x64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "X11; Linux x86_64",
        "X11; Linux i686",
    )

    browsers = ("Chrome", "Firefox", "Opera", "Edge")

    versions = (
        "90.0.4430.212",
        "90.0.4430.24",
        "90.0.4430.70",
        "90.0.4430.72",
        "90.0.4430.85",
        "90.0.4430.93",
        "91.0.4472.101",
        "91.0.4472.106",
        "91.0.4472.114",
        "91.0.4472.124",
        "91.0.4472.164",
        "91.0.4472.19",
        "91.0.4472.77",
        "92.0.4515.107",
        "92.0.4515.115",
        "92.0.4515.131",
        "92.0.4515.159",
        "92.0.4515.43",
        "93.0.4556.0",
        "93.0.4577.15",
        "93.0.4577.63",
        "93.0.4577.82",
        "94.0.4606.41",
        "94.0.4606.54",
        "94.0.4606.61",
        "94.0.4606.71",
        "94.0.4606.81",
        "94.0.4606.85",
        "95.0.4638.17",
        "95.0.4638.50",
        "95.0.4638.54",
        "95.0.4638.69",
        "95.0.4638.74",
        "96.0.4664.18",
        "96.0.4664.45",
        "96.0.4664.55",
        "96.0.4664.93",
        "97.0.4692.20",
    )

    return f"{random.choice(browsers)}/{random.choice(versions)} ({random.choice(platforms)})"


def parse_tx_song_info(song_info: dict) -> dict:
    # 解析歌曲信息
    info = {
        "id": song_info["id"],
        "mid": song_info["mid"],
        "name": song_info["name"],
        "title": song_info["title"],
        "subTitle": song_info.get("subtitle", ""),
        "language": song_info["language"],
        "timePublic": song_info.get("time_public", ""),
        "tag": song_info.get("tag", ""),
        "type": song_info["type"],
    }

    # 解析专辑信息
    album = {
        "id": song_info["album"]["id"],
        "mid": song_info["album"]["mid"],
        "name": song_info["album"]["name"],
        "timePublic": song_info["album"].get("time_public", ""),
    }

    # 解析MV信息
    mv = {
        "id": song_info["mv"]["id"],
        "name": song_info["mv"].get("name", ""),
        "vid": song_info["mv"]["vid"],
    }

    # 解析歌手信息
    singer = [
        {
            "id": s["id"],
            "mid": s["mid"],
            "name": s["name"],
            "type": s.get("type"),
            "uin": s.get("uin"),
        }
        for s in song_info["singer"]
    ]

    # 解析文件信息
    file = {
        "mediaMid": song_info["file"]["media_mid"],
        "AI00": song_info["file"]["size_new"][0],
        "Q000": song_info["file"]["size_new"][1],
        "Q001": song_info["file"]["size_new"][2],
        "F000": song_info["file"]["size_flac"],
        "O600": song_info["file"]["size_192ogg"],
        "O400": song_info["file"]["size_96ogg"],
        "M800": song_info["file"]["size_320mp3"],
        "M500": song_info["file"]["size_128mp3"],
        "C600": song_info["file"]["size_192aac"],
        "C400": song_info["file"]["size_96aac"],
        "C200": song_info["file"]["size_48aac"],
    }

    # 组装结果
    result = {
        "info": info,
        "album": album,
        "mv": mv,
        "singer": singer,
        "file": file,
        "lyric": {
            "match": song_info.get("lyric", ""),
            "content": song_info.get("content", ""),
        },
        "pay": song_info.get("pay", {}),
        "grp": [parse_tx_song_info(song) for song in song_info.get("grp", [])],
        "vs": song_info.get("vs", []),
    }

    return result
