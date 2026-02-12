import speech_recognition as sr
import webbrowser
import pyttsx3
import threading
from datetime import datetime

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Speak text using threading to avoid blocking issues"""
    print(text)
    engine.say(text)
    engine.runAndWait()

def speak_threaded(text):
    """Alternative threaded version if regular speak fails"""
    print(text)
    thread = threading.Thread(target=_speak_worker, args=(text,))
    thread.start()
    thread.join()

def _speak_worker(text):
    """Worker function for threaded speech"""
    temp_engine = pyttsx3.init()
    temp_engine.say(text)
    temp_engine.runAndWait()
    temp_engine.stop()

if __name__ == "__main__":
    speak("Initializing APEX.....")
    
    # Listen for the wake word "apex"
    while True:
        print("Understanding....")
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening for wake word...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            command = r.recognize_google(audio)
            print(f"Heard: {command}")
            
            if "apex" in command.lower():
                speak_threaded("On command Sir")
                
                # Now listen for the actual command
                while True:
                    try:
                        with sr.Microphone() as source:
                            speak_threaded("Listening for command...")
                            r.adjust_for_ambient_noise(source, duration=0.5)
                            audio = r.listen(source, timeout=5, phrase_time_limit=4)
                        user_command = r.recognize_google(audio)
                        print(f"Command: {user_command}")
                        
                        if user_command:
                            cmd_lower = user_command.lower()
                            
                            # Web commands
                            if "open youtube" in cmd_lower:
                                speak_threaded("Opening YouTube")
                                webbrowser.open("https://youtube.com")
                            elif "open google" in cmd_lower:
                                speak_threaded("Opening Google")
                                webbrowser.open("https://google.com")
                            elif "open claude" in cmd_lower:
                                speak_threaded("Opening Claude")
                                webbrowser.open("https://claude.ai/")
                            elif "open github" in cmd_lower:
                                speak_threaded("Opening GitHub")
                                webbrowser.open("https://github.com")
                            elif "open reddit" in cmd_lower:
                                speak_threaded("Opening Reddit")
                                webbrowser.open("https://reddit.com")
                            elif "open twitter" in cmd_lower or "open x" in cmd_lower:
                                speak_threaded("Opening Twitter")
                                webbrowser.open("https://twitter.com")
                            elif "open stack overflow" in cmd_lower:
                                speak_threaded("Opening Stack Overflow")
                                webbrowser.open("https://stackoverflow.com")
                            elif "i want to listen to music" in cmd_lower:
                                speak_threaded("Opening YouTube Music")
                                webbrowser.open("https://music.youtube.com/")
                            
                            # Personal interaction commands
                            elif "how r u" in cmd_lower or "how are you" in cmd_lower:
                                speak_threaded("I am good Aaadddiiitttya. How about you?")
                            elif "i am not fine" in cmd_lower:
                                speak_threaded("Ok sir Opening bot; you can share your thoughts")
                                webbrowser.open("https://chatgpt.com/")
                            elif "i am fine" in cmd_lower:
                                speak_threaded("Good to hear that;  waiting for your Command")
                            elif "do you know my sister" in cmd_lower:
                                speak_threaded("Yes Sir, I know your sister. Her name is Aaddiittii. She is very short tempered. And her exams are coming soon but she has not studied anything, hahahahahahahahaha")
                            
                            # Search commands
                            elif "search" in cmd_lower or "google" in cmd_lower:
                                query = cmd_lower.replace("search", "").replace("google", "").strip()
                                speak_threaded(f"Searching for {query}")
                                webbrowser.open(f"https://www.google.com/search?q={query}")
                            
                            # Time and date
                            elif "time" in cmd_lower:
                                now = datetime.now()
                                current_time = now.strftime("%I:%M %p")
                                speak_threaded(f"The time is {current_time}")
                            elif "date" in cmd_lower:
                                now = datetime.now()
                                current_date = now.strftime("%B %d, %Y")
                                speak_threaded(f"Today is {current_date}")
                            
                            # System commands
                            elif "stop" in cmd_lower or "exit" in cmd_lower or "quit" in cmd_lower:
                                speak_threaded("Goodbye Sir")
                                exit()
                            elif "sleep" in cmd_lower or "standby" in cmd_lower:
                                speak_threaded("Going to standby mode")
                                break  # Return to wake word listening
                            
                            else:
                                speak_threaded("No data for Command: " + user_command)
                            
                    except sr.WaitTimeoutError:
                        print("Listening timeout")
                        continue
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                        continue
                    except Exception as e:
                        print(f"Command Error: {e}")
                        continue
                        
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except Exception as e:
            print("Error: {0}".format(e))