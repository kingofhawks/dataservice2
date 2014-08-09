# coding=utf-8
import time
import threading
import logging
import commands
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et
import osapi
import dao
from cluster import hadoopCluster

class controlThread(threading.Thread):
    def __init__(self, token, tenant, dpid, dpname, serverCount,
                 serverLabel, image, flavorURL,
                 files, algos, output,
                 serverMeta, hadoopMeta, nameIP):
        threading.Thread.__init__(self)
        self.dpid = dpid
        self.setName(dpname)
        self.hadoop = hadoopCluster(token, tenant, dpid, dpname, serverCount,
                                    serverLabel, image, flavorURL,
                                    files, algos, output,
                                    serverMeta, hadoopMeta, nameIP)
        self.thread_stop = False
    
    def run(self):
        # print self.hadoop.get_token()
        # print self.hadoop.get_tenant()
        # print self.hadoop.get_nameNode()
        # print self.hadoop.get_nameNode()['label']
        # print self.hadoop.get_nameNode()['image']
        # print self.hadoop.get_nameNode()['flavor']
        # print self.hadoop.get_dataNodeList()
        # print self.hadoop.get_clusterStatus()
        print self.hadoop.get_input()
        print self.hadoop.get_output()
        print self.hadoop.get_algos()
        
        print 'M:building-----------------------------------------------------------------------'
        flag_building = False
        interval = 0
        dppath = '/var/dscp/dp'
        hadoop_version = '1.1.2'
        print 'M:dpid:%s    datanodes:%d' % (
                                             self.hadoop.get_dpid(),
                                             len(self.hadoop.get_dataNodeList()))
        dao.data_process_add_message(self.hadoop.get_dpid(), 'start building', hadoop_version)
        if(flag_building):
            status, mes = osapi.server_create(self.hadoop.get_token(),
                                          self.hadoop.get_tenant(),
                                          self.hadoop.get_nameNode()['label'],
                                          self.hadoop.get_nameNode()['image'],
                                          self.hadoop.get_nameNode()['flavor'],
                                          {})
            # print 'M:namenode status:%s -- mes:%s' % (status, mes)
            dao.data_process_add_message(self.hadoop.get_dpid(),
                                       'namenode:%s' % self.hadoop.get_nameNode()['label'],
                                       mes)
            time.sleep(interval)
                # for i in range(interval):
                # time.sleep(1)
                # print 'M:wait %d' % (interval - i) 
            if(status == 200):
                self.hadoop.set_nameNodeID(mes)
                flag_building = flag_building and True
                # print 'M:launch namenode %s %s %s SUCCESSFUL.' % (
                                                           # self.hadoop.get_nameNode()['label'],
                                                           # status, mes)
                # print self.hadoop.get_nameNode()
            else:
                self.hadoop.set_nameNodeID('')
                flag_building = flag_building and False
                # print 'M:launch namenode %s ERROR' % self.hadoop.get_nameNode()['label']
        else:
            print 'skipped.'
        
        if(flag_building):
            for dataNode in self.hadoop.get_dataNodeList():
                status, mes = osapi.server_create(self.hadoop.get_token(),
                                              self.hadoop.get_tenant(),
                                              dataNode['label'],
                                              dataNode['image'],
                                              dataNode['flavor'],
                                              {})
                # print 'M:datanode status:%s -- mes:%s' % (status, mes)
                dao.data_process_add_message(self.hadoop.get_dpid(),
                                           'datanode:%s' % dataNode['label'],
                                           mes)
                time.sleep(interval)
                # for i in range(interval):
                    # time.sleep(1)
                    # print 'M:wait %d' % (interval - i)
                if(status == 200):
                    self.hadoop.set_dataNodeID(dataNode['label'], mes)
                    # print 'M:launch datanode %s %s %s SUCCESSFUL.' % (
                                                                # dataNode['label'],
                                                                # status, mes)
                else:
                    self.hadoop.set_dataNodeID(dataNode['label'], '')
                    # print 'M:launch datanode %s %s %s FAILED' % (
                                                           # dataNode['label'],
                                                           # status, mes)
        else:
            print 'skipped.'
        
        # print 'M:servers launch requested completed.'
        # print self.hadoop.get_nameNode()
        # print self.hadoop.get_dataNodeList()
        dao.data_process_add_message(self.hadoop.get_dpid(),
                                       'serverStatus',
                                       str({'namenode':self.hadoop.get_nameNode(),
                                            'datanode':self.hadoop.get_dataNodeList()}))
        time.sleep(10)
        if(flag_building):
            active = 0
            t = 30 * 60 * (len(self.hadoop.get_dataNodeList()) + 1) / 5
            while(t > 0 and active < (len(self.hadoop.get_dataNodeList()) + 1)):
                # print 'M:check %d' % t
                t = t - 1
                active = 0
                serverList = osapi.server_list(self.hadoop.get_token(), self.hadoop.get_tenant())
                # print 'M:len(serverList):%d' % len(serverList)
                for server in serverList:
                    # print 'M:server name status: %s %s' % (server['name'], server['status'])
                    if server['id'] == self.hadoop.get_nameNode()['serverID']:
                        # print 'M:nameNode %s %s' % (server['name'], server['id'])
                        # print 'M:%s : %s' % (self.hadoop.get_nameNode()['label'], server['status'])
                        self.hadoop.set_nameNodeStatus(server['status'])
                        if(server['status'] == 'ACTIVE'):
                            active = active + 1
                    for node in self.hadoop.get_dataNodeList():
                        if server['id'] == node['serverID']:
                            # print 'M:%s : %s' % (node['label'], server['status'])
                            self.hadoop.set_dataNodeStatus(node['label'], server['status'])
                            if(server['status'] == 'ACTIVE'):
                                active = active + 1
                print 'M:active:%d/%d' % (active, (len(self.hadoop.get_dataNodeList()) + 1))
                dao.data_process_add_message(self.hadoop.get_dpid(),
                                       'serverStatus',
                                       str({'namenode':self.hadoop.get_nameNode(),
                                            'datanode':self.hadoop.get_dataNodeList()}))
                time.sleep(10)
            if active == (len(self.hadoop.get_dataNodeList()) + 1):
                flag_building = flag_building and True
            else:
                flag_building = flag_building and False
        else:
            # print 'M:building flag is false,out of check.'
            dao.data_process_add_message(self.hadoop.get_dpid(),
                                           'check launch',
                                           'not all nodes actived.')
        
        if(flag_building):
            if dao.data_process_status_change(self.hadoop.get_dpid(), 'setting'):
                print 'M:cluster server launch successful.'
            else:
                print 'M:cluster status change failed.'
        else:
            print 'M:ERROR occurd while launching cluster servers.'
                
        print 'M:setting-----------------------------------------------------------------------'
        flag_setting = flag_building
        status, reason = osapi.floating_ip_associate(self.hadoop.get_token(),
                                                     self.hadoop.get_tenant(),
                                                     self.hadoop.get_nameIP(),
                                                     self.hadoop.get_nameNode()['serverID'])
        if(status == 202):
            print 'M:associate successful.'
            flag_setting = flag_setting and True
            dao.data_process_add_message(self.hadoop.get_dpid(),
                                           'associate',
                                           'associate successful.')
        else:
            print 'M:associate failed.'
            flag_setting = flag_setting and False
            dao.data_process_add_message(self.hadoop.get_dpid(),
                                           'associate',
                                           'associate failed.')
        time.sleep(2)
        
        serverDetailList = osapi.server_list(self.hadoop.get_token(), self.hadoop.get_tenant())
        if(flag_setting):
            s, o = commands.getstatusoutput('mkdir %s/dpid_%s' % (dppath, self.hadoop.get_dpid())) 
            if (s == 0):
                print 'M:mkdir for dp successful.'
                flag_setting = flag_setting and True
            else:
                print 'M:mkdir for dp failed.'
                flag_setting = flag_setting and False
            time.sleep(2)
        else:
            print 'M:mkdir skipped.'
        
        if(flag_setting):
            com = 'cp -r %s/hadoop-%s/conf/ %s/dpid_%s/' % (dppath, hadoop_version, dppath,
                                                            self.hadoop.get_dpid())
            s, o = commands.getstatusoutput(com)
            if (s == 0):
                print 'M:copy conf files successful.'
                flag_setting = flag_setting and True
            else:
                print 'M:copy conf files failed.'
                flag_setting = flag_setting and False
            time.sleep(2)
        else:
            print 'M:copy conf skipped.'
        
        if(flag_setting):
            tree = et.parse('%s/dpid_%s/conf/core-site.xml' % (dppath, self.hadoop.get_dpid()))
            root = tree.getroot()
            for child in root:
                if(child[0].text == 'fs.default.name'):
                    for server in serverDetailList:
                        if server['id'] == self.hadoop.get_nameNode()['serverID']:
                            child[1].text = 'hdfs://%s:8020/' % (server['addresses']['private'][0]['addr'])
            tree.write('%s/dpid_%s/conf/core-site.xml' % (dppath, self.hadoop.get_dpid()),
                       encoding='utf-8')
            print 'M:core-site.xml configured.'
            time.sleep(2)

            tree = et.parse('%s/dpid_%s/conf/mapred-site.xml' % (dppath, self.hadoop.get_dpid()))
            root = tree.getroot()
            for child in root:
                if(child[0].text == 'mapred.job.tracker'):
                    for server in serverDetailList:
                        if server['id'] == self.hadoop.get_nameNode()['serverID']:
                            child[1].text = '%s:8021' % (server['addresses']['private'][0]['addr'])
            tree.write('%s/dpid_%s/conf/mapred-site.xml' % (dppath, self.hadoop.get_dpid()),
                       encoding='utf-8') 
            print 'M:mapred-site.xml configured.'
            time.sleep(2)
            
            file = open('%s/dpid_%s/conf/masters' % (dppath, self.hadoop.get_dpid()), 'r+')
            for server in serverDetailList:
                if server['id'] == self.hadoop.get_nameNode()['serverID']:
                    file.write(server['addresses']['private'][0]['addr'])
            file.write('\n')
            file.close()
            print 'M:masters configured.'
            time.sleep(2)
            
            file = open('%s/dpid_%s/conf/slaves' % (dppath, self.hadoop.get_dpid()), 'r+')
            for node in self.hadoop.get_dataNodeList():
                for server in serverDetailList:
                    if node['serverID'] == server['id']:
                        file.write(server['addresses']['private'][0]['addr'] + '\n')
            file.close()
            print 'M:slaves configured.'
            time.sleep(2)
            
            rsa = ' ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAnV31+ikERbBh6WHoOBbY2z0gGC07jSdPMUui1Ez+0BT87+BoDaL3lykgVpQ73DdbL5+AxFR6yixDSFgd2Bd447mbm1ml0hN1i5besWmHv41r95A9bsrCrhe8USMs0Whnt3E/GDlmFWavlDRGyOtKmDiv3xA0M6EaoXwkGiDUF9cMqfUHDAAng0hqXpX8pPqVQkvmvx6b7Y1wBBtPB6CltdwNeOxnJ79nBIRKpyeuI2sfMGSh4E2BypD3iNsQ5KYaBMHQEr1RCin12NhLY4Kc/v2z0cbaJ86hBsbiQNZ+hHDfLbWUj+so/lzLgaGJxOrFimZzmlaMMxSxWqrHqEQxgw=='
            file = open('/root/.ssh/known_hosts', 'r+')
            file.read()
            file.write('%s%s\n' % (self.hadoop.get_nameIP(), rsa))
            file.close()
            print 'M:ssh known hosts configured.'
            dao.data_process_add_message(self.hadoop.get_dpid(),
                                           'configure environment',
                                           'successful')
            time.sleep(2)
        else:
            dao.data_process_add_message(self.hadoop.get_dpid(),
                                           'configure environment',
                                           'skipped')
            print 'M:set file skipped.'
        
        if(flag_setting):
            com = 'scp -r %s/hadoop-%s/* %s@%s:%s' % (dppath,
                                                      hadoop_version,
                                                      'grid',
                                                      self.hadoop.get_nameIP(),
                                                      '/home/grid/hadoop/')
            print com
            s, o = commands.getstatusoutput(com)
            print s, o
            if(s == 0):
               print 'M:copy hadoop core files to namenode successful.'
               flag_setting = flag_setting and True
            else:
               print 'M:copy hadoop core files to namenode failed.'
               flag_setting = flag_setting and False
            time.sleep(2)
            
            com = 'scp -r %s/dpid_%s/conf/ %s@%s:%s' % (dppath,
                                                        self.hadoop.get_dpid(),
                                                        'grid',
                                                        self.hadoop.get_nameIP(),
                                                        '/home/grid/hadoop/')
            print com
            s, o = commands.getstatusoutput(com)
            print s, o
            if(s == 0):
               dao.data_process_add_message(self.hadoop.get_dpid(),
                                              'copy file to namenode',
                                              'successful')
               print 'M:copy hadoop conf files to namenode successful.'
               flag_setting = flag_setting and True
            else:
               dao.data_process_add_message(self.hadoop.get_dpid(),
                                              'copy file to namenode',
                                              'failed')
               print 'M:copy hadoop conf files to namenode failed.'
               flag_setting = flag_setting and False
        else:
            dao.data_process_add_message(self.hadoop.get_dpid(),
                                              'copy file to namenode',
                                              'skipped')
            print 'M:copy files to namenode skipped.'
        
        if(flag_setting):
            for node in self.hadoop.get_dataNodeList():
                for server in serverDetailList:
                    if node['serverID'] == server['id']:
                        com = 'ssh %s@%s scp -r /home/grid/hadoop/* %s@%s:%s' % (
                                'grid', self.hadoop.get_nameIP(),
                                'grid', server['addresses']['private'][0]['addr'],
                                '/home/grid/hadoop/')
                        print 'M:copy to datanode : ' + com
                        s, o = commands.getstatusoutput(com)
                        print s, o
                        if(s == 0):
                            dao.data_process_add_message(self.hadoop.get_dpid(),
                                                           'copy file to datanode %s' % node['label'],
                                                           'successful')
                            print 'M:copy files to datanode %s successful.' % node['label']
                            flag_setting = flag_setting and True
                        else:
                            dao.data_process_add_message(self.hadoop.get_dpid(),
                                                           'copy file to datanode %s' % node['label'],
                                                           'failed')
                            print 'M:copy files to datanode %s failed.' % node['label']
                            flag_setting = flag_setting and False
                        time.sleep(2)
        else:
            print 'M:copy files to datanode skipped.'
        
        if(flag_building):
            if dao.data_process_status_change(self.hadoop.get_dpid(), 'running'):
                print 'M:cluster setting successful.'
            else:
                print 'M:cluster status change failed.'
        else:
            print 'M:ERROR occurd while setting cluster servers.'

        print 'M:running-----------------------------------------------------------------------'
        flag_running = flag_setting
        if(flag_running):
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    '/home/grid/hadoop/bin/hadoop namenode -format')
            s, o = commands.getstatusoutput(com)
            print com, s, o
            dao.data_process_add_message(self.hadoop.get_dpid(), 'namenode format : %s' % s, o)
            # if s == 0:
                # print 'M:namenode format successful.'
            # else:
                # print 'M:namenode format failed.'
            time.sleep(10)
        else:
            dao.data_process_add_message(self.hadoop.get_dpid(), 'namenode format', 'skipped')
            print 'M:namenode format skipped.'
        
        if(flag_running):
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    '/home/grid/hadoop/bin/start-all.sh')
            s, o = commands.getstatusoutput(com)
            print com, s, o
            dao.data_process_add_message(self.hadoop.get_dpid(), 'start daemons : %s' % s, o)
            # if s == 0:
                # print 'M:start all successful.'
            # else:
                # print 'M:start all failed.'
            time.sleep(10)
        else:
            dao.data_process_add_message(self.hadoop.get_dpid(), 'start daemons', 'skipped')
            print 'M:start all daemon skipped.'
        
        print 'M:control thread stop-----------------------------------------------------------------------'    
        
        dao.data_process_add_message(self.hadoop.get_dpid(), 'prepare space for files.', '')
        if(flag_running):
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    'mkdir /home/grid/%s_input' % (self.hadoop.get_dpname()))
            s, o = commands.getstatusoutput(com)
            print com, s, o
        else:
            print 'M:make input dir skipped.'
        
        if(flag_running):
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    'mkdir /home/grid/%s_algo' % (self.hadoop.get_dpname()))
            s, o = commands.getstatusoutput(com)
            print com, s, o
        else:
            print 'M:make algo dir skipped.'
        
        if(flag_running):
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    'mkdir /home/grid/%s_output' % (self.hadoop.get_dpname()))
            s, o = commands.getstatusoutput(com)
            print com, s, o
        else:
            print 'M:make output dir skipped.'
        time.sleep(2)
        
        dao.data_process_add_message(self.hadoop.get_dpid(), 'prepare required files.', '')
        if(flag_running):
            for file in self.hadoop.get_input():
                temp = file.split(file)
                name = temp[len(temp) - 1]
                com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                        '''curl -X GET  
                                        -H "X-Auth-Token: %s" 
                                        http://192.168.0.55:8888/v1/AUTH_%s/%s  
                                        > /home/grid/%s_input/%s''' % (
                                                                       self.hadoop.get_token(),
                                                                       self.hadoop.get_tenant(),
                                                                       file,
                                                                       self.hadoop.get_dpname(),
                                                                       name
                                                                       )
                                        )
                s, o = commands.getstatusoutput(com)
                print com, s, o
        else:
            print 'download input files skipped.'

        if(flag_running):
            path, algo_name = self.hadoop.get_algos()
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    '''curl -X GET 
                                    -H "X-Auth-Token: %s" 
                                    http://192.168.0.55:8888/v1/AUTH_%s/%s 
                                    > /home/grid/%s_algo/%s''' % (
                                                                  self.hadoop.get_token(),
                                                                  self.hadoop.get_tenant(),
                                                                  path,
                                                                  self.hadoop.get_dpname(),
                                                                  algo_name
                                                                  )
                                    )
            s, o = commands.getstatusoutput(com)
            print com, s, o
        else:
            print 'download algo files skipped.'
        time.sleep(2)
        
        dao.data_process_add_message(self.hadoop.get_dpid(), 'hdfs setting.', '')
        if(flag_running):
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    '/home/grid/hadoop/bin/hadoop dfs -copyFromLocal %s %s' * (
                                    '/home/grid/%s_input/', '/'))
            s, o = commands.getstatusoutput(com)
            print com, s, o
        else:
            print 'M:hdfs setting skipped.'
        time.sleep(2)
        
        dao.data_process_add_message(self.hadoop.get_dpid(), 'start job.', '')
        if(flag_running):
            com = 'ssh %s@%s %s' % ('grid', self.hadoop.get_nameIP(),
                                    '/home/grid/hadoop/bin/hadoop jar %s %s' % (
                                    '/home/grid/%s_algo/%s' % (self.hadoop.get_dpname(), algo_name),
                                    '/%s_input /%s_output' % (self.hadoop.get_dpname())
                                    ))
            s, o = commands.getstatusoutput(com)
            print com, s, o
        else:
            dao.data_process_add_message(self.hadoop.get_dpid(), 'start job', 'skipped')
            print 'M:start job skipped.'
        
        self.thread_stop = True
        
    def stop(self):
        self.thread_stop = True

