"""
Comando: localizar a farmácia mais próxima.

Requisito citado no desafio mas não implementado no exemplo do curso.
Implementação sem depender de chave de API paga:

1. Geolocalização aproximada via IP (ip-api.com, gratuito).
2. Busca de farmácias próximas via Overpass API (dados OpenStreetMap,
   gratuito e sem chave).
3. Cálculo da distância real com `geopy.distance.geodesic`.
4. Abre o resultado no Google Maps e informa por voz.
"""
from __future__ import annotations

import webbrowser
from dataclasses import dataclass

import requests
from geopy.distance import geodesic

from virtual_assistant.commands.base import Command
from virtual_assistant.config import settings
from virtual_assistant.tts.text_to_speech import TextToSpeech
from virtual_assistant.utils.logger import get_logger

logger = get_logger(__name__)

IP_GEOLOCATION_URL = "http://ip-api.com/json/"
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"


class PharmacyLocatorError(Exception):
    """Erro genérico ao localizar a farmácia mais próxima."""


@dataclass
class Pharmacy:
    name: str
    latitude: float
    longitude: float
    distance_m: float


class PharmacyLocatorCommand(Command):
    triggers = ("farmácia", "farmacia", "pharmacy")

    def __init__(self, tts: TextToSpeech, search_radius_m: int | None = None) -> None:
        self.tts = tts
        self.search_radius_m = search_radius_m or settings.pharmacy_search_radius_m

    def execute(self, text: str) -> None:
        try:
            lat, lon = self._get_current_location()
            pharmacy = self._find_nearest_pharmacy(lat, lon)
        except PharmacyLocatorError as exc:
            logger.error("Erro ao localizar farmácia: %s", exc)
            self.tts.speak("Não consegui localizar uma farmácia próxima agora.")
            return

        if pharmacy is None:
            self.tts.speak("Não encontrei farmácias próximas dentro do raio de busca.")
            return

        distance_km = pharmacy.distance_m / 1000
        maps_url = (
            f"https://www.google.com/maps/dir/?api=1&destination="
            f"{pharmacy.latitude},{pharmacy.longitude}"
        )
        webbrowser.get().open(maps_url)

        self.tts.speak(
            f"A farmácia mais próxima é {pharmacy.name}, "
            f"a {distance_km:.1f} quilômetros daqui. Abrindo a rota no mapa."
        )

    @staticmethod
    def _get_current_location() -> tuple[float, float]:
        """Obtém latitude/longitude aproximadas a partir do IP público."""
        try:
            response = requests.get(IP_GEOLOCATION_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("status") != "success":
                raise PharmacyLocatorError("Falha ao geolocalizar por IP.")
            return data["lat"], data["lon"]
        except requests.RequestException as exc:
            raise PharmacyLocatorError(f"Erro de rede na geolocalização: {exc}") from exc

    def _find_nearest_pharmacy(self, lat: float, lon: float) -> Pharmacy | None:
        """Consulta a Overpass API por farmácias dentro do raio configurado."""
        query = f"""
        [out:json][timeout:10];
        node["amenity"="pharmacy"](around:{self.search_radius_m},{lat},{lon});
        out body;
        """
        try:
            response = requests.post(OVERPASS_API_URL, data={"data": query}, timeout=10)
            response.raise_for_status()
            elements = response.json().get("elements", [])
        except requests.RequestException as exc:
            raise PharmacyLocatorError(f"Erro de rede na Overpass API: {exc}") from exc

        if not elements:
            return None

        origin = (lat, lon)
        nearest = None
        nearest_distance = float("inf")

        for element in elements:
            candidate_coords = (element["lat"], element["lon"])
            distance = geodesic(origin, candidate_coords).meters
            if distance < nearest_distance:
                nearest_distance = distance
                nearest = Pharmacy(
                    name=element.get("tags", {}).get("name", "Farmácia sem nome"),
                    latitude=element["lat"],
                    longitude=element["lon"],
                    distance_m=distance,
                )

        return nearest
