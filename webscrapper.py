import os
import json
import requests

from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv


load_dotenv()


def get_credentials():
    ava_user = os.getenv('AVA_USER', '.env not created')
    ava_pass = os.getenv('AVA_PASS', '.env not created')

    return ava_user, ava_pass


def get_preliminary_activities(soup):
    activities = {}

    things = soup.find_all(
        'div', class_='d-none d-md-block hidden-phone text-xs-center')

    for thing in things:
        day = thing.span.contents[0].split(' ')
        if (day[0] != 'Sem'):
            events = thing.div.ul.find_all('li')
            for event in events:
                event_type = event['data-event-eventtype']

                if (event_type != 'close'):
                    try:
                        if len(activities[f'{day[3]} {day[4]}']) > 0:
                            activities[f'{day[3]} {day[4]}'] = activities[f'{day[3]} {day[4]}']

                    except KeyError:
                        activities[f'{day[3]} {day[4]}'] = []

                    if (event_type == 'due'):
                        string = ' '
                        title = event.a['title'].split()[:-5]
                        title = string.join(title)
                    else:
                        title = event.a['title']

                    activities[f'{day[3]} {day[4]}'].append({
                        'link': event.a['href'],
                        'type': event['data-event-eventtype'],
                        'title': title
                    })

    return activities


def get_full_homeworks(activities, s):
    homeworks = {}

    for key, values in activities.items():
        for value in values:
            re = s.get(value['link'])
            soup = bs(re.content, 'html.parser')

            if (value['type'] != 'due'):
                content = soup.find('div', class_='box py-3 quizinfo')

                paragraphs = content.p.find_next_siblings()

                start = paragraphs[0].contents[0].split(' ')[-4:]
                end = paragraphs[1].contents[0].split(' ')[-4:]

                start_date = {
                    'day': int(start[0]),
                    'month': start[1],
                    'year': int(start[2][:-1]),
                    'hour': int(start[-1][:2]),
                    'min': int(start[-1][-2:]),
                }

                end_date = {
                    'day': int(end[0]),
                    'month': end[1],
                    'year': int(end[2][:-1]),
                    'hour': int(end[-1][:2]),
                    'min': int(end[-1][-2:]),
                }

                # print(value)
                print(start_date, end_date)

            else:
                print(value['title'])


def main():
    ava_user, ava_pass = get_credentials()

    login_url = 'https://ava3.cefor.ifes.edu.br/login/index.php'
    calendar_url = 'https://ava3.cefor.ifes.edu.br/calendar/view.php?view=month'

    try:
        with requests.session() as s:
            req = s.get(login_url).text

            html = bs(req, 'html.parser')
            token = html.find('input', {'name': 'logintoken'}).attrs['value']

            payload = {
                'logintoken': token,
                'username': ava_user,
                'password': ava_pass,
            }

            s.post(login_url, data=payload)

            r = s.get(calendar_url)
            soup = bs(r.content, 'html.parser')

            activities = get_preliminary_activities(soup)

            homework = get_full_homeworks(activities, s)

            with open('activities.json', 'w') as file:
                json.dump(activities, file)

    except requests.exceptions.ConnectionError:
        print('Site inalcançável')
        exit(0)


if (__name__ == '__main__'):
    main()
