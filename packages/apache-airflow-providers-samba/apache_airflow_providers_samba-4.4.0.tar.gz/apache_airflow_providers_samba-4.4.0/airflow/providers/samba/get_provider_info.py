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
        "package-name": "apache-airflow-providers-samba",
        "name": "Samba",
        "description": "`Samba <https://www.samba.org/>`__\n",
        "suspended": False,
        "source-date-epoch": 1701983413,
        "versions": [
            "4.4.0",
            "4.3.0",
            "4.2.2",
            "4.2.1",
            "4.2.0",
            "4.1.0",
            "4.0.0",
            "3.0.4",
            "3.0.3",
            "3.0.2",
            "3.0.1",
            "3.0.0",
            "2.0.0",
            "1.0.1",
            "1.0.0",
        ],
        "dependencies": ["apache-airflow>=2.6.0", "smbprotocol>=1.5.0"],
        "integrations": [
            {
                "integration-name": "Samba",
                "external-doc-url": "https://www.samba.org/",
                "logo": "/integration-logos/samba/Samba.png",
                "tags": ["protocol"],
            }
        ],
        "hooks": [{"integration-name": "Samba", "python-modules": ["airflow.providers.samba.hooks.samba"]}],
        "transfers": [
            {
                "source-integration-name": "Google Cloud Storage (GCS)",
                "target-integration-name": "Samba",
                "how-to-guide": "/docs/apache-airflow-providers-samba/transfer/gcs_to_samba.rst",
                "python-module": "airflow.providers.samba.transfers.gcs_to_samba",
            }
        ],
        "connection-types": [
            {"hook-class-name": "airflow.providers.samba.hooks.samba.SambaHook", "connection-type": "samba"}
        ],
    }
