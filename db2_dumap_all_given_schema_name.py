import jaydebeapi

jdbc_driver = "com.ibm.db2.jcc.DB2Driver"
jdbc_url = "jdbc:db2://10.1.1.251:50000/<db_name>:sslConnection=true;"
jdbc_driver_path = "./jcc-11.5.9.0.jar"
username = "jimmy"
password = "password"
driver_class = "com.ibm.db2.jcc.DB2Driver"
target_schema = "<schema_name>"

conn = jaydebeapi.connect(jdbc_driver, jdbc_url, [username, password], jdbc_driver_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT NAME FROM SYSIBM.SYSTABLES WHERE CREATOR = ?", (target_schema,))
    tables = cursor.fetchall()

    if not tables:
        print(f"No tables found in schema '{target_schema}'.")
    else:
        for (table_name,) in tables:
            print(f"\n=== Dumping table: {table_name} ===")

            cursor.execute("""
                SELECT NAME FROM SYSIBM.SYSCOLUMNS
                WHERE TBNAME = ? AND TBCREATOR = ?
                ORDER BY COLNO
            """, (table_name, target_schema))
            columns = [col[0] for col in cursor.fetchall()]

            if not columns:
                print("  No columns found.")
                continue

            try:
                query = f'SELECT * FROM "{target_schema}"."{table_name}"'
                cursor.execute(query)
                rows = cursor.fetchall()

                # Print headers
                print(" | ".join(columns))

                # Print each row
                for row in rows:
                    print(" | ".join(str(val) if val is not None else "NULL" for val in row))

            except Exception as e:
                print(f"  Error querying {table_name}: {e}")

except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()

