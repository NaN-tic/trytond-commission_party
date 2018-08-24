# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Sale', 'Opportunity']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @fields.depends('party', 'agent')
    def on_change_party(self):
        super(Sale, self).on_change_party()
        if self.party and self.party.agent and not self.agent:
            self.agent = self.party.agent


class Opportunity(metaclass=PoolMeta):
    __name__ = 'sale.opportunity'

    def _get_sale_opportunity(self):
        sale = super(Opportunity, self)._get_sale_opportunity()
        if self.party and self.party.agent:
            sale.agent = self.party.agent
        return sale
