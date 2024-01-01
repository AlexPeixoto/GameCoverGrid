from igdb.wrapper import IGDBWrapper
import json
import requests
import os
import subprocess
import math

# Retrieve access token 
credentials = open('credentials.txt', "r")
client_id = credentials.readline().rstrip()
client_secret = credentials.readline().rstrip()

# Create empty platforms map
platforms = {}
skipped_games = [] 

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)
keys = r.json();
wrapper = IGDBWrapper(client_id, keys['access_token'])

# Load platform list
# Seems that currently we have 200 entries, so 500 should be a reasonable value for now
platform_byte_array = wrapper.api_request(
    'platforms',
    'fields name; limit 500;' 
    )
platform_data = json.loads(platform_byte_array.decode('utf8'))

# Store all platforms on a dictionary instead of running this query once per game.
for entry in platform_data:
    platforms[entry["id"]] = entry["name"]

# Start creating montage commands
montage_cmd = ['montage']

# Open file with games
file = open('list.txt', 'r')

# Delete previous corrected list and create a new one
if os.path.exists('correctedlist.txt'):
    os.remove('correctedlist.txt')
file_corrected = open('correctedlist.txt', 'w')

line_idx = 0
while True:
    game_name = file.readline().rstrip()
    # This code is quite dumb it will assume that
    # if a image with corresponding line index exists it can
    # be skipped

    if os.path.exists('images/{}.jpg'.format(line_idx)):
        print("Skipping {} as its the {} item on the list and this item already has a correspondig image, if needed, delete it from the images folder".format(game_name, line_idx))
        montage_cmd.extend(['images/{}.jpg'.format(line_idx)]);
        line_idx+=1
        continue

    if not game_name:
        break

    print("Processing: {}".format(game_name))
    # Get cover id from JSON API request
    # Category is 0 for main game so we use asc to make dlcs go down
    search = 'fields name, platforms, cover; offset 0; sort release_dates.date desc; limit 40; sort category asc; where name ~ "{}"*;'.format(game_name)
    byte_array = wrapper.api_request(
            'games',
            search
          )
    data = json.loads(byte_array.decode('utf8'))

    # select game entry
    selected_entry = 0 
    if len(data) == 0:
        print ("No Entry found for {}".format(game_name))
        skipped_games.extend([game_name])
        line_idx+=1;
        continue
    elif len(data) > 1:
        idx = 1
        for entry in data:
            # Do we have platform information to fill?
            platform_str = ""
            if 'platforms' in entry:
                for p in entry['platforms']:
                    platform_str += platforms[p] + ", "

            # Print game name
            if len(platform_str):
                print("{}. {} ({})".format(idx, entry['name'], platform_str[:-2]))
            else:
                print("{}. {}".format(idx, entry['name']))
            idx+=1
        print()
        print("0. Continue/Skip entry")

        
        selected_entry = 99 
        while selected_entry < 0 or selected_entry > len(data):
            print()
            print("Please select a valid entry as multiple where found when looking for (Pressing just return selects first option): ".format(game_name))
            value=input()
            if value == '':
                selected_entry = 1
            else:
                selected_entry=int(value)
        
        if selected_entry == 0:
            skipped_games.extend([game_name])
            line_idx+=1
            continue
        
    data = data[selected_entry-1]
    file_corrected.write(data['name'] + '\n')

    if 'cover' not in data.keys():
        print("{} not found".format(data))
        line_idx+=1
        continue

    byte_array = wrapper.api_request(
                'covers',
                'fields url; where id = ' + str(data['cover']) + ';'
    )

    data = json.loads(byte_array.decode('utf8'))
    data = data[0]

    # assumes jpg image format
    path = "images/{}.jpg".format(line_idx) 
    url = "http:{}".format(data['url'].replace("_thumb", "_cover_big"))
    r = requests.get(url, stream=True)
    if r.ok:
        print("Image being stored on", os.path.abspath(path))
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())

    montage_cmd.extend([path]);
    line_idx+=1

#close files
file.close()
file_corrected.close()

if len(skipped_games) > 0:
    print()
    print("The following games were not found or skipped:")
    for game in skipped_games:
        print(game)

# Generate image
print("Generating final image!")
grid_size = int(math.sqrt(line_idx));
montage_cmd.extend(['-tile', "{}x{}".format(grid_size, grid_size + 1), '-background', 'none', '-geometry', '+0+0', 'jpg:./result.jpg'])
subprocess.Popen(montage_cmd)
