# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

class ValidaCurp(models.Model):
    _name = 'valida_curp.valida_curp'
    _description = 'valida_curp.valida_curp'

    curp = fields.Char("CURP")
    response = fields.Text("RESPONSE")
    
    def comprobar(self):
        for record in self:
            curp_usuario = record.curp
            header = {"Authorization": "Basic bXVsdGlwbGljYTprR19NeC4yeUI5","Content-Type":"application/json"}
            payload = {"documento":"0","curp":curp_usuario}
            r=requests.post("https://curp.nubarium.com/renapo/valida_curp",headers=header,data=json.dumps(payload))
            #json_response = r.json()
            #aux=json.dumps(json_response)
            #mapa=json.loads(aux)
            #estatus=mapa["estatus"]
            record.response = r.content
