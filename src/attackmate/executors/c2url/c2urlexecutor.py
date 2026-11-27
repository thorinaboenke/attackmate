"""
c2urlexecutor.py
============================================
Execute c2url controller and session commands.

A single executor instance owns all controllers (one per configured
connection). The listener runs in c2url's own daemon threads, so ``listen``
returns immediately and sessions register in the background while the playbook
continues. ``c2url-session`` commands are routed to this same executor (see the
``sftp`` -> ``ssh`` style alias in ``attackmate.py``) so they share the running
controllers.
"""

from typing import Dict
from c2url import C2url, C2urlConfig as C2urlLibConfig, C2urlError, SessionState

from attackmate.variablestore import VariableStore
from attackmate.processmanager import ProcessManager
from attackmate.executors.baseexecutor import BaseExecutor
from attackmate.executors.features.cmdvars import CmdVars
from attackmate.execexception import ExecException
from attackmate.result import Result
from attackmate.schemas.base import BaseCommand
from attackmate.schemas.config import C2urlConfig
from attackmate.schemas.c2url import C2urlCommand, C2urlSessionCommand
from attackmate.executors.executor_factory import executor_factory


@executor_factory.register_executor('c2url')
class C2urlExecutor(BaseExecutor):
    def __init__(
        self, pm: ProcessManager, cmdconfig=None, *,
        varstore: VariableStore, c2url_config: Dict[str, C2urlConfig] = {}
    ):
        self.c2url_config = c2url_config
        self._controllers: Dict[str, C2url] = {}
        super().__init__(pm, varstore, cmdconfig)

    def _resolve_connection(self, command: BaseCommand) -> str:
        conn = getattr(command, 'connection', None)
        if conn:
            return conn
        if self.c2url_config:
            conn_name = next(iter(self.c2url_config))
            self.logger.debug(f'No connection specified, using default: {conn_name}')
            return conn_name
        return 'default'

    def _get_controller(self, conn_name: str) -> C2url:
        if conn_name not in self._controllers:
            cfg = self.c2url_config.get(conn_name, C2urlConfig())
            lib_config = C2urlLibConfig(
                token=cfg.token,
                certificate=cfg.certificate,
                private_key=cfg.private_key,
                merge_stderr=cfg.merge_stderr,
                upgrade_pty=cfg.upgrade_pty,
            )
            self._controllers[conn_name] = C2url(config=lib_config, logger=self.logger)
        return self._controllers[conn_name]

    async def _exec_cmd(self, command: BaseCommand) -> Result:
        controller = self._get_controller(self._resolve_connection(command))
        try:
            if isinstance(command, C2urlSessionCommand):
                return self._exec_session(controller, command)
            return self._exec_controller(controller, command)
        except (C2urlError, TimeoutError, OSError) as error:
            raise ExecException(str(error))

    def _exec_controller(self, controller: C2url, command: C2urlCommand) -> Result:
        if command.cmd == 'listen':
            host, port = controller.listen(command.host, CmdVars.variable_to_int('port', command.port))
            return Result(f'Listening on {host}:{port}', 0)
        if command.cmd == 'wait_for_session':
            session = controller.wait_for_session(CmdVars.variable_to_int('timeout', command.timeout))
            return Result(f'{session.label} {session.session_id}', 0)
        if command.cmd == 'stop':
            controller.stop()
            return Result('Listener stopped', 0)
        raise ExecException(f'Unknown c2url cmd: {command.cmd}')

    def _exec_session(self, controller: C2url, command: C2urlSessionCommand) -> Result:
        session = command.session
        if session is None:
            connected = [s for s in controller.sessions() if s.state is SessionState.CONNECTED]
            if not connected:
                raise ExecException('No connected c2url session available')
            session = connected[0]
        result = controller.execute(
            command.cmd,
            session=session,
            timeout=CmdVars.variable_to_int('timeout', command.timeout),
        )
        return Result(result.stdout.decode(errors='replace'), result.exit_code)

    def cleanup(self):
        for controller in self._controllers.values():
            controller.stop()
        self._controllers.clear()
