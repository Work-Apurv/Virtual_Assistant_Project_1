# --- 1. GATHERING YOUR TOOLS ---
import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary  # Your music "database"
import os            # For opening local music files
import datetime      # For the time skill
import wikipedia     # For the Wikipedia skill
import requests      # <-- 1. IMPORT THE REQUESTS LIBRARY
import json          # <-- 2. IMPORT JSON TO READ THE API DATA

# --- 2. ONE-TIME SETUP ---
engine = pyttsx3.init()
# ... (speak function is the same) ...
# --- 3. DEFINING YOUR SKILLS (FUNCTIONS) ---

def speak(text):
    """This function takes text and speaks it out loud."""
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listens for a command and returns it as text."""
    # ... (listen_for_command function is the same) ...
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source) 
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except sr.UnknownValueError:
        speak("Sorry, I did not understand that. Please try again.")
        return "None"
    except sr.RequestError as e:
        speak(f"Could not request results; check your internet connection. Error: {e}")
        return "None"
        
    return query.lower() # Return the command in lowercase

# --- 4. THE MAIN PROGRAM (THE "STARTING BELL") ---
if __name__ == '__main__':
    speak("Jarvis is online and at your service.")
    while True:
        # 1. Get the command from the user.
        command = listen_for_command()

        # 2. If listening failed, just loop again.
        if command == "none":
            continue

        # --- 3. THE "BRAIN": CHECKING THE COMMAND ---
        if 'exit' in command or 'goodbye' in command:
            speak("Goodbye, sir.")
            break 

        elif "open google" in command:
            speak("Opening Google, sir.")
            
        elif "open facebook" in command:
            speak("Opening Facebook.")

        elif "open linkedin" in command:
            speak("Opening LinkedIn.")
            
        elif "open youtube" in command:
            speak("Opening YouTube.")
        
        # ---!!! THIS IS YOUR NEW, CORRECTED "NEWS" CODE !!!---
        # We check for the word "news" in the 'command' variable
        elif 'news' in command:
            
            # --- 3. This is the new URL you provided ---
            # It gets top headlines from the US using your API key
            url = "https://newsapi.org/v2/top-headlines?country=us&apikey="

            # --- 4. HANDLE THE API REQUEST ---
            # We can go directly to the 'try' block since the key is in the URL
            try:
                # 'requests.get(url)' fetches the data from the internet
                response = requests.get(url)
                # 'response.json()' converts the raw data into a Python dictionary
                news_data = response.json()
                
                # --- 5. READ THE NEWS ---
                # Check if the API request was successful
                if news_data["status"] == "ok" and news_data["totalResults"] > 0:
                    speak("Here are the top headlines from the US...")
                    # 'articles' is a list of news items. Let's read the top 3.
                    articles = news_data["articles"]
                    for article in articles[:3]: # Read the first 3 articles
                        headline = article["title"]
                        print(headline)
                        speak(headline)
                    speak("That's all for now.")
                else:
                    speak("Sorry, I couldn't fetch the news at this time.")
            
            except Exception as e:
                print(f"Error fetching news: {e}")
                speak("Sorry, I ran into an error while trying to fetch the news.")
        # ---!!! ---------------------------------- !!!---

        elif 'time' in command:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {strTime}")

        elif 'wikipedia' in command:
            speak('Searching Wikipedia...')
            command = command.replace("wikipedia", "")
            results = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'play' in command:
            song_name = command.replace("play", "").strip()
            
            if song_name in musiclibrary.songs:
                song_path = musiclibrary.songs[song_name]
                speak(f"Playing {song_name}")
                os.startfile(song_path)
            else:
                speak(f"Sorry, I don't have the song {song_name} in my library.")

        else:
            speak(f"Sorry, I don't have a skill for the command: {command}")