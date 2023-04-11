from odoo import models, fields 

# ===========================================================================================

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'
    
    name = fields.Char()
    date = fields.Date()
    
    # Una acción o varias acciones solo podrán estar en un ticket de venta
    # En este caso hay que hacer un inverso en la clase HelpdeskTicket de tipo One2many
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket')

# =======================================================================================================    

class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Tag'
    
    name = fields.Char()
    
    # Con este campo apuntamos al modelo de tickets y vemos que tickets tienen asociados una determinada etiqueta 
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        relation='helpdesk_ticket_tag_rel', # Este es el nombre de la tabla intermedia para relacionar los pares de registros en los Many2many
        column1='tag_id', # Este es el nombre de la columna de la tabla1 que queremos relacionar
        column2='ticket_id', # Este es el nombre de la columna de la tabla2 que queremos relacionar
        string='Tickets')
    
# ===================================================================================================================  

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket' 
    
    # Con este campo apuntamos al modelo de etiquetas (Tag) y vemos qué etiquetas tienen asociadas un determinado ticket
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        relation='helpdesk_ticket_tag_rel', # Este es el nombre de la tabla intermedia para relacionar los pares de registros en los Many2many
        column1='ticket_id', # Este es el nombre de la columna de la tabla1 que queremos relacionar
        column2='tag_id', # Este es el nombre de la columna de la tabla2 que queremos relacionar
        string='Tags')
    
        
    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions')
    
    # Hacemos un campo many to one para apuntar al usuario. Muchos apuntan a uno solo, en este caso apuntan a user_id
    user_id = fields.Many2one(
        comodel_name='res.users', # res.users porque en link de la web aparece de esa forma cuando gestionamos usuarios
        string='Assigned to')
    
        
    name = fields.Char(
        string='Name',
        required=True
    )
    description = fields.Text(
        string='Description',
        translate=True      
    )
    date = fields.Date(
        string='Date'
    )
    
    # - Estado del ticket, por defecto muestra nuevo si no le asignamos ninguno

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
    
    # Es un campo de tipo muchos a uno porque muchos tickets pueden ser asignados a un solo usuario
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Asignado a')
    
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


