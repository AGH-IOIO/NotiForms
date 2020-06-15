from bson import ObjectId


class NotificationDetails:
    """
    JSON format:
    {
      _id: ObjectId,
      type: string,
      dead_period: int,  # in seconds
      before_deadline_frequency: int,  # in seconds
      after_deadline_frequency: int  # in seconds
    }
    """

    ALLOWED_TYPES = [
        "push",
        "e-mail",
        "online"
    ]

    def __init__(self, notification_type, dead_period, before_deadline_frequency, after_deadline_frequency):
        if not self.__check_if_type_valid(notification_type):
            raise ValueError("Invalid notification type given!")

        self._data = dict()
        self._data["_id"] = ObjectId()
        self._data["type"] = notification_type.lower()
        self._data["dead_period"] = dead_period
        self._data["before_deadline_frequency"] = before_deadline_frequency
        self._data["after_deadline_frequency"] = after_deadline_frequency

    def __check_if_type_valid(self, notification_type):
        return notification_type.lower() in self.ALLOWED_TYPES

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
    def type(self):
        return self._data["type"]

    @type.setter
    def type(self, new_type):
        self._data["type"] = new_type

    @property
    def dead_period(self):
        return self._data["dead_period"]

    @dead_period.setter
    def dead_period(self, new_period):
        self._data["dead_period"] = new_period

    @property
    def before_deadline_frequency(self):
        return self._data["before_deadline_frequency"]

    @before_deadline_frequency.setter
    def before_deadline_frequency(self, new_frequency):
        self._data["before_deadline_frequency"] = new_frequency

    @property
    def after_deadline_frequency(self):
        return self._data["after_deadline_frequency"]

    @after_deadline_frequency.setter
    def after_deadline_frequency(self, new_frequency):
        self._data["after_deadline_frequency"] = new_frequency

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self._data)
