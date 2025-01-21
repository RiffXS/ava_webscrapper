import json


def main():
    with open('activities.json', 'r') as file:
        activities = json.load(file)

        for key, value in activities.items():
            print('a')


if (__name__ == '__main__'):
    main()
