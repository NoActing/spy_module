# -*- coding: utf-8 -*-
from openerp import models, fields, api
import random

#   TO DO TASK
class spy(models.Model):
    _name = 'spy'
    _description = 'Spy description'

    isKilled = fields.Boolean('Killed by the Agency?')
    licenceToKill = fields.Boolean('Licence to kill:', default=False)

    # Spy
    name = fields.Char('Name', required=True)
    age = fields.Integer('Age', required=True)
    numberOfAssignations = fields.Integer('Kills')

    # date of employment
    dateOfEmployment = fields.Date('Date of employment', required=True)

    # list of specialities
    specialitiesList = fields.Many2many('speciality', string='Speciality')

    #list of enemy
    enemyList = fields.Many2many(comodel_name='spy',
                                 relation='spy_rel',
                                 column1='spy1_id',
                                 column2='spy2_id', string='Enemy')

    bestFriend = fields.Many2one('spy', 'Best Friend')

    status = fields.Selection([('a', 'Alive'), ('d', 'Dead'), ('u', 'Unknow')], 'Status', required=True)
    scubaNoKnife = fields.Boolean('Scuba no knife', compute='divingNoKnife', store=True)
    isCreated = fields.Boolean('Save', default=False)

    # Searches for speciality scuba diving without knife
    @api.one
    @api.depends('specialitiesList')
    def divingNoKnife(self):
        hasScuba = False
        hasKnife = False
        sp= self.specialitiesList
        for s in sp:
            if s.specialityName == 'knife-throwing':
                hasKnife=True
            elif s.specialityName == 'scuba diving':
                hasScuba = True
        self.scubaNoKnife=hasScuba and not hasKnife
        return self.scubaNoKnife

    # api
    # need rename to doKill marks a spy as  killed and dead but DOES NOT unlink() him
    # it sets status to dead because spy has self detonation chip in his head
    @api.one
    def doKill(self):
        domain = [('id', '=', self.id)]
        done_recs = self.search(domain)
        done_recs.write({'isKilled': True})
        done_recs.write({'status': 'd'})
        return True

    # Kills all spies with 2 kills with no licence to kill
    # it sets status to dead because spy has self detonation chip in his head
    @api.multi
    def doKill2KillsNoLicencce(self):
        domain = [('numberOfAssignations', '>', 1), ('licenceToKill', '=', False)]
        done_recs = self.search(domain)
        done_recs.write({'isKilled': True})
        done_recs.write({'status': 'd'})
        return True

    # override create in order to set isCreated so in edit some fields are read only
    @api.model
    def create(self, vals):
        vals['isCreated'] = True
        res_id = super(spy, self).create(vals)
        return res_id

    # add one more numberOfAssignations to total number for a spy
    @api.one
    def addOneKill(self):
        if (self.status != 'd'):
            self.numberOfAssignations = self.numberOfAssignations + 1
            return self.numberOfAssignations
        else:
            return False


class speciality(models.Model):
    _name = 'speciality'
    _description = 'a pursuit, area of study, or skill to which someone has devoted much time and effort and in which they are expert.'

    speciality_ids = fields.Integer()
    specialityName = fields.Char('Speciality', required=True)

class tag(models.Model):
    _name = "tag"
    _description = 'taggig soemthing'
