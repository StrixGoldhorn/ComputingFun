# WHY

Why does none of the Windows method work for my laptop?

The world may never know.

However, following the instructions for Linux works, when I run the commands via WSL.

Unfortunately, it is quite a hassle to have to copy paste the long command and edit the ID, printer name, filename everytime.

As such, this script was born. Out of laziness.

# How to use

1. Download and move `printscript.sh` to a suitable directory. Preferably in home directory to easily access files.

(If you are unable to download `printscript.sh` for whatever reason, copy paste contents of `printscript.sh` into a `printscript.sh` on your own device.)

2. Run `chmod +x printscript.sh` to make it executable.

3. **IMPT: You need to set your NUSNET-ID and preferred printer, on lines 3 and 4 respectively.**

```sh
NUSNET_ID="e1234567"
PRINTER="pstsc"
```

You can edit the file however way you like, via vim/emacs/micro/nano/notepad++/HxD.

4. After setting up, you can just run `./printscript.sh -f <filename-to-be-printed>` from now on

5. Other params you can tag on:
   - `-h` or `--help`              Displays help message.
   - `-l` or `--list-printers`     Prints out list of printers and associated code.
   - `-p` or `--printer[=PRINTER]` Changes to print on specified printer.     
   - `-u` or `--user[=NUSNET_ID]`  Changes the NUSNET ID used to print.

6. Check that the params are all correct

7. `Y` or `y` to confirm. This will run the long-winded command and connect you to the printer. Follow on-screen commands to proceed.