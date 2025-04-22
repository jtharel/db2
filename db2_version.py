#Shows DB2 version

import jaydebeapi
import jpype

jdbc_driver = "com.ibm.db2.jcc.DB2Driver"
jdbc_url = "jdbc:db2://10.1.1.251:50000/{DB_Name}:sslConnection=true;"
jdbc_driver_path = "./jcc-11.5.9.0.jar"
username = "jimmy"
password = "password"
driver_class = "com.ibm.db2.jcc.DB2Driver"

if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=" + jdbc_driver_path)

conn = jaydebeapi.connect(jdbc_driver, jdbc_url, [username, password], jdbc_driver_path)

conn_jdbc = conn.jconn
meta = conn_jdbc.getMetaData()
print("DB2 Product Name:", meta.getDatabaseProductName())
print("DB2 Version:", meta.getDatabaseProductVersion())

conn.close()
