import pytest

from virtual_assistant.tts.text_to_speech import TextToSpeech, TextToSpeechError


def test_synthesize_raises_on_empty_text():
    tts = TextToSpeech()
    with pytest.raises(TextToSpeechError):
        tts.synthesize("")


def test_synthesize_creates_audio_file(mocker):
    mock_gtts = mocker.patch("virtual_assistant.tts.text_to_speech.gTTS")
    tts = TextToSpeech(language="pt")

    result = tts.synthesize("Olá mundo")

    mock_gtts.assert_called_once_with(text="Olá mundo", lang="pt", slow=False)
    mock_gtts.return_value.save.assert_called_once()
    assert result.suffix == ".mp3"


def test_speak_plays_and_cleans_up(mocker):
    mocker.patch("virtual_assistant.tts.text_to_speech.gTTS")
    mock_playsound = mocker.patch("virtual_assistant.tts.text_to_speech.playsound")
    mock_remove = mocker.patch("virtual_assistant.tts.text_to_speech.os.remove")

    tts = TextToSpeech()
    tts.speak("Teste")

    mock_playsound.assert_called_once()
    mock_remove.assert_called_once()
