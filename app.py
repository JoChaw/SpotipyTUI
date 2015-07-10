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

        self.track_list_subwin = stdscreen.subwin(track_list_height, track_list_length, 0, 0)
        self.playlist_subwin = stdscreen.subwin(play_list_height, play_list_length, 0, track_list_length+1)

        #for index in range(0,track_list_height):
        #    self.track_list_subwin.addstr(index, 0, "hop")
        #    self.playlist_subwin.addstr(index, 0, "blahh")

        #self.track_list_subwin.refresh()
        #self.playlist_subwin.refresh()
        #time.sleep(5)



def run():
    player = MusicPlayer()
    curses.wrapper(player.run)

run()
