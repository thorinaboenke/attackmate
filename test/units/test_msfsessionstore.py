import pytest
from unittest.mock import MagicMock
from attackmate.execexception import ExecException
from attackmate.executors.metasploit.msfsessionstore import MsfSessionStore
from attackmate.variablestore import VariableStore


@pytest.fixture
def varstore():
    return VariableStore()


@pytest.fixture
def store(varstore):
    return MsfSessionStore(varstore)


def _msfsessions(entries):
    """Build a mock msfsessions object from {session_id: exploit_uuid} dict."""
    mock = MagicMock()
    mock.list = {sid: {'exploit_uuid': uuid} for sid, uuid in entries.items()}
    return mock


# --- add_session ---

class TestAddSession:
    def test_stores_uuid_under_connection(self, store):
        store.add_session('server1', 'shell', 'uuid-A')
        assert store.sessions['server1']['shell'] == 'uuid-A'

    def test_two_connections_are_independent(self, store):
        store.add_session('server1', 'shell', 'uuid-A')
        store.add_session('server2', 'shell', 'uuid-B')
        assert store.sessions['server1']['shell'] == 'uuid-A'
        assert store.sessions['server2']['shell'] == 'uuid-B'

    def test_overwrite_within_same_connection(self, store):
        store.add_session('server1', 'shell', 'uuid-A')
        store.add_session('server1', 'shell', 'uuid-B')
        assert store.sessions['server1']['shell'] == 'uuid-B'


# --- get_session_by_name ---

class TestGetSessionByName:
    def test_returns_session_id_for_matching_uuid(self, store):
        store.add_session('server1', 'shell', 'uuid-A')
        sessions = _msfsessions({'42': 'uuid-A'})
        assert store.get_session_by_name('server1', 'shell', sessions) == '42'

    def test_different_connections_do_not_cross_contaminate(self, store):
        store.add_session('server1', 'shell', 'uuid-A')
        store.add_session('server2', 'shell', 'uuid-B')
        sessions1 = _msfsessions({'1': 'uuid-A'})
        sessions2 = _msfsessions({'2': 'uuid-B'})
        assert store.get_session_by_name('server1', 'shell', sessions1) == '1'
        assert store.get_session_by_name('server2', 'shell', sessions2) == '2'

    def test_raises_when_session_not_found_and_block_false(self, store):
        sessions = _msfsessions({})
        with pytest.raises(ExecException, match='Session.*not found'):
            store.get_session_by_name('server1', 'shell', sessions, block=False)

    def test_wrong_connection_raises_when_block_false(self, store):
        store.add_session('server1', 'shell', 'uuid-A')
        # server2 has no sessions — uuid-A is not in server2's list
        sessions2 = _msfsessions({'99': 'uuid-X'})
        with pytest.raises(ExecException, match='Session.*not found'):
            store.get_session_by_name('server2', 'shell', sessions2, block=False)


# --- add_or_queue_session ---

class TestAddOrQueueSession:
    def test_sets_last_msf_session_variable(self, store):
        _msfsessions({})
        store.add_or_queue_session('server1', 'shell', 'uuid-A', session_id=7)
        assert store.varstore.get_variable('LAST_MSF_SESSION') == '7'

    def test_sets_connection_scoped_variable(self, store):
        store.add_or_queue_session('server1', 'shell', 'uuid-A', session_id=7)
        assert store.varstore.get_variable('LAST_MSF_SESSION_server1') == '7'

    def test_connection_scoped_variables_are_independent(self, store):
        store.add_or_queue_session('server1', 'shell', 'uuid-A', session_id=1)
        store.add_or_queue_session('server2', 'shell', 'uuid-B', session_id=2)
        assert store.varstore.get_variable('LAST_MSF_SESSION_server1') == '1'
        assert store.varstore.get_variable('LAST_MSF_SESSION_server2') == '2'

    def test_puts_conn_name_in_queue(self, store):
        queue = MagicMock()
        store.add_or_queue_session('server1', 'shell', 'uuid-A', queue=queue, session_id=5)
        queue.put.assert_called_once_with(('server1', 'shell', 'uuid-A', 5))


# --- wait_for_session ---

class TestWaitForSession:
    def test_stores_session_when_uuid_matches(self, store):
        sessions = _msfsessions({'3': 'uuid-A'})
        store.wait_for_session('server1', 'shell', 'uuid-A', sessions)
        assert store.sessions['server1']['shell'] == 'uuid-A'

    def test_does_not_store_on_wrong_connection(self, store):
        sessions = _msfsessions({'3': 'uuid-A'})
        store.wait_for_session('server1', 'shell', 'uuid-A', sessions)
        assert 'server2' not in store.sessions
