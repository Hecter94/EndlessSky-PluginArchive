# Sounds of Endless Sky

This is a plugin aiming to provide music for Endless Sky as well as remaster the
audio to balance it.

# Music by Anthrophantasmus

Licensed CC-BY-4.0.  See [copyright](copyright) for licensing.

The original uncompressed WAV files released by Anthrophantasmus can be found at
[raw-sounds-of-endless-sky][raw-sounds-of-endless-sky].

Other profiles:

- [Anthrophantasmus YouTube channel][Anthrophantasmus-youtube]
- [Anthrophantasmus GitHub profile][Anthrophantasmus-github]

[Anthrophantasmus-youtube]: https://www.youtube.com/channel/UCryMx7RshwDKNHQ-amgEm0A
[Anthrophantasmus-github]: https://github.com/Anthrophantasmus
[raw-sounds-of-endless-sky]: https://github.com/samrocketman/raw-sounds-of-endless-sky

# Audio conversion

Endless Sky is extremely specific about how it supports audio.  Currently, only
WAV for sound effects and MP3 for music is supported.

### Encoding sound effects

Sound effects are in WAV format.  Specifically, little-endian 16-bit PCM at
44100 Hz.

Here's an `ffmpeg` command to get sounds into an appropriate format.

    ffmpeg -i original.wav -ac 1 -f wav -c pcm_s16le -ab 705k -ar 44100 sounds/effect.wav

### Encoding music

MP3 specifically requires stereo format (2-channel) bit rate 179kb/s at 44100
Hz.

    ffmpeg -i original.wav -f mp3 -ar 44100 -ab 179k -ac 2 sounds/music.mp3
