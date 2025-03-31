import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import keys
from datetime import date
import streamlit as st

client_id = keys.CLIENT_ID
client_secret = keys.CLIENT_SECRET

# client_id = st.secrets['CLIENT_ID']
# client_secret = st.secrets['CLIENT_SECRET']

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
if sp:
    print("successul")

def get_by_year(year, month, day, market):
    # Initialize an empty list for this specific call
    filtered_albums = []
    query = f'year:{year}'
    try:
        results = sp.search(q=query, type='album', limit=50, market=market)  # Max limit is 50
        for album in results["albums"]["items"]:
            release_date = album["release_date"]
            if len(release_date) >= 10:  # Expecting at least YYYY-MM-DD
                release_month_day = release_date[5:10]  # Extract MM-DD
                target_month_day = f"{month:02d}-{day:02d}"  # Ensure 2-digit format
                if release_month_day == target_month_day:
                    # alb = f"{album['name']} ---- {album['artists'][0]['name']}"
                    if album not in filtered_albums:
                        filtered_albums.append(album)
    except Exception as e:
        print(e)
    return filtered_albums

def get_albums(year, month, day):
    markets = ['US', 'IN', 'GB', 'DE', 'AU']
    all_albums = []
    current_year = date.today().year
    for y in range(year - 10, current_year + 1):
        print(f"Fetching albums for year: {y}")
        for m in markets:
            print(f"  Market: {m}")
            albums = get_by_year(y, month, day, m)
            for alb in albums:
                if alb not in all_albums:
                    all_albums.append(alb) 
    # print(all_albums)

    if all_albums:
        print(f"\n🎵 Albums Released on {day}-{month}: 🎵\n")
        for i, album in enumerate(all_albums, start=1):
            print(f"{i}.{album['name']} - {album['artists'][0]['name']} ({album['release_date']})")
    else:
        print(f"\n😔 No albums found for {day}-{month}. 'You were dead for music' 🎶")

# Get user input
bd = input('enter birthdate: ')
day, month, year = bd.split('-')
day = int(day)
month = int(month)
year= int(year)
# Run the function
get_albums(year, month, day)