# coding=utf-8
class Customer:
    id = ''
    osdb_user = ''
    loginName = ''
    loginPass = ''
    isOwner = ''
    create_at = ''
    delete_at = ''
    email = ''
    customerName = ''
    identification = ''
    customerLevel = ''
    customerBalance = ''
    mobile = ''
    address = ''
    company = ''
    
    def __init__(self):
        self.id = ''
    
    def set_lle(self, loginName, loginPass, email):
        self.loginName = loginName
        self.loginPass = loginPass
        self.email = email
    
    def get_loginName(self):
        return self.loginName
    
    def get_loginPass(self):
        return self.loginPass
    
    def get_email(self):
        return self.email
    

if __name__ == '__main__':
    abc = Customer()
    abc.setNewCustomer('aa', 'bb', 'cc')
    print abc.get_loginName()
#
#
#
#
#
