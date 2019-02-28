import numpy as np
import copy
import inspect

class Primitive:
    DIC = {}
    DATATYPE = np.float32
    def __init__(self, data, title:str = None):
        """
        Parent of all tools classes.
        rule#1_ in child class functions never return Hlist
        - add functions for general management and meta control -
        :param data:
        :param title:
        """
        # make new dict for child class
        if self.DIC == Primitive.DIC:
            self.__class__.DIC = {}

        # make name for indexing
        if title is None:
            title = str(len(self.keys()) + 1)
        self._dict_insert_unique(self.__class__.DIC, title, data)
        self._data = data
    def _dict_insert_unique(self,dic: dict, key: str, value=None, preffix: str = 'new_', suffix: str = ''):
        key_list = list(dic.keys())

        def make_unique_name(source: list, target: str, preffix: str, suffix: str):
            # function for detecting coincident name
            new_name = target
            for i in source:
                if i == target:
                    source.remove(i)
                    new_target = preffix + target + suffix
                    new_name = make_unique_name(source, new_target, preffix, suffix)
                    """
                    If coincident name is found, There is no need to continue iteration.
                    Else recursion is called to compare with the elements that were passed
                    in front in parent iteration. Coincident element is removed from
                    the original list to avoid pointless iteration.
                    """
                    break
            # finishing condition for recursive action
            # return value only if 'for' is fully iterated -
            # without getting into 'if' branch
            return new_name

        dic[make_unique_name(key_list, key, preffix, suffix)] = value

    def get_data(self):
        return self._data

    @classmethod
    def get_from_dic(cls, title:str):
        return cls.dic[title]

    @classmethod
    def make_new(cls, data, title:str = None):
        instance = cls(cls.DIC, data, title)

    @classmethod
    def get_dic(cls):
        return cls.DIC

    @classmethod
    def keys(cls):
        return cls.DIC.keys()

    def __str__(self):
        return f'{self.__class__.__name__} : {self._data}'

    def set_data(self,data):

        # to ensure all the proceeding numpy calculation efficient
        if isinstance(data,np.ndarray):
            data = self.__class__.DATATYPE(data)
        self._data = data

    def get_data(self):
        return self._data

    def _printmessage(self,text:str,header:str = 'ERROR '):
        func_name = inspect.currentframe().f_back.f_code.co_name
        fullvarinfo = inspect.getargvalues(inspect.currentframe().f_back)
        varvalue = [fullvarinfo[3][i] for i in fullvarinfo[0]]
        varinfo = []
        for name, value in zip(fullvarinfo[0],varvalue):
            varinfo.append(f'{name} : {str(value)}')

        head = f'FROM {self.__class__.__name__}.{func_name}: '

        varhead = ' '*(len(head)-6) + 'ARGS: ' + varinfo[0]
        for i,j in enumerate(varinfo):
            varinfo[i] = ' '*len(head) + j

        top = header+'-'*(len(head+text)- len(header))
        bottom = '-'*len(head+text)

        lines = top,head + text,varhead,*varinfo[1:],bottom

        for i in lines:
            print(i)


class Item:

    def __init__(self,data):
        self._data = data

    def __str__(self):
        return 'i'+str(self._data)

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, key, value):
        self._data = value

    def type(self):
        return type(self._data)

