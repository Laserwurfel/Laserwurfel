import pyaudio
import decoder
import atexit

_p = pyaudio.PyAudio()
_stream = None
_song = None


def _callback(in_data, frame_count, time_info, status):
    data = _song.readframes(frame_count)
    return (data, pyaudio.paContinue)


def play(file):
    global _stream, _song

    if _stream is not None and _stream.is_active():
        stop()

    _song = decoder.open(file)
    _stream = _p.open(
        format=_p.get_format_from_width(_song.getsampwidth()),
        channels=_song.getnchannels(),
        rate=_song.getframerate(),
        output=True,
        stream_callback=_callback,
    )

    _stream.start_stream()


def stop():
    if _stream is not None and _stream.is_active():
        _stream.stop_stream()
        _stream.close()
        _song.close()


@atexit.register
def _exit():
    stop()
    _p.terminate()
