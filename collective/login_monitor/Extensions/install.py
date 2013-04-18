# -*- coding: utf-8 -*-

from collective.login_monitor import logger

def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-collective.login_monitor:uninstall')
        logger.info("Uninstall done")
