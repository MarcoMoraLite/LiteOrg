# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
import base64

class ValidaCurp(models.Model):
    _name = 'valida_curp.valida_curp'
    _description = 'valida_curp.valida_curp'

    #status = fields.Selection[('ine','INE'),('cedula','CEDULA')]
    cedula = fields.Char("CURP")
    response = fields.Text("RESPUESTA")
    ine = fields.Image("INE parte delantera")
    ine_atras = fields.Image("INE parte de atras")
    response2 = fields.Text("RESPUESTA INE")
    
    def comprobar(self):
        for record in self:
            cedula_usuario = record.cedula
            header = {"Authorization": "Basic bXVsdGlwbGljYTprR19NeC4yeUI5","Content-Type":"application/json"}
            payload = {"numeroCedula":cedula_usuario}
            r=requests.post("https://api.nubarium.com/sep/obtener_cedula",headers=header,data=json.dumps(payload))
            #json_response = r.json()
            #aux=json.dumps(json_response)
            #mapa=json.loads(aux)
            #estatus=mapa["estatus"]
            record.response = r.content
            
    def comprobar2(self):
        for record2 in self:
            ine = record2.ine
            ine_bytes = ine.encode('utf-8')
            ine64 = base64.b64encode(ine_bytes)
            ine2 = record2.ine_atras
            ine2_bytes = ine2.encode('utf-8')
            ine264 = base64.b64encode(ine2_bytes)
            payload2 = {"id":ine64,"idReverso":ine264}
            r2=request.post("https://ine.nubarium.com:443/ocr/obtener_datos",headers=header,data=json.dumps(payload2))
            record.response2 = r2.content
