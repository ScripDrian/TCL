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


class Bot(Clientes):  # Bot
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.list_clientes = []

        self.add_event_handler(self.on_start, events.NewMessage(pattern="/start"))
        self.add_event_handler(self.on_log_in, events.NewMessage(pattern="/log_in"))

        for cli in self.list_clientes:
            try:
                cli.start().run_until_disconnected()
            except:
                print("un error a ocurrido")

    async def connect(self: "TelegramClient") -> None:
        try:
            await super().connect()
            self.me = await self.get_me()
        except errors as e:
            print(e)

    async def on_start(self, event):
        try:
            cantidad_usuarios = len(self.list_clientes)
            await event.reply(
                "Dashboard: \n\nCantidad de usuarios registrados {} \n\nRegistro de nuevo usuario:\n\n/log_in *Nombre*\n\n".format(
                    cantidad_usuarios
                )
            )
        except:
            print("A ocurrido un error")

    async def on_log_in(self, event):
        try:
            await event.reply("Intentando inicio:\n\n  En desarrollo...")
            with open("src/configuracion.json") as conf:
                c = json.load(conf)
            text = event.raw_text.split()

            nombre_cliente = text[1]
            self.list_clientes.append(
                Clientes(f"{nombre_cliente}", c["api_id"], c["api_hash"])
            )

        except:
            print("A ocurrido un error")


if __name__ == "__main__":
    with open("src/configuracion.json") as conf:
        c = json.load(conf)
    bot = Bot("NombreBot", c["api_id"], c["api_hash"])
    bot.start().run_until_disconnected()
