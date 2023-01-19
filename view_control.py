import os , sys , pathlib , json

from pathlib import Path

from datetime import datetime

import View_Agregar_Registro

from services.db_service import obtener_todos_los_registros , cerrar_conexion , abrir_connection , eliminar_registro_por_id

from PyQt5.Qt import *
from PyQt5 import uic , QtWidgets #Carga la interfaz  grafica
from PyQt5.QtWidgets import QMainWindow , QApplication , QDialog
from PyQt5.QtCore import QFile, QTextStream

BASE_DIR = pathlib.Path( 'Vista_Principal.ui' ).parent.absolute()
print( f"Direccion actual{BASE_DIR}" )
file = open("texto.txt","w")
file.write( str(BASE_DIR) )

def leer_archivo_json( dir_file_json ):
	with open( dir_file_json , encoding='utf-8') as json_file:
		data = json.load(json_file)
		#data_dumps = json.dumps( data , indent=2) #Solo sirve para mostrar ordenadamente los datos
	return data

class Inicio_App( QMainWindow ):

	def __init__(self):

		super().__init__()
		uic.loadUi( 'View_Registro.ui' , self )

		Json_Properties = leer_archivo_json( 'Properties_App.json' )
		title_app = Json_Properties['Nombre'] + " V_"+str( Json_Properties['Version'] )
		self.setWindowTitle( title_app ) #Cambia el titulo de la aplicasion

		#d = QDateTime( 2023 , 1 , 14 , 0, 0)
		#self.Date_Desde_Filtro.setDateTime(d)

		self.Genera_Tabla_Registro_Ganancias_Gastos()

		# Acciones Button ---------------------->>>>>>>>>>>>>>>
		self.Button_Eliminar_Registro.clicked.connect( self.eliminar_registro )
		self.Button_Calcular_Registro.clicked.connect( self.calcular_ganancias_gastos )
		self.Button_Agregar_Registro.clicked.connect( self.abrir_view_agregar_registro )
		self.Button_Actualizar_Registros.clicked.connect( self.actualizar_datos_Tabla_Registro_Ganancias_Gastos )
		#self.Tabla_Registro_Ganancias_Gastos.itemChanged.connect( self.autocalcular_gasto_ganancia )
		# -------------------------------------->>>>>>>>>>>>>>>

	def eliminar_filas_Tabla_Registro_Ganancias_Gastos( self ):
		for fila in range( self.Tabla_Registro_Ganancias_Gastos.rowCount() ):
			for columna in range( self.Tabla_Registro_Ganancias_Gastos.columnCount() ):
				self.Tabla_Registro_Ganancias_Gastos.setItem( fila , columna , None )

	def Genera_Tabla_Registro_Ganancias_Gastos(self):

		self.Tabla_Registro_Ganancias_Gastos.setRowCount( 1500 )
		self.Tabla_Registro_Ganancias_Gastos.setColumnCount( 10 )
		self.Tabla_Registro_Ganancias_Gastos.setHorizontalHeaderLabels( ['ID','Venta','Descripcion','Razon','Gastos D.','Gananc D.','Valor D.','Fecha','Chi','Arg'] )

		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(0, 10)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(1, 25)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(2, 100)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(3, 75)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(4, 77)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(5, 77)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(6, 60)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(7, 85)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(8, 5)
		self.Tabla_Registro_Ganancias_Gastos.setColumnWidth(9, 5)

	def calcular_ganancias_gastos( self ):
		list_registros_ingresados = self.obtener_registros_tabla_Ganancias_Gastos()
				
		date_desde = self.Date_Desde_Filtro.date().toPyDate()
		date_hasta = self.Date_Hasta_Filtro.date().toPyDate()

		desde_datetime = datetime.strptime( str(date_desde) , '%Y-%m-%d').date() #(  , date_desde.month , date_desde.day )
		hasta_datetime = datetime.strptime( str(date_hasta) , '%Y-%m-%d').date() #( date_hasta.year , date_hasta.month , date_hasta.day )
		
		
		ganancias_totales = 0
		gastos_totales = 0
		for registro in list_registros_ingresados:
			date_actual = datetime.strptime( registro[7][0:10] , '%Y-%m-%d').date()
			if date_actual >= desde_datetime and date_actual <= hasta_datetime:
				ganancias_totales += float( registro[5] ) #ganancias
				gastos_totales += float( registro[4] ) #gastos
		
		self.Label_Ganancias_Dolar.setText( str(ganancias_totales) )
		self.Label_Gastos_Dolar.setText( str(gastos_totales) )
		self.Label_Ganancias_Netas.setText( str( ganancias_totales-gastos_totales ) )

	def eliminar_registro( self ):
		id_eliminar = int( self.Entrada_Valor_Id_Eliminar.text() )
		conn = abrir_connection( BASE_DIR/'Registro_DB.db' )
		eliminar_registro_por_id( conn , id_eliminar )
		cerrar_conexion( conn )

		self.actualizar_datos_Tabla_Registro_Ganancias_Gastos()

	def obtener_registros_tabla_Ganancias_Gastos( self ):
		#['ID','Venta','Descripcion','Razon','Gastos D.','Gananc D.','Valor D.','Fecha','Chi','Arg']
		list_restistros = []
		count_row = self.Tabla_Registro_Ganancias_Gastos.rowCount()
		for num_row in range( count_row ):
			if self.Tabla_Registro_Ganancias_Gastos.item( num_row , 0) != None and self.Tabla_Registro_Ganancias_Gastos.item( num_row , 2) != None:
				fila = []
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 0).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 1).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 2).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 3).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 4).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 5).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 6).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 7).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 8).text() )
				fila.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , 9).text() )
				list_restistros.append( fila )
		return list_restistros 

	def obtener_registro_tabla_Ganancias_Gastos_por_fila( self , num_row ):
		count_column = self.Tabla_Registro_Ganancias_Gastos.columnCount()
		lista_elementos = []
		for num_column in range( count_column ):
			try:
				lista_elementos.append( self.Tabla_Registro_Ganancias_Gastos.item( num_row , num_column).text() )
			except:
				lista_elementos.append("")
		return lista_elementos

	def autocalcular_gasto_ganancia( self , item):
		#['ID','Venta','Descripcion','Razon','Gastos D.','Gananc D.','Valor D.','Fecha','Chi','Arg']

		if item.column() == 3: #Razon
			fila_item = item.row()
			list_elements_row = self.obtener_registro_tabla_Ganancias_Gastos_por_fila( fila_item )
			
			ID = list_elements_row[0]
			es_Venta = list_elements_row[1]
			Descripcion = list_elements_row[2]
			Razon = list_elements_row[3]
			Gastos_D = list_elements_row[4]
			Ganancias_D = list_elements_row[5]
			Valor_D = list_elements_row[6]
			Fecha_D = list_elements_row[7]
			es_Chi = list_elements_row[8]
			es_Arg = list_elements_row[9]


			self.Tabla_Registro_Ganancias_Gastos.setItem( fila_item , 6 , QTableWidgetItem( "" ) )
			moneda = self.Entrada_Valor_Argentino_Dolar.text() 
			if es_Chi == "S":
				moneda = self.Entrada_Valor_Chileno_Dolar.text()
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila_item , 6 , QTableWidgetItem( moneda ) )


			monto_dolares_calculado =  float( Razon )/float( moneda )

			self.Tabla_Registro_Ganancias_Gastos.setItem( fila_item , 5 , QTableWidgetItem( "" ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila_item , 4 , QTableWidgetItem( "" ) )
			if es_Venta == "S":
				self.Tabla_Registro_Ganancias_Gastos.setItem( fila_item , 5 , QTableWidgetItem( str( monto_dolares_calculado ) ) )
			else:
				self.Tabla_Registro_Ganancias_Gastos.setItem( fila_item , 4 , QTableWidgetItem( str( monto_dolares_calculado ) ) )

	def guardar_datos( self , item):
		list_registros = self.obtener_registros_tabla_Ganancias_Gastos()
		#Verificamos los datos
		for registro in list_registros:
			registro
		#================>>>>>

	def abrir_view_agregar_registro( self ):
		self.controlador = View_Agregar_Registro.Controller_Ventana_Emergente()
		self.controlador.mostrar_ventana()
	
	def actualizar_datos_Tabla_Registro_Ganancias_Gastos( self ):
		dir_sqlite3 = BASE_DIR/'Registro_DB.db'
		conn = abrir_connection( dir_sqlite3 )

		list_registros = obtener_todos_los_registros( conn )
		
		self.eliminar_filas_Tabla_Registro_Ganancias_Gastos()

		for fila , registro in enumerate( list_registros ):
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 0 , QTableWidgetItem( str( registro[0] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 1 , QTableWidgetItem( str( registro[1] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 2 , QTableWidgetItem( str( registro[2] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 3 , QTableWidgetItem( str( registro[3] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 4 , QTableWidgetItem( str( registro[5] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 5 , QTableWidgetItem( str( registro[4] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 6 , QTableWidgetItem( str( registro[6] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 7 , QTableWidgetItem( str( registro[12] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 8 , QTableWidgetItem( str( registro[7] ) ) )
			self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 9 , QTableWidgetItem( str( registro[8] ) ) )
			
			if registro[7] == 'True': #Es Chileno
				self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 6 , QTableWidgetItem( str( registro[11] ) ) )
			else:
				self.Tabla_Registro_Ganancias_Gastos.setItem( fila , 6 , QTableWidgetItem( str( registro[10] ) ) )

		cerrar_conexion( conn )

app = QApplication( sys.argv )

Aplicacion = Inicio_App()
Aplicacion.setFixedSize( 781 , 610 ) #759
Aplicacion.show()

sys.exit( app.exec_() )