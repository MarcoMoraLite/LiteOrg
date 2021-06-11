# -*- coding: utf-8 -*-
# from odoo import http


# class ValidaCurp(http.Controller):
#     @http.route('/valida_curp/valida_curp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/valida_curp/valida_curp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('valida_curp.listing', {
#             'root': '/valida_curp/valida_curp',
#             'objects': http.request.env['valida_curp.valida_curp'].search([]),
#         })

#     @http.route('/valida_curp/valida_curp/objects/<model("valida_curp.valida_curp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('valida_curp.object', {
#             'object': obj
#         })
