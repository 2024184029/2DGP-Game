def event_to_string(state_event):
    from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_MOUSEWHEEL
    import pico2d

    event_names = {
        SDL_KEYDOWN: 'KEYDOWN',
        SDL_KEYUP: 'KEYUP',
        SDL_MOUSEMOTION: 'MOUSEMOTION',
        SDL_MOUSEBUTTONDOWN: 'MOUSEBUTTONDOWN',
        SDL_MOUSEBUTTONUP: 'MOUSEBUTTONUP',
        SDL_MOUSEWHEEL: 'MOUSEWHEEL'
    }

    state_event_type = state_event[0]  # state_event is ('INPUT', event)
    event = state_event[1]  # state_event is ('INPUT', event)
    if state_event_type != 'INPUT':
        return f"{state_event}"

    key_names = {}
    for name in dir(pico2d):
        if name.startswith('SDLK_'):
            key_code = getattr(pico2d, name)
            key_name = name.replace('SDLK_', '')
            key_names[key_code] = key_name

    event_type = event_names.get(event.type, f'Unknown({event.type})')
    key_attr = getattr(event, 'key', None)
    if key_attr is not None:
        key_name = key_names.get(key_attr, f'key({key_attr})')
    else:
        key_name = ''

    info = f'{event_type}:{key_name}'

    # 마우스 위치 정보 추가
    if event.type in (SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
        info += f', pos=({event.x},{event.y})'

    # 마우스 버튼 정보 추가
    if event.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
        info += f', button={event.button}'

    if event.type == SDL_MOUSEWHEEL:
        wheel_x = getattr(event, 'x', None)
        wheel_y = getattr(event, 'y', None)
        if wheel_x is not None or wheel_y is not None:
            info += f', wheel=({wheel_x},{wheel_y})'
        if hasattr(event, 'direction'):
            info += f', direction={event.direction}'

    if hasattr(event, 'mod') and event.mod:
        info += f', mod={event.mod}'

    return f"('{state_event_type}', {info})"