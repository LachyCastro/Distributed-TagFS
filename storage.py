import operator
import pickle
import sys
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from itertools import takewhile

sys.path.append('auxiliar/')
from auxiliar.utils import digest


class Storage(ABC):
    @abstractmethod
    def __setitem__(self, key, value):
        """
        Set a key to the given value.
        """

    @abstractmethod
    def __getitem__(self, key):
        """
        Get the given key.  If item doesn't exist, raises C{KeyError}
        """

    @abstractmethod
    def get(self, key, default=None):
        """
        Get given key.  If not found, return default.
        """

    @abstractmethod
    def iter_older_than(self, seconds_old):
        """
        Return the an iterator over (key, value) tuples for items older
        than the given secondsOld.
        """

    @abstractmethod
    def __iter__(self):
        """
        Get the iterator for this storage, should yield tuple of (key, value)
        """

class ForgetfulStorage(Storage):
    def __init__(self, ttl=604800):
        """
        By default, max age is a week.
        """
        self.data = OrderedDict()
        self.ttl = ttl

    def __setitem__(self, key, value):
        if key in self.data:
            del self.data[key]
        self.data[key] = (time.monotonic(), value)
        self.cull()

    def delete(self, key):
        self.cull()
        if key in self.data:
            del self.data[key]

    def cull(self):
        for _, _ in self.iter_older_than(self.ttl):
            self.data.popitem(last=False)

    def get(self, key, default=None):
        self.cull()
        if key in self.data:
            return self[key]
        return default

    def __getitem__(self, key):
        self.cull()
        return self.data[key][1]

    def __repr__(self):
        self.cull()
        return repr(self.data)

    def iter_older_than(self, seconds_old):
        min_birthday = time.monotonic() - seconds_old
        zipped = self._triple_iter()
        matches = takewhile(lambda r: min_birthday >= r[1], zipped)
        return list(map(operator.itemgetter(0, 2), matches))

    def _triple_iter(self):
        ikeys = self.data.keys()
        ibirthday = map(operator.itemgetter(0), self.data.values())
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ibirthday, ivalues)

    def __iter__(self):
        self.cull()
        ikeys = self.data.keys()
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ivalues)

class FileStorage(Storage):

    def __init__(self, ttl=604800):
        self.data_tag = OrderedDict() 
        self.data_file = OrderedDict()
        self.max_age = ttl

    def __setitem__(self, key, value):
        return Storage.__setitem__(key,value)

    # { tagid, (time, set(  fileid ) ) }
    def set(self, dkey, key, name, value, hash = True):
        if dkey in self.data_tag:
            s = pickle.loads(self.data_tag[dkey][1])
            if hash:
                s.add(digest(value))
            else:
                s.add(value)
            self.data_tag[dkey] = (time.monotonic(), pickle.dumps(s))
        else:
            s = set()
            if hash:
                s.add(digest(value))
            else:
                s.add(value)
            self.data_tag[dkey] = (time.monotonic(), pickle.dumps(s))
        dvalue = value
        if hash:
            dvalue = digest(value)
        self.set_file(dvalue, value, key, name)
        self.cull()

    def set_file(self, key, value, tag, name):
        """
        self.data_file[key] = (time.monotonic(), pickle.dumps(value))
        """
        if key in self.data_file:
            f,t,_name = pickle.loads(self.data_file[key][1])
            tags = pickle.loads(t)
            tags.add(tag)
            self.data_file[key] = (time.monotonic(), pickle.dumps((f, pickle.dumps(tags),_name)))
        else:
            tags = set()
            tags.add(tag)
            self.data_file[key] = (time.monotonic(), pickle.dumps((pickle.dumps(value), pickle.dumps(tags), name)))
        self.cull()

    def cull(self):
        for _, _ in self.iter_older_than(self.max_age):
            self.data_tag.popitem(last = False)

    def get(self, key, default = None):
        self.cull()
        # print('--------------get-------------')
        # print(key)
        # print(self.data_file)
        if key in self.data_tag:
            # print('in here')
            return self.data_tag[key][1]
        if key in self.data_file:
            return self.data_file[key][1]
        return default

    def get_file(self, key, default = None):
        self.cull()
        if key in self.data_file:
            return pickle.loads(self.data_file[key][1])
        return default

    def __getitem__(self, key):
        self.cull()
        return self.data_tag[key][1]

    def __iter__(self):
        self.cull()
        ikeys = self.data_tag.keys()
        ivalues = map(operator.itemgetter(1), self.data_tag.values())
        return zip(ikeys, ivalues)

    def delete(self, key):
        self.cull()
        del self.data_file[key]

    def delete_tag(self, dkey ,key, value):
        self.cull()
        # print('----------delete-tags----------')
        # print(dkey)
        # print(key)
        # print(value)
        if dkey in self.data_tag:
            files = pickle.loads(self.data_tag[dkey][1])
            # d = digest(value)
            if value in files:
                files.remove(value)
            if(len(files)>0):
                self.data_tag[dkey] = (time.monotonic(), pickle.dumps(files))
            else: del self.data_tag[dkey]
        if value in self.data_file:
            f, t, _ = pickle.loads(self.data_file[value][1])
            tags = pickle.loads(t)
            # print('tagssssssssssssssssss')
            # print(tags)
            # input()
            if key in tags:
                # print('here---------------')
                tags.remove(key)
                # print(tags)
                if(len(tags)>0):
                    self.data_file[value] = (time.monotonic(), pickle.dumps((f, pickle.dumps(tags), _)))
                else:
                    del self.data_file[value]


    def __repr__(self):
        self.cull()
        return repr(self.data_tag)

    def iter_older_than(self, seconds_old):
        t = time.monotonic() - seconds_old
        zipped = self._triple_iter()
        matches = takewhile(lambda r: t >= r[1], zipped)
        print(matches,'matchessss', flush= True)
        return list(map(operator.itemgetter(0,2),matches))

    def _triple_iter(self):
        ikeys = self.data_tag.keys()
        it = map(operator.itemgetter(0),self.data_tag.values())
        ivalues = map(operator.itemgetter(1), self.data_tag.values())
        return zip(ikeys, it, ivalues)