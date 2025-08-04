import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import config

conn = MySQLdb.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    passwd=config.DB_PASSWORD
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS markethub")
cursor.execute("USE markethub")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS producto (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    precio DECIMAL(10,2),
    cantidad INT
)
""")

cursor.execute("""
INSERT INTO usuario (username, password)
VALUES ('admin', 'markethub123')
""")

conn.commit()
conn.close()
print("Base de datos y tablas creadas con éxito.")
