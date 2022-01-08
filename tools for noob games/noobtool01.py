import json
import requests
import re
from time import sleep

def displayroom(tiles):
    cnt = 0
    for i in range(20):
        for j in range(25):
            # find spawnpoint
            if tiles[cnt] == 11:
                print("XX", end = ' ')
            # "grass" but its drawn poorly and doesn't match with the grass/dirt blocks below, trash art
            elif tiles[cnt] == 12:
                print("__", end = ' ')
            # air
            elif tiles[cnt] == 0:
                print("  ", end = ' ')
            else:
                block = str(tiles[cnt])
                while len(block) < 2:
                    block += ' '
                print(block, end = ' ')
            cnt += 1
        print()
    return

def getsid():
    sidurl = "http://**********.***/socket.io/?EIO=3&transport=polling"
    r = requests.get(sidurl).text
    firstparsed = json.loads(r[r.index("{"):r.rindex("}")+1])
    sid = firstparsed["sid"]
    print(f'SESSION ID: {firstparsed["sid"]}')
    return sid

def main():
    lastknown = {}
    while True:
        sid = getsid()
        for i in range(5):
            dataurl = f"http://**********.***/socket.io/?EIO=3&transport=polling&sid={sid}"
            datar = requests.get(dataurl).text

            try:
                raw = datar[datar.index("newPositions")+14:datar.index("}]}]")+3]
                dataparsed = json.loads(raw)['player']
                
                for info in dataparsed:
                    print("-"*20)
                    try:
                        if lastknown[info['name']] == info['world']+str(info['x'])+str(info['y'])+str(info['gems']):
                            print(f"{info['name']} is AFK")
                    except:
                        pass
                    print(f"Name: \t{info['name']}\nVName: \t{info['visiblename']}\nGems: \t{info['gems']}\nVis: \t{info['visible']}\nWorld: \t{info['world']}\nX, Y: \t{info['x']}, {info['y']}")
                    lastknown[info['name']] = info['world']+str(info['x'])+str(info['y'])+str(info['gems'])
            
            except:
                try:
                    print("-"*20)
                    raw = re.split("(\d+:\d+)",datar)
                    cnt = 1
                    # this part can be optimised but it works so no point changing
                    rnd = 1
                    for i in range(3):
                        if rnd == 2:
                            worldinfo = json.loads(raw[cnt+1][raw[cnt+1].index("tiles")-2:-1])
                            displayroom(worldinfo["tiles"])
                            print(f"ROOM NAME: {worldinfo['name']}")
                        if rnd == 3:
                            print("-"*20)
                            print(raw[cnt], raw[cnt+1])
                        rnd += 1
                        cnt += 2
                    print("-"*20)
                    print("No players online.")
                except:
                    print("-"*20)
                    print("FAILED, unknown reason")
            sleep(5)

if __name__ == "__main__":
    main()