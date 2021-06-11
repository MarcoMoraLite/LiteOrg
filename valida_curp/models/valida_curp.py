# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

class ValidaCurp(models.Model):
    _name = 'valida_curp.valida_curp'
    _description = 'valida_curp.valida_curp'

    cedula = fields.Char("CURP")
    response = fields.Text("RESPUESTA")
    
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
