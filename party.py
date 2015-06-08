# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Party', 'Agent', 'Invoice', 'Sale']
__metaclass__ = PoolMeta


class Party:
    __name__ = 'party.party'

    agent = fields.Many2One('commission.agent', 'Agent')


class Agent:
    __name__ = 'commission.agent'

    assigned_parties = fields.One2Many('party.party', 'agent',
        'Assigned Parties')

    @classmethod
    def copy(cls, agents, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['assigned_parties'] = None
        return super(Agent, cls).copy(agents, default)


class Sale:
    __name__ = 'sale.sale'

    @fields.depends('agent')
    def on_change_party(self):
        changes = super(Sale, self).on_change_party()
        if self.party and self.party.agent and not self.agent:
            changes['agent'] = self.party.agent.id
            changes['agent.rec_name'] = self.party.agent.rec_name
        return changes


class Invoice:
    __name__ = 'account.invoice'

    @fields.depends('agent')
    def on_change_party(self):
        changes = super(Invoice, self).on_change_party()
        if self.party and self.party.agent and not self.agent:
            changes['agent'] = self.party.agent.id
            changes['agent.rec_name'] = self.party.agent.rec_name
        return changes
