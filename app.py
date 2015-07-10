import time
import curses



class MusicPlayer(object):
    def __init__(self):
        pass

    def run(self, stdscreen):
        self.setUpWindows(stdscreen)

    def setUpWindows(self, stdscreen):
        track_list_length = 120
        track_list_height = 40

        play_list_length = 50
        play_list_height = 40

        search_buffer_length = 100
        search_buffer_height = 0

        curr_playing_length = 100
        curr_playing_height = 2

        self.track_list_subwin = stdscreen.subwin(track_list_height, track_list_length, 0, 0)
        self.playlist_subwin = stdscreen.subwin(play_list_height, play_list_length, 0, self.track_list_subwin.getmaxyx()[1]+1)
        self.search_subwin = stdscreen.subwin(search_buffer_height, search_buffer_length, self.playlist_subwin.getmaxyx()[0]+1, 0)
        self.curr_playing_subwin = stdscreen.subwin(curr_playing_height, curr_playing_length, stdscreen.getmaxyx()[0]-2, 0)

        #for index in range(0,track_list_height):
        #    self.track_list_subwin.addstr(index, 0, "hop")
        #    self.playlist_subwin.addstr(index, 0, "blahh")

        #self.search_subwin.addstr(0, 0, "DAMNNN")
        #self.curr_playing_subwin.addstr(0, 0, "HERRR")
        #stdscreen.refresh()
        #time.sleep(5)



def run():
    player = MusicPlayer()
    curses.wrapper(player.run)

run()
