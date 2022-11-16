import logging.config
from socket import error, gaierror
from typing import Optional, Union

import pika
from pika.adapters.blocking_connection import BlockingChannel

from settings import settings

logging.config.fileConfig("logging.conf")
logger = logging.getLogger()


class EventProducer:
    """
    Функции публикации сообщений для коммуникации между микросервисами.
    """

    def __init__(self, url: str = settings.rabbitmq.uri):
        """
        Конструктор продюсера событий.

        :param url: Строка подключения к RabbitMQ.
        :return:
        """

        self.channel: Optional[BlockingChannel] = None
        params = pika.URLParameters(url)
        try:
            connection = pika.BlockingConnection(params)
            self.channel = connection.channel()
        except (error, gaierror):
            logger.error("Error during connection establishing.", exc_info=True)

    def publish(
        self,
        queue_name: str,
        body: Union[bytes, str],
    ) -> None:
        """
        Публикация сообщения в канал.

        :param queue_name: Название очереди.
        :param body: Данные сообщения.
        :return:
        """

        logger.info("Received data to publish (queue: '%s').", queue_name)
        if not self.channel:
            logger.warning("Channel is not created.")

            return

        try:
            self.channel.basic_publish(exchange="", routing_key=queue_name, body=body)
        except (error, gaierror, TypeError):
            logger.error("Error during data publishing.", exc_info=True)

        logger.info("Successfully published event data: %s", body)
