import speech_recognition as sr
import webbrowser
import pyttsx3
import threading

recognizer = sr.Recognizer()


def speak(text):
    """Speak text using threading to avoid engine conflicts"""
    print(text)

    def worker():
        try:
            engine = pyttsx3.init()  # Fresh engine each time
            engine.say(text)
            engine.runAndWait()
            engine.stop()  # Clean shutdown
        except Exception as e:
            print("Speech Error: {}".format(e))

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()  # Wait for speech to complete


if __name__ == "__main__":
    speak("Initializing APEX.....")

    # Listen for the wake word "Orbit"
    while True:
        print("Understanding....")
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            command = r.recognize_google(audio)
            print(command)

            if "apex" in command.lower():
                speak("On command Sir")

                # Now listen for the actual command
                while True:
                    try:
                        with sr.Microphone() as source:
                            speak("Listening for command...")
                            audio = r.listen(source, timeout=5, phrase_time_limit=4)
                        user_command = r.recognize_google(audio)
                        print(f"Command: {user_command}")

                        # Check if user_command is valid before using .lower()
                        if user_command:
                            command_lower = user_command.lower()

                            if "open youtube" in command_lower:
                                speak("Opening YouTube")
                                webbrowser.open("https://youtube.com")

                            elif "open google" in command_lower:
                                speak("Opening Google")
                                webbrowser.open("https://google.com")

                            elif (
                                "how r u" in command_lower
                                or "how are you" in command_lower
                            ):
                                speak("I am good Sir. How about you?")

                            elif "i am not fine" in command_lower:
                                speak("Ok sir Opening bot; you can share your thoughts")
                                webbrowser.open("https://chatgpt.com/")

                            elif "i am fine" in command_lower:
                                speak("Good to hear that;  waiting for your Command")

                            elif "do you know my sister" in command_lower:
                                speak(
                                    "Yes Sir, I know your sister. She is very short tempered. And her exams are coming soon but she has not studied anything, hahahahahahahahaha"
                                )

                            elif "open cloud" in command_lower:
                                speak("Opening Claude")
                                webbrowser.open("https://claude.ai/")

                            elif "i want to listen to music" in command_lower:
                                speak("Opening youtube Music")
                                webbrowser.open("https://music.youtube.com/")
                            elif "open stack overflow" in command_lower:
                                speak("Opening Stack Overflow")
                                webbrowser.open("https://stackoverflow.com")
                            elif "open github" in command_lower:
                                speak("Opening GitHub")
                                webbrowser.open("https://github.com/AD1TYA-A1")
                            elif "open reddit" in command_lower:
                                speak("Opening Reddit")
                                webbrowser.open("https://reddit.com")
                            elif "open twitter" in command_lower or "open x" in command_lower:
                                speak("Opening Twitter")
                                webbrowser.open("https://twitter.com")

                            elif "stop" in command_lower:
                                speak("Goodbye Sir")
                                exit()

                            else:
                                speak("No data for Command : " + user_command)

                    except Exception as e:
                        print(f"Command Error: {e}")
                        continue

        except Exception as e:
            print("Error: {0}".format(e))
