import os
import json
import requests

from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv


load_dotenv()


def get_credentials():
    ava_user = os.getenv('AVA_USER', '')
    ava_pass = os.getenv('AVA_PASS', '')

    return ava_user, ava_pass


def get_preliminary_activities(soup):
    links = []

    activities = {}

    things = soup.find_all(attrs={'data-type': 'event'})

    for thing in things:
        a = thing.find_all('a')
        course = a[-2].contents[0]

        try:
            if len(activities[course]) > 0:
                activities[course] = activities[course]

        except KeyError:
            activities[course] = []

        title = thing['data-event-title']
        link = a[-1]['href']

        event_type = thing['data-event-eventtype']
        if event_type == 'due':
            link = link[:link.find('&')]

            title = title.split(' ')[:-5]
            title = ' '.join(title)

        activities[course].append((title, link, event_type))

    return activities


def get_month_num(month):
    if month == 'jan':
        return '01'
    elif month == 'fev':
        return '02'
    elif month == 'mar':
        return '03'
    elif month == 'abr':
        return '04'
    elif month == 'mai':
        return '05'
    elif month == 'jun':
        return '06'
    elif month == 'jul':
        return '07'
    elif month == 'ago':
        return '08'
    elif month == 'set':
        return '09'
    elif month == 'out':
        return '10'
    elif month == 'nov':
        return '11'
    elif month == 'dez':
        return '12'
    else:
        return 'error'


def get_full_homeworks(activities, s):
    for key, values in activities.items():
        for i in range(len(values)):
            title, link, event_type = values[i]

            re = s.get(link)
            soup = bs(re.content, 'html.parser')

            if (event_type != 'due'):
                content = soup.find('div', class_='box py-3 quizinfo')

                paragraphs = content.p.find_next_siblings()

                start = paragraphs[0].contents[0].split(' ')[-4:]
                end = paragraphs[1].contents[0].split(' ')[-4:]

                start_month = get_month_num(start[1])
                end_month = get_month_num(end[1])

                if start_month == 'error' or end_month == 'error':
                    exit(0)

                start_date = (
                    int(start[2][:-1]),
                    start_month,
                    int(start[0]),
                    int(start[-1][:2]),
                    int(start[-1][-2:]),
                )

                end_date = (
                    int(end[2][:-1]),
                    end_month,
                    int(end[0]),
                    int(end[-1][:2]),
                    int(end[-1][-2:]),
                )

                # g_start_date = f'{start[2][:-1]}-{start_month}-{start[0]}T{start[-1][:2]}:{start[-1][-2:]}:00-03:00'
                # g_end_date = f'{end[2][:-1]}-{end_month}-{end[0]}T{end[-1][:2]}:{end[-1][-2:]}:00-03:00'

                activities[key][i] = (
                    title,
                    link,
                    event_type,
                    # (g_start_date, g_end_date),
                    (start_date, end_date)
                )

            else:
                content = soup.find_all('td')

                date = content[-4].contents[0].split(' ')[1:]

                start_day = int(date[0])
                start_hour = int(date[-1][:2])

                if start_hour == 0:
                    start_day -= 1
                    start_hour = '23'
                else:
                    start_hour -= 1
                    if start_hour < 11:
                        start_hour = f'0{start_hour}'
                    else:
                        start_hour = f'{start_hour}'

                date_month = get_month_num(date[1])

                if date_month == 'error':
                    exit(0)

                start_date = (
                    int(date[2][:-1]),
                    date_month,
                    start_day,
                    int(start_hour),
                    int(date[-1][-2:]),
                )

                end_date = (
                    int(date[2][:-1]),
                    date_month,
                    int(date[0]),
                    int(date[-1][:2]),
                    int(date[-1][-2:]),
                )

                # g_start_date = f'{date[2][:-1]}-{date_month}-{date[0]}T{end_hour}:{date[-1][-2:]}:00-03:00'
                # g_end_date = f'{date[2][:-1]}-{date_month}-{date[0]}T{date[-1][:2]}:{date[-1][-2:]}:00-03:00'

                activities[key][i] = (
                    title,
                    link,
                    event_type,
                    # (g_start_date, g_end_date),
                    (start_date, end_date),
                )


def main():
    ava_user, ava_pass = get_credentials()

    login_url = 'https://ava3.cefor.ifes.edu.br/login/index.php'
    calendar_url = 'https://ava3.cefor.ifes.edu.br/calendar/view.php?view=upcoming'

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

            get_full_homeworks(activities, s)

            with open('homeworks.json', 'w') as file:
                json.dump(activities, file)

    except requests.exceptions.ConnectionError as err:
        print(f'An error has occurred: {err}')
        exit(0)


if (__name__ == '__main__'):
    main()
