import pyttsx3
import queue

import state


def run(tts_queue):

    print("[TTS] started")

    while state.running:

        try:

            text = tts_queue.get(timeout=0.1)

        except queue.Empty:

            continue

        try:

            state.tts_active = True

            print("TTS:", text)

            # NEW ENGINE EVERY TIME
            engine = pyttsx3.init()

            engine.setProperty("rate", 170)

            engine.say(text)

            engine.runAndWait()

            engine.stop()

            del engine

            print("[TTS] finished")

        except Exception as e:

            print("[TTS ERROR]", e)

        finally:

            state.tts_active = False

            print("[TTS] released")