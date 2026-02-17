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

    # 1. 音声読み上げの確認
    is_speak = (
        input("音声読み上げを有効にしますか？ (y/n) [default: n]: ").lower() == "n"
    )

    # 2. ファイル指定の確認
    print(f"\nデータディレクトリ: {DATA_DIR}")
    files = list(DATA_DIR.glob("*.md"))

    if not files:
        print("ファイルが見つかりません。")
        return

    print("0: すべてのファイル (現状どおり)")
    for i, f in enumerate(files, 1):
        print(f"{i}: {f.name}")

    choice = input("\n読み込むファイルの番号を入力してください [default: 0]: ")

    if choice.isdigit() and 0 < int(choice) <= len(files):
        target_file = files[int(choice) - 1]
        words = load_words_from_file(target_file)
        print(f"--- '{target_file.name}' を読み込みました ---")
    else:
        words = load_all_words(DATA_DIR)
        print("--- すべてのファイルを読み込みました ---")

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
                if is_speak:
                    speak(word)
                else:
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
