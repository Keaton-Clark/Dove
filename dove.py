import terminalio, random
import adafruit_imageload
import terminalio
from adafruit_display_text import label
from io import BytesIO
import supervisor
import microcontroller
import traceback
from random import randint
messages = [" ILY\nDove", " Ur\nCute", "Babzy\nWabzy", " <3 ", "Love\nDove", "I Luv\n You"]

class Dove:
    current_pokemon = 0
    def __init__(self):
        matrix = rgbmatrix.RGBMatrix(
            width=64, bit_depth=6,
            rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
            addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
            clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13)
        
        self.display = framebufferio.FramebufferDisplay(matrix)
        self.group = displayio.Group()
        #b, p = adafruit_imageload.load(BytesIO(self.get("https://raw.githubusercontent.com/Keaton-Clark/Dove/main/bmp/1.bmp").content))
        b, p = adafruit_imageload.load('300.bmp')
        self.bmp_tile = displayio.TileGrid(b, pixel_shader=p)
        self.time = label.Label(
            terminalio.FONT,
            text=messages[randint(0, len(messages)-1)],
            color = 0xffffff)
        self.time.x = 33
        self.time.y = 8 if '\n' in self.time.text else 15
        self.group.append(self.time)
        self.group.append(self.bmp_tile)
        self.display.show(self.group)
        
    def get(self, url):
        print("Getting: " + url)
        try:
            return requests.get(url)
        except Exception as e:
            print("Error getting: " + url)
            return self.get(url)
    
    def displaybmp(self, filename):
        b, p = adafruit_imageload.load(filename)
        self.bmp_tile = displayio.TileGrid(b, pixel_shader=p)
    
    def getdisplaybmp(self, url):
        b, p = adafruit_imageload.load(BytesIO(self.get(url).content))
        self.group.pop()
        self.bmp_tile = displayio.TileGrid(b, pixel_shader=p)
        self.group.append(self.bmp_tile)
        self.display.show(self.group)
        
    def displaypokemon(self, num):
        self.current_pokemon = num
        print("https://raw.githubusercontent.com/Keaton-Clark/Dove/main/bmp/%d.bmp"%(num))
        self.getdisplaybmp("https://raw.githubusercontent.com/Keaton-Clark/Dove/main/bmp/%d.bmp"%(num))
        
    def updatetime(self):
        dt = self.gettime()
        self.time.text = '%.2d:%.2d'%(
            dt['hour'] - 12 if dt['hour'] > 12 else (dt['hour'] if dt['hour'] != 0 else 12),
            dt['minute']
            )
        self.time.y = 15
    def getday(self):
        return self.get("http://worldtimeapi.org/api/timezone/America/Los_Angeles").json()['day_of_year']
    def gettime(self):
        return self.get("https://www.timeapi.io/api/Time/current/zone?timeZone=America/Los_Angeles").json()



try:
    dove = Dove()
    while (True):
        day = dove.getday()
        dove.displaypokemon(day)
        dove.updatetime()
except Exception as e:
    print(e)
    supervisor.reload()