'''
Created on 2013-5-15

@author: YUWANG
'''
from django.db import models
from hashlib import md5


'''
system admins are represented by this model.
'''

'''
create table sysAdmin(id char(30) primary key,name varchar(100),password varchar(128),email varchar(50),adminGroupId char(30))
create table adminGroup(id char(30) primary key,name varchar(100),comment text)
'''


class sysAdmin(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=50)
    adminGroupId = models.CharField(max_length=30)

    def md5_password(self, password):
        pwd_md5 = md5()
        pwd_md5.update(password)
        return pwd_md5.hexdigest()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "sysAdmin"
        ordering = ['id']


class adminGroup(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    comment = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "adminGroup"
        ordering = ['id']

""" customer """
'''
create table customer(id char(30) primary key,
                      name varchar(100),
                      contactName varchar(20),
                      identification char(20),
                      tel char(20),
                      email varchar(50),
                      address varchar(200),
                      post int(6),
                      createDate date,
                      cancelDate date,
                      is_enterprise char(1),
                      customerGroupId char(30)
                      );

create table account(id char(30) primary key,
                    customerId char(30),
                    payKey char(10),
                    openDate date,
                    openInfo varchar(300),
                    balance int,
                    cancelDate date,
                    comment text);
'''


class customer(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    contactName = models.CharField(max_length=20)
    identification = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    post = models.IntegerField(max_length=6)
    createDate = models.DateField()
    cancelDate = models.DateField()
    is_enterprise = models.CharField(max_length=1)
    customerGroupId = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "customer"
        ordering = ['id']


class account(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    customerId = models.CharField(max_length=30)
    payKey = models.CharField(max_length=10)
    openDate = models.DateField()
    openInfo = models.CharField(max_length=300)
    balance = models.IntegerField()
    cancelDate = models.DateField()
    comment = models.TextField()

    class Meta:
        db_table = "account"
        ordering = ['id']

'''
create table customerGroup(id char(30) primary key,name varchar(100),comment text);

create table groupDiscountService (id char(30) primary key,customerGroupId char(30),discountId char(30),productId char(30));
'''


class customerGroup(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    discountId = models.CharField(max_length=30)
    productId = models.TextField()
    comment = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "customerGroup"
        ordering = ['id']


"""
create table discount(id char(30) primary key,discount float(3,2),isActive char(1),comment text)
create table package(id char(30)primary key,name varchar(100),packageDetail text,price int,isActive char(1),comment text)
"""


class discount(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    discountValue = models.DecimalField(max_digits=3, decimal_places=2)
    isActive = models.CharField(max_length=1)
    comment = models.TextField()

    class Meta:
        db_table = "discount"
        ordering = ['id']


class package(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    packageDetail = models.TextField()
    timeLimit = models.CharField(max_length=10)
    price = models.FloatField()
    isActive = models.CharField(max_length=1)
    comment = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "package"
        ordering = ['id']

'''
create table serviceCategory(id char(30) primary key,name varchar(100),comment text);

create table productCategory(id char(30) primary key,name varchar(100),serviceCategoryId char(30),comment text);

create table product(id char(30) primary key,name varchar(100),productCategoryId char(30),isActive tinyint(1),path varchar(200),price int,unit char(20),comment text);
'''


class serviceCategory(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    comment = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "serviceCategory"
        ordering = ['id']


class productCategory(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    serviceCategoryId = models.CharField(max_length=30)
    comment = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "productCategory"
        ordering = ['id']


class product(models.Model):
    #id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    productCategoryId = models.CharField(max_length=30)
    isActive = models.CharField(max_length=1)
    path = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    unit = models.CharField(max_length=20)
    comment = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "product"
        ordering = ['id']

"""
create table purchaseProduct(transactionId char(30) primary key, 
                            customerId char(30),
                            productId char(30),
                            discountValue float(3,2),
                            duration int,
                            quantity int,
                            transactionDate date,
                            comment text)
create table purchasePackage(transactionId char(30) primary key,
                            customerId char(30),
                            packageId char(30),
                            duration int,
                            quantity int,
                            transactionDate date,
                            comment text)

"""


class purchaseProduct(models.Model):
    transactionId = models.CharField(max_length=30, primary_key=True)
    customerId = models.CharField(max_length=30)
    productId = models.CharField(max_length=30)
    discountValue = models.DecimalField(max_digits=3, decimal_places=2)
    duration = models.IntegerField()
    quantity = models.IntegerField()
    transactionDate = models.DateField()
    comment = models.TextField()

    class Meta:
        db_table = "purchaseProduct"
        ordering = ['transactionDate']


class purchasePackage(models.Model):
    transactionId = models.CharField(max_length=30, primary_key=True)
    customerId = models.CharField(max_length=30)
    packageId = models.CharField(max_length=30)
    duration = models.IntegerField()
    quantity = models.IntegerField()
    transactionDate = models.DateField()
    comment = models.TextField()

    class Meta:
        db_table = "purchasePackage"
        ordering = ['transactionDate']

"""
create table transactionBill (transactionId char(30) primary key,accountId char(30), item varchar(300),deposit int,expense int,transactionDate date,comment text);
"""


class transactionBill(models.Model):
    transactionId = models.CharField(max_length=30, primary_key=True)
    accountId = models.CharField(max_length=30)
    item = models.CharField(max_length=300)
    deposit = models.IntegerField()
    expense = models.IntegerField()
    transactionDate = models.DateField()
    comment = models.TextField()

    class Meta:
        db_table = "transactionBill"
        ordering = ['transactionDate']
