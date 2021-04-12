import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from _token import token
import datetime
import random


group = 187318939


class Bot:
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id

        self.vk_api = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(vk=self.vk_api, group_id=self.group_id)

        self.api = self.vk_api.get_api()

    def run(self):
        for event in self.long_poll.listen():
            # Запись лога любого события
            self.log(event)
            # Обаботка события
            self.on_event(event)

    def on_event(self, event):
        # Новое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:
            # Доп. действия/информация по необходимости
            print('  От: ', event.obj.message['from_id'])
            print('  Текст:', event.obj.message['text'])
            self.return_message(obj=event.obj)

    # Функция ответа на сообщение
    def return_message(self, obj):
        self.api.messages.send(message=f"Hi, {obj.message['from_id']}",
                               random_id=random.randint(0, 2**20),
                               peer_id=obj.message['peer_id'])

    @staticmethod
    def log(event):
        print(datetime.datetime.now(), event.type)


def staticmetod():
    def log(event):
        print(datetime.datetime.now(), event.type)
    




if __name__ == '__main__':
    bot = Bot(token=token, group_id=group)
    bot.run()