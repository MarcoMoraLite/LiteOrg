# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
import base64, os

class ValidaCurp(models.Model):
    _name = 'valida_curp.valida_curp'
    _description = 'valida_curp.valida_curp'
    
    state = fields.Selection([('ine','INE'),('cedula','CEDULA'),('foto','FOTO')],'estatus', default='ine')
    cedula = fields.Char("CEDULA")
    response = fields.Text("RESPUESTA")
    ine = fields.Binary("INE parte delantera")
    response2 = fields.Text("RESPUESTA INE")
    name = fields.Char("Nombre")
    apellido = fields.Char("Apellido")
    
    def comprobar(self):
        for record in self:
            cedula_usuario = record.cedula
            header = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
            payload = {"numeroCedula":cedula_usuario}
            r=requests.post("https://api.nubarium.com/sep/obtener_cedula",headers=header,data=json.dumps(payload))
            record.response = r.content
            
            
    def comprobar2(self):
        for record2 in self:
            header2 = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
            r2=requests.post("https://ine.nubarium.com:443/ocr/obtener_datos",headers=header2,json={"id":record2.ine})
            record2.response2 = r2.content
            
    def confirmarCed(self):
        for record3 in self:
            record3.name = "Marco"
            record3.write({'state': 'foto'})
    
    def confirmarIne(self):
        for record4 in self:
            record4.apellido = "Mora"
            record4.write({'state': 'cedula'})
       
            
