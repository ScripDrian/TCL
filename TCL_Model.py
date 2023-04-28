import json
import logging
import random
import re
import time

from telethon import TelegramClient, events, errors
from datetime import datetime

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


class Clientes(TelegramClient):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.add_event_handler(
            self.on_cw, events.NewMessage(chats="chtwrsbot", incoming=True)
        )
        self.add_event_handler(
            self.on_squad, events.NewMessage(chats="Id del saquad", incoming=True)
        )
        self.add_event_handler(
            self.on_autotag, events.NewMessage(chats="id del grpo de ordenes", incoming=True)
        )
        self.add_event_handler(
            self.on_lycaon, events.NewMessage(chats="LycaonBot", incoming=True)
        )
        self.add_event_handler(
            self.on_pve, events.NewMessage(chats="wolf_pve_bot", incoming=True)
        )
        self.add_event_handler(
            self.on_btnt, events.NewMessage(chats="botniatobot", incoming=True)
        )

    async def connect(self: "TelegramClient") -> None:
        try:
            await super().connect()
            self.me = await self.get_me()
        except errors as e:
            print(e)
            pass

    def update_data(self, message): # esto esta en desarrollo 
        self.message = message

        level_match = re.search(r"Level:(\d+)", message)
        level_value = level_match.group(1)

        atk_match = re.search(r"⚔️Atk:(\d+)", message)
        atk_value = atk_match.group(1)

        def_match = re.search(r"Def:(\d+)", message)
        def_value = def_match.group(1)

        hp_match = re.search(r"Hp:(\d+)/(d+)", message)
        current_hp = hp_match.group(1)
        max_hp = hp_match.group(2)

        stamina_match = re.search(r"Stamina:(\d+)/(d+)", message)
        current_stamina = stamina_match.group(1)
        max_stamina = stamina_match.group(2)

        data = {
            "Level": level_value,
            "Attack": atk_value,
            "defense": def_value,
            "c_hp": current_hp,
            "m_hp": max_hp,
            "c_stamina": current_stamina,
            "m_stamina": max_stamina,
        }

        with open("src/{}.json".format(self.me.username), "w") as f:
            json.dump(data, f)

    @classmethod
    def class_select(self, clase, master_mind):
        self.clase = clase
        self.master_mind = master_mind

        valley = ["Ranger", "Knigt", "Centinel", "Bercerker"]
        forest = ["LowLVL"]
        swamp = ["Noble", "BlackSmith", "Alchemist"]
        ramdom = ["collector", "otros"]

        if self.clase in forest:
            self.quest = True
            self.foray = False
            self.arena = False
            self.fix_quest = "Forest"
        elif self.clase in valley:
            self.quest = True
            self.foray = False
            self.arena = False
            self.fix_quest = "Valley"
        elif self.clase in swamp:
            self.quest = True
            self.foray = False
            self.arena = False
            self.fix_quest = "Swamp"
        elif self.clase in ramdom:
            self.quest = True
            self.foray = False
            self.arena = False
            self.fix_quest = "Ramdom"

    @staticmethod
    def reporte(self):
        salida = f"""Reporte de usuario {self.me}"""
        print(salida)

    async def on_cw(self, event):
        if "You were strolling around on your horse when you noticed" in event.raw_text:
            time.sleep(random.randint(1, 2))
            await self.clic_one(event)
            print(
                "{} interviniendo saqueo ".format(self.me.username)
                + datetime.now().isoformat(timespec="minutes")
            )
        if "/pledge" in event.raw_text:
            time.sleep(random.randint(1, 2))
            await super().send_message("chtwrsbot", "/pledge")
            print(
                "{} ocupando el Pledge ".format(self.me.username)
                + datetime.now().isoformat(timespec="minutes")
            )

        if "/use_cry" in event.raw_text:
            time.sleep(random.randint(1, 2))
            await super().send_message("chtwrsbot", "/use_cry")
            print(
                "{} utilizando Crytico ".format(self.me.username)
                + datetime.now().isoformat(timespec="minutes")
            )

        if "You met some hostile creatures" in event.raw_text:
            await event.forward_to("wolf_pve_bot")
            await event.forward_to(-1001267008726)
            await event.forward_to("LycaonBot")
            print(
                "{} Mob hunt,send".format(self.me.username)
                + datetime.now().isoformat(timespec="minutes")
            )
        if "Congratulations! You are still alive." in event.raw_text:
            await self.clic_mob_report(event)
        if "Your result on the battlefield:" and "👾Encounter:" in event.raw_text:
            async with event.conversation("chtwrsbot"):
                time.sleep(random.randint(1, 2))
                await event.forward_to("wolf_pve_bot")

        if "Stamina restored" in event.raw_text:
            time.sleep(random.randint(1, 10))
            await super().send_message("chtwrsbot", "🗺Quests")
            print(
                "{} a iniciado quest ".format(self.me.username)
                + datetime.now().isoformat(timespec="minutes")
            )
        if "You received:" in event.raw_text:
            time.sleep(random.randint(1, 10))
            await super().send_message("chtwrsbot", "🗺Quests")
            print(
                "{} a iniciado quest ".format(self.me.username)
                + datetime.now().isoformat(timespec="minutes")
            )

        if "🌲Forest" in event.raw_text:
            time.sleep(random.randint(1, 2))
            if self.arena:
                print(self.arena)
                if "🔒" not in event.raw_text:
                    await super().send_message("chtwrsbot", "▶️Fast fight")
            if "🌲Forest" and "🔥" in event.raw_text:
                if (
                    re.search("🌲Forest [1-9]min 🔥")
                    or re.search("🌲Forest [1-9]min 🎩") in event.raw_text
                ):
                    await self.clic_forest(event)
                elif (
                    re.search("🍄Swamp [1-9]min 🔥")
                    or re.search("🍄Swamp [1-9]min 🎩") in event.raw_text
                ):
                    await self.clic_swamp(event)
                elif (
                    re.search("🏔Mountain Valley [1-9]min 🔥")
                    or re.search("🏔Mountain Valley [1-9]min 🎩") in event.raw_text
                ):
                    await self.clic_valley(event)
            elif self.fix_quest == "Ramdom":
                alg = random.randint(1, 3)
                print("Go Ramdom {}".format(alg))
                print(alg)
                if alg == 1:
                    await self.clic_forest(event)
                elif alg == 2:
                    await self.clic_swamp(event)
                elif alg == 3:
                    await self.clic_valley(event)
            elif self.fix_quest == "Forest":
                await self.clic_forest(event)
            elif self.fix_quest == "Swamp":
                await self.clic_swamp(event)
            elif self.fix_quest == "Valley":
                await self.clic_valley(event)
        elif self.foray:
            await self.clic_foray(event)

    async def clic_mob_report(self, event):
        async with event.conversation("chtwrsbot"):
            time.sleep(random.randint(1, 2))
            buttons = await event.get_buttons()
            for bline in buttons:
                for button in bline:
                    if "Report" in button.button.text:
                        await button.click()
                        print(
                            "{} Mob report, Send ".format(self.me.username)
                            + datetime.now().isoformat(timespec="minutes")
                        )

    @staticmethod
    async def clic_one(event):
        buttons = await event.get_buttons()
        for bline in buttons:
            for button in bline:
                await button.click()

    async def clic_foray(self, event):
        buttons = await event.get_buttons()
        for bline in buttons:
            for button in bline:
                if "Foray" in button.button.text:
                    await button.click()
                    print(
                        "{} go to Foray".format(self.me.username)
                        + datetime.now().isoformat(timespec="minutes")
                    )

    async def clic_valley(self, event):
        buttons = await event.get_buttons()
        for bline in buttons:
            for button in bline:
                if "Valley" in button.button.text:
                    await button.click()
                    print(
                        "{} go to 🏔Valley ".format(self.me.username)
                        + datetime.now().isoformat(timespec="minutes")
                    )

    async def clic_swamp(self, event):
        buttons = await event.get_buttons()
        for bline in buttons:
            for button in bline:
                if "Swamp" in button.button.text:
                    await button.click()
                    print(
                        "{} go to 🍄Swamp ".format(self.me.username)
                        + datetime.now().isoformat(timespec="minutes")
                    )

    async def clic_forest(self, event):
        buttons = await event.get_buttons()
        for bline in buttons:
            for button in bline:
                if "Forest" in button.button.text:
                    await button.click()
                    print(
                        "{} go to 🌲forest ".format(self.me.username)
                        + datetime.now().isoformat(timespec="minutes")
                    )

    async def on_squad(self, event): # esto esta en proceso
        if self.master_mind:
            if "⚔️BATTLE IS OVER⚔️" in event.raw_text:
                self.message1 = await event.forward_to(
                    -1001510356585
                )  # nota: este es el AutoTag grupo de ordenes
                await super().pin_message(-1001510356585, self.message1, notify=True)
                self.message2 = await event.forward_to(
                    -1001489868968
                )  # reenviado al grupo del gremio 7nt
                await super().pin_message(-1001489868968, self.message2, notify=False)
                print("{} anuncia el fin de batalla ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
                async with super().conversation("chtwrsbot") as conv:
                    await conv.send_message("/report")
                    print("{} solicita report ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
                    response = await conv.get_response()
                    if "Your result on the battlefield:" in response.raw_text:
                        await response.forward_to("LycaonBot")
                        print("{} envia el reporte ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
                        time.sleep(random.randint(1, 2))
                    await super().send_message("chtwrsbot", "🗺Quests")
                    print("{} a iniciado quest ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore

        # ordenes de batalla

    async def on_autotag(self, event): # esto solo funciona en n squad con Lycaon
        if "⚔️Attack" in event.raw_text:
            if "⚔️Attack 🦈SHARKS" in event.raw_text:
                time.sleep(1)
                await super().send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "🦈")
                print("{} atacando 🦈 ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
            elif "🦅" in event.raw_text:
                time.sleep(1)
                await super().send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "🦅")
                print("{} atacando 🦅 ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
            elif "🐉" in event.raw_text:
                time.sleep(1)
                await super().send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "🐉")
                print("{} atacando 🐉 ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
            elif "🥔" in event.raw_text:
                time.sleep(1)
                await super().send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "🥔")
                print("{} atacando 🥔 ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
            elif "🌑" in event.raw_text:
                time.sleep(1)
                await super().send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "🌑")
                print("{} atacando 🌑 ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
            elif "🦌" in event.raw_text:
                time.sleep(1)
                await event.send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "🦌")
                print("{} atacando 🦌 ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
            elif "☘️" in event.raw_text:
                time.sleep(1)
                await super().send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "☘️")
                print("{} atacando ☘️ ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore
            elif "🐢" in event.raw_text:
                time.sleep(1)
                await super().send_message("chtwrsbot", "⚔️Attack")
                time.sleep(2)
                await super().send_message("chtwrsbot", "🐢")
                print("{} atacando 🐢 ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore

    async def on_lycaon(self, event):  # Handler del Lycaon
        if "Your arrows are getting low" in event.raw_text:
            time.sleep(2)
            if "Wooden arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_505")
            elif "Steel arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_511")
            elif "Silver arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_513")
            elif "Broad arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_515")
            elif "Heavy arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_517")
            elif "Compound arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_519")
            elif "Piercing arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_524")
            elif "Bodkin arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_523")
            elif "Mechblade arrow" in event.raw_text:
                await super().send_message("CHAT_WARS", "/use_525")

    async def on_pve(self, event):  # Handler del mob pve
        if "Prepare yourself to fight:" in event.raw_text:
            buttons = await event.get_buttons()
            for bline in buttons:
                for button in bline:
                    url_text = button.button.url
            global lucha
            lucha = (
                "/fight_"
                + url_text.split("https://t.me/share/url?url=/fight_")[1]
                .split()[0]
                .split(")")[0]
            )  # type: ignore
            await super().send_message("chtwrsbot", lucha)
            print("{} Hunting ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore

    async def on_btnt(self, event):  # Handler del Botniato
        if "needs your help" in event.raw_text:
            global lucha
            lucha = (
                "/fight_"
                + event.message.text.split("url?url=/fight_")[1]
                .split()[0]
                .split(")")[0]
            )
            await super().send_message("chtwrsbot", lucha)
            print("{} Hunting ".format(self.me.username) + datetime.now().isoformat(timespec="minutes"))  # type: ignore

if __name__ == "__main__":
    __version__ = "1.26.1"

    with open("src/configuracion.json") as conf:
        c = json.load(conf)
    print(
        "Iniciando protocolo de activacion \nversion del lanzador: {} ".format(
            __version__
        )
        + datetime.now().isoformat(timespec="minutes")
    )

    cliente1 = Clientes("CL1", c["api_id"], c["api_hash"])  # cliente 1
    cliente1.class_select(clase="Collector", master_mind=True)

    cliente2 = Clientes("CL2", c["api_id"], c["api_hash"])  # cliente 2
    cliente2.class_select(clase="LowLVL", master_mind=False)

    print("\niniciando client 1")
    cliente1.start()
    print("Cl1 Iniciado\n")

    print("iniciando client 2")
    cliente2.start()
    print("Cl2 Iniciado\n")
   
    cliente1.run_until_disconnected()
    cliente2.run_until_disconnected()