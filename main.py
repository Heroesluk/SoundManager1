import random

import speech_recognition as sr
from playsound import playsound, PlaysoundException
from speech_recognition import UnknownValueError, WaitTimeoutError


class HintMatcher():

    def __init__(self, hints):
        self.hints = hints
        self.no_hint = "09_out_of_hints_intel.wav"
        self.incorrect_request = "02_speak_more_clearly.wav"

    def match(self, data):
        for hint in self.hints:
            if hint.keywords.lower() in data.lower():
                return hint.hint_path

        return self.incorrect_request

        return self.no_hint


class Hint():
    def __init__(self, keywords=None, hint=None):
        self.keywords = keywords
        self.hint_path = hint


def play_hint(filename):
    playsound(filename)


def call_microphone():
    recognizer = sr.Recognizer()

    mic = sr.Microphone()
    with mic as source:
        # wait 1 second before providing sound input
        print("Wait, dont say anything microphone is adjusting noise levels ")
        recognizer.adjust_for_ambient_noise(source)
        print("now say")
        # print("Now say what you need, i.e 'give me a hint'  ")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=6)

    return recognizer.recognize_google(audio)


def activator():
    print("dziala")
    while True:
        try:
            siri = call_microphone()
            if "hello" in siri:
                print(siri, "chuj")
                return True
        except (UnknownValueError, PlaysoundException, TimeoutError) as e:
            pass


testdata = [{'tip_body': 'date', 'tip_call': '04_hint_forensics'}, {'tip_body': 'lock', 'tip_call': '05_hint_date'}]


def parser(data):
    tips = []

    for tip in data:
        print(tip)
        test = tip["tip_body"].replace(" ", "_")
        tips.append(Hint(tip["tip_call"], test + ".wav"))

    return tips


def game(data_json):
    matcher = HintMatcher(parser(data_json))
    while True:
        activator()
        print("Activiated, now after signal say hint")

        while True:
            try:
                print("Activiated, now after signal say hint")

                hint_path = ""
                text = call_microphone()
                print(text)

                hint_path = matcher.match(text)
                play_hint("Renders/" + hint_path)
            except (UnknownValueError, PlaysoundException, WaitTimeoutError) as e:
                print("Couldn't recognize what you said")
                play_hint("Renders/02_speak_more_clearly.wav")
                continue


