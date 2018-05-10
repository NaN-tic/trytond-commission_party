# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Party', 'Agent']


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
