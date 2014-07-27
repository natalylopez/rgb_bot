#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
  [RGB] Bot!

  Copyright (C) 2014 Nataly Lopez <natalylopez380@hotmail.com>
  Copyright (C) 2013 Crozz Cyborg <CrozzCyborg@hotmail.es> 

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 

  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see http://www.gnu.org/licenses/.

"""

import socket,re,sys

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient
bridge = bridgeclient()

servidor = "irc.ircnode.com" # Datos a donde conectarse
port = 6667

nick = "RGB" # Datos de nick y canal
canal = "#dot!"

def Conexion(Servidor): # Se realiza la conexion
	print "[!] Estableciendo conexion a "+Servidor[0]
	irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	irc.connect(Servidor)
	print "[+] Conexion establecida"

	return irc

def Identificar(irc): # Se identifica el bot con un nick y el usuario
	print "[!] Enviando datos de autentificacion";
	irc.send("NICK "+nick+"\n")
	irc.send("USER "+nick+" Apellido Apellido Nombre\n")
	return 0

def JoinPart(Canal,accion,irc): # Funcion para salir o entrar de un canal Sintaxis: JoinPart(canal, accion) , accion; 1 = entrar,  0 = salir
	if(accion):
		print "[!] Entrando en "+Canal;
		irc.send("JOIN "+Canal+"\n")
		#irc.send("PRIVMSG "+Canal+" :Welcome :D\n")

def EncenderLed(Canal,irc):
         bridge.put('D13','1') #esto enciende led de status
         irc.send("PRIVMSG "+Canal+" :led encendido\n")
                  
def ApagarLed(Canal,irc):
         bridge.put('D13','0') #esto apaga led de status
         irc.send("PRIVMSG "+Canal+" :led apagado\n")
                                    
def EncenderRojo(Canal,irc):
	 bridge.put('D02','1') #esto enciende led rojo
	 irc.send("PRIVMSG "+Canal+" :led rojo encendido\n")

def ApagarRojo(Canal,irc):
         bridge.put('D02','0') #esto apaga led rojo
         irc.send("PRIVMSG "+Canal+" :led rojo apagado\n")
                  
def EncenderVerde(Canal,irc):
         bridge.put('D03','1') #esto enciende led verde
         irc.send("PRIVMSG "+Canal+" :led verde encendido\n")
         
def ApagarVerde(Canal,irc):
         bridge.put('D03','0') #esto apaga led verde
         irc.send("PRIVMSG "+Canal+" :led verde apagado\n")
                  
def EncenderAzul(Canal,irc):
         bridge.put('D04','1') #esto enciende led azul
         irc.send("PRIVMSG "+Canal+" :led azul encendido\n")

def ApagarAzul(Canal,irc):
         bridge.put('D04','0') #esto apaga led azul
         irc.send("PRIVMSG "+Canal+" :led azul apagado\n")
                                    		 
def MDatos(data,irc): # Manipulacion de datos
	if re.match(r'^PING :',data): # Se envia pong
		irc.send("PONG :"+data[6:]+"\n")
	elif re.match(r'^:\S+ NOTICE AUTH :\*\*\* Looking up your hostname',data): # se solicita identificarse
		Identificar(irc)
	elif re.match(r'^:\S+ 001',data): # Si se recibe el mensaje de bienvenida entra al canal
		JoinPart(canal,1,irc)
	else:
		tmp = data.split(':')
		#print len(tmp)
		if len(tmp) > 2:
			if re.match(r'on\!', tmp[2]):   # Si se recibe on!
				EncenderLed(canal, irc)
			elif re.match(r'off\!',tmp[2]): # Si se recibe off!
				ApagarLed(canal, irc)
			elif re.match(r'rojo on\!',tmp[2]): # Si se recibe rojo on!
				EncenderRojo(canal, irc)
                        elif re.match(r'rojo off\!',tmp[2]): # Si se recibe rojo off!
                                ApagarRojo(canal, irc)
                        elif re.match(r'verde on\!',tmp[2]): # Si se recibe verde on!
                                EncenderVerde(canal, irc)
                        elif re.match(r'verde off\!',tmp[2]): # Si se recibe verde off!
                                ApagarVerde(canal, irc)
                        elif re.match(r'azul on\!',tmp[2]): # Si se recibe azul on!
                                EncenderAzul(canal, irc)
                        elif re.match(r'azul off\!',tmp[2]): # Si se recibe azul off!
                                ApagarAzul(canal, irc)                                                 

def main():
	print "[!] RGBOT :) [!]\n"
	irc = Conexion((servidor,port))

	while irc: # Bucle que lee el socket
		data = irc.recv(512)
		MDatos(data,irc)

	return 0

try:
	main()
except KeyboardInterrupt: # Funcion que se ejecuta en caso de Ctrl + C
	print "[!] Deteniendo el bot"
	exit()
