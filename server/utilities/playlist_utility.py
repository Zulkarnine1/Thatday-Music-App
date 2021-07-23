import requests as req
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from server.env import SPOTIFY_ID,SPOTIFY_SECRET, ROOT_ROUTE



class ScrapperManager:

    def get_song_list(self,target_time):
        try:
            res = req.get(f"https://www.billboard.com/charts/hot-100/{target_time}")
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            song_span_list = soup.find_all(name="span",
                                     class_="chart-element__information__song text--truncate color--primary")
            top100 = [song.getText() for song in song_span_list]
            return (True,top100)
        except Exception as error:
            print(error)
            return (False,[])



class PlaylistManager:
    def __init__(self,PlaylistModel):
        self.PlaylistModel = PlaylistModel
        self.scraper = ScrapperManager()
        self.spotipymanager = spotipy.Spotify(
                            auth_manager=SpotifyOAuth(
                                scope="playlist-modify-private",
                                redirect_uri=ROOT_ROUTE,
                                client_id=SPOTIFY_ID,
                                client_secret=SPOTIFY_SECRET,
                                show_dialog=True,
                                cache_path="token.txt"
                            )
                        )
        self.user_id = self.spotipymanager.current_user()["id"]

    def get_playlist(self, target_time,db):
        try:
            # Check if playlist already exists or no
            existing_playlist = self.PlaylistModel.query.filter_by(date=target_time).first()
            if(existing_playlist):
                return (True, existing_playlist.link)
            # If doesnt exist create a playlist entry by scraping and requesting spotify api
            else:
                return self.create_playlist(target_time,db)
        except Exception as e:
            print(e)

    def create_playlist(self,target_time,db):
            no_error,song_list  = self.scraper.get_song_list(target_time)
            if(no_error):
                songs = []
                year = target_time.split("-")[0]
                for song in song_list:
                    result = self.spotipymanager.search(q=f"track:{song} year:{year}", type="track")
                    try:
                        uri = result["tracks"]["items"][0]["uri"]
                        songs.append(uri)
                    except IndexError:
                        print(f"{song} doesn't exist in Spotify. Skipped.")
                        pass
                playlist = self.spotipymanager.user_playlist_create(user=self.user_id, name=f"{target_time} Billboard 100", public=False)
                self.spotipymanager.playlist_add_items(playlist_id=playlist["id"], items=songs)
                new_playlist = self.PlaylistModel(date=target_time,link=playlist["external_urls"]["spotify"])
                db.session.add(new_playlist)
                db.session.commit()
                return (True, playlist["external_urls"]["spotify"])
            else:
                return (False,"500:Internal server error.")

