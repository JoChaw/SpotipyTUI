
class CommandHandler(object):

    def __init__(self, track_list, curr_position, track_window):
        self.track_list = track_list
        self.curr_position = curr_position
        self.track_window = track_window

    def setTrackList(self, track_list)
        self.track_list = track_list

    def setCurrPosition(self, curr_position)
        self.curr_position = curr_position

    def moveUp():
        pass

    def moveDown():
        pass

    def nextSong():
        pass

    def prevSong():
        pass

    def playSong():
        pass

    def searchContent():
        pass

    def drawTrackList():
        result_output = []
        result_line = '{0:<50} | {1:<25} | {2:<40}'
        result_header = result_line.format('Song Name', 'Artist', 'Album')

        self.track_window.addstr(0, 0, result_header)

        for track in self.track_list:
            result_output.append(result_line.format(track[1][:50], track[2][:25], track[2][:40]))

        for index, track in enumerate(result_output, start=1):

            if self.curr_position == index:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            self.track_window.addstr(index, 0, track, mode)






