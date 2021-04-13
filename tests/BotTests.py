import unittest.mock

from vk_api.bot_longpoll import VkBotMessageEvent

from tests.main_for_tests import Bot


class RunTest(unittest.TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {
                     'message': {
                         'date': 1618333575,
                         'from_id': 251502045,
                         'id': 45, 'out': 0,
                         'peer_id': 251502045,
                         'text': '1',
                         'conversation_message_id': 41,
                         'fwd_messages': [],
                         'important': False,
                         'random_id': 0,
                         'attachments': [],
                         'is_hidden': False},
                     'client_info': {
                         'button_actions': [
                             'text',
                             'vkpay',
                             'open_app',
                             'location',
                             'open_link',
                             'callback',
                             'intent_subscribe',
                             'intent_unsubscribe'],
                         'keyboard': True,
                         'inline_keyboard': True,
                         'carousel': False,
                         'lang_id': 0}},
                 'group_id': 187318939,
                 'event_id': 'c7dde5bbaac3225292c9f5c2afa33a3025219a33'}

    def test_run(self):
        count = 5
        events = [{}] * count
        long_poll_mock = unittest.mock.Mock()
        long_poll_mock.listen = unittest.mock.Mock(return_value=events)
        with unittest.mock.patch('main.vk_api.VkApi'):
            with unittest.mock.patch('main.VkBotLongPoll', return_value=long_poll_mock):
                bot = Bot('', '')
                bot.on_event = unittest.mock.Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)

        with unittest.mock.patch('main.vk_api.VkApi'):
            with unittest.mock.patch('main.VkBotLongPoll'):
                bot = Bot('', '')
                bot.return_message = unittest.mock.Mock()

                bot.on_event(event)

                assert bot.return_message.call_count == 1

    def test_return_message(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = unittest.mock.Mock()

        with unittest.mock.patch('main.vk_api.VkApi'):
            with unittest.mock.patch('main.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = unittest.mock.Mock()
                bot.api.messages.send = send_mock

                bot.return_message(event.obj)
        assert send_mock.call_count == 1
        send_mock.assert_called_once_with(
            message=f"Hi, {event.obj.message['from_id']}",
            random_id=unittest.mock.ANY,
            peer_id=event.obj.message['peer_id']
        )


if __name__ == '__main__':
    unittest.main()
