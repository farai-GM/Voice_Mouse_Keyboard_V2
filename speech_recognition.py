import json
import queue
import sys
import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel

SetLogLevel(-1)
MODEL_PATH = "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
INSTANT_COMMANDS = {"click", "double click", "right click", "scroll up", "scroll down", "stop","close","up", "down", "left", "right","enter", "backspace", "shift","ctrl","alt","delete", "tab"}

INSTANT_COMMANDS = sorted(INSTANT_COMMANDS, key=len, reverse=True)


q = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(in_data))

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)



def speech_to_text(command_callback):

    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=512,
            dtype='int16',
            channels=1,
            callback=audio_callback,
        ):
            print("listening...")
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    # Standard final result for longer dictated phrases
                    result = json.loads(recognizer.Result())

                    if result["text"]:
                        command_callback(result["text"])
                        print("Dictated:", result["text"])
                else:
                    # Check partial text every 50ms for instant commands
                    partial = json.loads(recognizer.PartialResult()).get("partial", "")
                    if partial:
                        print("Partial:", partial, end="\r")

                        # Trigger immediately if a known command is spoken
                        for cmd in INSTANT_COMMANDS:
                            if cmd in partial:
                                print(" " * 80, end="\r")
                                print(f"Triggered: {cmd}")
                                command_callback(cmd)
                                # Clear the recognizer buffer so it doesn't fire twice
                                recognizer.Reset()
                                break

    except KeyboardInterrupt:
        print("\n Stopping ...")


