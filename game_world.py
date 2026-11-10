world = [[], []]


def add_object(o, depth=0):
    world[depth].append(o)


def add_oject(o, depth=0):
    """오타 방지용 별칭 함수"""
    add_object(o, depth)


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()
