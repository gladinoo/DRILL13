from pico2d import (
    clear_canvas, update_canvas, get_events,
    SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_p, SDLK_i
)
import game_framework
import game_world
from boy import Boy
from grass import Grass

boy = None
grass = None


def init():
    global boy, grass
    grass = Grass()
    game_world.add_oject(grass, 0)
    boy = Boy()
    game_world.add_oject(boy, 1)


def finish():
    global boy, grass
    game_world.clear()
    boy = None
    grass = None


def pause():
    """다른 모드(pause_mode, item_mode 등)로 진입할 때 호출"""
    if boy and hasattr(boy, 'pause'):
        boy.pause()


def resume():
    pass


def update():
    game_world.update()


def render_world():
    """게임 월드 내의 객체들 렌더링 (pause_mode 등에서 배경으로 사용)"""
    game_world.render()


def render():
    clear_canvas()
    render_world()
    update_canvas()


def draw():
    render()


def handle_events():
    global boy
    import title_mode
    import pause_mode

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # ESC를 누르면 종료
                game_framework.quit()
            elif event.key == SDLK_i:
                # i 키를 누르면 아이템 모드 진입
                import item_mode
                game_framework.push_mode(item_mode)
            elif event.key == SDLK_p:
                # P 키를 누르면 게임 일시정지 (pause_mode 진입)
                game_framework.push_mode(pause_mode)
            else:
                if boy:
                    boy.handle_event(event)
        else:
            if boy:
                boy.handle_event(event)


if __name__ == '__main__':
    from pico2d import open_canvas, close_canvas
    import sys
    open_canvas(800, 600)
    game_framework.run(sys.modules[__name__])
    close_canvas()

