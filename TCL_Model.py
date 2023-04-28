import json
import logging

from telethon import TelegramClient, events, errors

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


class Clientes(TelegramClient):  # clientes
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.add_event_handler(
            self.on_chat,
            events.NewMessage(chats="chat_id", incoming=True),  # cambiar por un id
        )

    async def connect(self: "TelegramClient") -> None:
        try:
            await super().connect()
            self.me = await self.get_me()
        except errors as e:
            print(e)
            pass

    async def on_chat(self, event):
        if "Hola" in event.raw_text:
            event.reply("Hola a ti")


if __name__ == "__main__":
    with open("src/configuracion.json") as conf:
        c = json.load(conf)
    client1 = Bot("Nombreclient", c["api_id"], c["api_hash"])


    client1.start()
    client1.run_until_disconnected()
