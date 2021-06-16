---
title: Hive 安装和配置 (Hive Setup)
author: 范叶亮
date: '2021-06-14'
slug: hive-setup
categories:
  - Tech101
  - 编程
tags:
  - Hive
  - MySQL
  - MySQL JDBC Connector
---

文本使用的软件版本分别为：

1. JDK：1.8.0_291，[下载地址](https://www.oracle.com/cn/java/technologies/javase/javase-jdk8-downloads.html)。
2. Hadoop：3.2.2，[下载地址](https://hadoop.apache.org/releases.html)。
3. Hive：3.2.1，[下载地址](https://hive.apache.org/downloads.html)。
4. MySQL：8.0.25，使用 `apt install mysql-server` 安装。
5. MySQL JDBC Connector：8.0.25，[下载地址](https://dev.mysql.com/downloads/connector/j/)。

按照[虚拟环境准备 (Virtual Environment Preparation)](/tech101/2021/06/virtual-env-preparation/) 准备虚拟机列表如下：

| 主机名 | IP             | 角色                      |
| ------ | -------------- | ------------------------- |
| vm-01  | 192.168.56.101 | Hadoop<br/>MySQL<br/>Hive |
| vm-02  | 192.168.56.102 | Hadoop                    |
| vm-03  | 192.168.56.103 | Hadoop                    |

按照 [Hadoop 集群搭建 (Hadoop Cluster Setup)](/tech101/2021/06/hadoop-cluster-setup/) 搭建 Hadoop 集群。

## MySQL 安装和配置

通过如下命令安装 MySQL：

```shell
sudo apt install mysql-server mysql-client libmysqlclient-dev
```

安装完毕后，使用如下命令初始化 MySQL：

```shell
sudo mysql_secure_installation
```

在密码安全性校验步骤，输入 `N` 关闭密码安全性校验：

```
VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No: N
```

输入新密码：

```
New password: *********
Re-enter new password: *********
```

在删除匿名用户环节，输入 `Y` 删除匿名用户：

```
By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) : Y
```

输入 `N` 允许远程登录 `root` 用户：

```
Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) : N
```

输入 `N` 保留 `test` 数据库：

```
By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.

Remove test database and access to it? (Press y|Y for Yes, any other key for No) : N
```

输入 `Y` 应用设置并生效：

```
Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) : Y
```

修改 MySQL 配置文件：

```shell
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
```

将绑定地址替换为 `0.0.0.0`：

```txt
bind-address            = 0.0.0.0
mysqlx-bind-address     = 0.0.0.0
```

重启 MySQL 服务：

```shell
sudo service mysql restart
```

在本地通过如下命令并输入密码进入 MySQL：

```shell
sudo mysql -uroot -p
```

在 MySQL 命令行中输入如下语句为 `root` 用户配置允许远程访问：

```sql
CREATE USER 'root'@'%' IDENTIFIED BY '**********';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;
```

之后在宿主机通过如下命令即可登录虚拟机中的 MySQL：

```shell
mysql -h192.168.56.101 -uroot -p
```

为 Hive 创建数据库和用户，并设置相关权限：

```sql
CREATE DATABASE hive;
CREATE USER 'hive'@'%' IDENTIFIED BY '**********';
GRANT ALL PRIVILEGES ON hive.* TO 'hive'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;
```

## Hive 安装和配置

将 Hive 安装包解压缩到 `/opt` 目录并创建软链接：

```shell
cd /opt
tar -zxvf apache-hive-3.1.2-bin.tar.gz
ln -s /opt/apache-hive-3.1.2-bin /opt/hive
```

将如下信息添加到 `/etc/profile` 中：

```txt
# Hive
export HIVE_HOME=/opt/hive
export PATH=$PATH:$HIVE_HOME/bin
```

复制环境变量文件：

```shell
cp /opt/hive/conf/hive-env.sh.template /opt/hive/conf/hive-env.sh
```

修改 `hive-env.sh` 内容如下：

```bash
export JAVA_HOME=/opt/jdk
export HADOOP_HOME=/opt/hadoop
export HIVE_HOME=/opt/hive
export HIVE_CONF_DIR=$HIVE_HOME/conf
```

创建配置文件：

```shell
vi /opt/hive/conf/hive-site.xml
```

修改 `hive-site.xml` 内容如下：

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://vm-01:3306/hive</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.cj.jdbc.Driver</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hive</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>*********</value>
  </property>
</configuration>
```

将 MySQL JDBC Connector 解压缩到 `/opt/hive/lib` 中：

```shell
cd /opt
tar -zxvf mysql-connector-java-8.0.25.tar.gz
mv /opt/mysql-connector-java-8.0.25/mysql-connector-java-8.0.25.jar /opt/hive/lib
rm -rf /opt/mysql-connector-java-8.0.25
```

修正不兼容的依赖包：

```shell
mv /opt/hive/lib/log4j-slf4j-impl-2.10.0.jar /opt/hive/lib/log4j-slf4j-impl-2.10.0.jar.bak
mv /opt/hive/lib/guava-19.0.jar /opt/hive/lib/guava-19.0.jar.bak
cp /opt/hadoop/share/hadoop/common/lib/guava-*.jar /opt/hive/lib
```

初始化元数据：

```shell
schematool -dbType mysql -initSchema
```

出现如下输出时表示元数据初始化成功：

```
Metastore connection URL:	 jdbc:mysql://vm-01:3306/hive
Metastore Connection Driver :	 com.mysql.cj.jdbc.Driver
Metastore connection User:	 hive
Starting metastore schema initialization to 3.1.0
Initialization script hive-schema-3.1.0.mysql.sql
......
Initialization script completed
schemaTool completed
```

## 启动 Hive

执行如下命令启动 Hive：

```shell
hive
```

出现如下输出时表示启动成功：

```
Hive Session ID = f3edb53b-5037-47c3-b318-75854e2328c5

Logging initialized using configuration in jar:file:/opt/apache-hive-3.1.2-bin/lib/hive-common-3.1.2.jar!/hive-log4j2.properties Async: true
Hive Session ID = 3331472a-a171-47be-843a-378611233f18
Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
hive>
```
