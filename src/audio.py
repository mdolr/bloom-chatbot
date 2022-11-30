import wave
import gtts
import pyaudio
from termcolor import colored
from playsound import playsound
import speech_recognition as sr
from pynput.keyboard import Key, Listener

import src.utils as utils
import src.config as config

# Audio variables shared among the recorder callback and the main thread
recording = False
processing = False
stream = None
p = None
wf = None
frames = []
voice_input = ""

# Audio settings
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
filename = "./audio/record.wav"


def text_to_speech(text):
    """
    A function to convert text to speech using Google Text-to-Speech API
    """
    tts = gtts.gTTS(text, lang=config.AUDIO_LANGUAGE)
    tts.save("./audio/tts.mp3")
    playsound("./audio/tts.mp3")


def recorder_callback(in_data, frame_count, time_info, status):
    """
    A callback function to be passed to the PyAudio object.
    """
    global wf
    global frames
    frames.append(in_data)
    return (in_data, pyaudio.paContinue if recording else pyaudio.paComplete)


def recorder_handler(key):
    global recording
    global processing
    global stream
    global p
    global wf
    global frames
    global voice_input

    if key == Key.space:
        if recording:
            processing = True
            recording = False
            stream.stop_stream()
            stream.close()

            utils.clear_previous_console_line()
            print(colored(f'{config.USER_NAME}: ', "yellow") +
                  colored("### ⚙️  PROCESSING ####", "white"))

            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
            p.terminate()

            r = sr.Recognizer()
            with sr.AudioFile(filename) as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(
                    audio_data, language=config.AUDIO_LANGUAGE)
                voice_input = text
                utils.clear_previous_console_line()
                print(colored(f'{config.USER_NAME}: ', "yellow") +
                      colored(f'🔉 {voice_input}', "cyan"))
                processing = False
        else:
            recording = True
            frames = []
            p = pyaudio.PyAudio()  # Create an interface to PortAudio
            stream = p.open(format=sample_format,
                            channels=1,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True,
                            stream_callback=recorder_callback)
            stream.start_stream()

            utils.clear_previous_console_line()
            print(colored(f'{config.USER_NAME}: ', "yellow") +
                  colored("### 🎙  RECORDING PRESS SPACE TO STOP ####", "red"))

    elif key == Key.enter:
        utils.clear_previous_console_line()
        print(colored(f'{config.USER_NAME}: ', "yellow") +
              colored(voice_input, "yellow"))
        return False
