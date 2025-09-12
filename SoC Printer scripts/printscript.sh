#!/bin/sh

NUSNET_ID="e1234567"
PRINTER="pstsc"

# PRINTERS
# -------- COM1 Basement --------
# psc008
# psc011
#
# -------- COM1 Level 1 -------
# psts
# pstsb
# pstsc
# 
# ------- COM3-01-24 -------
# pse124
#
# ------- COM4 Level 2 -------
# psf204


FILENAME="";


while [ "$#" -gt 0 ]; do
  case "$1" in
    --help|-h)
      echo "---HELP---";
      echo "Usage: ./printscript.sh [OPTIONAL ARGS] [-f FILENAME]";
      echo "Options";
      echo "-h, --help              Displays this help message.";
      echo "-l, --list-printers     Prints out list of printers and associated code.";
      echo "-p, --printer[=PRINTER] Changes to print on specified printer.";          
      echo "-u, --user[=NUSNET_ID] Changes the NUSNET ID used to print.";
      # EXIT EARLY
      exit;
      ;;
    --list-printers|-l)
      echo "---LIST OF PRINTERS---";
      echo "----- COM1 Basement -----";
      echo "psc008";
      echo "psc011";
      echo "";
      echo "----- COM1 Level 1 -----";
      echo "psts";
      echo "pstsb";
      echo "pstsc";
      echo "";
      echo "----- COM3-01-24 -----";
      echo "pse124";
      echo "";
      echo "----- COM4 Level 2 -----";
      echo "psf204";
      # EXIT EARLY
      exit;
      ;;
    --filename|-f)
      shift;
      FILENAME=$1;
      echo "\e[0;35mDBG\e[0m FILENAME: ${FILENAME}";
      ;;
     --printer|-p)
       shift;
       PRINTER=$1
       echo "\e[0;33m[!]\e[0m MODIFIED: Printer set to ${PRINTER}";
       ;;
     --user|-u)
       shift;
       NUSNET_ID=$1
       echo "\e[0;33m[!]\e[0m MODIFIED: User set to ${NUSNET_ID}";
  esac
  shift
done

# Check for filename, if blank, just exit
if [ -z "$FILENAME" ]
then
  echo "No filename. Use '-f <filename>' to specify file.";
  echo "Exiting.";
  exit
fi



# Print stuff for user to confirm
echo "--------------------------------------------------";
echo "NUSNET_ID: \e[40m\e[1;33m${NUSNET_ID}\e[0m";
echo "Printer:   \e[40m\e[1;33m${PRINTER}\e[0m";
echo "Filename:  \e[40m\e[1;33m${FILENAME}\e[0m";
echo "--------------------------------------------------";

echo "Generated command:"
echo "\e[40m\e[0;32msmbclient -U nusstu/${NUSNET_ID} //nts27.comp.nus.edu.sg/${PRINTER} -c \"print ${FILENAME}\"\e[0m";


# Get user confirmation
read -p "Confirm above command? [Y/n]: " yn
case $yn in 
  [Yy] )
    echo "Sending command, handing over to smbclient";
    smbclient -U nusstu/${NUSNET_ID} //nts27.comp.nus.edu.sg/${PRINTER} -c "print ${FILENAME}";;

  [Nn] )
    echo "Cancelled operation, exiting.";
    exit;;

   *)
     echo "Not an option. Exiting.";
     exit;;
esac
    
exit
