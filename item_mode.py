from pico2d import (
    load_image, clear_canvas, update_canvas, get_events,
    SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_0, SDLK_1, SDLK_2
)
import game_framework
import play_mode

image = None


def init():
    global image
    image = load_image('item_select.png')


def finish():
    global image
    del image


def update():
    pass


def render():
    clear_canvas()
    # 일시정지된 플레이 화면을 배경으로 먼저 렌더링
    play_mode.render_world()
    # 그 위에 중앙 아이템 선택 UI 창 출력
    image.draw(400, 300)
    update_canvas()


def draw():
    render()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # 취소하고 원래 플레이 화면으로 복귀
                game_framework.pop_mode()
            elif event.key == SDLK_0:
                # 0번: Clear (공 해제)
                play_mode.boy.item = None
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                # 1번: 작은 공 (ball21x21)
                play_mode.boy.item = 'Ball'
                game_framework.pop_mode()
            elif event.key == SDLK_2:
                # 2번: 큰 공 (ball41x41)
                play_mode.boy.item = 'BigBall'
                game_framework.pop_mode()


def pause():
    pass


def resume():
    pass

