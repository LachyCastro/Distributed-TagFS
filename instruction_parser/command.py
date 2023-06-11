from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class Add(Command):
    @staticmethod
    def execute(self, files, tags):
        return 'add', files, tags

class Delete(Command):
    @staticmethod
    def execute(self, tags):
        return 'delete', tags
    
class List(Command):
    @staticmethod
    def execute(self, tags):
        return 'list', tags
    
class AddTags(Command):
    @staticmethod
    def execute(self, query, tags):
        return 'add-tags', query, tags
    
class DeleteTags(Command):
    @staticmethod
    def execute(self, query, tags):
        return 'delete-tags', query, tags

class Get(Command):
    @staticmethod
    def execute(self, tags):
        return 'get', tags