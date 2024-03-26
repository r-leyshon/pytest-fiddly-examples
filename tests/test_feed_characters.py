"""Testing pandas operations with test fixtures."""
from example_pkg.feed_characters import serve_food, fancy_dessert


def test_scopes_before_action(
    _mm_session_scoped,
    _mm_module_scoped,
    _mm_class_scoped,
    _mm_function_scoped,
):
    """Assert that all characters have the munchies at the outset."""
    assert list(_mm_session_scoped["has_munchies"].values) == [True] * 5, (
        "The session-scoped DataFrame 'has_munchies' column was not as ",
        "expected before any action was taken.",
    )
    assert list(_mm_module_scoped["has_munchies"].values) == [True] * 5, (
        "The module-scoped DataFrame 'has_munchies' column was not as ",
        "expected before any action was taken.",
    )
    assert list(_mm_class_scoped["has_munchies"].values) == [True] * 5, (
        "The class-scoped DataFrame 'has_munchies' column was not as ",
        "expected before any action was taken.",
    )
    assert list(_mm_function_scoped["has_munchies"].values) == [True] * 5, (
        "The function-scoped DataFrame 'has_munchies' column was not as ",
        "expected before any action was taken.",
    )


class TestServeFood:
    """Tests that serve_food() updates the 'has_munchies' column."""

    def test_serve_food_updates_df(
        self,
        _mm_session_scoped,
        _mm_module_scoped,
        _mm_class_scoped,
        _mm_function_scoped,
    ):
        """Test serve_food updates the has_munchies columns as expected.

        This function will update each fixture in the same way, providing each
        character with their favourite_food and updating the contents of their
        stomach. The column we will assert against will be has_munchies, which
        should be updated to False after feeding in all cases except for Scooby
        Doo and Shaggy, who always have the munchies.
        """
        # first lets check that the session-scoped dataframe gets updates
        assert list(serve_food(_mm_session_scoped)["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The `serve_food()` has not updated the session-scoped df",
            " 'has_munchies' column as expected.",
        )
        # next check the same for the module-scoped fixture
        assert list(serve_food(_mm_module_scoped)["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The `serve_food()` has not updated the module-scoped df",
            " 'has_munchies' column as expected.",
        )
        # Next check class-scoped fixture updates
        assert list(serve_food(_mm_class_scoped)["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The `serve_food()` has not updated the class-scoped df",
            " 'has_munchies' column as expected.",
        )
        # Finally check the function-scoped df does the same...
        assert list(
            serve_food(_mm_function_scoped)["has_munchies"].values
        ) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The `serve_food()` has not updated the function-scoped df",
            " 'has_munchies' column as expected.",
        )

    def test_expected_states_within_same_class(
        self,
        _mm_session_scoped,
        _mm_module_scoped,
        _mm_class_scoped,
        _mm_function_scoped,
    ):
        """Test to ensure fixture states are as expected."""
        # Firstly, session-scoped changes should persist, only Scooby Doo &
        # Shaggy should still have the munchies...
        assert list(_mm_session_scoped["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The changes to the session-scoped df 'has_munchies' column have",
            " not persisted as expected.",
        )
        # Secondly, module-scoped changes should persist, as was the case for
        # the session-scope test above
        assert list(_mm_module_scoped["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The changes to the module-scoped df 'has_munchies' column have",
            " not persisted as expected.",
        )
        # Next, class-scoped changes should persist just the same
        assert list(_mm_class_scoped["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The changes to the class-scoped df 'has_munchies' column have",
            " not persisted as expected.",
        )
        # Finally, demonstrate that function-scoped fixture starts from scratch
        # Therefore all characters should have the munchies all over again.
        assert (
            list(_mm_function_scoped["has_munchies"].values) == [True] * 5
        ), (
            "The function_scoped df 'has_munchies' column is not as expected.",
        )


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
        changes performed in TestServeFood::test_serve_food_updates_df()
        persist, then characters will not have empty stomach_contents,
        resulting in a switch of their favourite_food.
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
            "brownie",
            "ice cream",
            "apple crumble",
            "pudding",
            "banana bread",
        ], (
            "The changes to the module-scoped df 'stomach_contents' column",
            " have not persisted as expected.",
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
