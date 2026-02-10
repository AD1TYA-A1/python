import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
# Initialize engine ONCE globally
engine = pyttsx3.init()

def speak(text):
    """Speak text using the global engine instance"""
    print(text)
    engine.say(text)
    engine.runAndWait()
    # DON'T call engine.stop() here!

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
                            if "open youtube" in user_command.lower():
                                speak("Opening YouTube")
                                webbrowser.open("https://youtube.com")
                            elif "open google" in user_command.lower():
                                speak("Opening Google")
                                webbrowser.open("https://google.com")
                            elif "stop" in user_command.lower():
                                speak("Goodbye")
                                exit()
                            else:
                                speak("Command received: " + user_command)
                            
                    except Exception as e:
                        print(f"Command Error: {e}")
                        continue
                        
        except Exception as e:
            print("Error: {0}".format(e))