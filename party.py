# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Party', 'Agent', 'Invoice', 'Sale', 'Opportunity']


class Party:
    __metaclass__ = PoolMeta
    __name__ = 'party.party'

    agent = fields.Many2One('commission.agent', 'Agent')


class Agent:
    __metaclass__ = PoolMeta
    __name__ = 'commission.agent'

    assigned_parties = fields.One2Many('party.party', 'agent',
        'Assigned Parties')

    @classmethod
    def copy(cls, agents, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default.setdefault('assigned_parties')
        return super(Agent, cls).copy(agents, default)


class Sale:
    __metaclass__ = PoolMeta
    __name__ = 'sale.sale'

    @fields.depends('party', 'agent')
    def on_change_party(self):
        super(Sale, self).on_change_party()
        if self.party and self.party.agent and not self.agent:
            self.agent = self.party.agent


class Opportunity:
    __metaclass__ = PoolMeta
    __name__ = 'sale.opportunity'

    def _get_sale_opportunity(self):
        sale = super(Opportunity, self)._get_sale_opportunity()
        if self.party and self.party.agent:
            sale.agent = self.party.agent
        return sale


class Invoice:
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice'

    @fields.depends('party', 'agent')
    def on_change_party(self):
        super(Invoice, self).on_change_party()
        if self.party and self.party.agent and not self.agent:
            self.agent = self.party.agent
