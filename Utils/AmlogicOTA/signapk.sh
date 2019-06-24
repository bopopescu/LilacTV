clear
echo "  ****************************************************************************"
echo "  **                                                                        **"
echo "  **                                Sign APK                                **"
echo "  **                                                                        **"
echo "  **                                                           by Bad Jin   **"
echo "  ****************************************************************************"

if [ -z "$1" ]; then
  clear
  echo "#########################################################"
  echo "# please execute with a device and version as option    #"
  echo "# example: ./signapk.sh your_apk                        #"
  echo "#########################################################"
  exit 1
fi

apk="$1"
SIGNAPK_DIR="signapk"

java -Xmx2048m -jar $SIGNAPK_DIR/signapk.jar -w $SIGNAPK_DIR/platform.x509.pem $SIGNAPK_DIR/platform.pk8 $apk signed/$apk


echo "Done!"
