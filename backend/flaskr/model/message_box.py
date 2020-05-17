from .utils import parse_id


class Message:
    # this can be expanded, e. g. add reference for direct link to a
    # message target (like form to fill)
    """
    JSON format:
    {
      _id: ObjectId,
      text: string,
      send_date: date,  # when was message sent
      ref_id: ObjectId  # ID reference to e. g. PendingForm or PendingMessage
    }
    """

    def __init__(self, data):
        data["_id"] = parse_id(data)
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def id(self):
        return self._data["_id"]

    @id.setter
    def id(self, new_id):
        self._data["_id"] = new_id

    @property
    def text(self):
        return self._data["text"]

    @text.setter
    def text(self, new_text):
        self._data["text"] = new_text

    @property
    def send_date(self):
        return self._data["send_date"]

    @send_date.setter
    def send_date(self, new_send_date):
        self._data["send_date"] = new_send_date

    @property
    def ref_id(self):
        return self._data["ref_id"]

    @ref_id.setter
    def ref_id(self, new_ref_id):
        self._data["ref_id"] = new_ref_id

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)


class MessageBox:
    """
    JSON format:
    {
      _id: ObjectId,
      owner: string,  # username, unique
      messages: list[message]  # Message class JSONs
    }
    """

    def __init__(self, data):
        data["_id"] = parse_id(data)
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def id(self):
        return self._data["_id"]

    @id.setter
    def id(self, new_id):
        self._data["_id"] = new_id

    @property
    def owner(self):
        return self._data["owner"]

    @owner.setter
    def owner(self, new_owner):
        self._data["owner"] = new_owner

    @property
    def messages(self):
        return self._data["messages"]

    @messages.setter
    def messages(self, new_messages):
        self._data["messages"] = new_messages

    def add_message(self, message):
        self._data["messages"].append(message)

    def remove_message(self, message):
        self._data["messages"].remove(message)

    def remove_message_by_ref_id(self, ref_id):
        i = 0
        for msg in self._data["messages"]:
            if msg["ref_id"] == ref_id:
                break
            else:
                i += 1
        del self._data["messages"][i]

    def remove_message_by_index(self, index):
        del self._data["messages"][index]

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
