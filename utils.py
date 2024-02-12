import pickle


def blend_color(color1, color2, blend_factor):
    r = color1[0] + (color2[0] - color1[0]) * blend_factor
    g = color1[1] + (color2[1] - color1[1]) * blend_factor
    b = color1[2] + (color2[2] - color1[2]) * blend_factor
    return int(r), int(g), int(b)


def apply_vertical_gradient(surface, start_color, end_color):
    height = surface.get_height()
    for y in range(height):
        blend = y / height
        color = blend_color(start_color, end_color, blend)
        for x in range(surface.get_width()):
            pixel = surface.get_at((x, y))
            surface.set_at((x, y), color + (pixel[3],))


def get_high_score() -> int:
    with open("high_score_storage", "rb") as data:
        highscore = pickle.load(data)
    return highscore


def write_high_score(score: int):
    with open("high_score_storage", "wb") as data:
        pickle.dump(score, data)

