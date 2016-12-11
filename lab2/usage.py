from rectdrawer.base import load_from_file, StartupParams, construct_root_window, gui_loop, redraw, Position
from rectdrawer.console import c
import argparse
import os


def get_arguments() -> dict():
    parser = argparse.ArgumentParser(description='Draw some rectangles.')
    parser.add_argument('file', type=str)

    args = parser.parse_args()
    if not os.path.exists(args.file):
        parser.error(c.FAIL + c.BOLD + 'File doesnt exists: %s %s' % (c.ENDC, args.file))
    else:
        return args


def debug_arguments(params: StartupParams) -> None:
    print(c.BOLD + c.HEADER + 'DEBUG' + c.ENDC)
    print(c.BOLD + 'Area:%s\t%d x %d' % (c.ENDC, params.width, params.height))
    for rect in params.rectangles:
        print(c.BOLD + 'Rect:%s\tx = [%d:%d], y = [%d:%d]' % (c.ENDC, rect.x1, rect.x2, rect.y1, rect.y2))


def act() -> None:
    args = get_arguments()
    try:
        startup_params = load_from_file(args.file)
    except Exception as exc:
        print(c.FAIL + c.BOLD + 'Error during loading file %s: %s %s' % (args.file, c.ENDC, exc))
        return

    gui = construct_root_window(startup_params)

    gui.root.bind('r', lambda x: redraw(startup_params, gui))
    gui.root.bind('d', lambda x: debug_arguments(startup_params))
    gui.root.bind('q', lambda x: exit(0))
    gui.canvas.bind('<ButtonPress-1>', lambda e: redraw(startup_params, gui, Position(e.x, e.y)))

    redraw(startup_params, gui)
    gui_loop()

if __name__ == '__main__':
    act()


