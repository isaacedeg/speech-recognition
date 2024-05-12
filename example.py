import streamlit as st
import speech_recognition as sr

Language_configuration = {
    "English (United States)": "en-US",
    "English (United Kingdom)": "en-GB",
    "Spanish (Spain)": "es-ES",
    "Spanish (Mexico)": "es-MX",
    "French (France)": "fr-FR",
    "French (Canada)": "fr-CA",
    "German (Germany)": "de-DE",
    "Italian (Italy)": "it-IT",
    "Japanese (Japan)": "ja-JP",
    "Chinese (Simplified, China)": "zh-CN",
    "Chinese (Traditional, Taiwan)": "zh-TW",
    "Russian (Russia)": "ru-RU",
    "Portuguese (Brazil)": "pt-BR",
    "Portuguese (Portugal)": "pt-PT",
    "Dutch (Netherlands)": "nl-NL",
    "Arabic (Egypt)": "ar-EG",
    "Korean (South Korea)": "ko-KR",
    "Swedish (Sweden)": "sv-SE",
    "Turkish (Turkey)": "tr-TR",
    "Polish (Poland)": "pl-PL"
}
class SpeechRecognizer:
    def __init__(self, api='google', language='en-US'):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.api = api
        self.language = language
        self.pause = False

    def set_language(self, language):
        self.language = language

    def set_api(self, api):
        self.api = api
        
    def set_pause(self, pause):
        self.pause = pause

    def transcribe_speech(self, save_to_file=False):
        if self.api == 'google':
            recognizer_func = sr.Recognizer().recognize_google
        elif self.api == 'wit':
            recognizer_func = sr.Recognizer().recognize_wit
        elif self.api == 'ibm':
            recognizer_func = sr.Recognizer().recognize_ibm
        else:
            raise ValueError("Unsupported API. Supported APIs are: 'google', 'wit', 'ibm'.")

        with self.microphone as source:
            if not self.pause:
                st.info("Speak now...")
                
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                audio = self.recognizer.listen(source)
                st.info("Transcribing...")

            try:
                if not self.pause:
                    if save_to_file:
                        with open("transcript.txt", "a") as f:
                            f.write(recognizer_func(audio, key=None, language=self.language))
                            f.write("\n")
                            st.write("Transcript saved to transcript.txt")
                           
                            return recognizer_func(audio, key=None, language=self.language)
                    else:
                        return recognizer_func(audio, key=None, language=self.language)
                else:
                    st.info("Recognition paused.")
                    try:
                        recognizer_func(audio, key=None, language=self.language)
                    except UnboundLocalError:
                        pass
            except sr.UnknownValueError:
                st.error("Could not understand audio")
            except sr.RequestError as e:
                st.error("Error fetching results; {0}".format(e))

# Initialize Streamlit
st.title("Speech Recognition")

# Create an instance of SpeechRecognizer
recognizer = SpeechRecognizer()

# UI controls
api = st.selectbox("Select API", ['google', 'wit', 'ibm'])
language = st.selectbox('Language ', list(Language_configuration.keys()))
save_to_file = st.checkbox("Save to file", False)
pause_audio = st.checkbox("Pause", False)

language_code = Language_configuration.get(language)
# Update recognizer settings
recognizer.set_api(api)
recognizer.set_language(language_code)
recognizer.set_pause(pause_audio)

# Transcribe speech on button click
if st.button("Start Recording/Resume"):
    recognized_text = recognizer.transcribe_speech(save_to_file)
    if recognized_text != None:
        st.write("Transcription:", recognized_text)
