import curses
import subprocess
import requester

class CommandHandler(object):

    def __init__(self, track_window, search_window, input_buffer):
        self.track_list = None
        self.curr_position = 1
        self.track_window = track_window
        self.search_window = search_window
        self.input_buffer = input_buffer

    def setTrackList(self, track_list):
        self.track_list = track_list

    def setCurrPosition(self, curr_position):
        self.curr_position = curr_position

    def moveUp(self):
        if self.track_list != None and self.curr_position > 1:
            self.curr_position -= 1
            self.drawTrackList()

    def moveDown(self):
        if self.track_list != None and self.curr_position < len(self.track_list):
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

        self.search_window.clear()
        desired_index = self.input_buffer.edit()

        try:
            desired_index = int(desired_index)
            if self.track_list != None and desired_index <= len(self.track_list) and desired_index > 0:
                self.curr_position = desired_index
                self.currentSong()
                self.drawTrackList()

        except ValueError:
            #TODO Error Message for invalid index
            pass

        curses.curs_set(0)

    def currentSong(self):
        if self.track_list != None:
            self.playSong(self.track_list[self.curr_position-1])

    def playSong(self, track):
        track_spotify_uri = track[4]
        apple_script_call = ['osascript', '-e', 'tell application "Spotify" to play track "{0}"'.format(track_spotify_uri)]

        subprocess.call(apple_script_call)

    def showClient(self):
        get_client_command = 'tell application "Spotify" \n activate \n end tell'
        apple_script_call = ['osascript', '-e', get_client_command]
        subprocess.call(apple_script_call)

    def searchContent(self):
        curses.curs_set(2)

        self.search_window.clear()
        user_search = self.input_buffer.edit()
        self.track_list = requester.execute_search(user_search)
        self.curr_position = 1
        self.drawTrackList()

        curses.curs_set(0)

    def drawTrackList(self):
        self.track_window.clear()

        result_output = []
        result_line = '{0:<40} | {1:<25} | {2:<40}'
        result_header = result_line.format('Song Name', 'Artist', 'Album')

        self.track_window.addstr(0, 0, result_header)

        for track in self.track_list:
            result_output.append(result_line.format(track[1][:40], track[2][:25], track[3][:40]))

        for index, track in enumerate(result_output, start=1):

            if self.curr_position == index:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            self.track_window.addstr(index, 0, track, mode)

        self.track_window.refresh()






