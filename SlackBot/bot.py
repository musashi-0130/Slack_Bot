import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import datetime


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def get_weekday():
    # 日本時間での現在の日付データ取得
    # 念のためUTCの時間を取得してから時差分を足してる
    jstTime = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    day = jstTime.day

    # 曜日を漢字で取得したかった
    # .weekday()ではint型の数が取得でき、0が月曜日で6が日曜日なのでリストと組み合わせた
    wd = ["月", "火", "水", "木", "金", "土", "日"]
    week = wd[jstTime.weekday()]

    # 1週間前の日付が同月かどうか調べる -> 1日より前か後かで判別
    # dayが1日以降(同月)なら出現回数+1してdayに1週間前の日付を代入(-7する)、1日より前(前の月の日付)なら処理終了
    weeks = 0
    while day > 0:
        weeks += 1
        day -= 7

    #text = '今日は第' + str(weeks) + weekday + '曜日です。'
    # 例：今日は第2月曜日です。
    weekday = week
    return weekday


def todo_l(weekday):
    work = []
    if weekday == "月":
        work.append("明日は資源ゴミの日です")
    elif weekday == "火":
        work.append("明日は可燃ゴミの日です")
    elif weekday == "木":
        if str(weeks) == 1 or str(weeks) == 3:
            work.append("明日はペットボトルの日です")
        else:
            work.append("明日は不燃ゴミの日です")
    elif weekday == "金":
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
        client.chat_postMessage(channel='#test', text=td)


if __name__ == "__main__":
    main()
