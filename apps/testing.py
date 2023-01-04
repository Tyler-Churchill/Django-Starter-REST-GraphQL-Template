import json

import factory  # type: ignore
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connections
from django.db.utils import DEFAULT_DB_ALIAS
from django.template.defaultfilters import truncatechars
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from graphene_django.utils.testing import GraphQLTestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore
from snapshottest import TestCase as SnapshotTestCase  # type: ignore

from apps.users.models import User


class BaseFactory(factory.StubFactory):
    pass


class BaseModelFactory(factory.django.DjangoModelFactory):
    pass


class UserFactory(BaseModelFactory):
    name = factory.Sequence(lambda n: "User #%s" % n)

    class Meta:
        model = settings.AUTH_USER_MODEL


class BaseTestCase(TestCase):
    pass


class BaseGraphglTestCase(GraphQLTestCase, BaseTestCase, SnapshotTestCase, TestCase):
    def make_request(self, query, assert_success=True, *args, **kwargs):
        response = self.query(query=query, *args, **kwargs)
        if assert_success:
            self.assertResponseNoErrors(response)
        return response


class BaseAPITestCase(BaseTestCase, SnapshotTestCase, TestCase):
    base_url: str | None = None
    client = APIClient()
    client_class = APIClient

    def set_client_auth(self, key: str):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {key}")

    def get_list_url(self):
        return self.base_url

    def json_loads(self, str):
        if str:  # Don't load JSON if no data given
            return json.loads(str)

    def delete_keys_from_dict(self, dict_del, lst_keys):
        for k in lst_keys:
            try:
                del dict_del[k]
            except KeyError:
                pass
        for v in dict_del.values():
            if isinstance(v, dict):
                self.delete_keys_from_dict(v, lst_keys)
            if isinstance(v, list):
                for x in v:
                    if isinstance(x, dict):
                        self.delete_keys_from_dict(x, lst_keys)
        return dict_del

    def _make_request(
        self,
        method,
        path,
        data=None,
        permitted_codes=None,
        query_params=None,
        content_type=None,
        client=None,
        *args,
        **kwargs,
    ):
        if data is None:
            data = {}

        if client is None:
            client = self.client

        if content_type is None:
            # Use JSON type+encoding by default
            content_type = "application/json"
            data = json.dumps(data, cls=DjangoJSONEncoder)

        # Add query parameters to URL, if given
        if query_params is not None:
            for query_key, query_val in query_params.items():
                if isinstance(query_val, bytes):
                    query_params[query_key] = query_val.decode()
            path_data = self.json_loads(self.json_dumps(query_params))

            # Add query strings to path
            path = self.url_with_querystring(path, **path_data)

        response = client.generic(
            method, path, data, content_type=content_type, *args, **kwargs
        )

        self.ensure_successful_response(response, permitted_codes)

        return response

    def make_request(self, *args, **kwargs):
        response = self._make_request(*args, **kwargs)

        return self.json_loads(response.content)

    def make_http_request(self, *args, **kwargs):
        return self._make_request(*args, **kwargs)

    def ensure_successful_response(self, response, permitted_codes=None):
        # Set default permitted_codes
        if permitted_codes is None:
            permitted_codes = [200, 201, 204]

        # Convert single status codes expected to array
        if not isinstance(permitted_codes, list):
            permitted_codes = [permitted_codes]

        code = response.status_code
        if code not in permitted_codes:
            reason = truncatechars(response.content or str(response), 500)
            raise AssertionError(
                "unexpected status code: %s (%s %s)"
                % (code, response.reason_phrase, reason)
            )

    def login_user(self, user=None):
        if user is None:
            user = User.objects.create()
        refresh = RefreshToken.for_user(user)
        self.set_client_auth(refresh.access_token)
        return user, refresh


def track_queries(fn):
    """
    Add this decorator to any test method to automatically track, store, and compare total queries of that test

    For performance optimization with Django, minimizing the number of quries being ran for a given View
    is preferred. This is not a hard rule, a single aggregate query can potentially still be optimized.

    @track_queries
    def test_whatever
        ...
    """

    def _wrapped(*args, **kwargs):
        conn = connections[DEFAULT_DB_ALIAS]
        func = args[0]
        with CaptureQueriesContext(conn) as queries:
            fn(*args, **kwargs)
        data = dict(total_queries=queries.final_queries)
        func.assertMatchSnapshot(data)

    return _wrapped
