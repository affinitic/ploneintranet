# coding=utf-8
import logging

default_profile = 'profile-ploneintranet.layout:default'
logger = logging.getLogger(__file__)


def update_registry(context):
    logger.info('Import Registry for %s', default_profile)
    context.runImportStepFromProfile(
        default_profile,
        'plone.app.registry',
        run_dependencies=False,
    )


def update_actions(context):
    logger.info('Import Actions for %s', default_profile)
    context.runImportStepFromProfile(
        default_profile,
        'actions',
        run_dependencies=False,
    )
