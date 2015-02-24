# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.login_monitor import Session
from collective.login_monitor import messageFactory as _
from collective.login_monitor.models import LoginRecord
from datetime import date, datetime, timedelta
from sqlalchemy import and_, or_, not_
from sqlalchemy import func, distinct
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError


class UsersLoginMonitorView(BrowserView):
    
    ignored_groups = ('Administrators', 'Reviewers', 'AuthenticatedUsers', 'Site Administrators')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        request.set('disable_border', True)
        self.last_query_size = 0

    def __call__(self):
        if self.request.form.get('export'):
            self._exportCSV()
            return
        return self.index()

    def _exportCSV(self):
        translate = lambda text: translation_service.utranslate(
            msgid=text,
            domain="collective.login_monitor",
            context=context)

        context = self.context
        translation_service = getToolByName(context,'translation_service')
        response = self.request.response
        response.setHeader('Content-Type', 'text/csv')
        response.addHeader('Content-Disposition',
                           'attachment;filename=login-report-%s.csv' % datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        response.write(("%s,%s,%s,%s,%s\n" % (translate(u"User ID"),
                                              translate(u"Full Name"),
                                              translate(u"E-mail"),
                                              translate(u"Login count"),
                                              translate(u"Last login date"))).encode('utf-8'))
        results = self.search_results()
        for row in results:
            response.write(("%s,%s,%s,%s,%s\n" % (row.get('user_id'),
                                                  row.get('user_fullname'),
                                                  row.get('user_email'),
                                                  row.get('login_count'),
                                                  row.get('last_login_date'))).encode('utf-8'))

    def default_start_date(self, canonical=False):
        today = date.today()
        monthago = today - timedelta(28)
        i = 0
        while today.day > monthago.day and i<3:
            i+=1
            monthago-=timedelta(1)
        if canonical:
            return monthago.strftime('%Y-%m-%d')
        return monthago.strftime('%d/%m/%Y')

    def default_end_date(self, canonical=False):
        if canonical:
            return date.today().strftime('%Y-%m-%d')
        return date.today().strftime('%d/%m/%Y')       

    @property
    def groups(self):
        '''
        Returns the groups of this site for filling the select in the form
        
        To add sample users do something like that
        [pas.userFolderAddUser(str(x).zfill(8), str(x).zfill(8), 
        ('Member',), (), ('Test 1',),) for x in range(4)]
        '''
        pas = getToolByName(self.context, 'acl_users')
        for group in pas.searchGroups():
            if not group['id'] in self.ignored_groups:
                yield group

    def _load_exclude_users(self, site_id):
        """Load user ids from login in the range. Used for performing negative logic"""
        exclude = self.request.form.get('exclude', '')
        if exclude:
            results = Session.query(distinct(LoginRecord.user_id)).filter(
                            LoginRecord.plone_site_id==site_id,
                            LoginRecord.timestamp>=self._start,
                            LoginRecord.timestamp<=self._end).all()
            return [user[0] for user in results]
        return None

    def _get_results(self, results):
        acl_users = getToolByName(self.context, 'acl_users')
        self.last_query_size = len(results)

        processed = []
        for row in results:
            result = {'user_id': row.user_id,
                      'login_count': row[1],
                      'user_fullname': None,
                      'user_email': None,
                      'last_login_date': row[2]}
            # unluckily searchUsers is not returnig the email address
            #user = acl_users.searchUsers(login=row.user_id, exact_match=True)
            user = acl_users.getUserById(row.user_id)
            if user:
                result['user_fullname'] = user.getProperty('fullname')
                result['user_email'] = user.getProperty('email')
            processed.append(result)
        return processed

    def _query_users(self, query, site_id):
        exclude_ids = self._load_exclude_users(site_id)
        if not exclude_ids:
            results = Session.query(LoginRecord.user_id, func.count(LoginRecord.user_id),
                                    func.max(LoginRecord.timestamp)) \
                    .filter(and_(LoginRecord.user_id.startswith(query),
                                 LoginRecord.plone_site_id==site_id,
                                 LoginRecord.timestamp>=self._start,
                                 LoginRecord.timestamp<=self._end)) \
                    .group_by(LoginRecord.user_id,
                              LoginRecord.plone_site_id).order_by(LoginRecord.user_id).all()
        else:
            results = Session.query(LoginRecord.user_id, func.count(LoginRecord.user_id),
                                    func.max(LoginRecord.timestamp)) \
                    .filter(and_(LoginRecord.user_id.startswith(query),
                                 LoginRecord.plone_site_id==site_id,
                                 not_(LoginRecord.user_id.in_(exclude_ids)))) \
                    .group_by(LoginRecord.user_id,
                              LoginRecord.plone_site_id).order_by(LoginRecord.user_id).all()
        return self._get_results(results)

    def _load_users(self, user_ids, site_id):
        """Load data from all users in the set (commonly taken from groups member ids)"""
        exclude_ids = self._load_exclude_users(site_id)
        if not exclude_ids:
            results = Session.query(LoginRecord.user_id, func.count(LoginRecord.user_id),
                                    func.max(LoginRecord.timestamp)) \
                    .filter(and_(LoginRecord.user_id.in_(user_ids),
                                 LoginRecord.plone_site_id==site_id,
                                 LoginRecord.timestamp>=self._start,
                                 LoginRecord.timestamp<=self._end)) \
                    .group_by(LoginRecord.user_id,
                              LoginRecord.plone_site_id).order_by(LoginRecord.user_id).all()
        else:
            results = Session.query(LoginRecord.user_id, func.count(LoginRecord.user_id),
                                    func.max(LoginRecord.timestamp)) \
                    .filter(and_(LoginRecord.user_id.in_(user_ids),
                                 LoginRecord.plone_site_id==site_id,
                                 not_(LoginRecord.user_id.in_(exclude_ids)))
                                 ) \
                    .group_by(LoginRecord.user_id,
                              LoginRecord.plone_site_id).order_by(LoginRecord.user_id).all()
            import pdb;pdb.set_trace()
        return self._get_results(results)

    def _all_users(self, site_id):
        exclude_ids = self._load_exclude_users(site_id)
        if not exclude_ids:
            results = Session.query(LoginRecord.user_id, func.count(LoginRecord.user_id),
                                    func.max(LoginRecord.timestamp)) \
                    .filter(LoginRecord.plone_site_id==site_id,
                            LoginRecord.timestamp>=self._start,
                            LoginRecord.timestamp<=self._end) \
                    .group_by(LoginRecord.user_id,
                              LoginRecord.plone_site_id).order_by(LoginRecord.user_id).all()
        else:
            results = Session.query(LoginRecord.user_id, func.count(LoginRecord.user_id),
                                    func.max(LoginRecord.timestamp)) \
                    .filter(LoginRecord.plone_site_id==site_id,
                            not_(LoginRecord.user_id.in_(exclude_ids))) \
                    .group_by(LoginRecord.user_id,
                              LoginRecord.plone_site_id).order_by(LoginRecord.user_id).all()            
        return self._get_results(results)

    def _prepare_interval(self):
        # we don't have strptime on Python 2.4
        sy,sm,sd = self.request.form.get('start_date').split('-')
        ey,em,ed = self.request.form.get('end_date').split('-')
        self._start = datetime(int(sy), int(sm), int(sd))
        self._end = datetime(int(ey), int(em), int(ed), 23, 59, 59)

    def search_results(self):
        """Search results"""
        self._prepare_interval()
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        user_id = self.request.form.get('user_id', '')
        try:
            if user_id:
                return self._query_users(user_id, portal.getId())
            group_id = self.request.form.get('group_id', '')
            if group_id:
                pas = getToolByName(self.context, 'acl_users')
                group = pas.getGroupById(group_id)
                if not group:
                    group_users = []
                else:
                    group_users = group.getGroupMemberIds()
                return self._load_users(group_users, portal.getId())
            # no filter; let's load ALL users
            return self._all_users(portal.getId())
        except ComponentLookupError:
            self.request.response.redirect("%s/%s" % (portal.absolute_url(), self.__name__))
            portal.plone_utils.addPortalMessage(_('component_lookup_error',
                                                  default=u"Could not connect to the database engine. "
                                                          u"Please check your configuration"),
                                                type="error")
            return []

    def toLocalizedTime(self, date):
        ploneview = getMultiAdapter((self.context, self.request), name=u'plone')
        return ploneview.toLocalizedTime(date, long_format=True)
    
