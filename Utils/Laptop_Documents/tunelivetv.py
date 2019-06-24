################################################################################
#      This file is part of OpenELEC - http://www.openelec.tv
#      Copyright (C) 2009-2013 Stephan Raue (stephan@openelec.tv)
#      Copyright (C) 2013 Lutz Fiebach (lufie@openelec.tv)
#
#  This program is dual-licensed; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with OpenELEC; see the file COPYING.  If not, see
#  <http://www.gnu.org/licenses/>.
#
#  Alternatively, you can license this library under a commercial license,
#  please contact OpenELEC Licensing for more information.
#
#  For more information contact:
#  OpenELEC Licensing  <license@openelec.tv>  http://www.openelec.tv
################################################################################
# -*- coding: utf-8 -*-
import subprocess
import sys
import time
import random
import xbmc
import os
import re
import thread
import traceback
import register
import math


class tunelivetv:

    ENABLED = False
    
    process = None
    
    fpWrite = None
    
    flagForWizard = False
    
    menu = {'3': {
        'name': 32400,
        'menuLoader': 'menu_loader',
        'listTyp': 'tvlist',
        'InfoText': 32401,
        }}

    def __init__(self, oeMain):
        try:

            oeMain.dbg_log('tunelivetv::__init__', 'enter_function', 0)

            self.oe = oeMain
            self.controls = {}

            self.oe.dbg_log('tunelivetv::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tunelivetv::__init__', 'ERROR: (' + repr(e)
                            + ')')

    def menu_loader(self, menuItem):
        try:

            self.oe.dbg_log('tunelivetv::menu_loader', 'enter_function', 0)

            if len(self.controls) == 0:
                self.init_controls()

            self.oe.dbg_log('tunelivetv::menu_loader', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tunelivetv::menu_loader', 'ERROR: (' + repr(e)
                            + ')', 4)

    def exit_addon(self):
        try:

            self.oe.dbg_log('tunelivetv::exit_addon', 'enter_function', 0)
            
            self.stop_tune()
            
            self.oe.winOeMain.close()

            self.oe.dbg_log('tunelivetv::exit_addon', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tunelivetv::exit_addon', 'ERROR: (' + repr(e)
                            + ')')

    def init_controls(self):
        try:

            self.oe.dbg_log('tunelivetv::init_controls', 'enter_function', 0)
            
            self.stop_tune()

            self.oe.winOeMain.setProperty('w_scan_result', '')
            
            self.oe.dbg_log('tunelivetv::init_controls', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tunelivetv::init_controls', 'ERROR: ('
                            + repr(e) + ')')

    def exit(self):
        try:

            self.oe.dbg_log('tunelivetv::exit', 'enter_function', 0)
            
            self.stop_tune()

            for control in self.controls:
                try:
                    self.oe.winOeMain.removeControl(self.controls[control])
                except:
                    pass

            self.controls = {}

            self.oe.dbg_log('tunelivetv::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tunelivetv::exit', 'ERROR: (' + repr(e) + ')')

    def onClick(self, ControlID):
        if (ControlID == 1500):
            self.oe.dictModules['connman'].do_wizard()
	    self.oe.dictModules['connman'].refresh_network()
            self.oe.write_setting('tunelvetv', 'wizard_completed', 'True')
        if (ControlID == 1601):
            self.oe.dictModules['register'].do_wizard()
            
    def setFlagForWizard(self, flag):
        global flagForWizard
        if (flag):
            flagForWizard = True
        else:
            flagForWizard = False
        
            
    def do_wizard(self):
        try:
            global flagForWizard
            if (flagForWizard):
                self.oe.dbg_log('tunelivetv::do_wizard', 'enter_function', 0)
    
                self.oe.winOeMain.set_wizard_title('')
                self.oe.winOeMain.set_wizard_text('')
                self.oe.winOeMain.getControl(35040).setLabel('show')
                self.init_controls()		
    
                self.oe.dbg_log('tunelivetv::do_wizard', 'exit_function', 0)
                
                self.oe.winOeMain.f.write("In TUNE LIVE TV - Do Wizard\n")
                self.oe.winOeMain.f.flush()
                self.oe.winOeMain.getControl(1401).setLabel('')  
                self.oe.winOeMain.getControl(1402).setLabel('')  
                
                
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[1]['id']).setVisible(False)
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[5]['id']).setVisible(False)
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[7]['id']).setVisible(False)                          
                
                self.oe.winOeMain.showButton(1, 32303)
                self.oe.winOeMain.showButton(7, 32411)
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[1]['id']).setVisible(True)
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[7]['id']).setVisible(True)
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[1]['id']).controlLeft(self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[7]['id']))
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[7]['id']).controlRight(self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[1]['id']))
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[1]['id']).controlUp(self.oe.winOeMain.getControl(self.oe.winOeMain.radiobuttons[3]['id']))
                self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[7]['id']).controlUp(self.oe.winOeMain.getControl(self.oe.winOeMain.radiobuttons[3]['id']))
                #self.oe.winOeMain.buttons[7]['action'] = self.oe.dictModules['register'].do_wizard()
            else:
                self.oe.dictModules['connman'].setFlagForWizard(True)
                self.oe.dictModules['connman'].do_wizard()
                self.oe.dictModules['connman'].setFlagForWizard(False)
                        
        except Exception, e:
            
            self.oe.winOeMain.f.write("TUNE TV do_wiz exception " + repr(e) + traceback.format_exc() + "\n");
            self.oe.winOeMain.f.flush()
            
            self.oe.dbg_log('tunelivetv::do_wizard', 'ERROR: (' + repr(e)
                            + ')')


    def estScanTime(self,country_region):	
	return {
		'au-Melbourne' : 4*60,			
		'auto-tune-Australia' : 14*60,
	}.get(country_region, 15*60) #make the default unknown scanning 15 minutes
                            
    def tune(self,country_region):
        try:

            self.oe.dbg_log('tunelivetv::tune', 'enter_function', 0)

            self.oe.execute('vdr.stop', 0)
            self.oe.winOeMain.getControl(35042).setPercent(0)
            self.oe.winOeMain.setProperty('w_scan_result', 'Now tuning Seebo LiveTV. Please wait...')
            time.sleep(15)
            
            chunks = []
            chunks.append('/storage/.xbmc/addons/lib.multimedia.w_scan/bin/w_scan -f t -I /storage/.xbmc/addons/service.openelec.settings/dvb-t/')
            chunks.append(country_region)
            chunks.append(' > /storage/.xbmc/userdata/addon_data/service.multimedia.vdr-addon/config/channels.conf')
            command_line = ''.join(chunks)
            
            tmpFile = "/storage/.xbmc/temp/%d.tmp" % random.randint(10000,99999)
            fpWrite = open(tmpFile,'w')
            process = subprocess.Popen(command_line,stdout = subprocess.PIPE,stderr = fpWrite, shell=True);
            scanning = True
            estimate_scan_time = self.estScanTime(country_region) #estimate the scanning time
            start_scan = time.time()
            while process.poll() is None:
                fpRead = open(tmpFile,'r')
                lines = fpRead.readlines()
                for line in lines:  
                    print line
                    scan_percentage = (time.time() - start_scan) / estimate_scan_time * 100
                    if scan_percentage > 90:
                        scan_percentage = 90
                    self.oe.winOeMain.getControl(35042).setPercent(scan_percentage)
                    self.oe.dbg_log('tunelivetv::tune', line, 0)
                    
                    time_elapsed = time.time() - start_scan
                    
                    #if time_elapsed>=60:
                    #    mins = math.floor(time_elapsed/60)
                    #    secs = round(time_elapsed%60)
                    #    if mins<10:
                    #        if str(mins).endswith('.0'):
                    #            minsstr = str(mins)
                    #            mins = minsstr[:-2]
                    #        mins = '0'+str(mins)+':'
                    #    if secs<10:
                    #        secs = '0'+str(secs)
                    #else:
                    #    mins = '00:'
                    #   if time_elapsed>10:
                    #        secs = round(time_elapsed%60)
                    #    else:
                    #        secs = '0'+str(round(time_elapsed%60))
                    #
                    #timeElapsedinStr = str(mins)+str(secs)
                    #
                    #if timeElapsedinStr.endswith('.0'):
                    #    timeElapsedinStr = timeElapsedinStr[:-2]

	   	    mins = int(math.floor(time_elapsed/60))
                    secs = int(round(time_elapsed%60))	

		    if	mins==0:
			minsStr = '00'
		    elif (mins>0) and (mins<10) :
		        minsStr = '0' + str(mins)  
		    else:
		        minsStr  =  str(mins)

		    if  secs<10:
			secsStr = '0'+str(secs)
		    else:	
			secsStr = str(secs)
                    
                    timeElapsedinStr = minsStr + ':' + secsStr 

                    #self.oe.winOeMain.setProperty('w_scan_result', line)
                    self.oe.winOeMain.setProperty('w_scan_result', "Time Elapsed: " + timeElapsedinStr)
                if process.poll():
                    break
                fpWrite.truncate()
                fpRead.close()
                time.sleep(1)
            fpWrite.close()
            os.remove(tmpFile)
            self.oe.winOeMain.getControl(35037).setLabel('Tune')
            process = None
            self.oe.dbg_log('tunelivetv::tune', 'finished', 0)	    
            self.oe.winOeMain.setProperty('w_scan_result', 'Finished!')
            self.oe.winOeMain.getControl(35042).setPercent(100)                                 
            self.oe.execute('vdr.start', 0)
            xbmc.executebuiltin('ResetPVRDB')                         
            self.oe.dbg_log('tunelivetv::tune', 'exit_function', 0)
	    self.oe.dictModules['connman'].refresh_network()
        except Exception, e:
            self.oe.winOeMain.getControl(35037).setLabel('Tune')
            self.oe.dbg_log('tunelivetv::tune', 'ERROR: ('
                            + repr(e) + ')')
                            
    def stop_tune(self):
        try:

            self.oe.dbg_log('tunelivetv::stop_tune', 'enter_function', 0)
            
            if not self.process == None:
                self.process.kill()
                self.process = None
            if not self.fpWrite == None:
                self.fpWrite.close()
                self.fpWrite = None
            self.oe.winOeMain.setProperty('w_scan_result', 'stopped')

            self.oe.dbg_log('tunelivetv::stop_tune', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tunelivetv::stop_tune', 'ERROR: ('
                            + repr(e) + ')')
