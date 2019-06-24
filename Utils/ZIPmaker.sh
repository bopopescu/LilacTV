clear
echo "  ****************************************************************************"
echo "  **                                                                        **"
echo "  **                           Update.zip maker                             **"
echo "  **                                                                        **"
echo "  **                                                           by Bad Jin   **"
echo "  ****************************************************************************"

if [ -z "$1" ]; then
  clear
  echo "#########################################################"
  echo "# please execute with a device and version as option    #"
  echo "# example: ./Zipmaker.sh Kor 1.0.3                      #"
  echo "#########################################################"
  exit 1
fi

Device="S905"
Language="$1"
Version="$2"

targetZIP=$Device-$Language-$Version-update.zip

base=`pwd`
AddonHome=${base}/../backuptar/${Device}
KernelHome=${base}/../LibreELEC.tv
cd $AddonHome

workingPos=$AddonHome/AmlogicOTA
targetPos=$AddonHome/${Language}_${Version}
tarballPos=$AddonHome/bktarball_${Language}

installer_path=$workingPos/install
AML_PKG_DIR=$workingPos/aml_recovery

if [ ! -f "$targetPos/$Device-$Language-$Version.tar" ]; then
  echo "Copy System tarbar..."
  cp ${KernelHome}/target/$Device-$Language-$Version.tar $targetPos
fi

if [ ! -d "$targetPos/$Device-$Language-$Version" ]; then
  cd $targetPos
  tar -xf $Device-$Language-$Version.tar
  cd $AddonHome
fi

sourcePos=$targetPos/$Device-$Language-$Version/target

mkdir -p $AML_PKG_DIR/system

echo "Copy logo.img..."
cp -f $installer_path/files/logo.img $AML_PKG_DIR/logo.img

mkdir -p $AML_PKG_DIR/META-INF/com/google/android
mkdir -p $AML_PKG_DIR/recovery/etc
echo "Copy System files..."
cp -f $installer_path/update-binary $AML_PKG_DIR/META-INF/com/google/android
cp -f $installer_path/updater-script $AML_PKG_DIR/META-INF/com/google/android
	
cp -f $sourcePos/KERNEL $AML_PKG_DIR
cp -f $sourcePos/SYSTEM $AML_PKG_DIR/system/SYSTEM
cp -f $sourcePos/KERNEL.md5 $AML_PKG_DIR
cp -f $sourcePos/SYSTEM.md5 $AML_PKG_DIR

cp -f $tarballPos/backup.tar.bz2 $AML_PKG_DIR
cp -f $tarballPos/backup.tar.bz2.md5 $AML_PKG_DIR
cp -f $targetPos/update.tar.bz2.md5 $AML_PKG_DIR

# create the update package
pushd "$AML_PKG_DIR" > /dev/null
zip -rq update.zip *

echo "Signing the update package"
mkdir -p sign

SIGNAPK_DIR="$workingPos/signapk"

java -Xmx2048m -jar $SIGNAPK_DIR/signapk.jar -w $SIGNAPK_DIR/testkey.x509.pem $SIGNAPK_DIR/testkey.pk8 update.zip sign/$targetZIP

# copy update package to target directory
echo "copy $targetZIP to $targetPos"
cp sign/$targetZIP $targetPos
popd > /dev/null

rm -rf $AML_PKG_DIR

echo "Done!"
