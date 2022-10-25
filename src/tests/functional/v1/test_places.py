import pytest
from starlette import status

from models import Place
from repositories.places_repository import PlacesRepository


@pytest.mark.usefixtures("session")
class TestPlacesCreateMethod:
    """
    Тестирование метода создания любимого места.
    """

    @staticmethod
    async def get_endpoint() -> str:
        """
        Получение адреса метода API.

        :return:
        """

        return "/api/v1/places"

    @pytest.mark.asyncio
    async def test_method_success(self, client, session):
        """
        Тестирование успешного сценария.

        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :return:
        """

        # передаваемые данные
        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание тестового места",
        }
        # осуществление запроса
        response = await client.post(
            await self.get_endpoint(),
            json=request_body,
        )

        # проверка корректности ответа от сервера
        assert response.status_code == status.HTTP_201_CREATED

        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"]["id"], int)
        assert isinstance(response_json["data"]["created_at"], str)
        assert isinstance(response_json["data"]["updated_at"], str)
        assert response_json["data"]["latitude"] == request_body["latitude"]
        assert response_json["data"]["longitude"] == request_body["longitude"]
        assert response_json["data"]["description"] == request_body["description"]

        # проверка существования записи в базе данных
        created_data = await PlacesRepository(session).find_all_by(
            latitude=request_body["latitude"],
            longitude=request_body["longitude"],
            description=request_body["description"],
            limit=100,
        )
        assert len(created_data) == 1
        assert isinstance(created_data[0], Place)
        assert created_data[0].latitude == request_body["latitude"]
        assert created_data[0].longitude == request_body["longitude"]
        assert created_data[0].description == request_body["description"]