# A stands for array? array list?
class Tlist(Primitive):

    def __init__(self, data: (list,tuple)):
        """
        write cases and rules
        rule 1: Tlist either leaf or node
        rule 2: leafs can contain any generics
        rule 3: nods can contain only other Tlists
        rule 4: input data should be given as list representing structure?
        rule 5: if a user want to put generic iterables,
        other function will be provided

        case1 input generics and make leaf
        case2 input Tlists and make node
        :param data:
        """

        self._data = dict
        # check input type
        if not isinstance(data, (list,tuple)):
            self._printmessage('input should be list or tuple')
            return None

        # # check cases
        # count_gen = 0
        # count_tlist = 0
        # for i in data:
        #     if isinstance(i, self.__class__):
        #         count_tlist += 1
        #     else:
        #         count_gen += 1
        # if len(data) is count_gen:
        #     self._isleaf = True
        # elif len(data) is count_tlist:
        #     self._isleaf = False
        # else:
        #     # avoid mixed input
        #     self._printmessage('input incorrect')
        #     return None

        self._data = self._parslist(data)
        self._checkifleaf()
        # wrap with Item class for referencing
        # for i in data:
        #     if not isinstance(i,Item) and not isinstance(i,Tlist):
        #         self._data.append(Item(i))
        #     else:
        #         self._data.append(i)

        # self._data = data
        # self._checkifleaf()


    def _parslist(self, input:list):

        # if all([isinstance(i,Item) for i in input]):
        #     return input

        if all([not isinstance(i,(list,tuple)) for i in input]):
            referenced = []
            for i in input:
                referenced.append(Item(i))
            return referenced

        else:
            self._isleaf = False
            parsed = []
            for i in input:
                '''
                for example input is very complex:
                [0,2,[2,3],Tlist,[Tlist,Tlist]]
                target1 : generics? no generics remove this
                target2 : Tlist
                target3 : (list, tuple)
                I'm gonna read from above into bottom
                should i match the length of all branches?
                
                '''
                if not isinstance(i, (tuple,list, Tlist)):
                    self._printmessage('inputs must be tuple, list, or Tlist')
                    return None
                elif isinstance(i,(tuple,list)):

                    branch = Tlist(self._parslist(i))
                    branch._checkifleaf()
                    parsed.append(branch)
                elif isinstance(i,Tlist):
                    i._checkifleaf()
                    parsed.append(i)
            return parsed

    # def _parslist(self, input: list):
    #
    #     parsed = {}
    #     if all([not isinstance(i, (list, tuple, Tlist)) for i in input]):
    #         for index, value in enumerate(input):
    #             parsed[str(index)] = value
    #     else:
    #         count = 0
    #         for i in input:
    #             if isinstance(i,(list,tuple)):
    #                 child = self._parslist(i)
    #                 new = {f'{count},'+i:child[i] for i in child}
    #                 parsed.update(new)
    #             elif isinstance(i, Tlist):
    #                 child = i.get_data()
    #                 new = {f'{count},' + i:child[i] for i in child}
    #                 parsed.update(new)
    #             else:
    #                 self._printmessage('input type incorrect')
    #                 return None
    #             count += 1
    #     return parsed


    def _checkifleaf(self):
        a = all([isinstance(i, Item) for i in self.get_data()]) and len(self.get_data()) is not 0
        self._isleaf = a

    def calculate(self):
        pass

    def append(self,shape):
        pass
    def insert(self,shape):
        pass

    def leafs(self):
        pass

    def items(self,_count = 0):

        if self.isleaf():
            return self.get_data()
        else:
            items = []
            for i in self.get_data():
                items += i.items(_count = _count +1)
            if _count is 0:
                return Tlist(items)
            else:
                return items

    def copy(self,item:slice= None):
        if item is None:
            return copy.deepcopy(self)
        else:
            return copy.deepcopy(self[item])

    def __getitem__(self, item:(slice, tuple)):
        if self.isleaf():

            try:
                if item.__class__ is Ellipsis.__class__:
                    pass

                elif isinstance(item, slice):
                    print('item slice')
                    return Tlist([self.get_data()[item]])

                elif isinstance(item, int):
                    print('item single')

                    return Tlist([self.get_data()[item]])

                elif all(isinstance(i,int) for i in item):
                    print('tiem integers')
                    new_data = []
                    for i in item:
                        new_data.append(self._data[i])
                    return Tlist(*new_data)

                else:
                    self._printmessage('indexing type incorrect')
                    return None

            except:
                self._printmessage('index out of bound')
                return None
        else:
            if item.__class__ is Ellipsis.__class__:
                print('ddd')
                return self
            else:

                return self.get_data()[item]
    def __getitem__(self,item):
        print(item)
        print(self._data)
        keys =self._data.keys()
        values = self._data.values()
        print(self._data.ite)


    def __setitem__(self, key, value):
        #cases
        try:
            # single key
            if isinstance(key, int):
                self._data[key][0] = value
            # slice
            elif isinstance(key,slice):
                if not isinstance(value,(tuple,list)):
                    for i in self._data[key]:
                        i[0] = value
                else:
                    value = list(value)
                    items = self._data[key]
                    d = divmod(len(items),len(value))
                    reshapedval = value*d[0] + value[:d[1]]
                    for i,j in zip(items,reshapedval):
                        i[0] = j
            elif isinstance(key, (tuple,list)):
                value = list(value)
                items = []
                for i in key:
                    items.append(self._data[i])
                d = divmod(len(items), len(value))
                reshapedval = value * d[0] + value[:d[1]]
                for i, j in zip(items, reshapedval):
                    i[0] = j

        except:
            self._printmessage('probably index out of bound')

    # def wrap(self,times:int = 1, _count= 1):
    #     if times is _count:
    #         newtlist = copy.Tlist()
    #         print(id(self))
    #
    #     else:
    #         pass

    def set_data(self,data):
        self._data = data

    def isleaf(self):
        return self._isleaf

    def print_data(self, _count=0):
        lu = u'\u2554'
        ru = u'\u2557'
        ld = u'\u255a'
        rd = u'\u255d'
        vr = u'\u2551'
        hr = u'\u2550'

        if self.isleaf():
            listlen = len(self.get_data())
            types = []
            texts = []
            lentypes = []
            lentexts = []
            for i in self.get_data():
                types.append(str(i.type().__name__))
                if isinstance(i, Geometry):
                    texts.append(i.__str__(True))
                else:
                    texts.append(str(i))
                lentypes.append(len(str(type(i))))
                lentexts.append(len(str(i)))

            max_lentype = max(lentypes)
            max_lentext = max(lentexts)

            types = [j + ' ' * (max_lentype - lentypes[i]) for i, j in enumerate(types)]
            texts = [j + ' ' * (max_lentext - lentexts[i]) for i, j in enumerate(texts)]
            lines = [vr + i + ':' + j + vr for i, j in zip(types, texts)]
            top = lu + hr * (len(lines[0]) - 2) + ru
            bottom = ld + hr * (len(lines[0]) - 2) + rd
            lines.insert(0, top)
            lines.append(bottom)

            if _count is 0:
                for i in lines:
                    print(i)
            else:
                return lines
        else:
            blocklines = []
            blocklen = []
            print(self._data)
            for i in self._data:
                data = i.print_data(_count=_count + 1)
                blocklines += data
                blocklen.append(len(data[0]))
            max_blocklen = max(blocklen)

            for i in range(len(blocklines)):
                line = blocklines[i]
                blocklines[i] = vr + line + ' ' * (max_blocklen - len(line)) + vr

            top = lu + hr * (max_blocklen) + ru
            bottom = ld + hr * (max_blocklen) + rd
            blocklines.insert(0, top)
            blocklines.append(bottom)

            if _count is 0:
                for i in blocklines:
                    print(i)
            else:
                return blocklines


    def _parse_strindex(self):
        return [[int(ii) for ii in i.split(',')] for i in self.get_data().keys()]
    def _parse_listindex(self, list):
        pass

class Vector(Primitive):

    def __init__(self,x:(int, float),y:(int, float),z:(int, float)):
        self.set_data(np.array([x,y,z,0]))

    def __str__(self):
        arr = self.get_data()
        return f'{self.__class__.__name__} : {arr[:3]}'


class Geometry(Primitive):
    pass


class Point(Geometry):

    def __init__(self,x:(int, float),y:(int, float),z:(int, float)):
        self.set_data(np.array([[x],[y],[z],[1]]  ))

    def __str__(self, dataonly = False):
        arr = self.get_data()
        if dataonly:
            return f'{arr.T[0,:3]}'
        else:
            return f'{self.__class__.__name__} : {arr.T[0,:3]}'

    def __repr__(self):
        t = self.__str__()
        return t