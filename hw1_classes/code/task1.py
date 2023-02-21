import datetime


class Chat:
    def __init__(self, chat_history=[]):
        self.chat_history = chat_history
        self.sent_message_info = None

    def recieve(self):
        # add datetime of message and put in at start of list chat_history
        if self.sent_message_info is not None:
            self.sent_message_info[1] = str(datetime.datetime.now())
            self.chat_history.insert(0, self.sent_message_info)
            self.sent_message_info = None
        else:
            raise 'The message wasn\'t sent to the chat'

    def show_last_message(self, idx=0):
        # show last message like - Username (datetime): Text
        print(f'{self.chat_history[idx][0]} ({self.chat_history[idx][1]}): {self.chat_history[idx][2]}')

    def show_chat(self):
        # show all history chat the same as show_last_message()
        for idx in range(len(self.chat_history)):
            self.show_last_message(idx)

    @staticmethod
    def __find_time_interval(l_of_datetimes, start, stop):
        # supporting method for get_history_for_the_time_period(); find time intervals, return indexes
        l_of_idx = []
        for idx in range(len(l_of_datetimes)):
            if start <= l_of_datetimes[idx][1] <= stop:
                l_of_idx.append(idx)
        return l_of_idx[0], l_of_idx[-1]

    def get_history_for_the_time_period(self, start=None, stop=None):
        # check type of datetime; needs string
        if isinstance(start, datetime.datetime):
            start = str(start)
        if isinstance(stop, datetime.datetime):
            stop = str(stop)

        # by default use the earliest date (start) and the latest date (stop)
        if start is None:
            start = self.chat_history[-1][1]
        if stop is None:
            stop = self.chat_history[0][1]

        idx_start_messages, idx_stop_messages = self.__find_time_interval(self.chat_history, start, stop)
        return type(self)(self.chat_history[idx_start_messages:idx_stop_messages + 1])


class Message:
    def __init__(self, object_chat, user='No_name', text=None):
        self._text = text
        self._user = user
        self._datetime = None
        self._object_chat = object_chat

    def send(self):
        # send to chat list of message info: user, datetime=None, text
        self._object_chat.sent_message_info = [self._user, None, self._text]

    def show(self):
        # print message info like - Username (datetime): Text
        self._datetime = self._object_chat.chat_history[0][1]
        print(f'{self._user} ({self._datetime}): {self._text}')


class User:
    def __init__(self, user):
        self.user = user

    def say_hi(self):
        print(f'Hi everyone! I\'m {self.user}')
