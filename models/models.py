# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _
import base64
import xlrd
import io
from odoo.tools import pycompat
from datetime import datetime
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class RelojControl(models.TransientModel):
    _name = 'reloj.wizard'
    
    data_file = fields.Binary(string="Archivo")
    ultimo_dia = fields.Date('Fecha Final',help='Selecciona el último días del mes de la nómina')

    @api.one
    def formatear_rut(self,cadena):
        rut = ''.join(filter(str.isdigit, cadena))  # elimina caracteres no numéricos
        rut_sin_dv = rut[:-1]  # obtiene el RUT sin el dígito verificador
        dv = rut[-1]  # obtiene el dígito verificador
        rut_formateado = f'{rut_sin_dv[:-6]}.{rut_sin_dv[-6:-3]}.{rut_sin_dv[-3:]}-{dv}'  # agrega puntos y guión
        return rut_formateado    

    @api.multi
    def Import_reloj(self):        
        try:
            file_datas = base64.decodestring(self.data_file)
            workbook = xlrd.open_workbook(file_contents=file_datas)
            sheet = workbook.sheet_by_index(0)
            data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
            data.pop(0)
            file_data = data
        except:
            raise exceptions.Warning(_('Please select proper file type.'))

        nomina = self.env['hr.payslip']
        empleado= self.env['hr.employee']
        fila=1        
        for row in file_data:
            if fila>=5:
                if not (row[0] or row[2] or row[3]):
                    raise exceptions.Warning(_('Partner,Journal,Date values are required.'))
                rut=""
                rut=str(row[0]).replace('.0','')
                rut_formateado=self.formatear_rut(rut)
                rut_formateado=rut_formateado[0]
                dias_trabajados_excel=row[11]
                
                empleado_id = empleado.search([('identification_id', '=ilike', rut_formateado)],limit=1)            
                if empleado_id:
                    empleado_id=empleado_id.id
                else:
                    empleado_id = empleado.search([('identification_id', '=ilike', rut),('active','=',False)],limit=1)            
                    if empleado_id:
                        empleado_id=empleado_id.id
                    else:
                        raise ValidationError("Empleado con rut {} y nombre {} no existe!".format(rut_formateado,row[2]))                

                nomina_empleado=nomina.search([('employee_id','=',empleado_id),('date_to','=',self.ultimo_dia)],limit=1)
                if nomina_empleado:
                    domain=[
                        ('payslip_id','=',nomina_empleado.id),
                        ('sequence','=',1)
                    ]
                    dias_trabajados=self.env['hr.payslip.worked_days'].search(domain)
                else:
                    raise ValidationError("No existe nómina para el rut %s !" % rut)

                worked_days_vals = {
                        'number_of_days':dias_trabajados_excel
                    }
                dias_trabajados.write(worked_days_vals)

            fila+=1
