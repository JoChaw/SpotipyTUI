from curses import textpad
import curses
import subprocess
import requester

class CommandHandler(object):

    def __init__(self, stdscreen):

        track_list_length = 120
        track_list_height = 38

        search_buffer_length = 100
        search_buffer_height = 1

        self.country_id = None
        self.stdscreen = stdscreen
        self.track_list = None
        self.track_start = 2
        self.curr_position = self.track_start
        self.track_window = stdscreen.subwin(track_list_height, track_list_length, 0, 0)
        self.search_window = stdscreen.subwin(search_buffer_height, search_buffer_length, self.track_window.getmaxyx()[0]+1, 8)
        self.input_buffer  = textpad.Textbox(self.search_window)
        self.input_buffer.stripspaces = 1
        self.input_prompt = stdscreen.subwin(1, 10, self.track_window.getmaxyx()[0]+1, 1)
        self.now_playing_window = stdscreen.subwin(1, 120, stdscreen.getmaxyx()[0] - 1, 0)

    def setTrackList(self, track_list):
        self.track_list = track_list

    def setCurrPosition(self, curr_position):
        self.curr_position = curr_position

    def moveUp(self):
        if self.track_list != None and self.curr_position > self.track_start:
            self.curr_position -= 1
            self.drawTrackList()

    def moveDown(self):
        if self.track_list != None and self.curr_position < (len(self.track_list) + self.track_start - 1):
            self.curr_position += 1
            self.drawTrackList()

    def nextSong(self):
        self.moveDown()
        self.currentSong()

    def prevSong(self):
        self.moveUp()
        self.currentSong()

    def playAtIndex(self):
        curses.curs_set(2)

        self.input_prompt.addstr(0, 0, "Index#:")
        self.input_prompt.refresh()
        self.search_window.clear()
        desired_index = self.input_buffer.edit()

        self.input_prompt.clear()
        self.input_prompt.refresh()
        self.search_window.clear()
        self.search_window.refresh()

        try:
            desired_index = int(desired_index)
            screen_index = desired_index + self.track_start - 1
            if self.track_list != None and screen_index <= (len(self.track_list) + self.track_start - 1) and screen_index >= self.track_start:
                self.curr_position = screen_index
                self.currentSong()
                self.drawTrackList()

        except ValueError:
            #TODO Error Message for invalid index
            pass

        curses.curs_set(0)

    def currentSong(self):
        if self.track_list != None:
            self.playSong(self.track_list[self.curr_position - self.track_start])

    def playSong(self, track):
        track_spotify_uri = track[4]
        apple_script_call = ['osascript', '-e', 'tell application "Spotify" to play track "{0}"'.format(track_spotify_uri)]

        subprocess.call(apple_script_call)
        self.updateNowPlaying(track)

    def updateNowPlaying(self, track):
        now_playing = ">>> Now Playing: {0} --- {1} <<<".format(track[1][:50], track[2][:40])
        self.now_playing_window.clear()
        self.now_playing_window.addstr(0, 0, now_playing)
        self.now_playing_window.refresh()

    def showClient(self):
        get_client_command = 'tell application "Spotify" \n activate \n end tell'
        apple_script_call = ['osascript', '-e', get_client_command]
        subprocess.call(apple_script_call)

    def searchContent(self):
        curses.curs_set(2)

        self.input_prompt.addstr(0, 0, "Search:")
        self.input_prompt.refresh()
        self.search_window.clear()
        user_search = self.input_buffer.edit()

        self.input_prompt.clear()
        self.input_prompt.refresh()
        self.search_window.clear()
        self.search_window.refresh()

        self.track_list = requester.execute_search(user_search)
        self.curr_position = self.track_start
        self.drawTrackList()

        curses.curs_set(0)

    def getArtistTop(self):

        while self.country_id == None: #TODO: Ensure Valid Country Country Code
            curses.curs_set(2)

            self.input_prompt.addstr(0, 0, "Country:")
            self.input_prompt.refresh()
            self.search_window.clear()
            self.country_id = self.input_buffer.edit()

            self.input_prompt.clear() #TODO: Bundle all these clear and refreshes into methods
            self.input_prompt.refresh()
            self.search_window.clear()
            self.search_window.refresh()

            curses.curs_set(0)

        track = self.track_list[self.curr_position - self.track_start]
        self.track_list = requester.get_artist_top(track[7], self.country_id)
        self.curr_position = self.track_start
        self.drawTrackList()

    def getAlbumTracks(self):
        track = self.track_list[self.curr_position - self.track_start]
        self.track_list = requester.get_album_tracks(track[8])
        self.curr_position = self.track_start
        self.drawTrackList()

    def drawTrackList(self):
        self.track_window.clear()

        result_line = '{0:<2} | {1:<40} | {2:<25} | {3:<40}'
        result_header = result_line.format('#', 'Song Name', 'Artist', 'Album')
        separator_bar = '=' * (self.track_window.getmaxyx()[1] - 5)

        self.track_window.addstr(0, 0, result_header)
        self.track_window.addstr(1, 0, separator_bar)

        for song_index, track in enumerate(self.track_list, start=1):
            if (self.curr_position - self.track_start) == track[0]:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            song_index = str(song_index)

            if len(song_index) == 1:
                song_index = '0' + song_index

            track_string = result_line.format(song_index, track[1][:40], track[2][:25], track[3][:40])
            self.track_window.addstr(track[0] + self.track_start, 0, track_string, mode)

        bottom_bar_position = self.track_start + len(self.track_list)
        self.track_window.addstr(bottom_bar_position, 0, separator_bar)
        self.track_window.refresh()






