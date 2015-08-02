from command import CommandHandler
import sys
import curses

def run_loop(stdscreen):
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
    forward_key = 110
    command_list_key = 99
    country_change_key = 121
    volume_up_key = 112
    volume_down_key = 111
    volume_set_key = 118

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
                    forward_key : command_handler.next_track_list,
                    command_list_key : command_handler.print_command_list,
                    country_change_key : command_handler.country_check,
                    volume_up_key : command_handler.increment_volume,
                    volume_down_key : command_handler.decrement_volume,
                    volume_set_key : command_handler.user_volume_input,
                  }

    curses.curs_set(0)
    intro(stdscreen)
    command_handler.country_check()
    command_handler.prompt_area.addstr(0, 0, "Good To Go! Start a search with [S]")
    command_handler.prompt_area.refresh()

    while True:
            char_input = stdscreen.getch()

            if char_input == quit_key:
                sys.exit()
            elif char_input in command_dict:
                command_dict.get(char_input)()


def intro(stdscreen):
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
                S: Search for music                             [Space]: Toggle Play/Pause
                I: Jump to song at index within search results  [Enter]: Play track at current position
                A: Go to album of current selection             [Up]/K: Go Up
                T: Get current selection's artist's top tracks  [Down]/J: Go Down
                C: Show Command List                            [Left]/H: Play previous track
                F: Bring up Spotify desktop client              [Right]/L: Play next track
                Y: Change Country ISO Code                      O: Decrease Volume
                B: Go backwards in track listing history        P: Increase Volume
                N: Go forward in track listing history          V: Set Volume Level
               '''

    stdscreen.addstr(0, 0, intro_text)
    stdscreen.refresh()

curses.wrapper(run_loop)
