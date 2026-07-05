from virtual_assistant.commands.pharmacy_locator import PharmacyLocatorCommand
from virtual_assistant.commands.router import CommandRouter
from virtual_assistant.commands.wikipedia_search import WikipediaSearchCommand


class DummyCommand:
    def __init__(self, trigger_word: str):
        self.trigger_word = trigger_word
        self.executed_with = None

    def matches(self, text: str) -> bool:
        return self.trigger_word in text

    def execute(self, text: str) -> None:
        self.executed_with = text


def test_router_dispatches_to_first_matching_command():
    cmd_a = DummyCommand("alpha")
    cmd_b = DummyCommand("beta")
    router = CommandRouter(commands=[cmd_a, cmd_b], tts=None)

    handled = router.route("execute beta please")

    assert handled is True
    assert cmd_b.executed_with == "execute beta please"
    assert cmd_a.executed_with is None


def test_router_returns_false_when_no_command_matches():
    router = CommandRouter(commands=[DummyCommand("alpha")], tts=None)

    handled = router.route("comando desconhecido")

    assert handled is False


def test_wikipedia_command_matches_trigger_words(mocker):
    cmd = WikipediaSearchCommand(tts=mocker.Mock(), stt=mocker.Mock())
    assert cmd.matches("quero pesquisar sobre python")
    assert not cmd.matches("abrir youtube")


def test_pharmacy_locator_picks_nearest_by_distance(mocker):
    tts = mocker.Mock()
    command = PharmacyLocatorCommand(tts=tts)

    mocker.patch.object(command, "_get_current_location", return_value=(0.0, 0.0))
    mocker.patch("virtual_assistant.commands.pharmacy_locator.webbrowser")

    fake_pharmacies_response = mocker.Mock()
    fake_pharmacies_response.json.return_value = {
        "elements": [
            {"lat": 0.01, "lon": 0.01, "tags": {"name": "Farmácia Longe"}},
            {"lat": 0.001, "lon": 0.001, "tags": {"name": "Farmácia Perto"}},
        ]
    }
    fake_pharmacies_response.raise_for_status = mocker.Mock()
    mocker.patch(
        "virtual_assistant.commands.pharmacy_locator.requests.post",
        return_value=fake_pharmacies_response,
    )

    command.execute("onde fica a farmácia mais próxima")

    tts.speak.assert_called_once()
    spoken_text = tts.speak.call_args[0][0]
    assert "Farmácia Perto" in spoken_text
