from bson import ObjectId


def parse_id(data):
    if "_id" not in data:
        return ObjectId()
    _id = data["_id"]
    if isinstance(_id, str):
        return ObjectId(_id)
    elif isinstance(_id, ObjectId):
        return _id
    else:
        raise ValueError("_id has to be of string or ObjectId type")


def check_question_type(question_type):
    allowed_types = {"open_text", "single_choice", "multiple_choice",
                     "date"}
    if question_type not in allowed_types:
        error_msg = "Question type \"" + question_type + "\" is not supported"
        raise ValueError(error_msg)
