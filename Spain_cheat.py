import PySimpleGUI as sg
import soundcard
import soundfile
import speech_recognition as sr
from deep_translator import GoogleTranslator
import sys
import os

rate = 48000


def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)



file_voice = "test.wav"


lang = ['Japanese', 'English', 'Spanish', 'French']

col1 = [[sg.Text('元の言語を選択', font=("Arial",20))],
          [sg.Listbox(lang, size=(20, 4),font=("Arial",15))]]

col2 = [[sg.Text('翻訳先の言語を選択',font=("Arial",20))],
        [sg.Listbox(lang, size=(20, 4),font=("Arial",15))]
        ]

col3 = [[sg.Text('録音時間(sec)',font=("Arial",20))],
        [sg.Input("5", size=(8, 4),font=("Arial",15))]
        ]

layout = [
    [sg.Column(col1),sg.Column(col2),sg.Column(col3)],
    [sg.OK("決定",font=("Arial",15)),sg.Text("Online language cheat tool. Developed by rize",font=(15),background_color= "#afeeee",text_color="#111111")],
    [sg.Text('', key='-ACT1-',font=(20),background_color = '#000000')],
    [sg.Text('', key='-ACT2-',font=(15),background_color = '#000000')],
    [sg.Text('', key='-ACT3-',font=(20),background_color = '#000000')],
    [sg.Text('', key='-ACT4-',font=(15),background_color = '#000000')],
    [sg.Image(filename=resource_path("47398183.gif"),background_color = '#afeeee')]
    
]


window = sg.Window('Spanish_cheat', layout, size=(800,500),background_color='#afeeee')

event, values = window.read()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '終了':
        break
        
    
    if event == "決定":
        
        def judge(values):
            if "Spanish" in values[0]:
                return ("es-ES","es")
            
            if "Japanese" in values[0]:
                return ("ja-JP","ja")
            
            if "French" in values[0]:
                return ("fr-FR","fr")
            
            if "English" in values[0]:
                return ("en-US","en")
            
        def judge2(values):
            if "Spanish" in values[1]:
                return ("es")
            
            if "Japanese" in values[1]:
                return ("ja")
            
            if "French" in values[1]:
                return ("fr")
            
            if "English" in values[1]:
                return ("en")
            
        #print(judge(values))
        
        
        record_time = int(values[2])
        
        with soundcard.get_microphone(id=str(soundcard.default_speaker().name), include_loopback=True).recorder(samplerate=rate) as voice:
            #print("録音を開始")
            
            data = voice.record(numframes=rate*record_time)
            
            soundfile.write(file=resource_path(file_voice), data=data[:, 0], samplerate=rate) #a
            
        r = sr.Recognizer()
 
        with sr.AudioFile(resource_path(file_voice)) as source: #a
            audio = r.record(source)
            
        
        text = r.recognize_google(audio, language=judge(values)[0])
        translate = GoogleTranslator(source=judge(values)[1],target=judge2(values)).translate(text)
        
        window['-ACT1-'].update("↓原文内容↓")
        window['-ACT2-'].update(text)
        window['-ACT3-'].update("↓翻訳結果↓")
        window['-ACT4-'].update(translate)
        
        
        

        
window.close()

