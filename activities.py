import json

def main():
  with open('activities.json', 'r') as file:
    activities = json.load(file)

    print(activities)

if (__name__ == '__main__'):
  main()
