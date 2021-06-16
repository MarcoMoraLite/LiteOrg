# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
import base64, os

class ValidaCurp(models.Model):
    _name = 'valida_curp.valida_curp'
    _description = 'valida_curp.valida_curp'
    
    state = fields.Selection([('ine','INE'),('cedula','CEDULA')],'estatus', default='ine')
    cedula = fields.Char("CEDULA")
    response = fields.Text("RESPUESTA")
    ine = fields.Binary("INE parte delantera")
    response2 = fields.Text("RESPUESTA INE")
    
    def comprobar(self):
        for record in self:
            cedula_usuario = record.cedula
            header = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
            payload = {"numeroCedula":cedula_usuario}
            r=requests.post("https://api.nubarium.com/sep/obtener_cedula",headers=header,data=json.dumps(payload))
            record.response = r.content
            #record.write({'state': 'cedula'})
            
            
    def comprobar2(self):
        for record2 in self:
            header2 = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
            r2=requests.post("https://ine.nubarium.com:443/ocr/obtener_datos",headers=header2,json={"id":record2.ine})
            record2.response2 = r2.content
            record2.write({'state': 'cedula'})
            
            '''
            "tipo": "INE",
            DATOS CREDENCIAL----------------------
    "subTipo": "E",
    "claveElector": "MRCLMR98041615H300",
    "registro": "2016 00",
    "estado": "15",
    "municipio": "052",
    "seccion": "2417",
    "localidad": "0005",
    "emision": "2016",
    "vigencia": "2026",
    DATOS PERSONALES-------------------------------
    "curp": "MOCM980416HMCRLR09",
    "fechaNacimiento": "16/04/1998",
    "primerApellido": "MORA",
    "segundoApellido": "COLIN",
    "nombres": "MARCO ANTONIO",
    "sexo": "H",
    "calle": "C 3 DE MAYO 122",
    "colonia": "- SANTA MARIA ATARASQUILLO 52044",
    "ciudad": "LERMA , MEX",
    "codigoValidacion": "gd1623881943.7599058"'''