import requests
import json

# Setup
URL = "https://musicbrainz.org/ws/2"

HEADERS = { "User-Agent": "KiwiHomeServer/1.0 (tommaso.piana.agostinetti@gmail.com)"}

# @title is the song title (what the user typed)
# @limit how many song to return (positive integer)
def get_songs_by_title(title, limit):

	query = f'recording:"{title}*"'
	url = URL + f"/recording?query={query}&limit={limit}&fmt=json"

	print(f"Fetching url: '{url}' ...")

	# Request
	response = requests.get(url, headers=headers)

	# Check if successful
	if response.status_code == 200:
		data = response.json()
		
		# Write to file
		with open("musicbrainz_response.json", "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4)
		
		print("JSON data saved to 'musicbrainz_response.json'")
	else:
		print("Request failed:", response.status_code)

# note: limits 100 isn't enough since we are not skipping duplicates
def get_songs_by_artist(artist):
	import requests, json

	# Step 1: Get artist MBID
	res = requests.get(f"{URL}/artist?query=artist:\"{artist}\"&fmt=json", headers=HEADERS)
	artist = res.json()["artists"][0]
	mbid = artist["id"]
	print(f"MBID for {artist}:", mbid)

	# Step 2A: Get recordings
	recordings_url = f"{URL}/recording?artist={mbid}&limit=100&fmt=json"
	recordings = requests.get(recordings_url, headers=HEADERS).json()

	# Step 2B: Get releases
	releases_url = f"{URL}/release?artist={mbid}&limit=100&fmt=json"
	releases = requests.get(releases_url, headers=HEADERS).json()

	# Save both
	with open("songs_by_artist.json", "w") as f:
		json.dump(recordings, f, indent=2)

	with open("albums_by_artist.json", "w") as f:
		json.dump(releases, f, indent=2)

if __name__ == "__main__":
	# get_songs_by_title("Eyes closed", 100)
	get_songs_by_artist("Ed Sheeran")