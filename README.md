# music_player_py
A python written music player using pygame and PyQt5. Currently supports .mp3, .wav and .ogg.

Planning on using other modules (e.g. music-player-core from albertz or PyQt5's inbuild QMediaPlayer) instead of pygame for better song control and more support on music file type.
<br>Also planned to include more functionality, such as audio visualizer (might not actually do this).

### Button controls
Backward: Basically play from start. Since currently songs played will be deleted from queue, you can't playback the previous song.
Pause/Continue: Literally. Load song if no songs are present in the queue.
Stop: Literally. **Also deletes the whole queue.**
Forward: Play the next song in queue. Will delete the previously playing song from queue.

### Changes
- v0.1: Base
- v0.2: Added drag&drop and list feature. You can now drag songs (currently **one** at a time!) into the player to play it. When multiple songs presents, you can jump to any specific songs to play it. You can also rearrange the song queue by simply drag and drop them in place.<br>**Last version with pygame mixer music player!**

### Known issue
> - Can't drag more than one song into the player
> - Might have weird behavior after internal movement of song queue

### Windows standalone executable (.exe)
See release.
