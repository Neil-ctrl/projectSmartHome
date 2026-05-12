import threading
import queue
import time

import listener
import scanner
import tts
import llm
import control
import state

COMMAND_MAP = {
    "lights on": "ON",
    "lights off": "OFF"
}

transcript_queue = queue.Queue()

command_queue = queue.Queue()

tts_queue = queue.Queue()

control.connect()

listener_thread = threading.Thread(
    target=listener.run,
    args=(transcript_queue,),
    daemon=True
)

scanner_thread = threading.Thread(
    target=scanner.run,
    args=(transcript_queue, command_queue),
    daemon=True
)

tts_thread = threading.Thread(
    target=tts.run,
    args=(tts_queue,),
    daemon=True
)

listener_thread.start()

scanner_thread.start()

tts_thread.start()

print("[MAIN] system running")

try:

    while True:

        try:

            text = command_queue.get(timeout=0.1)

        except queue.Empty:

            continue

        print("[MAIN] processing:", text)

        try:

            speech, commands = llm.process(text)

        except Exception as e:

            print("[LLM ERROR]", e)

            continue

        print("[MAIN] speech:", speech)
        print("[MAIN] commands:", commands)

        if speech:

            tts_queue.put(speech)

        for command in commands:

            if command == "NOP":

                print("[MAIN] NOP")

                continue

            if command in COMMAND_MAP:

                esp_command = COMMAND_MAP[command]

                print("[MAIN] sending:", esp_command)

                try:

                    control.send_command(esp_command)

                    time.sleep(0.5)

                except Exception as e:

                    print("[CONTROL ERROR]", e)

            else:

                print("[MAIN] invalid command:", command)

except KeyboardInterrupt:

    print("[MAIN] shutting down")

    state.running = False