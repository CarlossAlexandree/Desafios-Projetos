import speech_recognition as sr

from virtual_assistant.stt.speech_to_text import SpeechToText


def test_transcribe_returns_lowercase_text(mocker):
    stt = SpeechToText(language="pt-BR")
    mocker.patch.object(stt.recognizer, "recognize_google", return_value="Ola Mundo")

    result = stt._transcribe(audio=mocker.Mock())

    assert result == "ola mundo"


def test_transcribe_returns_empty_on_unknown_value(mocker):
    stt = SpeechToText()
    mocker.patch.object(
        stt.recognizer, "recognize_google", side_effect=sr.UnknownValueError()
    )

    result = stt._transcribe(audio=mocker.Mock())

    assert result == ""
