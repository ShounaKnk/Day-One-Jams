import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import keys
from datetime import date

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=keys.CLIENT_ID, client_secret=keys.CLIENT_SECRET
))

st.set_page_config(page_title="Birthday Albums")

# Custom CSS for Styling
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stButton>button {
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 25px;
            border-color: #1ED760;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: #1ED760;
            color: white;
        }
        .album-card {
            border-radius: 15px;
            text-align: center;
            padding: 20px;
            background: #1C1C1C;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, border 0.3s ease;
            width: 220px;
            height: 320px; /* Ensuring all cards have the same height */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .album-card:hover {
            transform: translateY(-10px);
            border: 2px solid #1ED760;
        }
        .album-img {
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
        }
        .album-title {
            color: white;
            font-weight: bold;
            font-size: 16px;
            margin-top: 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 220px;
        }
        .album-artist {
            font-size: 14px;
            color: #B3B3B3;
            text-align: center;
            max-width: 220px;
        }
        .album-release{
            font-size: 12px;
            color: #B3B3B3;
            text-align: center;
            max-width: 220px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style='text-align: center;'>🎵 What Albums Dropped on Your Birthday?</h1>
    <p style='text-align: center;'>Find out which iconic albums were released on your special day!</p>
""", unsafe_allow_html=True)

# Date Input
bd = st.date_input("Select Your Birthday", min_value=date(1950, 1, 1), max_value=date.today())

# Function to Get Albums
def get_albums(year, month, day):
    markets = ['US', 'IN', 'GB', 'DE', 'AU']
    all_albums = []
    for y in range(year - 10, date.today().year + 1):
        for m in markets:
            query = f'year:{y}'
            results = sp.search(q=query, type='album', limit=50, market=m)
            for album in results["albums"]["items"]:
                release_date = album["release_date"]
                if len(release_date) >= 10 and release_date[5:10] == f"{month:02d}-{day:02d}":
                    album["url"] = album["external_urls"]["spotify"]
                    if album not in all_albums:
                        all_albums.append(album)
    return all_albums

# Truncate text function
def truncate_text(text, max_length=25):
    return text if len(text) <= max_length else text[:max_length] + "..."

# Button to Fetch Albums
if st.button("Find Albums"):
    albums = get_albums(bd.year, bd.month, bd.day)
    if albums:
        st.write("### Albums Released on Your Birthday 🎂")
        cols = st.columns(3)  # Creates a 3-column layout

        for i, album in enumerate(albums):
            with cols[i % 3]:  # Distribute albums evenly into columns
                st.markdown(f"""
                    <div class='album-card'>
                        <a href='{album['url']}' target='_blank'>
                            <img src='{album['images'][0]['url']}' class='album-img' />
                        </a>
                            <div class='album-title'>{truncate_text(album['name'])}</div>
                            <div class='album-artist'>{album['artists'][0]['name']}</div>
                            <div class='album-release'>({album['release_date']})</div>
                        </div>
                """, unsafe_allow_html=True)
    else:
        st.write("No albums found for this date. 🎵")