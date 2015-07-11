from curses import textpad
import command
import time
import curses



class MusicPlayer(object):

    def run(self, stdscreen):
        self.setUpWindows(stdscreen)
        self.runLoop(stdscreen)

    def setUpWindows(self, stdscreen):
        self.master_screen = stdscreen
        track_list_length = 120
        track_list_height = 40

        play_list_length = 50
        play_list_height = 40

        search_buffer_length = 100
        search_buffer_height = 1

        curr_playing_length = 100
        curr_playing_height = 2

        self.track_list_subwin = stdscreen.subwin(track_list_height, track_list_length, 0, 0)
        self.playlist_subwin = stdscreen.subwin(play_list_height, play_list_length, 0, self.track_list_subwin.getmaxyx()[1]+1)
        self.search_subwin = stdscreen.subwin(search_buffer_height, search_buffer_length, self.track_list_subwin.getmaxyx()[0]+1, 0)
        self.curr_playing_subwin = stdscreen.subwin(curr_playing_height, curr_playing_length, stdscreen.getmaxyx()[0]-2, 0)
        self.search_text_box = textpad.Textbox(self.search_subwin)
        self.search_text_box.stripspaces = 1

    def runLoop(self, stdscreen):
        search_key = 115
        quit_key = 113
        move_up_key = curses.KEY_UP
        move_down_key = curses.KEY_DOWN
        next_song_key = curses.KEY_RIGHT
        prev_song_key = curses.KEY_LEFT

        command_dict = { move_up_key : command.moveUp,
                        move_down_key : command.moveDown,
                        next_song_key : command.nextSong,
                        prev_song_key : command.prevSong,
                        search_key : command.searchContent,
                      }

        #welcomescreen
        self.intro()
        time.sleep(2)
#        self.search_subwin.clear()
#        user_input = self.search_text_box.edit()
#        self.track_list_subwin.addstr(0, 0, user_input)
#        self.track_list_subwin.refresh()

        while True:
            char_input = stdscreen.getch()

            if char_input == quit_key:
                break;

            command_dict.get(char_input)(self.track_list_subwin)


    def intro(self):
        intro_text = """
                  _______ _______ _______ _______ ___ _______ ___ ___        _______ ___ ___ ___
                  |   _   |   _   |   _   |       |   |   _   |   Y   |______|       |   Y   |   |
                  |   1___|.  1   |.  |   |.|   | |.  |.  1   |   1   |______|.|   | |.  |   |.  |
                  |____   |.  ____|.  |   `-|.  |-|.  |.  ____|\_   _/       `-|.  |-|.  |   |.  |
                  |:  1   |:  |   |:  1   | |:  | |:  |:  |     |:  |          |:  | |:  1   |:  |
                  |::.. . |::.|   |::.. . | |::.| |::.|::.|     |::.|          |::.| |::.. . |::.|
                  `-------`---'   `-------' `---' `---`---'     `---'          `---' `-------`---'

                    """

        intro_x = int(self.master_screen.getmaxyx()[1]/2)
        intro_y = int(self.master_screen.getmaxyx()[0]/5)

        self.master_screen.addstr(intro_y, intro_x, intro_text)


    def getQueryResults(self):
        pass

    def printTrackList(self):
        pass

    def printPlaylistList(self):
        pass




def run():
    player = MusicPlayer()
    curses.wrapper(player.run)

run()
