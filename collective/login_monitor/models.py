# -*- coding: utf-8 -*-

from sqlalchemy import schema, types
from sqlalchemy import Table
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKeyConstraint
from collective.login_monitor import ORMBase


metadata = ORMBase.metadata

class User(ORMBase):

    __tablename__ = 'users'

    user_id = schema.Column(types.Unicode(100), primary_key=True)
    plone_site_id = schema.Column(types.Unicode(20), primary_key=True)

    def __init__(self, user_id, plone_site_id):
        self.user_id = user_id
        self.plone_site_id = plone_site_id


users = Table('users', metadata)
users.append_constraint(PrimaryKeyConstraint('user_id', 'plone_site_id'))


class LoginRecord(ORMBase):

    __tablename__ = 'logins_registry'

    login_id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    user_id = schema.Column(types.Unicode(100), nullable=False)
    plone_site_id = schema.Column(types.Unicode(20), nullable=False)
    timestamp = schema.Column(types.DateTime(), nullable=False)

    def __init__(self, user_id, plone_site_id, timestamp):
        self.user_id = user_id
        self.plone_site_id = plone_site_id
        self.timestamp = timestamp

logins_registry = Table('logins_registry', metadata)
logins_registry.append_constraint(ForeignKeyConstraint(['user_id', 'plone_site_id'],
                                                       ['users.user_id', 'users.plone_site_id']))
