#!/bin/sh

NUSNET_ID="e1234567"
PRINTER="pstsc"

# Check if user provided arg
if [ "$#" -eq 0 ]; then
  echo "Missing filename to print."
  echo "Usage: ./printscript.sh <filename>"
  exit
fi

# Print stuff for user to confirm
echo "--------------------------------------------------"
echo "NUSNET_ID: $NUSNET_ID"
echo "Printer:   $PRINTER"
echo "Filename:  $1"
echo "--------------------------------------------------"

echo "Generated command:"
echo "smbclient -U nusstu/$NUSNET_ID //nts27.comp.nus.edu.sg/$PRINTER -c \"print $1\""


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
    
exit
