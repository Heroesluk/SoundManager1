import random

import speech_recognition as sr
from playsound import playsound, PlaysoundException
from speech_recognition import UnknownValueError


class HintMatcher():

    def __init__(self, hints):
        self.hints = hints
        self.no_hint = "09_out_of_hints_intel.wav"
        self.incorrect_request = "02_speak_more_clearly.wav"

    def match(self, data):
        for hint in self.hints:
            for phrase in hint.keywords:
                if phrase.lower() in data.lower():
                    return hint.hint_path

            return self.incorrect_request

        return self.no_hint


class Hint():
    def __init__(self, keywords=None, hint=None):
        self.keywords = keywords
        self.hint_path = hint


def play_hint(filename):
    playsound("Renders/{}".format(filename))


def call_microphone():
    recognizer = sr.Recognizer()

    mic = sr.Microphone()
    with mic as source:
        # wait 1 second before providing sound input
        print("Wait, dont say anything microphone is adjusting noise levels ")
        recognizer.adjust_for_ambient_noise(source)
        print("Now say what you need, i.e 'give me a hint'  ")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=6)

    return recognizer.recognize_google(audio, language="pl-PL")


def activator():
    while True:
        try:
            siri = call_microphone()
            if "hello siri" in siri:
                return True
        except (UnknownValueError or PlaysoundException) as e:
            continue


testdata = [{'tip_body': 'date', 'tip_call': '04_hint_forensics'}, {'tip_body': 'lock', 'tip_call': '05_hint_date'}]


def parser(data):
    tips = []

    for tip in data:
        test = tip["tip_body"].replace(" ", "_")
        tips.append(Hint(tip["tip_call"], test + ".wav"))


def game(data_json):
    matcher = HintMatcher(parser(testdata))
    while True:
        if activator():
            try:
                text = call_microphone()
            except (UnknownValueError or PlaysoundException) as e:
                print("Couldn't recognize what you said")
                play_hint("Renders/02_speak_more_clearly.wav")
                continue

            hint_path = matcher.match(text)
            play_hint(hint_path)


game()
