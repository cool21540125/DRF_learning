

```sql
CREATE DATABASE IF NOT EXISTS `dj` CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE USER IF NOT EXISTS 'drf'@'localhost' IDENTIFIED BY 'morning';
GRANT ALL ON dj.* TO 'drf'@'localhost';
```