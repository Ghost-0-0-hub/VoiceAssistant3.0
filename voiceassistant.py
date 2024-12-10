import time
import random
import speech_recognition as sr
import pyaudio
from datetime import datetime
import pyttsx3
import os
import webbrowser
from customtkinter import *
import cv2
import mediapipe as mp
import pyautogui
from PIL import Image

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    for voice in voices:
        if 'Zira' in voice.name:
            engine.setProperty('voice', voice.id)
            break
    else:
        engine.setProperty('voice',voice[0].id)

    engine.setProperty('rate',150)
    engine.setProperty('volume',1)

    engine.say(text)
    engine.runAndWait()

def listen_for_audio():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=1)
        print('Listening...')
        speak('Listening')
        audio = listener.listen(source)
    
    try:
        return listener.recognize_google(audio).lower()
    except sr.UnknownValueError:
        voice_lines = [
            "sorry, could you try again please?",
            "say that again please?",
            "I didn't quite catch that?"
            ]
        voices = random.choice(voice_lines)
        print(voices)
        speak(voices)
        return None
    except sr.RequestError:
        print('API is unavailable')
        return None

def web_searching():
    while True:
        s_prompts = [
            "what makes you curious today?",
            "what do you want to search?",
            "what are you looking for?",
            "ready when you are?",
            "I'm ready when you are",
        ]
        search_prompt = random.choice(s_prompts)
        print(search_prompt)
        speak(search_prompt)
        query = listen_for_audio()

        if query is None:
            voice_lines = [
                "sorry, could you try again please?",
                "say that again please?",
                "I didn't quite catch that?"
            ]
            voices = random.choice(voice_lines)
            print(voices)
            continue
        query = query.strip()
        if 'stop' in query.lower():
            print('Exiting Search...')
            speak('Exiting Search')
            break
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        print(f"Searching for: {query}")

def media_play():
    Tabs = {
    'netflix': "https://www.netflix.com/browse",
    'youtube': "https://www.youtube.com/",
    }

    while True:
        speak('What would you like Netflix or Youtube?')
        choice = listen_for_audio().lower()
        
        if choice:
            if choice == 'stop':
                print('Exiting Task Opener...')
                speak('Exiting Task Opener')
                break

            elif choice in Tabs:
                webbrowser.open(Tabs[choice])
                time.sleep(1)
                if choice == 'netflix' or choice == 'youtube':
                    speak('gesture control is starting')
                    mp_hand = mp.solutions.hands
                    hands = mp_hand.Hands()

                    def pause_gesture(hand_landmarks):
                    
                        index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
                        index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

                        thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]

                        middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
                        middle_dip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_DIP]

                        ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
                        ring_dip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_DIP]

                        pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]
                        pinky_dip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_DIP]

                        index_down = index_dip.y < index_tip.y
                        thumb_down = thumb_tip.y < index_tip.y
                        middle_down = middle_dip.y < middle_tip.y
                        ring_down = ring_dip.y < ring_tip.y
                        pinky_down = pinky_dip.y < pinky_tip.y

                        return index_down and thumb_down and middle_down and ring_down and pinky_down

                    def vol_down(hand_landmarks):
                    
                        index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
                        index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

                        thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]

                        middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]

                        ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]

                        pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]


                        index_extend = index_tip.y < index_dip.y
                        thumb_extend = thumb_tip.y < index_dip.y
                        ring_down =  ring_tip.y > index_dip.y
                        middle_down = middle_tip.y > index_dip.y
                        pinky_down = pinky_tip.y > index_dip.y

                        return index_extend and thumb_extend and ring_down and middle_down and pinky_down

                    def vol_up(hand_landmarks):

                        index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
                        index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

                        thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]

                        middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]

                        ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]

                        pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]

                        index_extend = index_tip.y < index_dip.y
                        middle_extend = middle_tip.y < index_dip.y
                        ring_down = ring_tip.y > index_dip.y
                        pinky_down = pinky_tip.y > index_dip.y

                        return index_extend and middle_extend and ring_down and pinky_down

                    def forward(hand_landmarks):
                        index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
                        index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

                        middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
                        middle_dip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_DIP]

                        ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
                        ring_dip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_DIP]

                        pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]
                        pinky_dip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_DIP]

                        thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]

                        index_down = index_tip.y > index_dip.y
                        middle_down = middle_tip.y > middle_dip.y
                        ring_down = ring_tip.y > ring_dip.y
                        pinky_extend = pinky_tip.y < pinky_dip.y 
                        thumb_extend = thumb_tip.y < index_dip.y   

                        return index_down and middle_down and ring_down and pinky_extend and thumb_extend

                    def backwards(hand_landmarks):

                        index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
                        index_dip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_DIP]

                        middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
                        middle_dip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_DIP]

                        ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
                        ring_dip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_DIP]

                        pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]
                        pinky_dip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_DIP]

                        thumb_tip = hand_landmarks.landmark[mp_hand.HandLandmark.THUMB_TIP]

                        index_extend = index_tip.y < index_dip.y 
                        middle_extend = middle_tip.y < middle_dip.y
                        ring_extend = ring_tip.y < ring_dip.y
                        pinky_extend = pinky_tip.y < pinky_dip.y
                        thumb_down = thumb_tip.y > index_dip.y 

                        return index_extend and middle_extend and ring_extend and pinky_extend and thumb_down
                    mp_draw = mp.solutions.drawing_utils
                    cap = cv2.VideoCapture(0)

                    while True:
                        Success, img = cap.read()
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        result = hands.process(img_rgb)

                        if result.multi_hand_landmarks:
                            for hand_landmarks in result.multi_hand_landmarks:
                                if pause_gesture(hand_landmarks):
                                    pyautogui.press('space')
                                    time.sleep(0.6)
                                elif vol_down(hand_landmarks):
                                    pyautogui.press('down')
                                    time.sleep(0.2)
                                elif vol_up(hand_landmarks):
                                    pyautogui.press('up')
                                    time.sleep(0.2)
                                elif forward(hand_landmarks):
                                    pyautogui.press('right')
                                    time.sleep(0.1)
                                elif backwards(hand_landmarks):
                                    pyautogui.press('left')
                                    time.sleep(0.1)
                                mp_draw.draw_landmarks(img, hand_landmarks, mp_hand.HAND_CONNECTIONS)

                        cv2.imshow('Hand Tracker', img)
                        if cv2.waitKey(5) & 0XFF == 27:
                            break
                        
                    cap.release()
                    cv2.destroyAllWindows()
        else:
            print('Sorry I could not find that')
            speak('Sorry I could not find that')
        
