import pytest
from apps.products.models import Product


from apps.testing import BaseAPITestCase, track_queries
from tests.integration.products.factories import ProductFactory


class PublicProductAPITest(BaseAPITestCase):
    base_url = "/api/public/products"

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test__list__success(self):
        # GIVEN 2 products
        product1 = ProductFactory()
        product2 = ProductFactory()
        # WHEN the list API is requested
        response = self.make_http_request("GET", self.get_list_url())
        # THEN the two products are returned in the reponse results
        product_ids = [str(product1.id), str(product2.id)]
        response_product_ids = [d["id"] for d in response.data["results"]]
        self.assertEqual(response_product_ids, product_ids)


class PublicProductPerformanceTest(BaseAPITestCase):
    base_url = "/api/public/products"

    def setUp(self):
        for _ in range(10):
            ProductFactory()

    @track_queries
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test__list__querycount(self):
        # we should be notified in CI if the number of queries for this view changes
        self.make_http_request("GET", self.get_list_url())


class UserBasedProductAPITest(BaseAPITestCase):
    base_url = "/api/products"

    def test_no_credentials__list__unauthorized(self):
        # GIVEN no user
        # WHEN request list view
        # THEN 401 unauthorized error
        self.make_http_request("GET", self.get_list_url(), permitted_codes=[401])

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_user__list__success(self):
        # GIVEN logged in user
        self.login_user()
        # WHEN list is called # THEN success
        self.make_http_request("GET", self.get_list_url())

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_user__create_product__success(self):
        # GIVEN logged in user
        self.login_user()
        product_name = "Test Product!"
        # WHEN create Product
        self.make_http_request(
            "POST", self.get_list_url(), data=dict(name=product_name)
        )
        # THEN it is saved/exists in the database
        self.assertTrue(Product.objects.filter(name=product_name).exists())
