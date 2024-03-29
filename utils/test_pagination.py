from unittest import TestCase

from django.urls import reverse

from recipes.tests.test_recipe_base import RecipeTestBase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),  # total number of pages avaliable
            qty_pages=4,  # number of pages to be shown to user
            current_page=1,  # the current page the user is in
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa E501
        # Current page = 1 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page = 14 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=14,
        )['pagination']
        self.assertEqual([13, 14, 15, 16], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_visible(self):
        # Current page = 19 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 19 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 20 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 20 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            # that page doesn't exists, but last range is shown anyways
            current_page=21,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)


class RecipePaginationTest(RecipeTestBase):
    def test_recipe_pagination_loads_correct_number_of_items_per_page(self):
        for index, _ in enumerate(range(0, 20)):
            self.make_recipe(slug=f'recipe-slug-{index}', author_data={
                'username': f'user-{index}'
            })

        response = self.client.get(reverse('recipes:home')+'?page=one')
        len_recipes = len(response.context['recipes'])
        self.assertEqual(len_recipes, 9)