def hadoop(token, tenant, dpid, dpname, serverCount,
           serverLabel, image, flavorURL,
           files, algos, output,
           serverMeta, hadoopMeta, nameIP):
    hadoopControlThread = controlThread(token, tenant, dpid, dpname, serverCount,
                                        serverLabel, image, flavorURL,
                                        files, algos, output,
                                        serverMeta, hadoopMeta, nameIP)
    hadoopControlThread.start()
    
if __name__ == "__main__":
    token = '7868c61b37b840549d0cb68fd2a5b933'
    tenant = '86e5ae17b73749b3957886c5ad512ba0'
    dpid = 10
    dpname = 'testProcess'
    serverCount = 4
    
    serverLabel = 'testCluster'
    image = "http://192.168.0.50:9292/v2/images/15338178-650e-4602-aade-55089d5aecab"
    flavorURL = "http://192.168.0.51:8774/v2/%s/flavor/%s" % (tenant, '0')

    files = []
    algos = []
    output = ''
    
    serverMeta = 'defaultServerMeta'
    hadoopMeta = 'defaultHadoopMeta'
    
    dao.change()
    
    '''
    t1 = controlThread(token, tenant, dpid, dpname, serverCount,
                       serverLabel, image, flavorURL,
                       files, algos, output,
                       serverMeta, hadoopMeta)
    t1.start()
    '''
