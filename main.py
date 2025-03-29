import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import keys

client_id = keys.CLIENT_ID
client_secret = keys.CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
if sp:
    print("successul")

def get_albums(year, month, day):
    query = f'year:{year}'
    filtered_albums = []
    markets = ['US','IN','GB', 'DE', 'FR', 'AU', 'CA']
    for m in markets:
        try:  
            results = sp.search(q=query, type='album', limit=10, market=m) # Increase limit to fetch more albums
            for album in results["albums"]["items"]:
                if album["release_date"] == f"{year}-{month}-{day}":
                    filtered_albums.append(f'{album['name']}----{album['artists'][0]['name']}')
        except Exception as e:
            print(e)
    # Filter albums by exact date
    print(filtered_albums)

    # Sort by popularity (most popular first)
    # sorted_albums = sorted(filtered_albums, key=lambda x: x.get('popularity', 0), reverse=True)

    # if sorted_albums:
    #     print(f"\n🎵 Albums Released on {day}-{month}-{year}: 🎵\n")
    #     for i, album in enumerate(sorted_albums, start=1):
    #         print(f"{i}. 📀 {album['name']} - {album['artists'][0]['name']} ({album['release_date']}) - Popularity: {album.get('popularity', 'N/A')}")
    # else:
    #     print(f"\n😔 No albums found for {day}-{month}-{year}. 'You were dead for music' 🎶")

# Get user input
bd = input('enter birthdate: ')
day, month, year = bd.split('-')

# Run the function
get_albums(year, month, day)