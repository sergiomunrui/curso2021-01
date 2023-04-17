from odoo import models, fields, api

# =====================================================================================================

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
        string='Tags')
    
# ===================================================================================================================  

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket' 
    
    # CAMPOS ONE2ONE, ONE2MANY Y MANY2MANY
    
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
    
    # Hacemos un campo many to one para apuntar al usuario. Muchos tickets pueden apuntar a uno solo, en este caso apuntan a user_id
    user_id = fields.Many2one(
        comodel_name='res.users', # res.users porque en link de la web aparece de esa forma cuando gestionamos usuarios
        string='Assigned to')
    
        
    # CAMPOS HABITUALES
    
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
    
    state = fields.Selection(
        [('nuevo', 'Nuevo'),
         ('asignado', 'Asignado'),
         ('proceso', 'En proceso'),
         ('pendiente', 'Pendiente'),
         ('resuelto', 'Resuelto'),
         ('cancelado', 'Cancelado'),],
        string='State',
        default='nuevo') # - Estado del ticket, por defecto muestra nuevo si no le asignamos ninguno
    
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
        
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False
            
    # Hacer un campo calculado que dentro de un ticket muestre la cantidad de tickets asociados al mismo user
    
    ticket_cantidad = fields.Integer(
        string='Ticket Cantidad',
        compute='_compute_ticket_cantidad') #le pasamos el resultado de la def _compute_ticket_cantidad
    
    @api.depends('user_id')
    def _compute_ticket_cantidad (self):
        for record in self:  # Iteramos sobre los registros que contiene el modelo en el que estamos
            other_tickets = self.env['helpdesk.ticket'].search([('user_id', '=', record.user_id.id)]) # Buscamos los usuarios que coincidan con ese user_id y guardamos en un array
            record.ticket_cantidad = len(other_tickets) # Guardamos en el campo ticket_cantidad el número de elementos del array other_tickets
            
    # crear un campo nombre de etiqueta, y hacer un botón que cree la nueva etiqueta con ese nombre y lo asocie al ticket
    tag_name = fields.Char(
        string='Nombre Etiqueta'
    )
    
    def create_tag(self):
        self.ensure_one() # Porque va a ser un botón que va a estar dentro del formulario
        self.write({ 
            'tag_ids': [(0,0, {'name': self.tag_name})]           
        })
        self.tag_name = False

