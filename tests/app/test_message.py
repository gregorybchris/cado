from cado.app.message import Message, MessageType


class TestMessage:

    def test_parse(self):
        message = Message.parse_obj({
            "type": "get-notebook",
        })
        assert message.type == MessageType.GET_NOTEBOOK
