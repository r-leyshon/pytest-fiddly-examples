"""Testing pandas operations with test fixtures."""
from example_pkg.update_food import fancy_dessert


class TestFancyDessert:
    """Tests for fancy_dessert()."""

    def test_fancy_dessert_updates_fixtures_as_expected(
        self,
        _mm_session_scoped,
        _mm_module_scoped,
        _mm_class_scoped,
        _mm_function_scoped,
    ):
        """Test fancy_dessert() changes favourite_food values to dessert.

        These assertions depend on the current state of the scoped fixtures. If
        changes performed in
        test_feed_characters::TestServeFood::test_serve_food_updates_df()
        persist, then characters will not have empty stomach_contents,
        resulting in a switch of their favourite_food to dessert.
        """
        # first, check update_food() with the session-scoped fixture.
        assert list(fancy_dessert(_mm_session_scoped)["fave_food"].values) == [
            "brownie",
            "ice cream",
            "apple crumble",
            "pudding",
            "banana bread",
        ], (
            "The changes to the session-scoped df 'stomach_contents' column",
            " have not persisted as expected.",
        )
        # next, check update_food() with the module-scoped fixture.
        assert list(fancy_dessert(_mm_module_scoped)["fave_food"].values) == [
            "carrots",
            "beans",
            "scooby snacks",
            "burgers",
            "hot dogs",
        ], (
            "The module-scoped df 'stomach_contents' column was not as",
            " expected",
        )
        # now, check update_food() with the class-scoped fixture. Note that we
        # are now making assertions about changes from a different class.
        assert list(fancy_dessert(_mm_class_scoped)["fave_food"].values) == [
            "carrots",
            "beans",
            "scooby snacks",
            "burgers",
            "hot dogs",
        ], (
            "The class-scoped df 'stomach_contents' column was not as",
            " expected",
        )
        # Finally, check update_food() with the function-scoped fixture. As
        # in TestServeFood::test_expected_states_within_same_class(), the
        # function-scoped fixture starts from scratch.
        assert list(
            fancy_dessert(_mm_function_scoped)["fave_food"].values
        ) == ["carrots", "beans", "scooby snacks", "burgers", "hot dogs"], (
            "The function-scoped df 'stomach_contents' column was not as",
            " expected",
        )
