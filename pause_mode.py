from pico2d import (
    clear_canvas, update_canvas, get_events, load_font, get_time,
    open_canvas, close_canvas,
    SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_p
)
import game_framework
import play_mode

font = None
start_time = 0.0


def init():
    global font, start_time
    try:
        font = load_font('ENCR10B.TTF', 36)
    except Exception:
        font = None
    start_time = get_time()


def finish():
    global font
    if font:
        del font


def update():
    pass


def render():
    clear_canvas()
    # 멈춘 플레이 화면을 배경으로 렌더링
    play_mode.render_world()

    # 화면 중앙에 PAUSE 텍스트 깜빡임 효과 연출
    if font:
        if int((get_time() - start_time) * 2) % 2 == 0:
            font.draw(320, 330, 'PAUSE', (255, 50, 50))
            font.draw(250, 280, 'Press P to Resume', (255, 255, 255))
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
            if event.key == SDLK_p:
                # P 키를 다시 누르면 일시정지 해제 후 원래 플레이 모드로 복귀
                game_framework.pop_mode()
            elif event.key == SDLK_ESCAPE:
                game_framework.pop_mode()


def pause():
    pass


def resume():
    pass


# 단독 테스트 실행
if __name__ == '__main__':
    open_canvas(800, 600)
    import pause_mode
    game_framework.run(pause_mode)
    close_canvas()
