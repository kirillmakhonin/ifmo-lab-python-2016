from collections import namedtuple
import os
import csv
from tkinter import Tk, Canvas, mainloop
from rectdrawer.console import c

Rectangle = namedtuple('Rectangle', ['idx', 'x1', 'y1', 'x2', 'y2'])
StartupParams = namedtuple('StartupParams', ['width', 'height', 'rectangles', 'indexes'])
Indexes = namedtuple('Indexes', ['cache', 'matrix'])
GUIElements = namedtuple('GUIElements', ['root', 'canvas'])
Position = namedtuple('Position', ['x', 'y'])


def pos2index(pos: Position) -> tuple:
    return pos.x, pos.y


def parse_positive_integer(val: str) -> int:
    try:
        if int(val) != float(val) or int(val) < 0:
            raise Exception('Should be integer')
    except:
        raise Exception('Should be integer')

    return int(val)


def build_index(width: int, height: int, rects: list) -> None:
    current_indexes = dict()
    matrix = dict()

    def build_index(store: dict, rect_id_set: set):
        id = store.get(rect_id_set, None)
        if id is None:
            store[rect_id_set] = id = len(store)
        return id


    for x in range(0, width + 1):
        for y in range(0, height + 1):
            targets = filter(lambda rect: rect.x1 <= x <= rect.x2 and rect.y1 <= y <= rect.y2, rects)
            idx = frozenset(rect.idx for rect in targets)
            matrix[x, y] = None if len(idx) == 0 else build_index(current_indexes, idx)

    return Indexes(current_indexes, matrix)


def load_from_file(path_to_file: str) -> StartupParams:
    if not os.path.exists(path_to_file):
        raise Exception("File %s not found" % path_to_file)

    with open(path_to_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')

        width, height = None, None
        lines = []
        idx = 0

        for elements in reader:
            if width is None:
                if len(elements) != 2:
                    raise Exception("First line should contains two integers: width and height")
                width, height = (parse_positive_integer(x) for x in elements)
            else:
                src_str = ','.join(elements)

                if len(elements) != 4:
                    raise Exception("Second and next lines should contains four integers: x1, y1, x2, y2")
                x1, y1, x2, y2 = (parse_positive_integer(x) for x in elements)

                if x2 <= x1 or y2 <= y1:
                    raise Exception("Condition: x2 > x1 & y2 > y1 failed for string %s" % src_str)

                if x2 > width or y2 > height:
                    raise Exception("Condition: x2 <= width & y2 <= height failed for string %s" % src_str)

                lines.append(Rectangle(idx, x1, y1, x2, y2))
                idx += 1

        params = StartupParams(width, height, lines, build_index(width, height, lines))
        return params


def construct_root_window(params: StartupParams) -> GUIElements:
    master = Tk()
    master.resizable(0,0)
    master.wm_title('LAB 2')

    w = Canvas(master, width=params.width, height=params.height)
    w.pack()
    w.create_rectangle(0, 0, params.width, params.height, fill='white')
    return GUIElements(master, w)


def draw_rectangle(rectangle: Rectangle, canvas: Canvas, style='empty', color='black', outline=None) -> None:
    kwargs = dict()

    if outline is None:
        outline = color

    if style == 'fill':
        kwargs['fill'] = color
        kwargs['outline'] = outline
    elif style == 'empty':
        kwargs['outline'] = outline
    elif style in ('hor', 'ver'):
        kwargs['outline'] = color
        kwargs['fill'] = color
    else:
        raise Exception("Unknown rect style: %s" % style)

    if style in ('hor', 'ver'):
        l = (rectangle.x2 - rectangle.x1) if (style == 'hor') else (rectangle.y2 - rectangle.y1)
        i = 0
        di = 3
        while i < l:
            curr_kwargs = {'fill': 'white', 'outline': color} if i %2 != 0 else kwargs
            ni = i + di
            if ni > l:
                ni = l

            if style == 'hor':
                canvas.create_rectangle(rectangle.x1, rectangle.y1 + i, rectangle.x2, rectangle.y1 + ni, **curr_kwargs)
            else:
                canvas.create_rectangle(rectangle.x1 + i, rectangle.y1, rectangle.x1 + ni, rectangle.y2, **curr_kwargs)
            i = ni
        canvas.create_rectangle(rectangle.x1, rectangle.y1, rectangle.x2, rectangle.y2, {'outline': outline})
    else:
        canvas.create_rectangle(rectangle.x1, rectangle.y1, rectangle.x2, rectangle.y2, **kwargs)


def draw_interception(params: StartupParams, gui: GUIElements, index_key: int, start_pos: Position) -> None:
    queue = [start_pos]
    good_cloud = []
    checked = set()

    while len(queue) > 0:
        current_queue = queue[:]
        for item in current_queue:
            if item in checked or params.indexes.matrix[pos2index(item)] != index_key:
                queue.remove(item)
                continue

            good_cloud.append(item)

            if item.x > 1:
                queue.append(Position(item.x - 1, item.y))
            if item.y > 1:
                queue.append(Position(item.x, item.y - 1))
            if item.x < params.width:
                queue.append(Position(item.x + 1, item.y))
            if item.y < params.height:
                queue.append(Position(item.x, item.y + 1))

            checked.add(item)
            queue.remove(item)

    for pos in good_cloud:
        gui.canvas.create_line(pos.x, pos.y, pos.x, pos.y, fill='red')


def redraw(params: StartupParams, gui: GUIElements, click_position: Position = None) -> None:
    if click_position is not None and (click_position.x > params.width or click_position.y > params.height):
        click_position = None
    cached_key = None

    print(c.BOLD + 'Redraw. %s Click position: %s' % (c.ENDC, str(click_position)))

    if click_position is not None:
        cached_key = params.indexes.matrix[(click_position.x, click_position.y)]

    gui.canvas.create_rectangle(0, 0, params.width, params.height, fill='white')

    for rectangle in params.rectangles:
        draw_rectangle(rectangle, gui.canvas, style='hor', color='#cacafa', outline='black')

    if cached_key is not None:
        print(c.UNDERLINE + 'Cached key detected: %d%s' % (cached_key, c.ENDC))
        draw_interception(params, gui, cached_key, click_position)

    gui.canvas.create_text((5, params.height - 3), text='HELP: r - redraw, d - debug, q - quit', anchor='sw', fill='green')


def gui_loop() -> None:
    mainloop()