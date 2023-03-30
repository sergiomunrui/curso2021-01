from odoo import models, fields 

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'
    
    name = fields.Char(
        string='Name',
        required=True
    )
    description = fields.Text(
        string='Description'
    )
    date = fields.Date(
        string='Date'
    )
    
    # Añadir los siguiente campos:
    
    # - Estado [Nuevo, Asignado, En proceso, Pendiente, Resuelto, Cancelado], que por defecto sea Nuevo

    state = fields.Selection(
        [('nuevo', 'Nuevo'),
         ('asignado', 'Asignado'),
         ('proceso', 'En proceso'),
         ('pendiente', 'Pendiente'),
         ('resuelto', 'Resuelto'),
         ('cancelado', 'Cancelado'),],
        string='State',
        default='nuevo')
    
    # - Tiempo dedicado (en horas) 
    time = fields.Float(
        string='Time')  
    
    # - Asignado (tipo check)  
    assigned = fields.Boolean(
        string='Assigned',
        readonly=True)
       
    # - Fecha límite
    date_limit = fields.Date(
        string='Date Limit')
    
    # - Acción correctiva (html)
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions to do')
    
    # - Acción preventiva (html)
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive preventive actions to do')
    
    # El campo nombre que sea obligatorio --> puesto arriba donde _name

    # En algún campo añadir un texto de ayuda indicando su funcionalidad, luego revisar que funciona.  --> con el help hecho

    # El campo Asignado:
    # - hacer que sea solo de lectura --> hecho en el campo assigned
    
    # EJERCICIO2
    # Añadir en el header los siguiente botones:

    # - Asignar, cambia estado a asignado y pone a true el campo asignado, visible sólo con estado = nuevo        
    def asignar(self):
        self.ensure_one()
        self.write({
            'state': 'asignado',
            'assigned': True})
    
    # - En proceso, visible sólo con estado = asignado
    def proceso(self):
        self.ensure_one()
        self.state = 'proceso'
        
    # - Pendiente, visible sólo con estado = en proceso o asignado
    def pendiente(self):
        self.ensure_one()
        self.state = 'pendiente'
        
    # - Finalizar, visible en cualquier estado, menos cancelado y finalizado
    def finalizar(self):
        self.ensure_one()
        self.state = 'resuelto'
        
    # - Cancelar, visible si no está cancelado
    def cancelar(self):
        self.ensure_one()
        self.state = 'cancelado'


