import json


def print_date(date):
    day = f'0{date[2]}' if date[2] > 0 and date[2] <= 9 else date[2]
    hour = f'0{date[3]}' if date[3] >= 0 and date[3] <= 9 else date[3]
    min = f'0{date[4]}' if date[4] >= 0 and date[4] <= 9 else date[4]

    print(
        f'{day} {date[1]} {date[0]}, {hour}:{min}')


def main():
    with open('homeworks.json', 'r') as file:
        homeworks = json.load(file)

        for key, events in homeworks.items():
            print(key + ':')

            for title, link, _, date, _ in events:
                print('  ' + title)
                print('    de  ', end='')
                print_date(date[0])

                print('    até ', end='')
                print_date(date[1])

                print('  em ' + link + '\n')
                # print(' ', event['g_date'])

            print()


if (__name__ == '__main__'):
    main()
