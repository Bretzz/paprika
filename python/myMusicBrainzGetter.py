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

# gets all the official releases of an artist by MBID
def get_all_releases_by_artist(mbid):
	all_releases = []
	limit = 100
	offset = 0

	while True:
		url = f'{URL}/release?query=arid:{mbid}&limit={limit}&offset={offset}&fmt=json'
		resp = requests.get(url, headers=HEADERS).json()
		releases = resp.get('releases', [])
		if not releases:
			break
		all_releases.extend(releases)
		offset += limit

	return all_releases

# gets all the official releases of an artist by MBID
def get_all_recordings_by_artist(mbid):
	all_recordings = []
	limit = 100
	offset = 0

	while True:
		url = f'{URL}/recording?artist={mbid}&limit={limit}&offset={offset}&fmt=json'
		resp = requests.get(url, headers=HEADERS).json()
		recordings = resp.get('recordings', [])
		if not recordings:
			break
		all_recordings.extend(recordings)
		offset += limit

	return all_recordings


# welp ... 
# def	remove_duplicates_by_title(all_releases):
# 	unique_releases = {}
# 	for release in all_releases:
# 		title = release.get("title")
# 		if title not in unique_releases:
# 			unique_releases[title] = release

# 	return unique_releases
def remove_duplicates_by_title(releases):
    """
    Remove duplicate releases based on title.
    Returns a list of unique release objects.
    """
    seen_titles = set()
    unique_releases = []

    for release in releases:
        title = release.get("title")
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_releases.append(release)

    return unique_releases

# welp ... 
def filter_elements_by_keys(filters, elements):
    """
    Filters elements based on nested keys using dot notation.
    Example filter: {"status": "Official", "release-group.primary-type": "Album"}
    Returns a dict of matched elements keyed by their ID.
    """
    def get_nested_value(data, key_path):
        keys = key_path.split('.')
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return None
        return data

    filtered = {}
    for element in elements:
        if all(get_nested_value(element, key) == value for key, value in filters.items()):
            filtered[element.get("id", len(filtered))] = element
    return filtered

# Drop the 'release-events' from the album
def drop_release_events(albums_dict):
    """
    Removes the 'release-events' key from each release in the given dictionary.
    
    Args:
        albums_dict (dict): Dictionary of releases keyed by ID.
    
    Returns:
        dict: Modified dictionary with 'release-events' removed.
    """
    for release_id, release_data in albums_dict.items():
        release_data.pop("release-events", None)  # Safe removal
    return albums_dict

# https://musicbrainz.org/ws/2/release/e12df6bd-b0c3-4e16-b6d2-9e9d5d09c308?inc=recordings&fmt=json
# def get_recordings_from_album(mbid):


# note: limits 100 isn't enough since we are not skipping duplicates
def get_songs_by_artist(artist):

	# Step 1: Get artist MBID
	res = requests.get(f"{URL}/artist?query=artist:\"{artist}\"&fmt=json", headers=HEADERS)
	artist = res.json()["artists"][0]
	mbid = artist["id"]
	print(f"MBID for {artist}:", mbid)

	# Step 2A: Get recordings
	recordings = get_all_recordings_by_artist(mbid)

	# Step 2B: Get releases
	releases = get_all_releases_by_artist(mbid)

	# Remove duplicates
	unique_recordings = remove_duplicates_by_title(recordings)
	unique_releases = remove_duplicates_by_title(releases)

	# Get only albums
	albums = filter_elements_by_keys({"status": "Official", "release-group.primary-type": "Album"}, unique_releases)
	cleaned_albums = drop_release_events(albums)

	# Save both
	with open("songs_by_artist.json", "w") as f:
		json.dump(unique_recordings, f, indent=2)

	with open("releases_by_artist.json", "w") as f:
		json.dump(unique_releases, f, indent=2)
	
	with open("albums_by_artist.json", "w") as f:
		json.dump(cleaned_albums, f, indent=2)

if __name__ == "__main__":
	# get_songs_by_title("Eyes closed", 100)
	get_songs_by_artist("Ed Sheeran")