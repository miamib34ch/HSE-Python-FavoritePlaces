from typing import Dict


class TestRepositoryBase:
    """
    Базовый репозиторий для тестирования.
    """

    @staticmethod
    async def assert_object(result, expected: Dict):
        """
        Тестирование соответствия полученных данных объекта ожидаемому результату.

        :param result: Полученный результат
        :param expected: Ожидаемый результат
        :return:
        """

        for key, value in expected.items():
            assert getattr(result, key) == value, key
