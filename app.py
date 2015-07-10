import time
import curses



class MusicPlayer(object):
    def __init__(self):
        pass

    def run(self, stdscreen):
        self.setUpWindows(stdscreen)

    def setUpWindows(self, stdscreen):
        result_win_x = 120
        result_win_y = 40

        self.result_window = stdscreen.subwin(result_win_y, result_win_x, 0, 0)

#        for index in range(0,result_win_y):
#            self.result_window.addstr(index, 0, "Hoopla")
#
#        self.result_window.refresh()
#        time.sleep(1)



def run():
    player = MusicPlayer()
    curses.wrapper(player.run)

run()
