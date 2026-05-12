import queue
import state

WAKE_WORDS = {
    "shack",
    "shhacc",
    "shaq",
    "shock",
    "shak",
    "shac",
    "jacques"
}


def run(transcript_queue, command_queue):

    print("[SCANNER] started")

    while state.running:

        try:

            text = transcript_queue.get(timeout=0.1)

        except queue.Empty:

            continue

        text = text.lower().strip()

        print("[SCANNER] heard:", text)

        words = text.split()

        wake_index = -1

        for i, word in enumerate(words):

            if word in WAKE_WORDS:

                wake_index = i

        if wake_index == -1:

            print("[SCANNER] no wake word")

            continue

        command_text = " ".join(words[wake_index + 1:]).strip()

        if not command_text:

            print("[SCANNER] wake word only")

            continue

        print("[SCANNER] command:", command_text)

        command_queue.put(command_text)