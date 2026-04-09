# Solution for Exercise 4: HelloExecutor
#
# Copy to: src/attackmate/executors/common/helloexecutor.py

from attackmate.executors.baseexecutor import BaseExecutor
from attackmate.result import Result
from attackmate.executors.executor_factory import executor_factory
from attackmate.schemas.hello import HelloCommand


@executor_factory.register_executor('hello')
class HelloExecutor(BaseExecutor):
    async def _exec_cmd(self, command: HelloCommand) -> Result:
        self.logger.info(f'Hello: {command.message}')
        return Result(stdout=command.message, returncode=0)
