# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# NOTE! THIS FILE IS AUTOMATICALLY GENERATED AND WILL BE
# OVERWRITTEN WHEN PREPARING PACKAGES.
#
# IF YOU WANT TO MODIFY THIS FILE, YOU SHOULD MODIFY THE TEMPLATE
# `get_provider_info_TEMPLATE.py.jinja2` IN the `dev/breeze/src/airflow_breeze/templates` DIRECTORY


def get_provider_info():
    return {
        "package-name": "apache-airflow-providers-opsgenie",
        "name": "Opsgenie",
        "description": "`Opsgenie <https://www.atlassian.com/software/opsgenie>`__\n",
        "suspended": False,
        "source-date-epoch": 1701983403,
        "versions": [
            "5.4.0",
            "5.3.0",
            "5.2.0",
            "5.1.1",
            "5.1.0",
            "5.0.0",
            "4.0.0",
            "3.1.0",
            "3.0.3",
            "3.0.2",
            "3.0.1",
            "3.0.0",
            "2.0.1",
            "2.0.0",
            "1.0.2",
            "1.0.1",
            "1.0.0",
        ],
        "dependencies": ["apache-airflow>=2.6.0", "opsgenie-sdk>=2.1.5"],
        "integrations": [
            {
                "integration-name": "Opsgenie",
                "external-doc-url": "https://www.atlassian.com/software/opsgenie",
                "how-to-guide": ["/docs/apache-airflow-providers-opsgenie/operators/opsgenie_alert.rst"],
                "logo": "/integration-logos/opsgenie/Opsgenie.png",
                "tags": ["service"],
            }
        ],
        "operators": [
            {
                "integration-name": "Opsgenie",
                "python-modules": ["airflow.providers.opsgenie.operators.opsgenie"],
            }
        ],
        "hooks": [
            {"integration-name": "Opsgenie", "python-modules": ["airflow.providers.opsgenie.hooks.opsgenie"]}
        ],
        "connection-types": [
            {
                "hook-class-name": "airflow.providers.opsgenie.hooks.opsgenie.OpsgenieAlertHook",
                "connection-type": "opsgenie",
            }
        ],
        "notifications": ["airflow.providers.opsgenie.notifications.opsgenie.OpsgenieNotifier"],
    }
