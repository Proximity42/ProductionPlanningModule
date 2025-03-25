import random


class ColorPalette:

    # @staticmethod
    # def generate_color_palette(num_colors: int) -> list[str]:
    #     rgb_colors = distinctipy.get_colors(num_colors, pastel_factor=0.4)
    #
    #     # Преобразование RGB в HEX
    #     hex_colors = [ColorPalette.rgb_to_hex(color) for color in rgb_colors]
    #     return hex_colors

    @staticmethod
    def generate_color_palette(num_colors: int) -> list[str]:
        colors = []
        for i in range(0, num_colors):
            colors.append(
                ColorPalette.generate_new_color(colors, pastel_factor=0.5)
            )
        hex_colors = [ColorPalette.rgb_to_hex(color) for color in colors]
        return hex_colors

    @staticmethod
    def get_random_color(pastel_factor=0.5):
        return [
            (x + pastel_factor) / (1.0 + pastel_factor)
            for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]
        ]

    @staticmethod
    def color_distance(c1, c2):
        return sum([abs(x[0] - x[1]) for x in zip(c1, c2)])

    @staticmethod
    def generate_new_color(existing_colors, pastel_factor=0.5):
        max_distance = None
        best_color = None
        for i in range(0, 100):
            color = ColorPalette.get_random_color(pastel_factor=pastel_factor)
            if not existing_colors:
                return color
            best_distance = min(
                [
                    ColorPalette.color_distance(color, c)
                    for c in existing_colors
                ]
            )
            if not max_distance or best_distance > max_distance:
                max_distance = best_distance
                best_color = color
        return best_color

    @staticmethod
    def rgb_to_hex(rgb: list[float]) -> str:
        return "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
