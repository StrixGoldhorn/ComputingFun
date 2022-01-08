# noobgame01 & noobtool01

## Description of noobgame01:
a web based game, which seems to be some sort of ripoff of Terreria, with less blocks and extremely poor UI and UX

controls are very laggy, with a noticeable huge delay between input and movement of character on screen

digging through the barely obfusecated code reveals it uses [Socket.IO](https://socket.io/) to send the player inputs to the server, then waiting for the websocket response before updating the screen

attached below are several code samples of how websocket is implemented in the so-called "game":
```js
socket['emit']("keyPress", {
      'inputId': "right",
      'state': !![] //either True or False
    });

socket['emit']('evalServer', chatInput['value']['slice'](0x1));
socket['emit']('playerCmd', chatInput['value']['slice'](0x1))

socket['emit']('playerCmd', 'help')

// how to get ez banned 101: copy-paste the single line below, into the f12 console
socket['emit']('changeEquip', {'item':99999999}), equip = 99999999;

socket['emit']('breakTile', {
      'x_pos': x_pos_var,
      'y_pos': y_pos_var
    })

// have no idea what this is supposed to do, normal users can't use it
Swal['fire']({
    'title': 'Are you sure you want to Desert Blast this world?',
    'text': 'You won\'t be able to revert this!',
    'type': 'warning',
    'showCancelButton': !![],
    'confirmButtonColor': '#3085d6',
    'cancelButtonColor': '#d33',
    'confirmButtonText': 'Yes, blast it!'
  })['then'](_0x105996 => {
    if(_0x105996['value']) socket['emit']('preformBlast', _0x5c6b7e), Swal['fire']('Blasted!', 'Enjoy your new world.', 'success');
    else return;
  });
```

### bad practices 101
there is no "change email" or "change password" option, so you're pretty much done for if your account is compromised

automated bans are also issued if your machine sends a request that the server thinks is malicious (ie requesting to hold an item that you do not have). obviously, this will have the possiblity of getting issued a false ban.

worse still, the main developer relased a screenshot on the game's discord server, that reveals a username and hashed password.

a quick google search of the hashed password reveals the unhashed version...

there's not much to say, apart from the fact that combined with the lack of "change password" option, this is extremely bad practice from the dev. not only are the stored passwords UNSALTED (and unpeppered), releasing these information publicy is a BIG NO-NO.

because of the myriad of bad practices, this "game" shall not be named, to protect readers against this dev's big mistake(s), and any potential future security issues.

## Description of noobtool01:
since the game uses websocket, we are able to find the websocket it connects to, and use Socket.IO's polling function

we can request the page via HTTP GET, and the response includes the tilemap of a world, plus player(s) online and their respective stats/data

### what it does:
this tool automatically GETs tilemap and players + stats

if no player is online, it displays the tilemap of the default world

if player(s) are online, it displays the player(s) name, gems, visibility, the world they are in, and their x y coordinates in the aforementioned world. it also has the ability to detect whether player(s) are AFK by comparing the world and x y coordinates of the current and previous response.

[python script](noobtool01.py)