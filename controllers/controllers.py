# -*- coding: utf-8 -*-
from odoo import http

# class MethodImportRelojControl(http.Controller):
#     @http.route('/method_import_reloj_control/method_import_reloj_control/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_import_reloj_control/method_import_reloj_control/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_import_reloj_control.listing', {
#             'root': '/method_import_reloj_control/method_import_reloj_control',
#             'objects': http.request.env['method_import_reloj_control.method_import_reloj_control'].search([]),
#         })

#     @http.route('/method_import_reloj_control/method_import_reloj_control/objects/<model("method_import_reloj_control.method_import_reloj_control"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_import_reloj_control.object', {
#             'object': obj
#         })