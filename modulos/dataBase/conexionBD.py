
#Importando Libreria mysql.connector para conectar Python con MySQL
#0Kh6wZtpBSbguvnPf4zUELc@@@
import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host ="localhost",
        user ="root",
        # passwd ="Admin1003_",
        database = "crud_clientes"
        )
    if mydb:
        print ("Conexion exitosa a BD")
        return mydb
    else:
        print("Error en la conexion a BD")
    

    
connectionBD()

