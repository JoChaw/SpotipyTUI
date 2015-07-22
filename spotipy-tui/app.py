from command import CommandHandler
import time
import curses



class MusicPlayer(object):

    def __init__(self, stdscreen):
        self.run(stdscreen)

    def run(self, stdscreen):
        self.runLoop(stdscreen)

    def runLoop(self, stdscreen):
        command_handler = CommandHandler(stdscreen)
        search_key = 115
        select_key = ord('\n')
        spotify_client_key = 102
        quit_key = 113
        goto_index_key = 105
        artist_tracks_key = 116
        album_tracks_key = 97
        move_up_key = curses.KEY_UP
        move_up_key_2 = 107
        move_down_key = curses.KEY_DOWN
        move_down_key_2 = 106
        next_song_key = curses.KEY_RIGHT
        next_song_key_2 = 108
        prev_song_key = curses.KEY_LEFT
        prev_song_key_2 = 104
        play_pause_key = 32
        back_key = 98
        command_list_key = 99

        command_dict = {
                        move_up_key : command_handler.move_up,
                        move_down_key : command_handler.move_down,
                        next_song_key : command_handler.next_song,
                        prev_song_key : command_handler.prev_song,
                        move_up_key_2 : command_handler.move_up,
                        move_down_key_2 : command_handler.move_down,
                        next_song_key_2 : command_handler.next_song,
                        prev_song_key_2 : command_handler.prev_song,
                        search_key : command_handler.search_content,
                        select_key : command_handler.current_song,
                        spotify_client_key : command_handler.show_client,
                        goto_index_key : command_handler.play_at_index,
                        artist_tracks_key : command_handler.get_artist_top,
                        album_tracks_key : command_handler.get_album_tracks,
                        play_pause_key : command_handler.toggle_play_pause,
                        back_key : command_handler.prev_track_list,
                        command_list_key : command_handler.print_command_list,
                      }

        curses.curs_set(0)
        self.intro(stdscreen)

        while True:
                char_input = stdscreen.getch()

                if char_input == quit_key:
                    break;
                elif char_input in command_dict:
                    command_dict.get(char_input)()


    def intro(self, stdscreen):

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
                    Space: Toggle Play/Pause
                    <Enter>: Play track at current position
                    <Up>/K: Go Up
                    <Down>/J: Go Down
                    <Left>/H: Play previous track (Based on current cursor position)
                    <Right>/L: Play next track (Based on current cursor position)
                    S: Search for music
                    I: Jump to song at index within search results
                    A: Go to album of current selection
                    T: Get top tracks of artist of curent selection
                    C: Show Command List
                    F: Show Spotify Client
                    Q: Quit

                [Press S to begin searching for music]
                   '''

        intro_x = int(stdscreen.getmaxyx()[1]/2)
        intro_y = int(stdscreen.getmaxyx()[0]/10)

        stdscreen.addstr(intro_y, intro_x, intro_text)


def run():
    player = MusicPlayer
    curses.wrapper(player)


run()
