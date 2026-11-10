from math import pi
from pico2d import load_image, get_time, get_canvas_width
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE
from transitions import Machine

import game_world
from ball import Ball


class Idle:
    def enter(self, boy):
        boy.idle_started_at = get_time()
        boy.frame = 0

    def do(self, boy):
        if get_time() - boy.idle_started_at >= 5.0:
            boy.fall_asleep()
        else:
            boy.frame = (boy.frame + 1) % 8

    def draw(self, boy):
        row = 300 if boy.face_dir == 1 else 200
        boy.image.clip_draw(boy.frame * 100, row, 100, 100, boy.x, boy.y)

    def space(self, boy):
        boy.fire_ball()

    def move(self, boy):
        boy.start_run()


class Sleep:
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy):
        pass

    def draw(self, boy):
        angle = pi / 2 if boy.face_dir == 1 else -pi / 2
        flip = '' if boy.face_dir == 1 else 'h'
        boy.image.clip_composite_draw(
            boy.frame * 100, 300, 100, 100,
            angle, flip, boy.x, boy.y - 30, 100, 100
        )

    def space(self, boy):
        boy.wake_up()

    def move(self, boy):
        boy.start_run()


class Run:
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        boy.x = max(25, min(get_canvas_width() - 25, boy.x))

    def draw(self, boy):
        row = 100 if boy.face_dir == 1 else 0
        boy.image.clip_draw(boy.frame * 100, row, 100, 100, boy.x, boy.y)

    def space(self, boy):
        boy.fire_ball()

    def move(self, boy):
        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.idle_started_at = get_time()
        self.dir = 0
        self.face_dir = 1
        self.pressed_keys = set()
        self.item = 'Ball'  # 기본 선택 아이템: 'Ball' (작은 공), 'BigBall' (큰 공), None (공 없음)

        self.states = {'IDLE': Idle(), 'SLEEP': Sleep(), 'RUN': Run()}

        self.machine = Machine(
            model=self,
            states=['IDLE', 'SLEEP', 'RUN'],
            transitions=[
                {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'start_run', 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
                {'trigger': 'stop_run', 'source': 'RUN', 'dest': 'IDLE'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def update(self):
        self.states[self.state].do(self)

    def draw(self):
        self.states[self.state].draw(self)

    def on_enter_IDLE(self):
        self.states['IDLE'].enter(self)

    def on_enter_SLEEP(self):
        self.states['SLEEP'].enter(self)

    def on_enter_RUN(self):
        self.states['RUN'].enter(self)

    def fire_ball(self):
        if self.item is None or self.item == 0:
            return
        ball_type = 1 if (self.item == 'Ball' or self.item == 1) else 2
        ball = Ball(self.x, self.y, self.face_dir * 10, ball_type=ball_type)
        game_world.add_object(ball, 1)

    def pause(self):
        self.pressed_keys.clear()
        if self.state == 'RUN':
            self.dir = 0
            self.stop_run()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.states[self.state].space(self)
            return

        if event.type not in (SDL_KEYDOWN, SDL_KEYUP) or event.key not in (SDLK_LEFT, SDLK_RIGHT):
            return

        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        else:
            self.pressed_keys.discard(event.key)

        if SDLK_RIGHT in self.pressed_keys and SDLK_LEFT in self.pressed_keys:
            self.dir = 0
            if self.state == 'RUN':
                self.stop_run()
        elif SDLK_RIGHT in self.pressed_keys:
            self.dir = 1
            self.face_dir = 1
            self.states[self.state].move(self)
        elif SDLK_LEFT in self.pressed_keys:
            self.dir = -1
            self.face_dir = -1
            self.states[self.state].move(self)
        else:
            self.dir = 0
            if self.state == 'RUN':
                self.stop_run()
