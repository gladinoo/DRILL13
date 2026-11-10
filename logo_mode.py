from pico2d import (
    load_image, get_time, clear_canvas, update_canvas, get_events,
    open_canvas, close_canvas,
    SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
)
import game_framework
import title_mode

image = None
logo_start_time = 0.0


def init():
    global image, logo_start_time
    image = load_image('tuk_credit.png')
    logo_start_time = get_time()


def finish():
    global image
    del image


def update():
    global logo_start_time
    # 2.0초 경과 시 타이틀 화면으로 자동 전환
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)


def render():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def draw():
    render()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def pause():
    pass


def resume():
    pass


if __name__ == '__main__':
    open_canvas(800, 600)
    import logo_mode
    game_framework.run(logo_mode)
    close_canvas()