def time_telling():
    def update_time():
        today = datetime.now()  
        date = today.strftime("%B %d, %Y")  
        day = today.strftime("%A")
        current_time = today.strftime('%I:%M %p') 
        app.after(1000, update_time)
        print(f'Today is {date} on a lovely {day}, and the current time is {current_time}')
        speak(f'Today is {date} on a lovely {day}, and the current time is {current_time}')
         

    update_time()

def help():
    print('''
I'm zoey, your Voice assistant, I'm here to automate your tasks and make your life easier with my assistance.
I can give you the status report of the day, play music, and perform small tasks like file opening and taking screenshots.
I also contain a Gesture Based Media Control system to automate your entertainment system.
whenever you need me, just speak when I say Listening''')
    speak('''
I'm zoey, your Voice assistant, I'm here to automate your tasks and make your life easier with my assistance.
I can give you the status report of the day, play music, and perform small tasks like file opening and taking screenshots.
 I also contain a Gesture Based Media Control system to automate your entertainment.
whenever you need me, just speak when I say Listening.''')
def music():    
    print('Playing Music..')
    speak('Playing Music')
    music = "https://open.spotify.com/playlist/3jH94SWDEDUGNrWwlGooyo"
    webbrowser.open(music)

def screenshot():
    speak('Taking a screenshot')
    pyautogui.hotkey('win','Shift','s')
    pyautogui.click(980,30, duration=1)
    pyautogui.click(980,100, duration=1)

def calculate():
    print('Opening Calculator..')
    speak('Opening Calculator')
    os.system('calc')

def weather():
    webbrowser.open('https://www.google.com/search?q=todays+weather&oq=todays+weather&gs_lcrp=EgZjaHJvbWUqDwgAEAAYRhiAAhixAxiABDIPCAAQABhGGIACGLEDGIAEMgcIARAAGIAEMgcIAhAAGIAEMgcIAxAAGIAEMgcIBBAAGIAEMgcIBRAAGIAEMgYIBhBFGDwyBggHEEUYPdIBCDMyNzZqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8&dlnr=1&ved=2ahUKEwjspcqcmJKKAxVi_rsIHbUnO4YQl6ENegQIChAG')

def tts():
    while True:
        print('What is your message?')
        speak('What is your message?')
    
        msg = listen_for_audio()
        if msg:
            pyautogui.write(msg)
            pyautogui.press('enter')
        elif msg == 'stop':
            speak('okay! Exiting Text To Speech')
            break

def main_assistant():
    print(f'Awake and at your service, what can I do for you?')
    speak(f'Awake and at your service, what can I do for you?')
    while True:
        task = listen_for_audio()
        
        if task:
            if 'search' in task:
                speak('on it')
                web_searching()
            elif 'media' in task:
                speak('sure')
                media_play()
            elif 'status' in task:
                speak('right away')
                time_telling()
            elif 'message' in task:
                speak('very well!')
                pyautogui.click(1175, 1060, duration=0.5)
                tts()
            elif 'file' in task:
                speak('Opening Your Files')
                pyautogui.click(960,1050,duration=0.5)
            elif 'weather' in task:
                speak('alright')
                weather()
            elif 'screenshot' in task:
                speak('alright')
                screenshot()
            elif "yourself" in task:
                speak('very well')
                help()
            elif 'music' in task:
                speak('okay boss')
                music()
            elif 'calculator' in  task:
                speak('precisely')
                calculate()
            elif 'stop' in task:
                print("Alright, Let me know if you need anything else.")
                speak("Alright, Let me know if you need anything else")
                break
        else:
            print("I didn't understand that command.")

app = CTk()
app.geometry('300x300')

set_appearance_mode('light')

mic_img = CTkImage(
    light_image = Image.open("D:\icons8-microphone-100.png"),
    size=(100,100)
)

btn = CTkButton(
    master=app,
    width=200,
    height=200,
    corner_radius=50,
    fg_color='#63C5DA',
    text='',
    hover_color='white',
    image=mic_img,
    command=main_assistant
)
btn.place(relx=0.5,rely=0.5,anchor='center')

app.mainloop()