# coding=utf-8
import osapi
import logging

class hadoopCluster:
    token = ''
    tenant = ''
    dpid = ''
    dpName = ''
    clusterStatus = ''
    serverLabel = ''
    nameNode = {}
    dataNode = {}
    dataNodeList = []
    hadoopVersion = ''
    hadoopMeta = ''
    serverMeta = ''
    nameIP = ''
    
    def __init__(self, token, tenant, dpid, dpname, serverCount,
                 serverLabel, image, flavorURL,
                 files, algos, output,
                 serverMeta, hadoopMeta, nameIPvalue):
        self.token = token
        self.tenant = tenant
        self.dpid = dpid
        self.dpName = dpname
        self.clusterStatus = 'building'
        self.serverLabel = serverLabel
        self.nameIP = nameIPvalue
        self.input = files.split(';')
        self.algos = algos.split(';')
        self.output = output
        self.nameNode = {
                         'image':image,
                         'flavor':flavorURL,
                         'label':serverLabel + '_0',
                        }
        i = 0
        for i in range(serverCount - 1):
            labelt = serverLabel + '_' + str(i + 1)
            self.dataNodeList.append({
                                      'image':image,
                                      'flavor':flavorURL,
                                      'label':labelt,
                                      })

    def get_token(self):
        return self.token
    
    def get_tenant(self):
        return self.tenant
    
    def get_dpid(self):
        return self.dpid
    
    def get_dpname(self):
        return self.dpName
    
    def get_nameNode(self):
        return self.nameNode
    
    def get_nameIP(self):
        return self.nameIP
    
    def set_nameNodeID(self, id):
        self.nameNode.setdefault('serverID', id)
        
    def set_nameNodeStatus(self, status):
        self.nameNode.setdefault('status', status)
    
    def get_dataNodeList(self):
        return self.dataNodeList
    
    def get_input(self):
        return self.input
    
    def get_output(self):
        return self.output
    
    def get_algos(self):
        path = file.split(self.algos)
        temp = path.split('/')
        name = temp[len(temp) - 1]
        return path, name
    
    def set_dataNodeID(self, name, id):
        for dataNode in self.dataNodeList:
            if dataNode['label'] == name:
                dataNode.setdefault('serverID', id)
    
    def set_dataNodeStatus(self, name, status):
        for dataNode in self.dataNodeList:
            if dataNode['label'] == name:
                dataNode.setdefault('status', status)
    
    def set_clusterStatus(self, status):
        self.clusterStatus = status

    def get_clusterStatus(self):
        return self.clusterStatus
    
    '''
    def get_cluster_info(self):
        print 'name:%s' % self.clusterName
        print 'token:%s' % self.token
        print 'tenant:%s' % self.tenant

    def get_dataNode(self):
        print 'dataNode:::'
        for dn in self.dataNodeList:
            print dn
    '''

if __name__ == "__main__":
    print 'hello'
