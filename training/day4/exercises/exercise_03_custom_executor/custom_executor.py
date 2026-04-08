# custom_executor.py
#
# Exercise 4: Implement the HelloExecutor.
#
# When finished, copy this file to:
#   src/attackmate/executors/common/helloexecutor.py

from attackmate.executors.baseexecutor import BaseExecutor
from attackmate.result import Result
# TODO: Import HelloCommand from the schema file.


# TODO: Register this executor with the factory using the decorator.
class HelloExecutor(BaseExecutor):

    # TODO: Implement the _exec_cmd method.
    #       It must:
    #         1. Accept a HelloCommand as its argument.
    #         2. Log the message at INFO level using self.logger.info().
    #         3. Return a Result with stdout set to the message and returncode 0.
    async def _exec_cmd(self, command: HelloCommand) -> Result:
        # TODO: self.logger.info(...)
        # TODO: return Result(stdout=..., returncode=...)
        pass
