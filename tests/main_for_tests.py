import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

try:
    import settings
except ImportError:
    exit("Fill fields in settings.py.default and rename for settings.py")

import random
import logging.config
from logs.log_config import log_config


# logging.config.dictConfig(log_config)
# reply_log = logging.getLogger('reply')
# main_log = logging.getLogger('main')

group = 187318939


class Bot:
    """
    Echo Bot для vk.com
    Use Python 3.9
    """
    def __init__(self, token, group_id):
        """
        Инициализация бота
        :param token: секретный токен для группы
        :param group_id: идентификатор группы
        """
        self.token = token
        self.group_id = group_id

        self.vk_api = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(vk=self.vk_api, group_id=self.group_id)

        self.api = self.vk_api.get_api()
        # main_log.info(f"Bot was init with group_id={self.group_id}")

    def run(self):
        """ Запуск бота """
        # main_log.info('Bot was started')
        for event in self.long_poll.listen():
            # Запись лога любого события
            # main_log.info(f"'New event {event.type}'")
            # main_log.debug(f"{event}")
            # Обаботка события
            self.on_event(event)

    def on_event(self, event):
        """
        Обработка событий
        :param event: событие
        """
        # Новое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:
            # Доп. действия/информация по необходимости
            # main_log.debug(f"'new mesg from:{event.obj.message['from_id']} text: {event.obj.message['text']}'")
            self.return_message(obj=event.obj)

    # Функция ответа на сообщение
    def return_message(self, obj):
        """
        Отправка ответного сообщения
        :param obj: "объект", которому направлено письмо
        """
        message = f"Hi, {obj.message['from_id']}"
        random_id = random.randint(0, 2 ** 20)
        peer_id = obj.message['peer_id']
        # reply_log.info(f"'Bot reply to user_id:{obj.message['from_id']}'")
        # reply_log.debug(f"'mesg: {message}, rand_id: {random_id}, peer_id: {peer_id}'")
        self.api.messages.send(message=message,
                               random_id=random_id,
                               peer_id=peer_id)

    def __del__(self):
        """
        Удаление бота
        """
        # main_log.info(f"Bot was exit with group_id={self.group_id}")


if __name__ == '__main__':
    bot = Bot(token=settings.TOKEN, group_id=settings.GROUP_ID)
    bot.run()
