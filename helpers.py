class Map(dict):
    """Dict wrapper to allow dot syntax

    Args:
        *args: Dicts with elements to be in Map (deep support implemented)
        **kwargs: Elements to be in Map (deep support implemented)

    Raises:
        AttributeError: If element in *args is not an instance of dict

    Example:
        >>> m = Map({'first_name': 'Eduardo', 'deep_one': {'foo': 'bar'}})
        >>> m.first_name
        'Eduardo'
        >>> m.deep_one.foo
        'bar'

    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)

        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        self[k] = Map(v)
                    else:
                        self[k] = v
            else:
                raise AttributeError('"{0}" is not an instance of dict'.format(str(type(arg))))

        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    self[k] = Map(v)
                else:
                    self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]