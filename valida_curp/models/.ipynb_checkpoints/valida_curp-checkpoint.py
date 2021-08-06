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
    ine_foto = fields.Binary("Foto/Selfie")
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
    intentos = fields.Integer("Intentos",default=3)
    intentos_ine = fields.Integer("Intentos INE",default=3)
    intentos_cedula = fields.Integer("Intentos cédula",default=3)
    id_contacto = fields.Many2one("Current User")
    
    def comprobar(self):
        for record in self:
            if record.cedula is False:
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': ('Atención!'),
                        'message': 'Antes de validar debes subir tu cédula. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx ',
                        'type': 'info',
                        'sticky': True,
                        }
                    }
                return notification
            else:
                if(record.intentos_cedula > 0):
                    record.intentos_cedula = record.intentos_cedula - 1
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
                                'title': 'Atención!',
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

                elif(record.intentos_cedula == 0):
                    notification = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Atención!',
                            'message': 'Has alcanzado el número máximo de intentos, todos tus datos fueron enviados al área de Soporte Comercial. En el siguiente día hábil recibirás vía e-mail la confirmación definitiva o solicitud de documentos extra para completar tu registro',
                            'type': 'info',
                            'sticky': False,
                            }
                        }
                    return notification
                
    def comprobar2(self):
        for record2 in self:
            if record2.ine is False:
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': ('Atención!'),
                        'message': 'Antes de validar debes subir tu INE/IFE. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx ',
                        'type': 'info',
                        'sticky': True,
                        }
                    }
                return notification
            else:
                if(record2.intentos_ine > 0):
                    record2.intentos_ine = record2.intentos_ine - 1
                    header2 = {"Authorization": "Basic bTJjcm93ZDpfM2U4dy4wUnMy","Content-Type":"application/json"}
                    r2=requests.post("https://ine.nubarium.com:443/ocr/obtener_datos",headers=header2,json={"id":record2.ine.decode('utf-8')})
                    json_response = r2.json()
                    a=json.dumps(json_response)
                    res=json.loads(a)
                    if "estatus" in json_response:
                        record2.response2 = res['mensaje']
                        notification = {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': ('Atención!'),
                                'message': 'Documento no encontrado o no identificado, Te invitamos a hacer el proceso desde tu dispositivo móvil, donde podrás tomar la foto de tu INE/IFE de forma directa. Si el problema persiste favor de contactar a soporte.comercial@zele.mx',
                                'type': 'info',
                                'sticky': True,
                                }
                            }
                        return notification
                    else:
                        if 'curp' in json_response:
                            record2.curp = res['curp']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'fechaNacimiento' in json_response:
                            record2.fechaNacimiento = res['fechaNacimiento']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'primerApellido' in json_response:
                            record2.primerApellido = res['primerApellido']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'segundoApellido' in json_response:
                            record2.segundoApellido = res['segundoApellido']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'nombres' in json_response:
                            record2.nombres = res['nombres']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'sexo' in json_response:
                            record2.sexo = res['sexo']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'calle' in json_response:
                            record2.calle = res['calle']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'colonia' in json_response:
                            record2.colonia = res['colonia']
                            longitud = len(record2.colonia)
                            record2.codigo_postal = record2.colonia[longitud-5:]
                        else:
                            record2.response2 = "Faltan datos"

                        if 'ciudad' in json_response:
                            record2.ciudad = res['ciudad']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'subTipo' in json_response:
                            record2.subTipo = res['subTipo']
                            record2.response2 = 'OK'
                        else:
                            record2.response2 = "Faltan datos"

                        if 'claveElector' in json_response:
                            record2.claveElector = res['claveElector']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'registro' in json_response:
                            record2.registro = res['registro']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'estado' in json_response:
                            record2.estado = res['estado']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'municipio' in json_response:    
                            record2.municipio = res['municipio']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'seccion' in json_response:    
                            record2.seccion = res['seccion']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'localidad' in json_response:     
                            record2.localidad = res['localidad']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'emision' in json_response:     
                            record2.emision = res['emision']
                        else:
                            record2.response2 = "Faltan datos"

                        if 'vigencia' in json_response:     
                            record2.vigencia = res['vigencia']
                        else:
                            record2.response2 = "Faltan datos"

                        if record2.response2 != "Faltan datos":
                            record2.response2 = 'OK'
                            
                elif(record2.intentos_ine == 0):
                    notification = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Atención!',
                            'message': 'Has alcanzado el número máximo de intentos, todos tus datos fueron enviados al área de Soporte Comercial. En el siguiente día hábil recibirás vía e-mail la confirmación definitiva o solicitud de documentos extra para completar tu registro',
                            'type': 'info',
                            'sticky': False,
                            }
                        }
                    return notification               

            
    def confirmarCed(self):
        for record3 in self:
            #record3.id_contacto = nuevo_contacto.id
                
            if(record3.estatus_cedula == "Cédula relacionada" and record3.response == "Cédula encontrada y coincidencia en nombre"):
                fecha = record4.fechaNacimiento
                lista_date = fecha.split("/")
                dia = lista_date[0].replace("0","")
                mes = lista_date[1].replace("0","")
                ano = lista_date[2].replace("0","")
                fecha_full = str(ano) + str('-') + str(mes) + str('-') + str(dia)
                nombre_completo = str(record3.nombres) + str(' ') + str(record3.primerApellido) + str(' ') + str(record3.segundoApellido)
                record3.write({'state': 'foto'})
                nuevo_contacto = self.env['res.partner'].create( {
                    'name': nombre_completo,
                    'names': record3.nombres,
                    'father_last_name': record3.primerApellido,
                    'mother_last_name': record3.segundoApellido,
                    'registration_type': record3.tipo_cedula,
                    'education_title': record3.titulo,
                    'education_institute': record3.institucion,
                    'nombrecomercial': nombre_completo,
                    'sel_mode': 'id_nr',
                    'id_nr': record3.cedula,
                    'type': 'contact',
                    'street_name': record3.calle,
                    'zip': record3.codigo_postal,
                    'state_id': record3.estado,
                    'birthdate': fecha_full,
                    'l10n_mx_edi_curp': record3.curp,
                    'cedula': True,
                    'ine': True,
                    'client_type': 'specialist',
                    'is_specialist': True
                })
            elif(record3.estatus_cedula == "Cédula no relacionada"):
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Atención!',
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
                            'title': 'Atención!',
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
                            'title': 'Atención!',
                            'message': 'Debes de ingresar tu cédula antes de avanzar. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx',
                            'type': 'info',
                            'sticky': False,
                        }
                    }
                return notification
                
    
    def confirmarIne(self):
        for record4 in self:
            if(record4.response2 == "OK"):
                record4.write({'state': 'cedula'})
                
            else:
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Atención!',
                        'message': 'Antes de pasar al siguiente paso debes subir de manera correcta tu INE/IFE. Te invitamos a hacer el proceso desde tu dispositivo móvil, donde podrás tomar la foto de tu INE/IFE de forma directa. Si el problema persiste favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
                return notification
    
    def selfie(self):
        for record5 in self:
            if record5.ine_foto is False:
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': ('Atención!'),
                        'message': 'Antes de validar debes subir tu foto/selfie. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx ',
                        'type': 'info',
                        'sticky': True,
                        }
                    }
                return notification
            else:
                
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
                            'title': 'Atención!',
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
                        'title': 'Atención!',
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
                        'title': 'Atención!',
                        'message': 'Contacto guardado, da clic en el botón de "Guardar" para terminar con el proceso. Cualquier pregunta o comentario, favor de contactar a soporte.comercial@zele.mx',
                        'type': 'info',
                        'sticky': False,
                        }
                    }
            return notification
    
    def send_email_template(self):
        # Find the e-mail template
        template = self.env.ref('valida_curp.email_template_contrato')
        #body = template.body_html
        correo = 'marcoamora98@gmail.com'
        template.write({'email_to': correo}) #'toh@tohsoluciones.com'})
        template.send_mail(self.id, force_send=True)

            
            
       
            

