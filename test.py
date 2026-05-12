import speech_recognition as sr

for i, name in enumerate(sr.Microphone.list_microphone_names()):

    # ignore garbage devices
    if any(x in name.lower() for x in [
        "bluetooth",
        "stereo",
        "mapper",
        "output",
        "headset",
        "hands-free",
        "oneplus"
    ]):
        continue

    print(i, name)