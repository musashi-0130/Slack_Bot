# -*- coding: utf-8 -*-

import slack
import os
from dotenv import load_dotenv
import datetime


env_path = '/Users/musashi/Desktop/Slack/Slack_Bot/SlackBot/.env'
load_dotenv(dotenv_path=env_path)


def get_weekday():
    # 日本時間での現在の日付データ取得
    # 念のためUTCの時間を取得してから時差分を足してる
    jstTime = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    day = jstTime.day

    #　0:月曜日 1:火曜日 2:水曜日 3:木曜日 4:金曜日 5:土曜日 6:日曜日
    week = jstTime.weekday()

    # 1週間前の日付が同月かどうか調べる -> 1日より前か後かで判別
    # dayが1日以降(同月)なら出現回数+1してdayに1週間前の日付を代入(-7する)、1日より前(前の月の日付)なら処理終了
    weeks = 0
    while day > 0:
        weeks += 1
        day -= 7

    weekday = week
    return weekday


def todo_l(weekday):
    work = []
    if weekday == 0:
        work.append("明日は資源ゴミの日です")
    elif weekday == 1:
        work.append("明日は可燃ゴミの日です")
    elif weekday == 3:
        if weeks == 1 or weeks == 3:
            work.append("明日はペットボトルの日です")
        else:
            work.append("明日は不燃ゴミの日です")
    elif weekday == 4:
        work.append("明日は可燃ゴミの日です")
    else:
        work.append("明日はゴミの日ではありません")

    todo = work
    return todo


def main():
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

    weekday = get_weekday()

    todo = todo_l(weekday)

    for td in todo:
        client.chat_postMessage(channel='#notification', text=td)


if __name__ == "__main__":
    main()
