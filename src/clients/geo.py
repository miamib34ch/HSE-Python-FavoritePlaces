"""
Функции для взаимодействия с внешним сервисом-провайдером данных о местонахождении.
"""
from http import HTTPStatus
from typing import Optional
from urllib.parse import urlencode, urljoin

import httpx

from clients.base.base import BaseClient
from clients.shemas import LocalityDTO


class LocationClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о местонахождении.
    """

    @property
    def base_url(self) -> str:
        return "https://api.bigdatacloud.net/data/"

    async def _request(self, url: str) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            # получение ответа
            response = await client.get(url)
            # проверка статус-кода ответа от сервера
            if response.status_code == HTTPStatus.OK:
                # преобразование ответа из JSON в словарь
                return response.json()

            return None

    async def get_location(
        self, latitude: float, longitude: float
    ) -> Optional[LocalityDTO]:
        """
        Получение данных о местонахождении по переданным координатам.

        :param latitude: Широта
        :param longitude: Долгота
        :return:
        """

        endpoint = "reverse-geocode-client"
        query_params = {
            "latitude": latitude,
            "longitude": longitude,
            "localityLanguage": "en",
        }
        url = urljoin(
            self.base_url,
            f"{endpoint}?{urlencode(query_params)}",
        )
        if response := await self._request(url):
            return LocalityDTO(
                city=response.get("city") if response.get("city", "").strip() else None,
                alpha2code=response.get("countryCode")
                if response.get("countryCode", "").strip()
                else None,
                locality=response.get("locality")
                if response.get("locality", "").strip()
                else None,
            )

        return None
