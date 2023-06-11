from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass
    @abstractmethod
    def execute(self):
        pass

class Add(Command):
    def __init__(self, files, tags) -> None:
        self.files = files
        self.tags = tags
    @staticmethod
    def execute(self):
        return 'add', self.files, self.tags

class Delete(Command):
    def __init__(self, tags) -> None:
        self.tags = tags
    @staticmethod
    def execute(self):
        return 'delete', self.tags
    
class List(Command):
    def __init__(self, tags) -> None:
        self.tags = tags
    @staticmethod
    def execute(self):
        return 'list', self.tags
    
class AddTags(Command):
    def __init__(self, query, tags) -> None:
        self.query = query
        self.tags = tags
    @staticmethod
    def execute(self):
        return 'add-tags', self.query, self.tags
    
class DeleteTags(Command):
    def __init__(self, query, tags) -> None:
        self.query = query
        self.tags = tags
    @staticmethod
    def execute(self):
        return 'delete-tags', self.query, self.tags

class Get(Command):
    def __init__(self, tags) -> None:
        self.tags = tags
    @staticmethod
    def execute(self):      
        return 'get', self.tags

