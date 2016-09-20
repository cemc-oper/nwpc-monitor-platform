"""init data

Revision ID: 8f0a4c7f4794
Revises: 9cc5f9104d2e
Create Date: 2016-09-20 15:52:46.126675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f0a4c7f4794'
down_revision = '9cc5f9104d2e'
branch_labels = None
depends_on = None

from sqlalchemy.orm import sessionmaker
Session = sessionmaker()

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../")
from install.nwpc_monitor.model import init_data



def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    init_data.initial_owners(session)


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    init_data.remove_owners(session)
