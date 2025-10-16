import yt_dlp

# --------------------------------------- #
# Field						Description
# --------------------------------------- #
# %(title)s					Video title
# %(id)s					Video ID
# %(ext)s					File extension (mp4, webm, mp3, etc.)
# %(uploader)s				Channel name
# %(upload_date)s			Date in YYYYMMDD
# %(playlist_title)s		Playlist title
# %(playlist_index)s		Index in playlist
# %(channel)s				Channel ID
# %(webpage_url_domain)s	Domain (e.g., youtube.com)
# %(resolution)s			Resolution (720p, etc.)
# %(epoch)s					UNIX timestamp
# --------------------------------------- #

# url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
url = "https://www.youtube.com/watch?v=34O4TxvuEKE"

def url_to_file(url, path):
	ydl_opts = {
		'format': 'bestaudio/best',				# audio best qquality
		'noplaylist': True,						# just first video of playlist
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',		# ffmpeg for format conversion
			'preferredcodec': 'mp3',			# or 'flac'
			'preferredquality': '192', 			# ignored for FLAC
		}],
		'outtmpl': f'data/audio/{path}/%(title)s.%(ext)s',	# where to save the file
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

if __name__ == "__main__":
	url_to_file(url, "Stromae/singles/")