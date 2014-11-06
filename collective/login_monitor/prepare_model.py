# -*- coding: utf-8 -*-


def prepare(engine):
    from collective.login_monitor import ORMBase
    import collective.login_monitor.models
    ORMBase.metadata.create_all(engine)
