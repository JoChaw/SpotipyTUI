from curses import textpad
import os
import time
import curses
import subprocess
import requester

class CommandHandler(object):

    def __init__(self, stdscreen):
        track_list_length = 120
        track_list_height = 33

        search_buffer_length = 100
        search_buffer_height = 1

        help_window_length = 120
        help_window_height = 5

        self.country_id = None
        self.stdscreen = stdscreen
        self.track_list = None
        self.back_track_history = []
        self.forward_track_history = []
        self.track_start = 2
        self.curr_position = self.track_start
        self.track_window = stdscreen.subwin(track_list_height, track_list_length, 0, 0)
        self.help_window = stdscreen.subwin(help_window_height, help_window_length, self.track_window.getmaxyx()[0], 1)
        self.prompt_area = self.help_window
        self.search_window = stdscreen.subwin(search_buffer_height, search_buffer_length, self.track_window.getmaxyx()[0], 10)
        self.input_prompt = stdscreen.subwin(1, 15, self.track_window.getmaxyx()[0], 1)
        self.now_playing_window = stdscreen.subwin(1, 120, stdscreen.getmaxyx()[0] - 1, 0)
        self.command_list_hint = stdscreen.subwin(1, 30, stdscreen.getmaxyx()[0] - 3, 0)

        self.command_list_hint.addstr(0, 0, "Press C for Command List")
        self.command_list_hint.refresh()

    def get_input(self):
        curses.echo()
        user_input = self.search_window.getstr().decode(encoding="utf-8")
        curses.noecho()
        return user_input

    def print_command_list(self):
        command_menu = """[<Up>/K: Go Up] [<Down>/J: Go Down] [<Left>/H: Prev Track] [<Right>/L: Next Track]
                          [<Enter>: Play Selected Track] [<Space>: Toggle Play/Pause] [Q: Quit] [Y: Change Country Code]
                          [S: Search] [I: Play Track at Index] [F: Bring Spotify Client to Front] [C: Show Command List]
                          [A: Go to Album of Selected Track] [T: Top Tracks of Artist of Selected Track]
                          [B: Go back one track listing] [N: Go forward one track listing]"""

        command_menu = '\n'.join(' '.join(line.split()) for line in command_menu.split('\n'))

        self.help_window.clear()
        self.help_window.addstr(0, 0, command_menu)
        self.help_window.refresh()

    def set_curr_position(self, curr_position):
        self.curr_position = curr_position

    def move_up(self):
        if self.track_list != None and self.curr_position > self.track_start:
            self.curr_position -= 1
            self.draw_track_list()

    def move_down(self):
        if self.track_list != None and self.curr_position < (len(self.track_list) + self.track_start - 1):
            self.curr_position += 1
            self.draw_track_list()

    def next_song(self):
        self.move_down()
        self.current_song()

    def prev_song(self):
        self.move_up()
        self.current_song()

    def play_at_index(self):
        curses.curs_set(2)

        self.prompt_area.clear()
        self.input_prompt.addstr(0, 0, " Index:")
        self.search_window.clear()
        self.prompt_area.refresh()

        desired_index = self.get_input()

        self.prompt_area.clear()
        self.prompt_area.refresh()

        try:
            desired_index = int(desired_index)
            screen_index = desired_index + self.track_start - 1
            if self.track_list != None and screen_index <= (len(self.track_list) + self.track_start - 1) and screen_index >= self.track_start:
                self.curr_position = screen_index
                self.current_song()
                self.draw_track_list()

        except ValueError:
            #TODO Error Message for invalid index
            pass

        curses.curs_set(0)

    def current_song(self):
        if self.track_list != None:
            self.play_song(self.track_list[self.curr_position - self.track_start])

    def toggle_play_pause(self):
        apple_script_call = ['osascript', '-e', 'tell application "Spotify" to playpause']
        subprocess.call(apple_script_call)

    def play_song(self, track):
        track_spotify_uri = track[4]
        apple_script_call = ['osascript', '-e', 'tell application "Spotify" to play track "{0}"'.format(track_spotify_uri)]

        subprocess.call(apple_script_call)
        self.update_now_playing(track)

    def update_now_playing(self, track):
        now_playing = ">>> Now Playing: {0} --- {1} <<<".format(track[1][:50], track[2][:40])
        self.now_playing_window.clear()
        self.now_playing_window.addstr(0, 0, now_playing)
        self.now_playing_window.refresh()

    def show_client(self):
        get_client_command = 'tell application "Spotify" \n activate \n end tell'
        apple_script_call = ['osascript', '-e', get_client_command]
        subprocess.call(apple_script_call)

    def prev_track_list(self):
        if len(self.back_track_history) > 1:
            self.forward_track_history.append(self.track_list)
            self.track_list = self.back_track_history.pop()
            self.curr_position = self.track_start
            self.draw_track_list()

    def next_track_list(self):
        if len(self.forward_track_history) > 0:
            self.back_track_history.append(self.track_list)
            self.track_list = self.forward_track_history.pop()
            self.curr_position = self.track_start
            self.draw_track_list()

    def search_content(self):
        curses.curs_set(2)

        self.prompt_area.clear()
        self.input_prompt.addstr(0, 0, "Search:")
        self.search_window.clear()
        self.prompt_area.refresh()

        user_search = self.get_input()

        self.prompt_area.clear()
        self.prompt_area.refresh()

        if len(user_search) > 0:
            if not self.back_track_history or self.track_list != self.back_track_history[-1] and self.track_list:
                self.forward_track_history = []
                self.back_track_history.append(self.track_list)

            self.track_list = requester.execute_search(user_search, self.country_id, self.track_window.getmaxyx()[0]-3)
            self.curr_position = self.track_start
            self.draw_track_list()

        curses.curs_set(0)

    def get_artist_top(self):
        if self.track_list != None:
            track = self.track_list[self.curr_position - self.track_start]
            artist_name = track[2]
            artist_id = track[7]
            artist_uri = track[6]

            if not self.back_track_history or self.track_list != self.back_track_history[-1] and self.track_list:
                self.forward_track_history = []
                self.back_track_history.append(self.track_list)

            self.track_list = requester.get_artist_top(artist_name, artist_id, artist_uri, self.country_id)
            self.curr_position = self.track_start
            self.draw_track_list()

    def get_album_tracks(self):
        if self.track_list != None:
            track = self.track_list[self.curr_position - self.track_start]
            album_name = track[3]
            album_id = track[8]
            album_uri = track[5]

            if not self.back_track_history or self.track_list != self.back_track_history[-1] and self.track_list:
                self.forward_track_history = []
                self.back_track_history.append(self.track_list)

            self.track_list = requester.get_album_tracks(album_name, album_id, album_uri)
            self.curr_position = self.track_start
            self.draw_track_list()

    def draw_track_list(self):
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

    def country_check(self):

        valid_countries = [line.strip() for line in open(os.path.dirname(os.path.realpath(__file__)) + "/country_iso_codes.txt", 'r')]
        self.country_check_prompt()

        while self.country_id not in valid_countries:
            self.prompt_area.addstr("::Invalid Country ISO Code::")
            self.prompt_area.refresh()
            time.sleep(1)
            self.country_check_prompt()


    def country_check_prompt(self):
        curses.curs_set(2)

        self.prompt_area.clear()
        self.input_prompt.addstr(0, 0, "Country:")
        self.search_window.clear()
        self.prompt_area.refresh()

        user_input = self.get_input()

        if len(user_input) > 0:
            self.country_id = user_input.split()[0].upper()

        self.prompt_area.clear()
        self.prompt_area.refresh()

        curses.curs_set(0)





