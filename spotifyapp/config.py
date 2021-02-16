import json
import os

if not os.path.isfile('config.json'):
    print("You have to create a config.json")
    quit()

config = json.loads(open('config.json').read())
