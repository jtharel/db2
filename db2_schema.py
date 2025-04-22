import jaydebeapi
import jpype

jdbc_driver = "com.ibm.db2.jcc.DB2Driver"
jdbc_url = f"jdbc:db2://10.1.1.251:50000/db_name:sslConnection=true;loginTimeout=30;socketTimeout=60;"
jdbc_driver_path = "./jcc-11.5.9.0.jar"  
username = "jimmy"
password = "password"
driver_class = "com.ibm.db2.jcc.DB2Driver"

if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=" + jdbc_driver_path)

conn = jaydebeapi.connect(jdbc_driver, jdbc_url, [username, password], jdbc_driver_path)

conn_jdbc = conn.jconn
meta = conn_jdbc.getMetaData()
print("Catalogs: ", meta.getCatalogs())
print("Schemas: ", meta.getSchemas())
print("Tables: ", meta.getTables(None, None, "%", None))

schemas = meta.getSchemas()
while schemas.next():
    print("Schema: ", schemas.getString("TABLE_SCHEM"))
schemas.close()

conn.close()
