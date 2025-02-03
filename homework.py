import json


def print_date(date):
    print(
        f'{date["day"]} {date["month"]} {date["year"]}, {date["hour"]}:{date["min"]}')


def main():
    with open('homeworks.json', 'r') as file:
        homeworks = json.load(file)

        for key, events in homeworks.items():
            print(key + ':')

            for event in events:
                print('  ' + event['title'])
                print('    de  ', end='')
                print_date(event['date'][0])

                print('    até ', end='')
                print_date(event['date'][1])

                print('  em ' + event['link'] + '\n')
                # print(' ', event['g_date'])


if (__name__ == '__main__'):
    main()
