import os , sys , sqlite3 , pathlib

from pathlib import Path

from datetime import datetime

from services.db_service import insertar_registro , abrir_connection , cerrar_conexion , insertar_valor_monedas_dolar , ultimo_id_registro_ingresado_valor_monedas_dolar

from PyQt5.Qt import *

from PyQt5 import uic , QtWidgets , QtGui#Carga la interfaz  grafica

from PyQt5.QtWidgets import QMainWindow , QApplication , QDialog , QTextEdit,QVBoxLayout,QPushButton

from PyQt5.QtCore import QFile, QTextStream


BASE_DIR = pathlib.Path( 'Vista_Principal.ui' ).parent.absolute()


class Ventana_Emergente( QMainWindow ):

	controller = None

	def __init__( self , self_controller ):
		
		self.controller = self_controller

		super().__init__()
		uic.loadUi( 'View_Agregar_Registro.ui' , self )

		self.setWindowTitle( 'titulo_Ventana' )
		self.resize( 421 , 267 )

		#Botones========================>>>>>
		self.Button_Guardar_Regitro.clicked.connect( self.agregar_registro )
		#===============================>>>>>
	def agregar_registro( self ):
		
		dicc = {}
		dicc["id_valor_moneda"] = 1
		dicc["peso_argentino"] = float( self.Entrada_Valor_Argentino_Dolar.text() )
		dicc["peso_chileno"] = float( self.Entrada_Valor_Chileno_Dolar.text() )
		dicc["fecha"] = datetime.now()
		dicc["razon"] = float( self.Entrada_Razon_Registro.text() )
		dicc["descripcion"] = self.Entrada_Descripcion.text()
		dicc["es_venta"] = self.CheckBox_es_Venta.isChecked()
		dicc["es_peso_chileno"] = self.CheckBox_es_Peso_Chileno.isChecked()
		dicc["es_peso_argentino"] = self.CheckBox_es_Peso_Argentino.isChecked()
		dicc["gasto"] = 0
		dicc["ganancia"] = 0

		moneda = dicc["peso_argentino"] 
		if self.CheckBox_es_Peso_Chileno.isChecked():
			moneda = dicc["peso_chileno"]

		monto_dolares_calculado = dicc["razon"]/moneda

		if dicc["es_venta"]:
			dicc["ganancia"] = monto_dolares_calculado
		else:
			dicc["gasto"] = monto_dolares_calculado

		id_ingresado = self.controller.agregar_valor_monedas_dolar( dicc )
		dicc["id_valor_moneda"] = id_ingresado
		self.controller.agregar_registro( dicc )

class Controller_Ventana_Emergente():

	def mostrar_ventana( self ):
		self.ventana_emergente = Ventana_Emergente( self )
		self.ventana_emergente.show()

	def agregar_registro( self , dicc_data ):
		dir_db = BASE_DIR/"Registro_DB.db"
		conn = abrir_connection( dir_db )
		insertar_registro( conn , dicc_data )
		cerrar_conexion( conn )

	def agregar_valor_monedas_dolar( self , dicc_data ):
		dir_db = BASE_DIR/"Registro_DB.db"
		conn = abrir_connection( dir_db )
		insertar_valor_monedas_dolar( conn , dicc_data )
		id_registro_ingresado = ultimo_id_registro_ingresado_valor_monedas_dolar( conn )
		cerrar_conexion( conn )
		return id_registro_ingresado

if __name__ == "__main__":
	
	controlador = Controller_Ventana_Emergente()
	controlador.mostrar_mensaje_emergente()
	