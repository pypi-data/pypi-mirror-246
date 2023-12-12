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
        "package-name": "apache-airflow-providers-pinecone",
        "name": "Pinecone",
        "description": "`Pinecone <https://docs.pinecone.io/docs/overview>`__\n",
        "suspended": False,
        "source-date-epoch": 1701983407,
        "versions": ["1.1.0", "1.0.0"],
        "integrations": [
            {
                "integration-name": "Pinecone",
                "external-doc-url": "https://docs.pinecone.io/docs/overview",
                "how-to-guide": ["/docs/apache-airflow-providers-pinecone/operators/pinecone.rst"],
                "tags": ["software"],
            }
        ],
        "dependencies": ["apache-airflow>=2.6.0", "pinecone-client>=2.2.4"],
        "hooks": [
            {"integration-name": "Pinecone", "python-modules": ["airflow.providers.pinecone.hooks.pinecone"]}
        ],
        "connection-types": [
            {
                "hook-class-name": "airflow.providers.pinecone.hooks.pinecone.PineconeHook",
                "connection-type": "pinecone",
            }
        ],
        "operators": [
            {
                "integration-name": "Pinecone",
                "python-modules": ["airflow.providers.pinecone.operators.pinecone"],
            }
        ],
    }
