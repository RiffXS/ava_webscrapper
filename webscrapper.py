import os
import json
import requests

from bs4 import BeautifulSoup as bs

def main():
  activities = {}

  ava_user = os.getenv('AVA_USER', '.env not created')
  ava_pass = os.getenv('AVA_PASS', '.env not created')

  login_url = 'https://ava3.cefor.ifes.edu.br/login/index.php'
  calendar_url = 'https://ava3.cefor.ifes.edu.br/calendar/view.php?view=month'

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
    things = soup.find_all('div', class_='d-none d-md-block hidden-phone text-xs-center')

    for thing in things:
      day = thing.span.contents[0].split(' ')
      if (day[0] != 'Sem'):
        events = thing.div.ul.find_all('li')
        for event in events:
          event_type = event['data-event-eventtype']

          if (event_type != 'close'):
            try:
              activities[f'{day[3]} {day[4]}'] = [] if len(activities[f'{day[3]} {day[4]}']) > 0 else activities[f'{day[3]} {day[4]}']
            except:
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

    print(activities)
    for key, values in activities.items():
      for value in values:
        re = s.get(value['link'])
        soup = bs(re.content, 'html.parser')

        if (value['type'] != 'due'):
          content = soup.find('div', class_='box py-3 quizinfo')

          paragraphs = content.p.find_next_siblings()
          start = paragraphs[0].contents[0].split(' ')[-4:]
          end = paragraphs[1].contents[0].split(' ')[-4:]

          end_min = int(end[-1][-2:])
          end_hour = int(end[-1][:2])
          start_min = int(start[-1][-2:])
          start_hour = int(start[-1][:2])
          
          
          
          print(f'{start_hour}:{start_min} {end_hour}:{end_min}')

        else:
          print(value['title'])

    with open('activities.json', 'w') as file:
      json.dump(activities, file)

if (__name__ == '__main__'):
  main()
