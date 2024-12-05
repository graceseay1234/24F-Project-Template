# `database-files` Folder

Contains one SQL File: `00_huskynet.sql` responsible for creating the project database including
all relationships and data.
There are no manual steps required to re-bootstrap the database with command lines, simply
rerun the container. Upon rerun, execute these SQL lines to confirm the tables were created correctly:

`USE huskynet;`\
`SHOW TABLES;`

 if you make changes to your database schema or sample data, you’ll need to recreate the database container in docker so the new files will be executed. 
