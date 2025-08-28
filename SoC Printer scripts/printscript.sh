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



# Check if user provided arg
if [ "$#" -eq 0 ]; then
  echo "Missing filename to print."
  echo "Usage: ./printscript.sh <filename>"
  exit
fi

FILENAME=$1;

# Check if user specified printer
shift
if [ "$#" != 0 ]; then
  PRINTER=$1;
fi

# Print stuff for user to confirm
echo "--------------------------------------------------"
echo "NUSNET_ID: $NUSNET_ID"
echo "Printer:   $PRINTER"
echo "Filename:  $FILENAME"
echo "--------------------------------------------------"

echo "Generated command:"
echo "smbclient -U nusstu/$NUSNET_ID //nts27.comp.nus.edu.sg/$PRINTER -c \"print $FILENAME\""


# Get user confirmation
read -p "Confirm above command? [Y/n]: " yn
case $yn in 
  [Yy] )
    echo "Sending command, handing over to smbclient";
    smbclient -U nusstu/${NUSNET_ID} //nts27.comp.nus.edu.sg/${PRINTER} -c "print ${1}";;

  [Nn] )
    echo "Cancelled operation, exiting.";
    exit;;

   *)
     echo "Not an option. Exiting.";
     exit;;
esac
    
echo "Have a good day ahead."
exit
