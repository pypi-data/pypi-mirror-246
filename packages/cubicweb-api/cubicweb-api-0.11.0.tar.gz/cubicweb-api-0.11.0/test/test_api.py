# copyright 2022-2023 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""cubicweb-api automatic tests


uncomment code below if you want to activate automatic test for your cube:

.. sourcecode:: python

    from cubicweb.devtools.testlib import AutomaticWebTest

    class AutomaticWebTest(AutomaticWebTest):
        '''provides `to_test_etypes` and/or `list_startup_views` implementation
        to limit test scope
        '''

        def to_test_etypes(self):
            '''only test views for entities of the returned types'''
            return set(('My', 'Cube', 'Entity', 'Types'))

        def list_startup_views(self):
            '''only test startup views of the returned identifiers'''
            return ('some', 'startup', 'views')
"""
import json

from cubicweb.schema_exporters import JSONSchemaExporter
from test.util import BASE_URL, ApiBaseTC


class ApiTC(ApiBaseTC):
    @classmethod
    def init_config(cls, config):
        super().init_config(config)
        config.global_set_option("base-url", BASE_URL)

    def test_get_schema(self):
        schema = self.webapp.get(
            self.get_api_path("schema"),
            headers=self.custom_headers,
        ).json
        exporter = JSONSchemaExporter()
        exported_schema = exporter.export_as_dict(self.repo.schema)

        assert exported_schema == schema

    def test_successful_login_returns_204(self):
        self.webapp.post(
            self.get_api_path("login"),
            params=json.dumps({"login": self.admlogin, "password": self.admpassword}),
            content_type="application/json",
            headers=self.custom_headers,
            status=204,
        )

    def test_wrong_login_returns_401(self):
        self.webapp.post(
            self.get_api_path("login"),
            params=json.dumps({"login": self.admlogin, "password": "INVALID PASSWORD"}),
            content_type="application/json",
            headers=self.custom_headers,
            status=401,
        )

    def test_missing_custom_headers_returns_400(self):
        expected_response = {
            "data": [
                {
                    "exception": "MissingRequiredParameter",
                    "field": "X-Client-Name",
                    "message": "Missing required parameter: X-Client-Name",
                },
            ],
            "message": "Your request could not be validated against the openapi "
            "specification.",
            "title": "OpenApiValidationError",
        }
        response = self.webapp.post(
            self.get_api_path("login"),
            params=json.dumps({"login": self.admlogin, "password": self.admpassword}),
            content_type="application/json",
            status=400,
        ).json
        assert response == expected_response
        response = self.webapp.post(
            self.get_api_path("rql"),
            params=json.dumps([{"query": "test", "params": {}}]),
            content_type="application/json",
            status=400,
        ).json
        assert response == expected_response
        response = self.webapp.post(
            self.get_api_path("rql"),
            params={"queries": ""},
            content_type="multipart/form-data",
            status=400,
        ).json
        assert response == expected_response

    def test_logged_user_can_insert_data(self):
        self.login_request()
        group_eid = self.webapp.post(
            self.get_api_path("rql"),
            params=json.dumps(
                [
                    {
                        "query": "INSERT CWGroup G: G name 'test-group'",
                    }
                ]
            ),
            content_type="application/json",
            headers=self.custom_headers,
            status=200,
        ).json[0][0][0]
        with self.admin_access.repo_cnx() as cnx:
            assert cnx.entity_from_eid(group_eid).name == "test-group"

    def test_current_user_returns_user_as_json(self):
        self.login_request()
        response = self.webapp.get(
            self.get_api_path("current-user"), headers=self.custom_headers, status=200
        ).json

        assert response["login"] == self.admlogin
        assert response["dcTitle"] == self.admlogin
        assert isinstance(response["eid"], int)


class ApiMountedOnBaseUrlTC(ApiBaseTC):
    @classmethod
    def init_config(cls, config):
        super().init_config(config)
        config.global_set_option("base-url", "https://testing.cubicweb/base_path")
        config.global_set_option("receives-base-url-path", True)

    def test_served_on_base_url_path(self):
        self.webapp.get(
            "https://testing.cubicweb/base_path/api/v1/schema",
            headers=self.custom_headers,
            status=200,
        )


class ApiMountedOnRootTC(ApiBaseTC):
    @classmethod
    def init_config(cls, config):
        super().init_config(config)
        config.global_set_option("base-url", "https://testing.cubicweb/base_path")
        config.global_set_option("receives-base-url-path", False)

    def test_served_on_base_url_path(self):
        self.webapp.get(
            "https://testing.cubicweb/api/v1/schema",
            headers=self.custom_headers,
            status=200,
        )


class ApiLoginDisabledTC(ApiBaseTC):
    settings = {
        "cubicweb.includes": ["cubicweb.pyramid.auth"],
    }

    def test_login_is_disabled(self):
        """we check that it is disabled by default"""
        self.webapp.post(
            self.get_api_path("login"),
            params=json.dumps({"login": self.admlogin, "password": self.admpassword}),
            content_type="application/json",
            headers=self.custom_headers,
            status=404,
        )


if __name__ == "__main__":
    from unittest import main

    main()
