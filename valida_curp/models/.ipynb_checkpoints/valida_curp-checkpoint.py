# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
import base64, os
from odoo.exceptions import UserError

class ValidaCurp(models.Model):
    _name = 'valida_curp.valida_curp'
    _description = 'valida_curp.valida_curp'
    
    state = fields.Selection([('ine','INE'),('cedula','CEDULA'),('foto','FOTO'),('guardar','GUARDAR')],'estatus', default='ine')
    cedula = fields.Char("Cédula")
    response = fields.Char("Respuesta")
    ine = fields.Binary("INE parte delantera")
    response2 = fields.Text("Respuesta INE")
    ine_foto = ine = fields.Binary("Foto")
    response3 = fields.Text("Respuesta foto")
    curp = fields.Char("Curp")
    fechaNacimiento = fields.Char("Fecha de Nacimiento")
    primerApellido = fields.Char("Primer Apellido")
    segundoApellido = fields.Char("Segundo Apellido")
    nombres = fields.Char("Nombres")
    sexo = fields.Char("Sexo")
    calle = fields.Char("Calle")
    colonia = fields.Char("Colonia")
    ciudad = fields.Char("Ciudad")
    subTipo = fields.Char("Sub Tipo")
    claveElector = fields.Char("Clave Elector")
    registro = fields.Char("Registro")
    estado = fields.Char("Estado")
    municipio = fields.Char("Municipio")
    seccion = fields.Char("Sección")
    localidad = fields.Char("Localidad")
    emision = fields.Char("Emisión")
    vigencia = fields.Char("Vigencia")
    primerApellidoCedula = fields.Char("Primer Apellido Cedula")
    segundoApellidoCedula = fields.Char("Segundo Apellido Cedula")
    nombresCedula = fields.Char("Nombres Cedula")
    institucion = fields.Char("Institución")
    tipo_cedula = fields.Char("Tipo")
    titulo = fields.Char("Titulo")
    estatus_cedula = fields.Char("Estatus")
    codigo_postal = fields.Char("Codigo Postal")
    intentos = fields.Integer("Intentos")
    id_contacto = fields.Many2one("Current User")
    
    def comprobar(self):
        for record in self:
            cedula_usuario = record.cedula
            header = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
            payload = {"numeroCedula":cedula_usuario}
            r=requests.post("https://api.nubarium.com/sep/obtener_cedula",headers=header,data=json.dumps(payload))
            json_cedula = r.json()
            b=json.dumps(json_cedula)
            cedu=json.loads(b)
            status = cedu['estatus']
            if(status == 'ERROR'):
                record.response = cedu['mensaje']
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': 'El formato de la cédula no ha sido identificado o tienes que tener una cédula relacionada a una licenciatura con las carreras autorizadas para prescribir Zélé. Favor de ingresar cédulas profesionales de nivel licenciatura solamente. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
                return notification
            
            else:
                record.primerApellidoCedula = cedu['cedulas'][0]['apellidoPaterno']
                record.segundoApellidoCedula = cedu['cedulas'][0]['apellidoMaterno']
                record.nombresCedula = cedu['cedulas'][0]['nombres']
                record.institucion = cedu['cedulas'][0]['institucion']
                record.tipo_cedula = cedu['cedulas'][0]['tipo']
                record.titulo = cedu['cedulas'][0]['titulo']
                titulo_lower = record.titulo.lower()
                if((titulo_lower.find('nutrición') != -1) or (titulo_lower.find('medicina') != -1) or (titulo_lower.find('médico') != -1)):
                    record.estatus_cedula = "Cédula relacionada"
                else:
                    record.estatus_cedula = "Cédula no relacionada"
                    
                if((record.primerApellidoCedula == record.primerApellido) and (record.segundoApellidoCedula == record.segundoApellido) and (record.nombresCedula == record.nombres)):
                   record.response = "Cédula encontrada y coincidencia en nombre"
                else:
                    record.response = "Cédula encontrada pero no existe coincidencia en nombre"
    
                   
    def comprobar2(self):
        for record2 in self:
            header2 = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
            r2=requests.post("https://ine.nubarium.com:443/ocr/obtener_datos",headers=header2,json={"id":record2.ine})
            json_response = r2.json()
            a=json.dumps(json_response)
            res=json.loads(a)
            if "estatus" in json_response:
                record2.response2 = res['mensaje']
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': ('Warning!'),
                        'message': 'Documento no encontrado o no identificado, Te invitamos a hacer el proceso desde tu dispositivo móvil, donde podrás tomar la foto de tu INE/IFE de forma directa. Si el problema persiste favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': True,
                        }
                    }
                return notification
            else:
                record2.curp = res['curp']
                record2.fechaNacimiento = res['fechaNacimiento']
                record2.primerApellido = res['primerApellido']
                record2.segundoApellido = res['segundoApellido']
                record2.nombres = res['nombres']
                record2.sexo = res['sexo']
                record2.calle = res['calle']
                record2.colonia = res['colonia']
                record2.ciudad = res['ciudad']
                record2.subTipo = res['subTipo']
                record2.claveElector = res['claveElector']
                record2.registro = res['registro']
                record2.estado = res['estado']
                record2.municipio = res['municipio']
                record2.seccion = res['seccion']
                record2.localidad = res['localidad']
                record2.emision = res['emision']
                record2.vigencia = res['vigencia']
                record2.response2 = 'OK'
                longitud = len(record2.colonia)
                record2.codigo_postal = record2.colonia[longitud-5:]
            
    def confirmarCed(self):
        for record3 in self:
            record3.intentos=3
            record3.write({'state': 'foto'})
            nuevo_contacto = self.env['res.users'].create( {
                "name": record3.nombres
            })
            #record3.id_contacto = nuevo_contacto.id
                
            if(record3.estatus_cedula == "Cédula relacionada" and record3.response == "Cédula encontrada y coincidencia en nombre"):
                record3.write({'state': 'foto'})
            elif(record3.estatus_cedula == "Cédula no relacionada"):
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': 'La licenciatura relacionada a tu cédula no concuerda con las licenciaturas autorizadas para prescribir Zélé. Favor de ingresar cédulas profesionales de nivel licenciatura solamente. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
                return notification
            elif(record3.response == "Cédula encontrada pero no existe coincidencia en nombre"):
                notification = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Warning!',
                            'message': 'Los datos relacionados a la cédula no concuerdan con los datos leídos de tu INE/IFE, favor de ingresar una cédula relacionada a los datos leídos de tu INE/IFE. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx',
                            'type': 'info',
                            'sticky': False,
                        }
                    }
                return notification
            else:
                notification = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Warning!',
                            'message': 'Debes de ingresar tu cédula antes de avanzar. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx',
                            'type': 'info',
                            'sticky': False,
                        }
                    }
                return notification
                
    
    def confirmarIne(self):
        for record4 in self:
            record4.write({'state': 'cedula'})
            if(record4.response2 == "OK"):
                record4.write({'state': 'cedula'})
            else:
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': 'Antes de pasar al siguiente paso debes subir de manera correcta tu INE/IFE. Te invitamos a hacer el proceso desde tu dispositivo móvil, donde podrás tomar la foto de tu INE/IFE de forma directa. Si el problema persiste favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
                return notification
    
    def selfie(self):
        for record5 in self:
            if(record5.intentos > 0):
                header3 = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
                r3=requests.post("https://ine.nubarium.com/antifraude/reconocimiento_facial",headers=header3,json={"credencial":record5.ine,"captura":record5.ine_foto,"tipo":"imagen"})
                json_r3 = r3.json()
                c=json.dumps(json_r3)
                res3=json.loads(c)
                status = res3['estatus']
                if(status=='OK'):
                    men = res3['mensaje']
                    por = res3['similitud']
                    mensaje = str(men) + str(' ') + str(por)
                    record5.response3 = mensaje
                    record5.intentos = record5.intentos - 1
                elif(status == 'ERROR'):
                    record5.response3 = res3['mensaje']
                    record5.intentos = record5.intentos - 1
                    
            elif(record5.intentos == 0):
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': 'Has alcanzado el número máximo de intentos, todos tus datos fueron enviados al área de Soporte Comercial. Por lo pronto podrás hacer uso de la tienda Zélé y en el siguiente día hábil recibirás vía e-mail la confirmación definitiva o solicitud de documentos extra para completar tu registro',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
                return notification
                
    
    def confirmarSelfie(self):
        for record6 in self:
            if(record6.response3 == "Similitud de rostros encontrada" or record6.intentos == 0):
                record6.write({'state': 'guardar'})
            else:
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': 'Debes ingresar y validar tu foto antes de avanzar. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
                return notification
                
                
    def guardaContacto(self):
        for record7 in self:
            notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': 'Contacto guardado, da clic en el botón de "Guardar" para terminar con el proceso. Cualquier pregunta o comentario, favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
            return notification
            
    
            
            
       
            
