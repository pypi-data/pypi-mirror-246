#!/usr/bin/env python
import logging
from pathlib import Path

from edc_test_utils import DefaultTestSettings, func_main

app_name = "edc_microscopy"
base_dir = Path(__file__).absolute().parent

project_settings = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=str(base_dir / app_name / "tests" / "etc"),
    SUBJECT_VISIT_MODEL="edc_microscopy.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="edc_appointment.subjectvisitmissed",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "simple_history",
        "multisite",
        "django_crypto_fields.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_appointment.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_export.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_microscopy.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
).settings


def main():
    func_main(project_settings, *[f"{app_name}.tests"])


if __name__ == "__main__":
    logging.basicConfig()
    main()
