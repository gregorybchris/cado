from cado.app.message import Message


class TestMessage:

    def test_parse(self):
        message = Message.parse({
            "message": "hello",
        })
        assert message.message == "hello"
