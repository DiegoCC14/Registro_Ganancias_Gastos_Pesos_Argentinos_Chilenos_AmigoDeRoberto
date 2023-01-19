import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def abrir_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect( db_file )
        return conn
    except Error as e:
        print(e)

def cerrar_conexion( conn ):
    conn.close()

def crea_tables_y_vistas( conn ):
    #El diagrama se encuentra en .Documentos/Diagrama_DB_XML.io

    c = conn.cursor()
    
    Registro = f'CREATE TABLE Registro( id INTEGER PRIMARY KEY AUTOINCREMENT , es_venta BOOLEAN , descripcion VARCHAR(900) , razon DOUBLE , ganancia DOUBLE , gasto DOUBLE , id_valor_moneda INT , es_peso_chileno BOOLEAN , es_peso_argentino BOOLEAN)'
    c.execute( Registro )


    Valor_Moneda_Dolar = f'CREATE TABLE Valor_Monedas_Dolar( id INTEGER PRIMARY KEY AUTOINCREMENT , peso_argentino DOUBLE , peso_chileno DOUBLE , fecha DATE)'
    c.execute( Valor_Moneda_Dolar )

    conn.commit()
    
def insertar_valor_monedas_dolar( conn , dicc_moneda ):
    c = conn.cursor()

    COLUMNAS = ' peso_argentino , peso_chileno , fecha '
    
    peso_argentino = dicc_moneda["peso_argentino"]
    peso_chileno = dicc_moneda["peso_chileno"]
    fecha = dicc_moneda["fecha"]

    VALUES = f'{peso_argentino} , "{peso_chileno}" , "{fecha}"'
    INSERT_ROW_MONEDA = f'INSERT INTO Valor_Monedas_Dolar({COLUMNAS}) VALUES ({VALUES})'
    
    c.execute( INSERT_ROW_MONEDA )
    conn.commit()

def ultimo_id_registro_ingresado_valor_monedas_dolar( conn ):
    c = conn.cursor()
    c.execute( f'SELECT id FROM Valor_Monedas_Dolar ORDER BY id DESC LIMIT 1;' )
    rows = c.fetchall()
    return [ row[0] for row in rows ][0]

def insertar_registro( conn , dicc_reg ):    
    c = conn.cursor()
    
    COLUMNAS =  ' es_venta , descripcion , razon , ganancia , gasto , id_valor_moneda , es_peso_chileno , es_peso_argentino '
    
    es_venta = dicc_reg["es_venta"]
    descripcion = dicc_reg["descripcion"]
    razon = dicc_reg["razon"]
    ganancia = dicc_reg["ganancia"]
    gasto = dicc_reg["gasto"]
    id_valor_moneda = dicc_reg["id_valor_moneda"]
    es_peso_chileno = dicc_reg["es_peso_chileno"]
    es_peso_argentino = dicc_reg["es_peso_argentino"]

    VALUES = f'"{es_venta}" , "{descripcion}" , "{razon}" , "{ganancia}" , "{gasto}" , "{id_valor_moneda}" , "{es_peso_chileno}" , "{es_peso_argentino}" '
    INSERT_ROW_REGISTRO = f'INSERT INTO Registro({COLUMNAS}) VALUES ({VALUES})'
    
    c.execute( INSERT_ROW_REGISTRO )

    conn.commit()

def get_rows_table( conn , name_table ):
    c = conn.cursor()
    c.execute( f"SELECT * FROM {name_table}")

    rows = c.fetchall()
    return [ row for row in rows ]

def obtener_todos_los_registros( conn ):
    c = conn.cursor()
    c.execute( f"SELECT * FROM Registro INNER JOIN Valor_Monedas_Dolar ON Registro.id_valor_moneda=Valor_Monedas_Dolar.id ORDER BY fecha DESC")
    rows = c.fetchall()
    return [ row for row in rows ]

def eliminar_registro_por_id( conn , id ):
    c = conn.cursor()
    c.execute( f"DELETE FROM Registro WHERE id={id}")
    conn.commit()

if __name__ == "__main__":
    dir_sqlite3 = BASE_DIR/'Registro_DB.db'
    conn = abrir_connection( dir_sqlite3 )
    
    #crea_tables_y_vistas( conn )
    registros = obtener_todos_los_registros( conn )
    for registro in registros:
        print( registro )

    #print( get_rows_table( conn , 'XML' ) )
    #print( get_rows_table( conn , 'Logs_XML' ) )
    #print( get_rows_table( conn , 'Ultimo_XML_Ingresado' ) )
    #print( get_rows_table( conn , 'XML_Reporte_Logs' ) )
    
    cerrar_conexion( conn )