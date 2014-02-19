
from Products.CMFPlone.utils import getToolByName


PROFILE_ID = 'profile-collective.login_monitor:default'


def run_import_step(context, step):
    """Re-import some specified import step for Generic Setup.
    """
    setup = getToolByName(context, 'portal_setup')
    return setup.runImportStepFromProfile(PROFILE_ID, step)


def upgrade_1000_to_1100(context):
    run_import_step(context, 'controlpanel')


