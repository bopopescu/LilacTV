import os
import xml.etree.ElementTree as ET

def ChangeData_XML(xml_file,PTag,STag,value):

  doc = ET.parse(xml_file)
  root = doc.getroot()
  removeFlag = False

  for e in root.findall(PTag):
    if e.findtext(STag) != value:
      e.find(STag).text = value
      removeFlag = True

  for e in root.iter(STag):
    if e.attrib:
      e.attrib.pop('default', None)
      removeFlag = True

  if removeFlag:
    doc.write(xml_file, encoding="utf-8", xml_declaration=True)


if __name__=='__main__':

    settings_file = '/storage/.kodi/userdata/guisettings.xml'
    #Enable the 'RSS' feed
    ParentTag = 'lookandfeel'
    SubTag = 'enablerssfeeds'
    ChangeData_XML(settings_file, ParentTag, SubTag, 'True')

    #Change the skin size
    ParentTag = 'lookandfeel'
    SubTag = 'skinzoom'
    ChangeData_XML(settings_file, ParentTag, SubTag, '-4')

    #Change volume amp
    ParentTag = 'defaultvideosettings'
    SubTag = 'volumeamplification'
    ChangeData_XML(settings_file, ParentTag, SubTag, '10.000000')

    #Change zoomamount
    SubTag = 'viewmode'
    ChangeData_XML(settings_file, ParentTag, SubTag, '0')

    #Change zoomamount
    SubTag = 'zoomamount'
    ChangeData_XML(settings_file, ParentTag, SubTag, '1.000000')

    #Change brightness
    SubTag = 'brightness'
    ChangeData_XML(settings_file, ParentTag, SubTag, '55.000000')

    #Change Subtitle Addon
    ParentTag = 'subtitles'
    ChangeData_XML(settings_file, ParentTag, 'movie', 'service.subtitles.opensubtitles')
    ChangeData_XML(settings_file, ParentTag, 'tv', 'service.subtitles.opensubtitles')
