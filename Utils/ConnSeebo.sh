#!/bin/sh
clear
echo "  ****************************************************************************"
echo "  **                                                                        **"
echo "  **                        Connect to Seebo Mini                           **"
echo "  **                                                                        **"
echo "  **                                                           by Bad Jin   **"
echo "  ****************************************************************************"

tIP="$1"
password="SetFree123"
ssh-keygen -f ~/.ssh/known_hosts -R ${tIP}
sshpass -p ${password} ssh -o StrictHostKeyChecking=no root@${tIP}
