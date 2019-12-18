class CDispatcher:
    def __init__(self, table=None):
        if not table:
            self.task_manager = {}
        else:
            self.task_manager = table

    def is_command(self, command):
        return self.task_manager.get(command)

    def run(self, command, *args, **kwargs):
        execute = self.task_manager.get(command)
        if execute:
            execute(*args, **kwargs)
        else:
            raise Exception('Command not found!')
