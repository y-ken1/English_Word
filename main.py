import random
import re
import os
import time
from pathlib import Path


DATA_DIR = Path(r"data")  # ← フォルダ名


def speak(word):
    cmd = (
        f'powershell -Command "Add-Type –AssemblyName System.Speech;'
        f"$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        f'$voice = $speak.GetInstalledVoices() | Where-Object {{$_.VoiceInfo.Culture.Name -eq \\"en-US\\"}} | Select-Object -First 1;'
        f"if ($voice) {{ $speak.SelectVoice($voice.VoiceInfo.Name) }};"
        f"$speak.Speak('{word}');\""
    )
    os.system(cmd)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def load_words_from_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    entries = []
    blocks = re.split(r"\n###\s+", text)

    for block in blocks[1:]:
        lines = block.strip().splitlines()
        word = lines[0].strip()

        meanings = [
            line[2:].strip() for line in lines[1:] if line.strip().startswith("- ")
        ]

        if meanings:
            entries.append((word, meanings))

    return entries


def load_all_words(directory):
    words = []

    for md_file in directory.glob("*.md"):
        words.extend(load_words_from_file(md_file))

    return words


def main():
    words = load_all_words(DATA_DIR)

    if not words:
        print("単語が見つかりません")
        return

    try:
        while True:
            word, meanings = random.choice(words)

            for i in range(1):
                # clear()
                print(f"\n")
                print(f"\033[97m▶ {word}\033[0m")

                # 読み上げる
                # speak(word)

                time.sleep(0.8)

                # clear()
                # print(f"▶ {word}")
                for m in meanings:
                    print(f"\033[90m  {m}\033[0m")

                time.sleep(1)
    except KeyboardInterrupt:
        clear()
        print("終了しました")


if __name__ == "__main__":
    main()
