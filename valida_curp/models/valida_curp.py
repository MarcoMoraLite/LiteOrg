# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
import base64, os
from odoo.exceptions import UserError

class ValidaCurp(models.Model):
    _name = 'valida_curp.valida_curp'
    _description = 'valida_curp.valida_curp'
    
    state = fields.Selection([('ine','INE'),('cedula','CEDULA'),('foto','FOTO'),('bancarios','DOC BANCARIOS')],'Estatus', default='ine')
    cedula = fields.Char("Cédula")
    response = fields.Char("Respuesta")
    ine = fields.Binary("INE parte delantera")
    ine_fname = fields.Char("Nombre de ine")
    response2 = fields.Text("Respuesta INE")
    ine_foto = fields.Binary("Foto/Selfie")
    selfie_fname = fields.Char("Nombre de foto")
    response3 = fields.Text("Respuesta foto")
    curp = fields.Char("Curp")
    fechaNacimiento = fields.Char("Fecha de nacimiento")
    primerApellido = fields.Char("Primer apellido")
    segundoApellido = fields.Char("Segundo apellido")
    nombres = fields.Char("Nombres")
    sexo = fields.Char("Sexo")
    calle = fields.Char("Calle")
    colonia = fields.Char("Colonia")
    ciudad = fields.Char("Ciudad")
    subTipo = fields.Char("Sub Tipo")
    claveElector = fields.Char("Clave elector")
    registro = fields.Char("Registro")
    estado = fields.Char("Estado")
    municipio = fields.Char("Municipio")
    seccion = fields.Char("Sección")
    localidad = fields.Char("Localidad")
    emision = fields.Char("Emisión")
    vigencia = fields.Char("Vigencia")
    primerApellidoCedula = fields.Char("Primer apellido cédula")
    segundoApellidoCedula = fields.Char("Segundo apellido cédula")
    nombresCedula = fields.Char("Nombres cédula")
    institucion = fields.Char("Institución")
    tipo_cedula = fields.Char("Tipo")
    titulo = fields.Char("Título")
    estatus_cedula = fields.Char("Estatus cedula")
    codigo_postal = fields.Char("Codigo postal")
    intentos = fields.Integer("Intentos",default=3)
    intentos_ine = fields.Integer("Intentos INE",default=3)
    intentos_cedula = fields.Integer("Intentos cédula",default=3)
    id_contacto = fields.Many2one("Current User")
    estatus_gen = fields.Char("Estatus general", default="Faltan datos")
    banco = fields.Char("Banco")
    cuenta = fields.Char("Cuenta bancaria")
    clabe = fields.Char("CLABE")
    rfc = fields.Char("RFC")
    noti_ine = fields.Char("Mensaje INE")
    noti_ced = fields.Char("Mensaje cédula")
    noti_foto = fields.Char("Mensaje foto")
    bool_ine = fields.Boolean("bool_ine")
    bool_ced = fields.Boolean("bool_ced")
    bool_foto = fields.Boolean("bool_foto")
    id_state = fields.Many2one("Id_estado")
    id_contacto = fields.Many2one("ID contacto")
    
    def comprobar(self):
        for record in self:
            record.estatus_cedula = "Sin validar"
            if record.cedula is False:
                record.noti_ced = "Antes de validar debes subir tu cédula. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record.intentos_cedula,"respuesta":record.noti_ced,"bool_ine":record.bool_ced,"api":record.response,"estatus_cedula":record.estatus_cedula}
                
            else:
                if(record.intentos_cedula > 0):
                    record.intentos_cedula = record.intentos_cedula - 1
                    cedula_usuario = record.cedula
                    header = {"Authorization": "Basic emVsZTpZbTRfOHcucFg=","Content-Type":"application/json"}
                    payload = {"numeroCedula":cedula_usuario}
                    r=requests.post("https://api.nubarium.com/sep/obtener_cedula",headers=header,data=json.dumps(payload))
                    json_cedula = r.json()
                    b=json.dumps(json_cedula)
                    cedu=json.loads(b)
                    status = cedu['estatus']
                    if(status == 'ERROR'):
                        record.response = cedu['mensaje']
                        record.noti_ced = "El formato de la cédula no ha sido identificado o tienes que tener una cédula relacionada a una licenciatura con las carreras autorizadas para prescribir Zélé. Favor de ingresar cédulas profesionales de nivel licenciatura solamente. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                        return {"intentos":record.intentos_cedula,"respuesta":record.noti_ced,"bool_ine":record.bool_ced,"api":record.response,"estatus_cedula":record.estatus_cedula}
                        
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
                            record.estatus_cedula = "La licenciatura de la cédula no esta autorizada para prescribir Zélé"

                        if((record.primerApellidoCedula == record.primerApellido) and (record.segundoApellidoCedula == record.segundoApellido) and (record.nombresCedula == record.nombres)):
                           record.response = "Cédula encontrada y coincidencia en nombre"
                           record.noti_ced = "Cédula encontrada y coincidencia en nombre"
                        else:
                            record.response = "Cédula encontrada pero no existe coincidencia en nombre"
                            record.noti_ced = "Cédula encontrada pero no existe coincidencia en nombre"
                        
                        if((record.response == "Cédula encontrada y coincidencia en nombre") and (record.estatus_cedula == "Cédula relacionada")):
                            record.bool_ced = True

                elif(record.intentos_cedula == 0):
                    record.noti_ced = "Has alcanzado el número máximo de intentos, todos tus datos fueron enviados al área de Soporte Comercial. En el siguiente día hábil recibirás vía e-mail la confirmación definitiva o solicitud de documentos extra para completar tu registro"
                    return {"intentos":record.intentos_cedula,"respuesta":record.noti_ced,"bool_ine":record.bool_ced,"api":record.response,"estatus_cedula":record.estatus_cedula}
                
                
    def comprobar2(self):
        for record2 in self:
            if record2.ine is False:
                record2.noti_ine = "Antes de validar debes subir tu INE/IFE. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record2.intentos_ine,"respuesta":record2.noti_ine,"bool_ine":record2.bool_ine,"api":record2.response2}
            else:
                if(record2.intentos_ine > 0):
                    record2.intentos_ine = record2.intentos_ine - 1
                    header2 = {"Authorization": "Basic emVsZTpZbTRfOHcucFg=","Content-Type":"application/json"}
                    r2=requests.post("https://ine.nubarium.com:443/ocr/obtener_datos",headers=header2,json={"id":record2.ine.decode('utf-8')})
                    json_response = r2.json()
                    a=json.dumps(json_response)
                    res=json.loads(a)
                    if "estatus" in json_response:
                        record2.response2 = res['mensaje']
                        record2.noti_ine = "Documento no encontrado o no identificado, Te invitamos a hacer el proceso desde tu dispositivo móvil, donde podrás tomar la foto de tu INE/IFE de forma directa. Si el problema persiste favor de contactar a soporte.comercial@zele.mx"
                        return {"intentos":record2.intentos_ine,"respuesta":record2.noti_ine,"bool_ine":record2.bool_ine,"api":record2.response2}
                    else:
                        if 'curp' in json_response:
                            record2.curp = res['curp']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el CURP no se pudo leer de manera correcta"

                        if 'fechaNacimiento' in json_response:
                            record2.fechaNacimiento = res['fechaNacimiento']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la FECHA DE NACIMIENTO no se pudo leer de manera correcta"

                        if 'primerApellido' in json_response:
                            record2.primerApellido = res['primerApellido']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el PRIMER APELLIDO no se pudo leer de manera correcta"

                        if 'segundoApellido' in json_response:
                            record2.segundoApellido = res['segundoApellido']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el SEGUNDO APELLIDO no se pudo leer de manera correcta"

                        if 'nombres' in json_response:
                            record2.nombres = res['nombres']
                            record2.ine_fname = "INE_" + str(record2.nombres)
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el NOMBRE no se pudo leer de manera correcta"

                        if 'sexo' in json_response:
                            record2.sexo = res['sexo']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el SEXO no se pudo leer de manera correcta"

                        if 'calle' in json_response:
                            record2.calle = res['calle']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la CALLE no se pudo leer de manera correcta"

                        if 'colonia' in json_response:
                            record2.colonia = res['colonia']
                            longitud = len(record2.colonia)
                            record2.codigo_postal = record2.colonia[longitud-5:]
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la COLONIA no se pudo leer de manera correcta"

                        if 'ciudad' in json_response:
                            record2.ciudad = res['ciudad']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la CIUDAD no se pudo leer de manera correcta"

                        if 'subTipo' in json_response:
                            record2.subTipo = res['subTipo']
                            record2.response2 = 'OK'
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el SUBTIPO no se pudo leer de manera correcta"

                        if 'claveElector' in json_response:
                            record2.claveElector = res['claveElector']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la CLAVE-ELECTOR no se pudo leer de manera correcta"

                        if 'registro' in json_response:
                            record2.registro = res['registro']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el AÑO DE REGISTRO no se pudo leer de manera correcta"

                        if 'estado' in json_response:
                            if (res['estado'] == "01"):
                                record2.estado = "Aguascalientes"
                            elif (res['estado'] == "02"):
                                record2.estado = "Baja California"
                            elif (res['estado'] == "03"):
                                record2.estado = "Baja California Sur"
                            elif (res['estado'] == "04"):
                                record2.estado = "Campeche"
                            elif (res['estado'] == "05"):
                                record2.estado = "Coahuila"
                            elif (res['estado'] == "06"):
                                record2.estado = "Colima"
                            elif (res['estado'] == "07"):
                                record2.estado = "Chiapas"
                            elif (res['estado'] == "08"):
                                record2.estado = "Chihuahua"
                            elif (res['estado'] == "09"):
                                record2.estado = "Ciudad de México"
                            elif (res['estado'] == "10"):
                                record2.estado = "Durango"
                            elif (res['estado'] == "11"):
                                record2.estado = "Guanajuato"
                            elif (res['estado'] == "12"):
                                record2.estado = "Guerrero"
                            elif (res['estado'] == "13"):
                                record2.estado = "Hidalgo"
                            elif (res['estado'] == "14"):
                                record2.estado = "Jalisco"
                            elif (res['estado'] == "15"):
                                record2.estado = "México"
                            elif (res['estado'] == "16"):
                                record2.estado = "Michoacán"
                            elif (res['estado'] == "17"):
                                record2.estado = "Morelos"
                            elif (res['estado'] == "18"):
                                record2.estado = "Nayarit"
                            elif (res['estado'] == "19"):
                                record2.estado = "Nuevo León"
                            elif (res['estado'] == "20"):
                                record2.estado = "Oaxaca"
                            elif (res['estado'] == "21"):
                                record2.estado = "Puebla"
                            elif (res['estado'] == "22"):
                                record2.estado = "Querétaro"
                            elif (res['estado'] == "23"):
                                record2.estado = "Quintana Roo"
                            elif (res['estado'] == "24"):
                                record2.estado = "San Luis Potosí"
                            elif (res['estado'] == "25"):
                                record2.estado = "Sinaloa"
                            elif (res['estado'] == "26"):
                                record2.estado = "Sonora"
                            elif (res['estado'] == "27"):
                                record2.estado = "Tabasco"
                            elif (res['estado'] == "28"):
                                record2.estado = "Tamaulipas"
                            elif (res['estado'] == "29"):
                                record2.estado = "Tlaxcala"
                            elif (res['estado'] == "30"):
                                record2.estado = "Veracruz"
                            elif (res['estado'] == "31"):
                                record2.estado = "Yucatán"
                            elif (res['estado'] == "32"):
                                record2.estado = "Zacatecas"
                            record2.id_state = self.env['res.country.state'].search([('name', '=', record2.estado)],limit=1).id
                            
    
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el ESTADO no se pudo leer de manera correcta"

                        if 'municipio' in json_response:    
                            record2.municipio = res['municipio']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el MUNICIPIO no se pudo leer de manera correcta"

                        if 'seccion' in json_response:    
                            record2.seccion = res['seccion']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la SECCIÓN no se pudo leer de manera correcta"

                        if 'localidad' in json_response:     
                            record2.localidad = res['localidad']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la LOCALIDAD no se pudo leer de manera correcta"

                        if 'emision' in json_response:     
                            record2.emision = res['emision']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, el AÑO DE EMISIÓN no se pudo leer de manera correcta"

                        if 'vigencia' in json_response:     
                            record2.vigencia = res['vigencia']
                        else:
                            record2.response2 = "Faltan datos"
                            record2.noti_ine = "Por favor intenta subir otra foto, la VIGENCIA no se pudo leer de manera correcta"

                        if record2.response2 != "Faltan datos":
                            record2.response2 = 'OK'
                            record2.bool_ine = True
                            
                elif(record2.intentos_ine == 0):
                    record2.noti_ine = "Has alcanzado el número máximo de intentos, todos tus datos fueron enviados al área de Soporte Comercial. En el siguiente día hábil recibirás vía e-mail la confirmación definitiva o solicitud de documentos extra para completar tu registro"
                    return {"intentos":record2.intentos_ine,"respuesta":record2.noti_ine,"bool_ine":record2.bool_ine,"api":record2.response2}

            
    def confirmarCed(self):
        for record3 in self:
            #record3.id_contacto = nuevo_contacto.id
                
            if(record3.estatus_cedula == "Cédula relacionada" and record3.response == "Cédula encontrada y coincidencia en nombre"):
                fecha = record3.fechaNacimiento
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
                    'state_id': record3.id_state,
                    'birthdate': fecha_full,
                    'l10n_mx_edi_curp': record3.curp,
                    'cedula': True,
                    'ine': True,
                    'client_type': 'specialist'
                })
                record3.id_contacto = nuevo_contacto.id
            elif(record3.estatus_cedula == "La licenciatura de la cédula no esta autorizada para prescribir Zélé"):
                record3.noti_ced = "La licenciatura relacionada a tu cédula no concuerda con las licenciaturas autorizadas para prescribir Zélé. Favor de ingresar cédulas profesionales de nivel licenciatura solamente. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record3.intentos_cedula,"respuesta":record3.noti_ced,"bool_ine":record3.bool_ced,"api":record3.response,"estatus_cedula":record3.estatus_cedula}
            
            elif(record3.response == "Cédula encontrada pero no existe coincidencia en nombre"):
                record3.noti_ced = "Los datos relacionados a la cédula no concuerdan con los datos leídos de tu INE/IFE, favor de ingresar una cédula relacionada a los datos leídos de tu INE/IFE. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record3.intentos_cedula,"respuesta":record3.noti_ced,"bool_ine":record3.bool_ced,"api":record3.response,"estatus_cedula":record3.estatus_cedula}
            else:
                record3.noti_ced = "Debes de ingresar tu cédula antes de avanzar. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record3.intentos_cedula,"respuesta":record3.noti_ced,"bool_ine":record3.bool_ced,"api":record3.response,"estatus_cedula":record3.estatus_cedula}  
            
    def confirmarIne(self):
        for record4 in self:
            if(record4.response2 == "OK"):
                record4.write({'state': 'cedula'})
                
            else:
                record4.noti_ine = "Antes de pasar al siguiente paso debes subir de manera correcta tu INE/IFE. Te invitamos a hacer el proceso desde tu dispositivo móvil, donde podrás tomar la foto de tu INE/IFE de forma directa. Si el problema persiste favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record4.intentos_ine,"respuesta":record4.noti_ine,"bool_ine":record4.bool_ine,"api":record4.response2}
                  
    def selfie(self):
        for record5 in self:
            if record5.ine_foto is False:
                record5.noti_foto = "Antes de validar debes subir tu foto/selfie. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record5.intentos,"respuesta":record5.noti_foto,"bool_ine":record5.bool_foto,"api":record5.response3}
            else:
                
                if(record5.intentos > 0):
                    header3 = {"Authorization": "Basic emVsZTpZbTRfOHcucFg=","Content-Type":"application/json"}
                    r3=requests.post("https://ine.nubarium.com/antifraude/reconocimiento_facial",headers=header3,json={"credencial":record5.ine.decode('utf-8'),"captura":record5.ine_foto.decode('utf-8'),"tipo":"imagen"})
                    json_r3 = r3.json()
                    c=json.dumps(json_r3)
                    res3=json.loads(c)
                    status = res3['estatus']
                    if(status=='OK'):
                        men = res3['mensaje']
                        por = res3['similitud']
                        record5.noti_foto = men
                        record5.bool_foto = True
                        mensaje = str(men) + str(' ') + str(por)
                        record5.response3 = mensaje
                        record5.intentos = record5.intentos - 1
                        record5.selfie_fname = "SELFIE_" + str(record5.nombres)
                    elif(status == 'ERROR'):
                        record5.response3 = res3['mensaje']
                        record5.intentos = record5.intentos - 1

                elif(record5.intentos == 0):
                    record5.noti_foto = "Has alcanzado el número máximo de intentos, todos tus datos fueron enviados al área de Soporte Comercial. Por lo pronto podrás hacer uso de la tienda Zélé y en el siguiente día hábil recibirás vía e-mail la confirmación definitiva o solicitud de documentos extra para completar tu registro"
                    return {"intentos":record5.intentos,"respuesta":record5.noti_foto,"bool_ine":record5.bool_foto,"api":record5.response3}
                    
    
    def confirmarSelfie(self):
        for record6 in self:
            if(record6.noti_foto == "Similitud de rostros encontrada" or record6.intentos == 0):
                record6.estatus_gen = "Completo"
            else:
                record6.noti_foto = "Debes ingresar y validar tu foto antes de avanzar. Si crees que esto es un error, favor de contactar a soporte.comercial@zele.mx"
                return {"intentos":record6.intentos,"respuesta":record6.noti_foto,"bool_ine":record6.bool_foto,"api":record6.response3}            
        
    def rechazarContacto(self):
        for record8 in self:
            record8.estatus_gen = "Rechazado"
            
    def aprobarContacto(self):
        for record9 in self:
            record9.estatus_gen = "Completo"
            
    
                
            



