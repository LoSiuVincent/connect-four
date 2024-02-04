class Node:
    def __init__(self):
        self._parent = self
        self._children = []

    def is_leaf(self):
        return len(self._children) == 0

    def add_children(self, children: list['Node']):
        for child in children:
            child._parent = self
        self._children.extend(children)

    def get_parent(self):
        return self._parent
