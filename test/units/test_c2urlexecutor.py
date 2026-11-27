import pytest
from unittest.mock import MagicMock
from attackmate.executors.c2url.c2urlexecutor import C2urlExecutor
from attackmate.schemas.c2url import C2urlCommand, C2urlSessionCommand
from attackmate.schemas.config import C2urlConfig
from attackmate.execexception import ExecException
from attackmate.variablestore import VariableStore
from attackmate.processmanager import ProcessManager


@pytest.fixture
def executor():
    ex = C2urlExecutor(
        MagicMock(spec=ProcessManager),
        varstore=MagicMock(spec=VariableStore),
        c2url_config={'default': C2urlConfig(token='secret')},
    )
    # Replace the real C2url with a mock controller for the single connection.
    controller = MagicMock()
    ex._controllers['default'] = controller
    return ex, controller


@pytest.mark.asyncio
async def test_listen_returns_address(executor):
    ex, controller = executor
    controller.listen.return_value = ('127.0.0.1', 9099)
    result = await ex._exec_cmd(C2urlCommand(type='c2url', cmd='listen', host='127.0.0.1', port='9099'))
    controller.listen.assert_called_once_with('127.0.0.1', 9099)
    assert result.returncode == 0
    assert '127.0.0.1:9099' in result.stdout


@pytest.mark.asyncio
async def test_execute_decodes_and_maps_exit_code(executor):
    ex, controller = executor
    controller.execute.return_value = MagicMock(stdout=b'uid=0(root)\n', exit_code=0)
    result = await ex._exec_cmd(C2urlSessionCommand(type='c2url-session', cmd='id', session='s1'))
    controller.execute.assert_called_once_with('id', session='s1', timeout=30)
    assert result.stdout == 'uid=0(root)\n'
    assert result.returncode == 0


@pytest.mark.asyncio
async def test_execute_without_session_picks_connected(executor):
    from c2url import SessionState
    ex, controller = executor
    connected = MagicMock(state=SessionState.CONNECTED)
    controller.sessions.return_value = [connected]
    controller.execute.return_value = MagicMock(stdout=b'out', exit_code=3)
    result = await ex._exec_cmd(C2urlSessionCommand(type='c2url-session', cmd='whoami'))
    controller.execute.assert_called_once_with('whoami', session=connected, timeout=30)
    assert result.returncode == 3


@pytest.mark.asyncio
async def test_execute_without_session_none_connected_raises(executor):
    ex, controller = executor
    controller.sessions.return_value = []
    with pytest.raises(ExecException, match='No connected c2url session'):
        await ex._exec_cmd(C2urlSessionCommand(type='c2url-session', cmd='whoami'))


@pytest.mark.asyncio
async def test_c2url_error_becomes_execexception(executor):
    from c2url import C2urlError
    ex, controller = executor
    controller.wait_for_session.side_effect = C2urlError('boom')
    with pytest.raises(ExecException, match='boom'):
        await ex._exec_cmd(C2urlCommand(type='c2url', cmd='wait_for_session', timeout='5'))
