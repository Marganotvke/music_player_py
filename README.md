# music_player_py
It's pretty average. Kinda. Well not quite, but still.
<br>A python written music player using PyQt5. Currently supports a lot of file format (e.g. mp3, aac, wav, midi etc.)
<br>Planned to include more functionality, such as audio visualizer (might not actually do this).

### Button controls
- Backward: Play the previous music if played less than 5 seconds, else replay the music from start.
- Pause/Continue: Literally. Load song if no songs are present in the queue.
- Stop: Literally.
- Forward: Play the next song in queue.
- Playstyle: Select what the playlist will behave, e.g. loop/ play current playlist once.

### Song Queue Controls
- Drag: Rearrange the song queue. If rearrange the currently playing music, will play the new music in position instead of the originally playing one. Might change the behavior.
- Drop from outside: You can drop music files from the outside!

### Changes
- v0.1: Base
- v0.2: Added drag&drop and list feature. You can now drag songs (currently **one** at a time!) into the player to play it. When multiple songs presents, you can jump to any specific songs to play it. You can also rearrange the song queue by simply drag and drop them in place.<br>**Last version with pygame mixer music player!**
- v1.0: Reimplemented the music player with QMediaPlayer, as well as implemented new functions and improved old functions.

### Known issue
> - Can't drag more than one song into the player (might not change this behavior)

### Windows standalone executable (.exe)
See release.
