
class CommandParser:
    def __init__(self):
        self.commands = {
            'add': self.parse_add,
            'delete': self.parse_delete,
            'list': self.parse_list,
            'add-tags': self.parse_add_tags,
            'delete-tags': self.parse_delete_tags,
            'get': self.parse_get
        }

    def __call__(self, args):
        inst = self.split(args)
        if inst[0] in self.commands:
            return self.commands[inst[0]](inst[1:])
        else:
            raise Exception('syntax error: unknown command %s', inst[0])

    def parse_add(self, args):
        if '-f' in args and '-t' in args:
            try:
                idx = args.index('-t')
                files = args[:idx]
                tags = args[idx+1:]
                if not len(files) or not len(tags):
                    raise Exception('syntax error: <file-list> and <tag-list> must have files and tags to store')
            except:
                raise Exception('syntax error: <add> <-f> <file-list> <-t> <tag-list>')
            return 'add', files, tags
        else:
            raise Exception('syntax error: <add> <-f> <file-list> <-t> <tag-list>')

    def parse_delete(self, args):
        if '-q' in args:
            try:
                idx = args.index('-q')
                tags = args[idx+1:]
                if not len(tags):
                    raise Exception("syntax error: tags can't be empty")
            except:
                raise Exception('syntax error: <delete> <-q> <tag-query>')
            return 'delete', tags
        else:
            raise Exception('syntax error: <delete> <-q> <tag-query>')

    def parse_list(self, args):
        if '-q' in args:
            try:
                idx = args.index('-q')
                tags = args[idx+1:]
                if not len(tags):
                    raise Exception("syntax error: tags can't be empty")
            except:
                raise Exception('syntax error: <list> <-q> <tag-query>')
            return 'list', tags
        else:
            raise Exception('syntax error: <list> <-q> <tag-query>')

    def parse_add_tags(self, args):
        if '-q' in args and '-t' in args:
            try:
                idx = args.index('-t')
                query = args[:idx]
                tags = args[idx+1:]
                if not len(query) or not len(tags):
                    raise Exception('syntax error: <tag-query> and <tag-list> must have files and tags to store')
            except:
                raise Exception('syntax error: <add-tags> <-q> <tag-query> <-t> <tag-list>')
            return 'add-tags', query, tags
        else:
            raise Exception('syntax error: <add-tags> <-q> <tag-query> <-t> <tag-list>')

    def parse_delete_tags(self, args):
        if '-q' in args and '-t' in args:
            try:
                idx = args.index('-t')
                query = args[:idx]
                tags = args[idx+1:]
                if not len(query) or not len(tags):
                    raise Exception('syntax error: <tag-query> and <tag-list> must have files and tags to store')
            except:
                raise Exception('syntax error: <delete-tags> <-q> <tag-query> <-t> <tag-list>')
            return 'delete-tags', query, tags
        else:
            raise Exception('syntax error: <delete-tags> <-q> <tag-query> <-t> <tag-list>')

    def parse_get(self, args):
        if '-q' in args:
            try:
                idx = args.index('-q')
                tags = args[idx+1:]
                if not len(tags):
                    raise Exception("syntax error: tags can't be empty")
            except:
                raise Exception('syntax error: <get> <-q> <tag-query>')
            return 'get', tags
        else:
            raise Exception('syntax error: <get> <-q> <tag-query>')

    def split(self, args):
        return args.split()