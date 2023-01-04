import json

from apps.testing import BaseGraphglTestCase
from tests.integration.products.factories import ProductFactory


class ProductGraphqlTestCase(BaseGraphglTestCase):
    def test__list_all_products__success(self):
        # GIVEN 2 products
        product1 = ProductFactory()
        product2 = ProductFactory()

        # WHEN allProducts query is called
        response = self.make_request(
            """
                query {
                    allProducts {
                        edges {
                            node {
                                id
                                name
                            }
                        }
                    }
                }
            """
        )
        # THEN products are returned from the GraphQL API
        product_ids = [str(product1.id), str(product2.id)]
        response_product_ids = [
            d["node"]["id"]
            for d in json.loads(response.content)["data"]["allProducts"]["edges"]
        ]
        self.assertEqual(response_product_ids, product_ids)
