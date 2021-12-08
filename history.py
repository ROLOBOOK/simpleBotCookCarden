import json
import datetime
import os


def save_history(cookrequest):
    if os.path.isfile('history.json'):
        with open('history.json') as f:
            data = json.load(f)
    else:
        data = {}
    today = datetime.datetime.today().strftime('%Y.%m.%d')
    if not data.get(today):
        data[today] = []
    data[today].append((cookrequest.count_people, cookrequest.dish, cookrequest.chat_id))
    with open('history.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    pass
