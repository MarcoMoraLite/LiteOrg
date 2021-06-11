# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

class ValidaCedula(models.Model):
    _name = 'valida_cedula.valida_cedula'
    _description = 'valida_cedula.valida_cedula'

    cedula = fields.Char("CURP")
    response = fields.Text("RESPUESTA")
    
    def comprobar(self):
        for record in self:
            cedula_usuario = record.cedula
            header = {"Authorization": "Basic bXVsdGlwbGljYTprR19NeC4yeUI5","Content-Type":"application/json"}
            payload = {"documento":"0","curp":curp_usuario}
            r=requests.post("https://curp.nubarium.com/renapo/valida_curp",headers=header,data=json.dumps(payload))
            #json_response = r.json()
            #aux=json.dumps(json_response)
            #mapa=json.loads(aux)
            #estatus=mapa["estatus"]
            record.response = r.content
