"""Testing pandas operations with test fixtures."""
from example_pkg.feed_characters import serve_food


def test_session_scoped_before_action(_mm_session_scoped):
    """Assert that fixture is as expected before modification with src func."""
    assert list(_mm_session_scoped["has_munchies"].values) == [True] * 5, (
        "The session-scoped DataFrame 'has_munchies' column was not as ",
        "expected before any action was taken.",
    )


class TestServeFood:
    """Tests for serve_food()."""

    def test_serve_food_updates_df(self, _mm_session_scoped):
        """Test that serve_food updates the target columns as expected."""
        fed_mm = serve_food(_mm_session_scoped)
        assert list(fed_mm["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The `serve_food()` has not updated the session_scoped df",
            " 'has_munchies' column as expected.",
        )

    def test_session_scope_persists(self, _mm_session_scoped):
        """Test to ensure the changes to session-scoped fixture persist."""
        assert list(_mm_session_scoped["has_munchies"].values) == [
            False,
            False,
            True,
            True,
            False,
        ], (
            "The changes to the session_scoped df 'has_munchies' column have",
            " not persisted as expected.",
        )
