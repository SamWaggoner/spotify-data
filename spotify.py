"""
Demonstrating example usage of the Spotify API code from the YouTube tutorial
https://www.youtube.com/watch?v=WAmEZBEeNmg


Author: Samuel Waggoner
Version: 3/14/23
For: Data Science, COS 482 with Chaofan Chen
Assumptions:
    - Insert your spotify client id and secret (not needed for this project)
      into a file named .env in the same folder as spotify.py.
      .env should be only these two lines (for example):
      CLIENT_ID="1db53452516d04e634523372351de40f"
      CLIENT_SECRET="h684e54534cfgd797v91452346cgcbf5"
Example Usage:
    python spotify.py
"""


"""
Question 1: What countries' top songs are the loudest (or are the best for
dancing, energy, etc below), based off their top 50 playlist?

Note: not every country has a top 50 playlist, so this will only work for some.

Question 2: What is the average loudness (or danciness, energy, etc below)
for the top 100 songs each year 1970-2023?

Note: spotify was created in 2009, so I assume they made the other playlists
based off the billboards. I haven't looked this up.
Note: For years 1970-2019, this playlist is named "Top Hits of YYYY", and has 
100 songs. For years 2020 and more recent, this playlist is named 
"Top Tracks of YYYY" and has 50 songs.

Options:
Mood: Danceability, Valence, Energy, Tempo
Properties: Loudness, Speechiness, Instrumentalness
Context: Liveness, Acousticness
Segments, Tatums, Bars, Beats, Pitches, Timbre, and more
"""


"""
The code below is from the tutorial I watched. I have yet to write code to answer
the questions above.
"""
import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    # this is the heart of our function, the actual post request
    result = post(url, headers=headers, data=data)
    # convert json to python dictionary
    json_result = json.loads(result.content) # loads = load from string
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Function that allows you to search for an artist
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist,track&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    # json_result = json.loads(result.content)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()
result = search_for_artist(token, "ACDC")
# print(json.dumps(result, indent=2))
print(result["name"])

artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
# print(songs)

for idx, song in enumerate(songs):
    print(f"{idx+1}. {song['name']}")