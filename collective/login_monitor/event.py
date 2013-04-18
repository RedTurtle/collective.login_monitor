# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import and_

from zope.component import getSiteManager

from collective.login_monitor import Session
from collective.login_monitor.models import User, LoginRecord

def register_event(user, event):
    portal = getSiteManager().portal_url.getPortalObject()
    site_id = portal.getId()
    user_id = user.getId()
    
    if Session.query(User).filter(and_(User.user_id == user_id,
                                       User.plone_site_id == site_id)).count()==0:
        user = User(user_id.decode('utf-8'), site_id.decode('utf-8'))
        Session.add(user)
    else:
        user = Session.query(User).filter(and_(User.user_id == user_id,
                                               User.plone_site_id == site_id)).one()
    
    timestamp = datetime.now()
    record = LoginRecord(user_id.decode('utf-8'), site_id.decode('utf-8'), timestamp)
    Session.add(record)
