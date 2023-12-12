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
        "package-name": "apache-airflow-providers-oracle",
        "name": "Oracle",
        "description": "`Oracle <https://www.oracle.com/en/database/>`__\n",
        "suspended": False,
        "source-date-epoch": 1701983404,
        "versions": [
            "3.9.0",
            "3.8.0",
            "3.7.4",
            "3.7.3",
            "3.7.2",
            "3.7.1",
            "3.7.0",
            "3.6.0",
            "3.5.1",
            "3.5.0",
            "3.4.0",
            "3.3.0",
            "3.2.0",
            "3.1.0",
            "3.0.0",
            "2.2.3",
            "2.2.2",
            "2.2.1",
            "2.2.0",
            "2.1.0",
            "2.0.1",
            "2.0.0",
            "1.1.0",
            "1.0.1",
            "1.0.0",
        ],
        "dependencies": [
            "apache-airflow>=2.6.0",
            "apache-airflow-providers-common-sql>=1.3.1",
            "oracledb>=1.0.0",
        ],
        "integrations": [
            {
                "integration-name": "Oracle",
                "external-doc-url": "https://www.oracle.com/en/database/",
                "logo": "/integration-logos/oracle/Oracle.png",
                "tags": ["software"],
            }
        ],
        "additional-extras": [{"name": "numpy", "dependencies": ["numpy"]}],
        "operators": [
            {"integration-name": "Oracle", "python-modules": ["airflow.providers.oracle.operators.oracle"]}
        ],
        "hooks": [
            {"integration-name": "Oracle", "python-modules": ["airflow.providers.oracle.hooks.oracle"]}
        ],
        "transfers": [
            {
                "source-integration-name": "Oracle",
                "target-integration-name": "Oracle",
                "python-module": "airflow.providers.oracle.transfers.oracle_to_oracle",
            }
        ],
        "connection-types": [
            {
                "hook-class-name": "airflow.providers.oracle.hooks.oracle.OracleHook",
                "connection-type": "oracle",
            }
        ],
    }
