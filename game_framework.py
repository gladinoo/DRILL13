import time

running = False
stack = []
frame_time = 0.0


def change_mode(mode):
    global stack
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if stack:
        stack.pop().finish()
    if stack:
        stack[-1].resume()
    else:
        quit()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    current_time = time.time()
    try:
        start_mode.init()
        while running:
            stack[-1].handle_events()
            stack[-1].update()
            stack[-1].render()
            frame_time = time.time() - current_time
            current_time = time.time()
            time.sleep(0.01)
    finally:
        while stack:
            stack.pop().finish()
        running = False
