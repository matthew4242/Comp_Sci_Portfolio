For the data processor the following packages must be installed:

python 3.7.3 

cycler==0.10.0
fpdf==1.7.2
kiwisolver==1.1.0
matplotlib==3.1.1
mysql==0.0.2
mysql-connector-python==8.0.17
mysqlclient==1.4.4
numpy==1.17.1
pandas==0.25.1
pyparsing==2.4.2
python-dateutil==2.8.0
pytz==2019.2
six==1.12.0

You can check what you have in windows 10 command line by pip freeze
The version of python can be checked in the command line by typing: python

Without these packages or an earlier version, the application may not work.

The application can be ran using: python application.py
The Unit tests can be run using: python data_proccessor_unittests.py

To modify the data being imputed and outputted. Please use the config.py file.

--------------------------------------

To set up this device a local server must be made through using : 
https://www.mysql.com/products/workbench/

How to set up a database using MySQL workbench :
https://dev.mysql.com/doc/workbench/en/wb-getting-started-tutorial-create-connection.html

To create tables either call DatabaseManager.create_tables() in application.py or call SQL statements found in
create_tables.txt.

-----------------------------------

The config.py file can be used to edit the primary variables in the database. Some comments explain 
what the variables do.

-----------------------------------

If modification needed for;
     importing data -> look at record_handler.py
     database management -> db_manager.py
     visualisation and handout -> visualisation_manager.py

In the graphs, records and reports are already created files. That is from previous runs. Do Not Delete any records 
or reports as they are used for testing and explaining in the final report and acceptance testing.