import pytest
from unittest.mock import patch
import streamlit as st
from streamlit.runtime.scriptrunner import RerunException
from navigation.dijkstra_page import dijkstra_page
from navigation.clark_wright_page import clark_wright_page


@pytest.fixture
def mock_session_state():
    """Mock Streamlit session state."""
    with patch.dict(st.session_state, {}, clear=True):
        yield


def test_dijkstra_page_renders(mock_session_state):
    """Test if the Dijkstra's page runs without errors."""
    with patch.dict(
        st.session_state,
        {"graph": {}, "node_names": [], "confirm_reset": False},
        clear=True,
    ):
        try:
            dijkstra_page()
        except RerunException:
            # Ignore rerun exceptions caused by session updates in Streamlit
            pass

        # Assertions to ensure required keys are present in session state
        assert "graph" in st.session_state
        assert "node_names" in st.session_state
        assert "confirm_reset" in st.session_state


def test_clark_wright_page_renders(mock_session_state):
    """Test if the Clark-Wright page runs without errors."""
    with patch.dict(
        st.session_state,
        {"graph": {}, "node_names": [], "confirm_reset": False},
        clear=True,
    ):
        try:
            clark_wright_page()
        except RerunException:
            # Ignore rerun exceptions caused by session updates in Streamlit
            pass

        # Basic check to ensure no errors during execution
        assert True


def test_dijkstra_page(mock_session_state):
    """Populate graph and node names in session state."""
    with patch.dict(
        st.session_state,
        {"graph": {"A": {"B": 1}, "B": {"A": 1}}, "node_names": ["A", "B"]},
        clear=True,
    ):
        try:
            dijkstra_page()
        except RerunException:
            # Ignore Streamlit's rerun exception
            pass

        # Assertions to ensure session state is correctly initialized
        assert st.session_state["graph"] == {"A": {"B": 1}, "B": {"A": 1}}
        assert st.session_state["node_names"] == ["A", "B"]


def test_clark_wright_page(mock_session_state):
    """Test the UI elements of the Clark-Wright page."""
    with patch.dict(
        st.session_state,
        {"graph": {}, "node_names": [], "confirm_reset": False},
        clear=True,
    ):
        try:
            clark_wright_page()
        except RerunException:
            # Ignore Streamlit's rerun exception
            pass

        # Basic check to ensure no errors during execution
        assert True