 # compose/mysql/init/init.sql
 CREATE SCHEMA if not exists `core_base` DEFAULT CHARACTER SET utf8 ;
 GRANT ALL PRIVILEGES ON *.* TO root@"%" IDENTIFIED BY "p@ssw0rdwcx";
 FLUSH PRIVILEGES;
