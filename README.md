# JamesDjango

##docker 部署数据库
```
vim docker-compose.yml
version: '3.3'

services:
  lwmysql:
    environment:
        MYSQL_ROOT_PASSWORD: 123456
    image: mysql:5.6
    restart: always
    volumes:
        - /data/mysql/data/:/var/lib/mysql/
        - /data/mysql/my.cnf:/etc/my.cnf
    ports:
        - 3306:3306
    container_name: mysql5.6
```
> 启动
```
docker-compose -d up .
```
> 创建数据库
```
mysql -uroot -h127.0.0.1 -p
create database db_name default character set utf8 collate utf8_general_ci;
```
