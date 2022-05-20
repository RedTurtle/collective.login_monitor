# -*- coding: utf-8 -*-

from ZODB.POSException import ConflictError
from collective.login_monitor import Session, logger
from collective.login_monitor.models import User, LoginRecord
from datetime import datetime
from sqlalchemy import and_
from zope.component import getSiteManager
import traceback


def register_event(user, event):
    portal = getSiteManager().portal_url.getPortalObject()
    site_id = portal.getId()
    user_id = user.getId()
    try:
        if Session.query(User).filter(and_(User.user_id == user_id,
                                           User.plone_site_id == site_id)).count() == 0:
            user = User(user_id, site_id)
            Session.add(user)
        else:
            user = Session.query(User).filter(and_(User.user_id == user_id,
                                                   User.plone_site_id == site_id)).one()

        timestamp = datetime.now()
        record = LoginRecord(user_id, site_id, timestamp)
        Session.add(record)
    except ConflictError:
        raise
    except Exception:
        logger.error(f"Unable to store login informations: {traceback.format_exc()}" )
