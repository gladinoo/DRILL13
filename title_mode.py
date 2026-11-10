from pico2d import (
    load_image, clear_canvas, update_canvas, get_events,
    open_canvas, close_canvas,
    SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
)
import game_framework

image = None


def init():
    global image
    image = load_image('title.png')


def finish():
    global image
    del image


def update():
    pass


def render():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def draw():
    """render 별칭 함수"""
    render()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # ESC를 누르면 프로그램 종료 (escape)
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                # SPACE를 누르면 플레이 모드로 이동
                try:
                    import play_mode
                    game_framework.change_mode(play_mode)
                except ImportError:
                    pass


def pause():
    pass


def resume():
    pass


# 타이틀 모드 하나만 갖는 게임 단독 실행
if __name__ == '__main__':
    open_canvas(800, 600)
    import title_mode
    game_framework.run(title_mode)
    close_canvas()
