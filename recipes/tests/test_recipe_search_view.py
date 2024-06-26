from django.urls import resolve, reverse

from recipes.views import site

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func.view_class, site.RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        """ In this point, for the search feature, we already have a url that
        calls a view, and that view renders a correct template. """

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<test>'
        response = self.client.get(url)
        self.assertIn(
            # Search for "<test>", but escaped
            'Search for &quot;&lt;test&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            title=title1, slug='recipe-one', author_data={'username': 'one'},
        )
        recipe2 = self.make_recipe(
            title=title2, slug='recipe-two', author_data={'username': 'two'},
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
