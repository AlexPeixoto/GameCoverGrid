# What is this?
This is a simple python script that relies on IGDB to create a single image with the covers of all games from a list?

## Why do I need this?
Basically, you don't :), but its a nice thing to have for top x games or maybe finished games of 2023?

## What do I need to run this?

You need to have python running on your machine, imagemagik and have IGDBWrapper installed (can be done via pip3 with: `pip3 install igdb-api-v4`)

You also need the credentials that can be generated using this tutorial (remember to have client_type as confidential): https://api-docs.igdb.com/#account-creation

### How do I run this now?

Once you have the main.py file downloaded, the account created and igdb pip package installed you need to:

1. Create a text file called credentials on the same folder with the `client_id` on the first line and `client_secret` on the 2nd.
2. Create a new folder called images, you can leave it empty. The covers will be downloaded there.
3. Create a list.txt file and have the name of each game on each line of the file. Those will be downloaded and put on the final image in order

Now just run with `python3 main.py`.

### What now that it was executed?

There should be a result.jpg file on the place from which you ran the script or on the place where the main.py is located.

### I had to select a bunch of proper game names, can I save those for later?

Yes, once you finish the execution there should be a `correctedlist.txt`

### My game cannot be found or does not appear on the list, why?

- Your game name is incorrect, the filtering is not very great with things like 2 VS II, so you might need to adjust it.
- The game is just not there.

Good thing is that it will skip any file that it thinks that was already downloaded.

### Script states that it already downloaded something that it did not.

The script uses the image name and game position on the file, so if the game on the line 30 has a 30.jpg on the images file it will skip it, so you should either avoid adding games in the middle of the text or delete images from that position down to the bottom.

## I cannot find my game!!!

Check igdb search https://www.igdb.com/, it matches against this database and while we do have match for case insensitive it expects the start of the match to be correct (kind of a like 'game_name%').

## The script crashes on a specific game

This can be due to a new bug or the fact that for now it doesn't handle special characters like ö from "God of War Ragnarök" very well. You can either reduce the name and match it when asked or remove it for now.

## Script is buggy, not good.

Sorry to hear that, this was basically a "1h" hackaton and I do plan to improve things, feel free to open a merge request or open a bug tracking, I hope to have this in a better shape in the future.

