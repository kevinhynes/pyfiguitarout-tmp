from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
Window.maximize()
# Window.size = (500, 300)
from kivy.clock import Clock
from songlibrary import SongLibraryPopup
from spotifylogin import SpotifyLoginPopup

import spotipy

Builder.load_file("style.kv")
Builder.load_file("slideupmenu.kv")
Builder.load_file("fretboarddisplay.kv")
Builder.load_file("scaleoptionschooser.kv")
Builder.load_file("keysigchooser.kv")
Builder.load_file("keysigdisplay.kv")
Builder.load_file("keysigtitlebar.kv")
Builder.load_file("chorddisplay.kv")
Builder.load_file("metronome.kv")
Builder.load_file("tuner.kv")
Builder.load_file("numfretschanger.kv")
Builder.load_file("fretboard.kv")
Builder.load_file("piano.kv")
Builder.load_file("instrumentrack.kv")
Builder.load_file("songbuilder.kv")


class SpotifyConnection:

    def __init__(self, token):
        self.conn = spotipy.Spotify(auth=token)
        print('connected to spotify')

    def play_on_spotify(self, query):
        results = self.conn.search(q=query)
        track_id = results['tracks']['items'][0]['id']
        self.conn.start_playback(uris=['spotify:track:' + track_id])
        print('started spotify playback')

class MainPage(FloatLayout):
    spt_conn = ObjectProperty()

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def show_song_library(self, *args):
        self.song_library_popup = SongLibraryPopup()
        self.song_library_popup.open()

    def show_spotify_login_popup(self, *args):
        self.spotify_log_in_popup = SpotifyLoginPopup(login_func=self.log_in_to_spotify)
        self.spotify_log_in_popup.open()

    def log_in_to_spotify(self, username):
        self.spotify_log_in_popup.dismiss()
        scope = 'user-library-read user-modify-playback-state'
        token = spotipy.util.prompt_for_user_token(username, scope,
                                           client_id="b8a306fd829d4ea4a757cb1411baf0eb",
                                           client_secret="a00b878607994e4fbcc08cf9c053bd21",
                                           redirect_uri="http://localhost:5000/callback/spotify")
        self.spt_conn = SpotifyConnection(token)




class MainApp(App):
    def build(self):
        return MainPage()


if __name__ == "__main__":
    MainApp().run()