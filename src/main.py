import pyautogui
from colorama import Fore, Style, init
import keyboard
import mss
import time
import sys
import config_loader

class AutoAgentSelector:
    """ Auto select agents in Valorant"""
    def __init__(self) -> None:
        # Imported Module config
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False
        mss.windows.CAPTUREBLT = 0
        
        # Class config
        config: config_loader.Config = config_loader.load()
        self.MONITOR_NUMBER: int = config.monitor_number
        self.STATE_DELAY_MS: int = config.state_delay_ms
        self.SWITCH_KEY: str = config.switch_key
        # Class state
        self.live: bool = False

    def handleDisplay(self, lastStr, count, liveState):
        sys.stdout.write(" ")
        sys.stdout.write("\b" * (len(lastStr)+1))
        liveState = "Yes" if liveState else "No"
        fstr = f"{Fore.CYAN}FPS: {count} {Fore.GREEN}Live: {liveState}{Style.RESET_ALL}"
        sys.stdout.write(fstr)
        sys.stdout.flush()
        return fstr

    def development_screenshot_on_command(self) -> None:
        """Development function to take a screenshot on command"""
        with mss.mss() as sct:
            num_shots: int = 0
            last_state: bool = False
            while(True):
                if keyboard.is_pressed(self.SWITCH_KEY and not last_state):
                    last_state = True
                    print("Grabbed screenshot")
                    _img = sct.grab(self.MONITOR_NUMBER)
                    mss.tools.to_png(_img.rgb, _img.size, output=f"screenshot_{num_shots}.png")
                    num_shots += 1
                elif not keyboard.is_pressed(self.SWITCH_KEY):
                    last_state = False
    
    def start(self):
        init()
        SWITCH_KEY = "ctrl + alt"
        with mss.mss() as sct:
            print("Managing Screenshots")
            lastStr = ""
            itime = time.time()
            finalCount = 0
            count = 0
            while(True):
                if(not self.live):
                    time.sleep(.01)
                if keyboard.is_pressed(SWITCH_KEY):
                    self.live = not self.live
                    self.handleSound(self.live)
                if(self.live):
                    _img = sct.grab(self.CAPTURE)
                    self._checkForColision(_img)
                count += 1
                lastStr = self.handleDisplay(lastStr, finalCount, self.live)
                if(time.time() - itime > 1):
                    finalCount = count
                    count = 0
                    itime = time.time() 
                

if __name__ == "__main__":
    aas = AutoAgentSelector()
    aas.development_screenshot_on_command()