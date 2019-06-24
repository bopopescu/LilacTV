clear
echo "  ****************************************************************************"
echo "  **                                                                        **"
echo "  **                     Seebo Create backup.tar.bz2                        **"
echo "  **                                                                        **"
echo "  **                                                           by Bad Jin   **"
echo "  ****************************************************************************"

if [ -z "$1" ]; then
  clear
  echo "#########################################################"
  echo "# please execute with your target Ip address            #"
  echo "# example: ./backup_maker.sh 17.3                       #"
  echo "#########################################################"
  exit 1
fi

Project="S905"
Language="$1"

base=`pwd`
AddonHome=${base}/../backuptar/${Project}
target=${AddonHome}/bktarball_${Language}

cd $target

tar cjfv backup.tar.bz2 .kodi
#clear
md5sum -t backup.tar.bz2 > backup.tar.bz2.md5

mv .kodi all.kodi
mv update.kodi .kodi

tar cjfv update.tar.bz2 .kodi
#clear
echo " "
echo " "
echo "=== Finished to compress for >>update&backup<< tarball"
echo " "
md5sum -t update.tar.bz2 > update.tar.bz2.md5

mv .kodi update.kodi
mv all.kodi .kodi

echo " "
echo "=== Complete to create tarball for $Project $Language"
