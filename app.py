from curses import textpad
from command import CommandHandler
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

        command_handler = CommandHandler(self.track_list_subwin, self.search_subwin, self.search_text_box)
        search_key = 115
        select_key = ord('\n')
        client_key = 99
        quit_key = 113
        goto_index_key = 105
        move_up_key = curses.KEY_UP
        move_down_key = curses.KEY_DOWN
        next_song_key = curses.KEY_RIGHT
        prev_song_key = curses.KEY_LEFT

        command_dict = {
                        move_up_key : command_handler.moveUp,
                        move_down_key : command_handler.moveDown,
                        next_song_key : command_handler.nextSong,
                        prev_song_key : command_handler.prevSong,
                        search_key : command_handler.searchContent,
                        select_key : command_handler.currentSong,
                        client_key : command_handler.showClient,
                        goto_index_key : command_handler.playAtIndex,
                      }

        self.intro()

        while True:
            try:
                char_input = stdscreen.getch()

                if char_input == quit_key:
                    break;

                command_dict.get(char_input)()
            except TypeError:
                #TODO: Add error message for user - Invalid Key Input
                pass


    def intro(self):
        intro_text = '''


                .d88888b                      dP   oo                            d888888P dP     dP dP
                88.    "'                     88                                    88    88     88 88
                `Y88888b. 88d888b. .d8888b. d8888P dP 88d888b. dP    dP             88    88     88 88
                      `8b 88'  `88 88'  `88   88   88 88'  `88 88    88 88888888    88    88     88 88
                d8'   .8P 88.  .88 88.  .88   88   88 88.  .88 88.  .88             88    Y8.   .8P 88
                 Y88888P  88Y888P' `88888P'   dP   dP 88Y888P' `8888P88             dP    `Y88888P' dP
                          88                          88            .88
                          dP                          dP        d8888P

                ~Spotify-TUI (Spotify Terminal User Interface)
                    Control the Spotify Desktop Client from this text-based interface
                    Python 3.0+

                ~ Key Commands:
                    Up-Arrow and Down-Arrow: Traverse Search Results
                    Left-Arrow: Play Previous Song (Based on current cursor position)
                    Right-Arrow: Play Next Song (Based on current cursor position)
                    S: Search [Enter Query] + Enter
                    C: Show Spotify Client
                    Q: Quit
                   '''

        intro_x = int(self.master_screen.getmaxyx()[1]/2)
        intro_y = int(self.master_screen.getmaxyx()[0]/10)

        self.master_screen.addstr(intro_y, intro_x, intro_text)






def run():
    player = MusicPlayer()
    curses.wrapper(player.run)

run()
