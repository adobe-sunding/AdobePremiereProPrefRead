from lxml import etree, objectify

def parseXML(xmlFile):
    """Parse the XML File"""
    with open(xmlFile, 'rb') as f:
        xml = f.read()

    root = objectify.fromstring(xml)

    #   instanciating lists for the recent projects with dates
    date = []
    path = []

    # returns attributes in element nodes dict
    attrib = root.attrib

    # loop over elements and print their tags and text
    properties = dict()

    for setting in root.getchildren():
        # print(setting)
        for e in setting.getchildren():
            # print("%s => %s" % (e.tag, e.text))
            for p in e.getchildren():
                properties.update({p.tag:p.text})

    print()
    print(">>>> EDITOR NAME: ", properties['BE.Prefs.ProjectLocking.UserName'])
    print()
    print(">>>> Last Directory used: ", properties['be.prefs.last.used.directory'])
    print()
    print(">>>> Project Open in last ShutDown: ", properties['MZ.Prefs.ProjectsOpenAtLastShutdown'])
    print()
    # Scratch Disks
    for k, v in properties.items():
        if 'BE.Prefs.ScratchDisks.First' in k:
            print(">>>> Scratch Disks: ", k.split(".")[3][5:], v)
    print()
    # Recent projects with dates
    print(">>>> Recent projects with dates:  ")
    for k, v in properties.items():
        if 'BE.Prefs.MRU.Document.' in k and k.split(".")[4] != "Size":
            if k.split(".")[4] != "Date":
                path.append((k[-1], v))

            else:
                date.append((k[-1], v))
    dateS = sorted(date)
    pathS = sorted(path)
    for d, p in zip(dateS, pathS):
        print(d, p)
    print()
    # END Recent projects with dates

    # Last imported files
    for k, v in properties.items():
        if 'FE.DocumentManager.MRUImportFile' in k:
            print(">>>> Last imported files: ", v)
    print()

    #OMF.last.used.directory

    print(">>>> OMF last used directory : ", properties['OMF.last.used.directory'])
    print()

    # remove the py:pytype stuff
    objectify.deannotate(root)
    etree.cleanup_namespaces(root)
    obj_xml = etree.tostring(root.Preferences, pretty_print=True)


if __name__ == "__main__":
    file_name = input("Enter the full path to where the folder \"Adobe Premiere Pro Prefs\" can be seen: ")
    parseXML(file_name + "\Adobe Premiere Pro Prefs")
