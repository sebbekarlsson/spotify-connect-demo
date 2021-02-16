# how to run
> First create database in mysql
```sql
CREATE DATABASE spotify charset=utf8;
```
> Then create config file `config.json` with these variables:
```json
{
  "client_id": "",
  "client_secret": "",
  "mysql_user": "",
  "mysql_password": "",
  "mysql_dbname": "",
  "mysql_host": ""
}
```
> Then run:
```bash
python setup.py develop
```
> Then run
```bash
python __main__.py
```
