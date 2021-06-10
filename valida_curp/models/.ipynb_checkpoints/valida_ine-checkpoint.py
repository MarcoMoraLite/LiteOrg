# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

class ValidaINE(models.Model):
    _name = 'valida_ine.valida_ine'
    _description = 'valida_ine.valida_ine'
    
    cic = fields.Char("cic")
    identificadorCiudadano = fields.Char("Identificador Ciudadano")
    response2 = fields.Text("RESPONSE2")
            
    def comprobar_ine(self):
        for record2 in self:
            cic = record2.cic
            identificadorCiudadano = record.identificadorCiudadano
            payload2 ={"cic":cic,"identificadorCiudadano":identificadorCiudadano}
            r2=requests.post("https://ine.nubarium.com/ine/v2/valida_ine",headers=header,data=json.dumps(payload2))
            record2.response2 = r2.content

