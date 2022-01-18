from numlab.lang.type import Type


class Instance:
    def __init__(self, _type: Type):
        self.type = _type
        self._dict = {}
        self._init_attributes()

    def _init_attributes(self):
        for attr, default in self.type.attributes.items():
            self._dict[attr] = default
