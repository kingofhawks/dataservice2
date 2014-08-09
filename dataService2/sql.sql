CREATE DATABASE DSCPDB DEFAULT CHARACTER SET utf8;

USE DSCPDB;

CREATE TABLE t_level (
  id int(11) NOT NULL AUTO_INCREMENT,
  levelName varchar(20) NOT NULL,
  demand varchar(100) DEFAULT NULL,
  privilege varchar(100) DEFAULT NULL,
  createTime datetime NOT NULL,
  cancelTime datetime DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

insert into t_level(id,levelName,demand,privilege,createTime,cancelTime) values (1,'普通会员',NULL,NULL,'2013-03-01 21:00:00',NULL);

CREATE TABLE t_role (
  id int(11) NOT NULL AUTO_INCREMENT,
  osdb_role char(64) DEFAULT NULL,
  name char(64) NOT NULL,
  description varchar(100) DEFAULT NULL,
  create_at datetime NOT NULL,
  delete_at datetime DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

insert into t_role(id,osdb_role,name,description,create_at,delete_at) values (1,'6ee6be09284545ba9c39e56f36c1bceb','admin','OpenStack admin','2013-03-01 12:00:00',NULL);
insert into t_role(id,osdb_role,name,description,create_at,delete_at) values (2,'6ee6be09284545ba9c39e56f36c1bceb','owner','主帐户默认角色','2013-03-01 12:00:00',NULL);
insert into t_role(id,osdb_role,name,description,create_at,delete_at) values (3,'075ef3a17ecd4fba95d00e44072d7fcb','member','子帐户默认角色','2013-03-01 12:00:00',NULL);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE t_customer (
  id int(11) NOT NULL AUTO_INCREMENT,
  email char(50) DEFAULT NULL,
  name varchar(20) DEFAULT NULL,
  identification char(18) DEFAULT NULL,
  customerLevel int(11) DEFAULT '1',
  mobile char(20) DEFAULT NULL,
  address varchar(50) DEFAULT NULL,
  company varchar(50) DEFAULT NULL,
  create_at datetime NOT NULL,
  delete_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_customer (customerLevel),
  CONSTRAINT FK_customer FOREIGN KEY (customerLevel) REFERENCES t_level (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE t_account (
  id int(11) NOT NULL AUTO_INCREMENT,
  osdb_user char(64) DEFAULT NULL,
  loginName char(64) NOT NULL,
  loginPassword char(64) NOT NULL,
  email char(50) DEFAULT NULL,
  balance float(7,3) NOT NULL DEFAULT '0.000',
  master char(64) DEFAULT NULL,
  customerID int(11) DEFAULT NULL,
  create_at datetime NOT NULL,
  delete_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_account_customer (customerID),
  CONSTRAINT FK_account_customer FOREIGN KEY (customerID) REFERENCES t_customer (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE t_dataProcessing (
  id int(11) NOT NULL AUTO_INCREMENT,
  processName varchar(64) DEFAULT NULL,
  tenant int(11) DEFAULT NULL,
  user int(11) DEFAULT NULL,
  algofile text,
  datafile text,
  output char(128) DEFAULT NULL,
  serverName char(64) DEFAULT NULL,
  serverCount int(11) DEFAULT NULL,
  serverConfig text,
  serverMeta text,
  hadoopMeta text,
  status char(20) DEFAULT NULL,
  create_at datetime DEFAULT NULL,
  end_at datetime DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_t_dataProcessing (tenant),
  KEY FK_t_dataProcessing_account (user),
  CONSTRAINT FK_t_dataProcessing FOREIGN KEY (tenant) REFERENCES t_tenant (id),
  CONSTRAINT FK_t_dataProcessing_account FOREIGN KEY (user) REFERENCES t_account (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into sysAdmin(id,name,password,adminGroupId) values(1,'admin','e10adc3949ba59abbe56e057f20f883e',1)