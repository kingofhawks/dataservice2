from xml.dom import minidom

def testXML(xmlfile):
    '''
    <?xml version="1.0"?><?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    <configuration><property>
    <name>fs.default.name</name><value></value></property><property>
    <name>hadoop.tmp.dir</name><value>/home/grid/hadoop/run/tmp_dir</value>
    </property></configuration>
    '''
    
    print xmlfile
    dom = minidom.parse(xmlfile)
    root = dom.documentElement
    propertys = root.getElementsByTagName('property')
    
    for property in propertys:
        print '----------------------------'
        print property.nodeName
        print property.toxml()
        name = property.getElementsByTagName('name')
        value = property.getElementsByTagName('value')

if __name__ == "__main__":
    testXML('/usr/share/dataService/dataService2/dataService2/hao/hadoop/conf/core-site.xml')
