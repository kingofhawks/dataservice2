CREATE DATABASE DSCPDB DEFAULT CHARACTER SET utf8;

USE DSCPDB;

CREATE TABLE t_role (
  id int(11) NOT NULL AUTO_INCREMENT,
  osdb_role char(64) DEFAULT NULL,
  name char(64) NOT NULL,
  description varchar(100) DEFAULT NULL,
  create_at datetime NOT NULL,
  delete_at datetime DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE t_level (
  id int(11) NOT NULL AUTO_INCREMENT,
  levelName varchar(20) NOT NULL,
  demand varchar(100) DEFAULT NULL,
  privilege varchar(100) DEFAULT NULL,
  createTime datetime NOT NULL,
  cancelTime datetime DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE t_customer (
  id int(11) NOT NULL AUTO_INCREMENT,
  email char(50) DEFAULT NULL,
  name varchar(20) DEFAULT NULL,
  identification char(18) DEFAULT NULL,
  customerLevel int(11) DEFAULT 1,
  mobile char(20) DEFAULT NULL,
  address varchar(50) DEFAULT NULL,
  company varchar(50) DEFAULT NULL,
  create_at datetime NOT NULL,
  delete_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_customer (customerLevel),
  CONSTRAINT FK_customer FOREIGN KEY (customerLevel) REFERENCES t_level (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE t_account (
  id int(11) NOT NULL AUTO_INCREMENT,
  osdb_user char(64) DEFAULT NULL,
  loginName char(64) NOT NULL,
  loginPassword char(64) NOT NULL,
  email char(50) DEFAULT NULL,
  balance float(7,3) NOT NULL DEFAULT 0.000,
  master char(64) DEFAULT NULL,
  customerID int(11) DEFAULT NULL,
  create_at datetime NOT NULL,
  cancel_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_account_customer (customerID),
  CONSTRAINT FK_account_customer FOREIGN KEY (customerID) REFERENCES t_customer (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE t_tenant (
  id int(11) NOT NULL AUTO_INCREMENT,
  osdb_tenant char(64) DEFAULT NULL,
  name char(64) NOT NULL,
  description varchar(100) DEFAULT NULL,
  create_by int(11) DEFAULT NULL,
  create_at datetime NOT NULL,
  delete_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_tenant_owner (create_by),
  CONSTRAINT FK_tenant_owner FOREIGN KEY (create_by) REFERENCES t_account (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE t_turMap (
  id int(11) NOT NULL AUTO_INCREMENT,
  tenant int(11) NOT NULL,
  user int(11) NOT NULL,
  role int(11) NOT NULL,
  description varchar(100) DEFAULT NULL,
  create_at datetime DEFAULT NULL,
  delete_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_t_turMap_tenant (tenant),
  KEY FK_t_turMap_role (role),
  KEY FK_t_turMap (user),
  CONSTRAINT FK_t_turMap FOREIGN KEY (user) REFERENCES t_account (id),
  CONSTRAINT FK_t_turMap_role FOREIGN KEY (role) REFERENCES t_role (id),
  CONSTRAINT FK_t_turMap_tenant FOREIGN KEY (tenant) REFERENCES t_tenant (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into t_level values (1,'普通会员',null,null,'2013-3-1 0:0:0',null);
insert into t_role values 
(1,'5d54a59052844925920d70a9542cf6ba','admin','OpenStack admin','2013-03-01 0:00:00',null),
(2,'5d54a59052844925920d70a9542cf6ba','owner','主帐户默认角色','2013-03-01 0:00:00',null),
(3,'2969707884e84117bd764d865478a9e0','member','子帐户默认角色','2013-03-01 0:00:00',null);
