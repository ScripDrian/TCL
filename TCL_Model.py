import json
import logging

from telethon import TelegramClient, events, errors

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


class Clientes(TelegramClient):  # clientes
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        
        self.quest = bool   # modificables segun se necesite 
         self.arena = bool 
         self.foray = bool   
         self.fix_quest = ""  # tipo de quests 
         self.ram_quest = bool 
         self.mob_hunt = bool 
         self.squad_orden = bool
        self.add_event_handler(
            self.on_chat,
                    self.add_event_handler(self.on_cw, events.NewMessage(chats='chtwrsbot', incoming=True))  # Add a Handler 
         self.add_event_handler(self.on_squad, events.NewMessage(chats=-1001237607365, incoming=True)) 
         self.add_event_handler(self.on_lycaon, events.NewMessage(chats='LycaonBot', incoming=True)) 
         self.add_event_handler(self.on_pve, events.NewMessage(chats='wolf_pve_bot', incoming=True)) 
         self.add_event_handler(self.on_btnt, events.NewMessage(chats='botniatobot', incoming=True)) 
  
     #        self.add_event_handler(self.on_update, events.NewMessage) # type: ignore   # solo para pruebas 
     #        self.add_event_handler(self.on_metodo, events.NewMessage(chats=('id_chat'), incoming = True)) 
  
     async def connect(self: 'TelegramClient') -> None:  # metodo de coneccion 
         try: 
             await super().connect()  # Llamada a la clase Client 
             self.me = await self.get_me()  # type: ignore  # Toma la informacion del Client 
         except errors as e:  # importante el manipular los errores 
             print(e) 
             pass 
  
     #    async def on_update(self, event): 
     #        print("Client: {} ejecutandose.. ".format(self.me.username)) # type: ignore 
  
     async def on_cw(self, event):  # Handler del ChatWars 
         # Foray & Pledge 
         if 'You were strolling around on your horse when you noticed' in event.raw_text: 
             time.sleep(random.randint(1, 2)) 
             await self.clic_one(event) 
             print('{} interviniendo saqueo'.format(self.me.username))  # type: ignore 
         if '/pledge' in event.raw_text: 
             time.sleep(random.randint(1, 2)) 
             await super().send_message('chtwrsbot', '/pledge') 
             print('{} ocupando el Pledge'.format(self.me.username))  # type: ignore 
         # Trigers de batalla 
         if '/use_cry' in event.raw_text: 
             time.sleep(random.randint(1, 2)) 
             await super().send_message('chtwrsbot', '/use_cry') 
             print('{} utilizando Crytico'.format(self.me.username))  # type: ignore 
         # Mobs Hunt 
         if 'You met some hostile creatures' in event.raw_text: 
             await event.forward_to('wolf_pve_bot') 
             await event.forward_to(-1001267008726) 
             await event.forward_to('LycaonBot') 
             print('{} Mob hunt,send'.format(self.me.username))  # type: ignore  
         if 'Congratulations! You are still alive.' in event.raw_text: 
             await self.clic_mob_report(event) 
         if 'Your result on the battlefield:' and '👾Encounter:' in event.raw_text: 
             async with event.conversation('chtwrsbot'): 
                 time.sleep(random.randint(1, 2)) 
                 await event.forward_to('wolf_pve_bot') 
         # Quests 
         if 'Stamina restored' in event.raw_text: 
             time.sleep(random.randint(1, 10)) 
             await super().send_message('chtwrsbot', '🗺Quests') 
             print('{} a iniciado quest'.format(self.me.username))  # type: ignore 
         if 'You received:' in event.raw_text: 
             time.sleep(random.randint(1, 10)) 
             await super().send_message('chtwrsbot', '🗺Quests') 
             print('{} a iniciado quest'.format(self.me.username))  # type: ignore 
         # quest 
  
         if '🌲Forest' in event.raw_text:  # Quest general 
             time.sleep(random.randint(1, 2)) 
             if self.quest: 
                 if self.arena: 
                     if '🔒' not in event.raw_text: 
                         await super().send_message('chtwrsbot', '▶️Fast fight') 
                 elif '🌲Forest' and '🔥' in event.raw_text: 
                     if re.search("🌲Forest [1-9]min 🔥") or re.search("🌲Forest [1-9]min 🎩") in event.raw_text:  # type: ignore 
                         await self.clic_forest(event) 
                     if re.search("🍄Swamp [1-9]min 🔥") or re.search("🍄Swamp [1-9]min 🎩") in event.raw_text:  # type: ignore 
                         await self.clic_swamp(event) 
                     if re.search("🏔Mountain Valley [1-9]min 🔥") or re.search("🏔Mountain Valley [1-9]min 🎩") in event.raw_text:  # type: ignore 
                         await self.clic_valley(event) 
                 elif self.ram_quest: 
                     alg = random.randint(1, 3) 
                     print(alg) 
                     if alg == 1: 
                         await self.clic_forest(event) 
                     elif alg == 2: 
                         await self.clic_swamp(event) 
                     elif alg == 3: 
                         await self.clic_valley(event) 
                 elif self.fix_quest == "Forest": 
                     await self.clic_forest(event) 
                 elif self.fix_quest == "Swamp": 
                     await self.clic_swamp(event) 
                 elif self.fix_quest == "Valley": 
                     await self.clic_valley(event) 
             elif self.foray: 
                 await self.clic_foray(event) 
  
     # metodos reutilizables 
     async def clic_mob_report(self, event): 
         async with event.conversation('chtwrsbot'): 
             time.sleep(random.randint(1, 2)) 
             buttons = await event.get_buttons() 
             for bline in buttons: 
                 for button in bline: 
                     if 'Report' in button.button.text: 
                         await button.click() 
                         print('{} Mob report, Send'.format(self.me.username))  # type: ignore 
  
     @staticmethod 
     async def clic_one(event): 
         buttons = await event.get_buttons() 
         for bline in buttons: 
             for button in bline: 
                 await button.click() 
  
     async def clic_foray(self, event):  # clic Valle 
         buttons = await event.get_buttons() 
         for bline in buttons: 
             for button in bline: 
                 if 'Foray' in button.button.text: 
                     await button.click() 
                     print('{} go to Foray'.format(self.me.username))  # type: ignore 
  
     async def clic_valley(self, event):  # clic Valle 
         buttons = await event.get_buttons() 
         for bline in buttons: 
             for button in bline: 
                 if 'Valley' in button.button.text: 
                     await button.click() 
                     print('{} go to 🏔Valley'.format(self.me.username))  # type: ignore 
  
     async def clic_swamp(self, event):  # clic Swamp 
         buttons = await event.get_buttons() 
         for bline in buttons: 
             for button in bline: 
                 if 'Swamp' in button.button.text: 
                     await button.click() 
                     print('{} go to 🍄Swamp'.format(self.me.username))  # type: ignore 
  
     async def clic_forest(self, event):  # clic Forest 
         buttons = await event.get_buttons() 
         for bline in buttons: 
             for button in bline: 
                 if 'Forest' in button.button.text: 
                     await button.click() 
                     print('{} go to 🌲forest'.format(self.me.username))  # type: ignore 
  
     # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ metodos #3 reutilizables ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
  
     async def on_squad(self, event):  # Handler del Squad 
         # wars's trigers 
         if '⚔️BATTLE IS OVER⚔️' in event.raw_text: 
             self.message1 = await event.forward_to(-1001510356585)  # nota: este es el AutoTag grupo de ordenes 
             await super().pin_message(-1001510356585, self.message1, notify=True) 
             self.message2 = await event.forward_to(-1001489868968)  # reenviado al grupo del gremio 7nt 
             await super().pin_message(-1001489868968, self.message2, notify=False) 
             print('{} anuncia el fin de batalla'.format(self.me.username))  # type: ignore 
             async with super().conversation('chtwrsbot') as conv: 
                 await conv.send_message('/report') 
                 print('{} solicita report'.format(self.me.username))  # type: ignore 
                 response = await conv.get_response() 
                 if 'Your result on the battlefield:' in response.raw_text: 
                     await response.forward_to('LycaonBot') 
                     print('{} envia el reporte'.format(self.me.username))  # type: ignore 
                     time.sleep(random.randint(1, 2)) 
                 await super().send_message('chtwrsbot', '🗺Quests') 
                 print('{} a iniciado quest'.format(self.me.username))  # type: ignore 
         # ordenes de batalla 
         if '⚔️Attack' in event.raw_text: 
             if '⚔️Attack 🦈SHARKS' in event.raw_text: 
                 time.sleep(1) 
                 await super().send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '🦈') 
                 print('{} atacando 🦈'.format(self.me.username))  # type: ignore 
             elif '🦅' in event.raw_text: 
                 time.sleep(1) 
                 await super().send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '🦅') 
                 print('{} atacando 🦅'.format(self.me.username))  # type: ignore 
             elif '🐉' in event.raw_text: 
                 time.sleep(1) 
                 await super().send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '🐉') 
                 print('{} atacando 🐉'.format(self.me.username))  # type: ignore 
             elif '🥔' in event.raw_text: 
                 time.sleep(1) 
                 await super().send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '🥔') 
                 print('{} atacando 🥔'.format(self.me.username))  # type: ignore 
             elif '🌑' in event.raw_text: 
                 time.sleep(1) 
                 await super().send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '🌑') 
                 print('{} atacando 🌑'.format(self.me.username))  # type: ignore 
             elif '🦌' in event.raw_text: 
                 time.sleep(1) 
                 await event.send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '🦌') 
                 print('{} atacando 🦌'.format(self.me.username))  # type: ignore 
             elif '☘️' in event.raw_text: 
                 time.sleep(1) 
                 await super().send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '☘️') 
                 print('{} atacando ☘️'.format(self.me.username))  # type: ignore 
             elif '🐢' in event.raw_text: 
                 time.sleep(1) 
                 await super().send_message('chtwrsbot', '⚔️Attack') 
                 time.sleep(2) 
                 await super().send_message('chtwrsbot', '🐢') 
                 print('{} atacando 🐢'.format(self.me.username))  # type: ignore 
  
     async def on_lycaon(self, event):  # Handler del Lycaon 
         if "Your arrows are getting low" in event.raw_text: 
             time.sleep(2) 
             if "Wooden arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_505") 
             elif "Steel arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_511") 
             elif "Silver arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_513") 
             elif "Broad arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_515") 
             elif "Heavy arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_517") 
             elif "Compound arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_519") 
             elif "Piercing arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_524") 
             elif "Bodkin arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_523") 
             elif "Mechblade arrow" in event.raw_text: 
                 await super().send_message("CHAT_WARS", "/use_525") 
  
     async def on_pve(self, event):  # Handler del mob pve 
         if 'Prepare yourself to fight:' in event.raw_text: 
             buttons = await event.get_buttons() 
             for bline in buttons: 
                 for button in bline: 
                     url_text = button.button.url 
             global lucha 
             lucha = '/fight_' + \ 
                     url_text.split('https://t.me/share/url?url=/fight_')[1].split()[0].split(')')[0]  # type: ignore 
             await super().send_message("chtwrsbot", lucha) 
             print('{} Hunting'.format(self.me.username))  # type: ignore 
  
     async def on_btnt(self, event):  # Handler del Botniato 
         if 'needs your help' in event.raw_text: 
             global lucha 
             lucha = '/fight_' + \ 
                     event.message.text.split('url?url=/fight_')[1].split()[0].split(')')[0] 
             await super().send_message("chtwrsbot", lucha) 
             print('{} Hunting'.format(self.me.username))  # type: ignore 
 


if __name__ == "__main__":
    with open("src/configuracion.json") as conf:
        c = json.load(conf)
    client1 = Bot("Nombreclient", c["api_id"], c["api_hash"])


    client1.start()
    client1.run_until_disconnected()
