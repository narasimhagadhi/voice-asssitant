import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import pystray
from PIL import Image, ImageDraw
import threading
import time

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("🗣️ You said:", command)
        return command.lower()
    except:
        print("❌ Could not understand.")
        return ""

def process_command(command):
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open mail" in command:
        speak("Opening mail")
        webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
    elif "open netflix" in command:
        speak("Opening netflix")
        webbrowser.open("https://www.netflix.com/in/login?nextpage=https%3A%2F%2Fwww.netflix.com%2Fbrowse")
    elif "play music" in command:
        speak("Playing music")
        os.system("start wmplayer")
    elif "good morning" in command:
        speak("good morning")
    elif "i love you" in command:
        speak("i love you too")
    elif "what is the time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")
    elif "stop assistant" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I didn’t understand that command.")
    return True

def run_assistant():
    print("🟢 Assistant is always listening. Say 'hello darling' to activate.")
    while True:
        command = listen_command()

        if "hello darling" in command:
            speak("How can I help you?")
            command = listen_command()
            if not process_command(command):
                break
        time.sleep(1)

def create_tray_icon():
    def on_quit(icon, item):
        print("🛑 stop assistant.")
        icon.stop()
        os._exit(0)

    image = Image.new('RGB', (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 54, 54), fill='green')

    icon = pystray.Icon("Assistant")
    icon.icon = image
    icon.menu = pystray.Menu(
        pystray.MenuItem("Quit", on_quit)
    )

    threading.Thread(target=run_assistant, daemon=True).start()
    icon.run()

create_tray_icon()
https