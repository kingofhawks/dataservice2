try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

def testXML(xmlfile):
    print xmlfile
    tree = et.parse(xmlfile)
    root = tree.getroot()
    print root
    for child in root:
        if(child[0].text == 'fs.default.name'):
            child[1].text = '192.168.0.1'

    for child in root:
        for c2 in child:
            print c2.tag, c2.text
    
    tree.write('out.xml', encoding='utf-8')

if __name__ == "__main__":
    # testXML('/usr/share/dataService/dataService2/dataService2/hao/hadoop/conf/core-site.xml')
    testXML('/root/Desktop/core-site.xml')
