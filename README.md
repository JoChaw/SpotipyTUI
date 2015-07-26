# Spotipy-TUI 
Spotipy-TUI is a text-based UI program to control the Spotify desktop client on OSX. <br>
Run it within a terminal session. <br>
Requires OSX and Python 3. <br>

[Quick Demo Video](https://www.youtube.com/watch?v=BYVSOE8mjWs)

##Installation
```python
$ sudo pip install spotipy-tui
```

###Usage 
```python 
# Start the program
$ spotify-tui
```
###Command List
* S: Search for music
* I: Jump to song at index within search results
* A: Go to album of current selection
* T: Get current selection's artist's top tracks
* C: Show command list
* F: Bring Up Spotify desktop client
* Y: Change Country ISO Code
* [Space]: Toggle Play/Pause
* [Enter]: Play track at current cursor position
* [Up]/K: Go Up
* [Down]/J: Go Down
* [Left]/H: Play previous track (based on cursor position)
* [Right]/L: Play next track (based on cursor position)
* Q: Quit

### Dependencies 
```bash
pip install requests
```
