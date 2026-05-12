import sounddevice as sd
import sherpa_onnx
import numpy as np

import state

SAMPLE_RATE = 16000

deviceno = 1

recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
    tokens="models/tokens.txt",

    encoder="models/encoder-epoch-99-avg-1.int8.onnx",

    decoder="models/decoder-epoch-99-avg-1.onnx",

    joiner="models/joiner-epoch-99-avg-1.int8.onnx",

    num_threads=1,

    sample_rate=SAMPLE_RATE,

    feature_dim=80,

    enable_endpoint_detection=True,
)

stream = recognizer.create_stream()

last_result = ""


def run(transcript_queue):

    global last_result

    print("[LISTENER] started")

    with sd.InputStream(
        device=deviceno,
        channels=1,
        samplerate=SAMPLE_RATE,
        dtype="float32",
        blocksize=3200,
    ) as audio_stream:

        while state.running:

            try:

                samples, overflowed = audio_stream.read(1600)

                samples = samples.reshape(-1)

                stream.accept_waveform(
                    SAMPLE_RATE,
                    samples
                )

                while recognizer.is_ready(stream):

                    recognizer.decode_stream(stream)

                result = recognizer.get_result(stream).strip().lower()

                if result:

                    last_result = result

                if recognizer.is_endpoint(stream):

                    final_text = last_result.strip()

                    recognizer.reset(stream)

                    last_result = ""

                    if not final_text:

                        continue

                    # ignore assistant speech
                    if state.tts_active:

                        print("[LISTENER] ignored due to TTS")

                        continue

                    print("FINAL:", final_text)

                    transcript_queue.put(final_text)

            except Exception as e:

                print("[LISTENER ERROR]", e)