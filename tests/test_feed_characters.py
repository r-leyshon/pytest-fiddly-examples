"""Testing pandas operations with test fixtures."""
from example_pkg.feed_characters import serve_food


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


class TestSomeOtherTestClass:
    """Demonstrate persistance of changes to class-scoped fixture."""

    def test_whether_changes_to_stomach_contents_persist(
        self, _mm_class_scoped, _mm_module_scoped
    ):
        """Check the stomach_contents column."""
        assert list(_mm_module_scoped["stomach_contents"].values) == [
            "carrots",
            "beans",
            "scooby snacks",
            "burgers",
            "hot dogs",
        ], "Changes to module-scoped fixture have not propagated as expected."
        assert (
            list(_mm_class_scoped["stomach_contents"].values) == ["empty"] * 5
        ), "Values in class-scoped fixture are not as expected"
