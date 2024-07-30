"""
vncexecutor.py
============================================
Execute Vnc Commands
"""

import asyncio
import os
import tempfile
from typing import Any
from attackmate.variablestore import VariableStore
from attackmate.executors.baseexecutor import BaseExecutor
from attackmate.execexception import ExecException
from attackmate.result import Result
from attackmate.executors.features.cmdvars import CmdVars
from attackmate.schemas.base import BaseCommand
from attackmate.schemas.vnc import VncCommand
from attackmate.processmanager import ProcessManager


class SliverExecutor(BaseExecutor):

    def __init__(self, pm: ProcessManager, cmdconfig=None, *, varstore: VariableStore):

        self.client = None
        self.client_config = None
        self.result = Result('', 1)

        super().__init__(pm, varstore, cmdconfig)

    def log_command(self, command: BaseCommand):
        self.logger.info(f"Executing Vnc-command: '{command.cmd}'")

    def _exec_cmd(self, command: VncCommand) -> Result:
        try:
            if command:
                output = "something"
            else:
                output = "something else"
        except Exception as e:
            raise ExecException(e)

        self.logger.debug(f'Something for Debugging')
        #    self.varstore.set_variable('LAST_VNC_SESSION', session_id)
        return Result(output, 0)
