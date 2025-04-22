#Display Manager Config - requires admin privileges

import jaydebeapi
import jpype

jdbc_driver_path = "./jcc-11.5.9.0.jar"  

host = "10.1.1.251"  
port = "50000" 
db_name = "{db_name}"
schema_name = "{scheuma_name}"
url = f"jdbc:db2://{host}:{port}/{db_name}:sslConnection=true;loginTimeout=30;socketTimeout=60;"

username = "jimmy"
password = "password"

jdbc_driver = "com.ibm.db2.jcc.DB2Driver"
jdbc_url = url
driver_class = "com.ibm.db2.jcc.DB2Driver"

jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=" + jdbc_driver_path)

conn = jaydebeapi.connect(jdbc_driver, jdbc_url, [username, password], jdbc_driver_path)

cursor = conn.cursor()

#cursor.execute(f"SELECT NAME, VALUE, VALUE_FLAGS FROM TABLE(SYSPROC.ADMIN_GET_DBMCFG()) AS T")
cursor.execute(f"SELECT * FROM TABLE(SYSPROC.ENV_GET_SYSTEM_INFO()) AS SYSINFO")
results = cursor.fetchall()

print("Database Manager Configuration Parameters:")
for row in results:
    print("Name: {}, Value: {}, Flags: {}".format(row[0], row[1], row[2]))

cursor.close()
conn.close()

jpype.shutdownJVM()

