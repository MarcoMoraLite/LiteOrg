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
    ine_atras = fields.Binary("INE parte de atras")
    response2 = fields.Text("RESPUESTA INE")
    
    def comprobar(self):
        for record in self:
            cedula_usuario = record.cedula
            header = {"Authorization": "Basic bXVsdGlwbGljYTprR19NeC4yeUI5","Content-Type":"application/json"}
            payload = {"numeroCedula":cedula_usuario}
            r=requests.post("https://api.nubarium.com/sep/obtener_cedula",headers=header,data=json.dumps(payload))
            record.response = r.content
            record.write({'state': 'cedula'})
            
            
    def comprobar2(self):
        for record2 in self:
            #ine64 = base64.b64encode(record2.ine)
            header2 = {"Authorization": "Basic bXVsdGlwbGljYTprR19NeC4yeUI5","Content-Type":"application/json"}
            r2=requests.post("https://ine.nubarium.com:443/ocr/obtener_datos",headers=header2,data={"id":record2.ine})
            record2.response2 = r2.content
            record2.response = record2.ine
            