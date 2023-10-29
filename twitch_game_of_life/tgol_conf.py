import json


class TgolConf(object):
    def __init__(self, theme_file="./themes/twitch.json"):
        self.theme_file = theme_file

        self.cell_color = (100, 65, 165)
        self.bg_color = (241, 241, 241)
        self.grid_color = (185, 163, 227)
        self.side_bg_color = (38, 38, 38)
        self.font_color = (241, 241, 241)

        self.rows = 50
        self.cols = 75
        self.cell_size = 20
        self.sidebar_width = 275

        self.draw_grid_lines = True
        self.draw_coordinates = True
        self.toroidal = False

        self.load()
        self.load_theme()

    def toggle_toroidal(self):
        self.toroidal = not self.toroidal

    def toggle_grid_lines(self):
        self.draw_grid_lines = not self.draw_grid_lines

    def toggle_coordinates(self):
        self.draw_coordinates = not self.draw_coordinates

    def load_colors_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                color_data = json.load(file)
                return color_data
        except FileNotFoundError:
            print(f"The file '{filename}' was not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in '{filename}'.")
        return None

    def save(self):
        content = {
            "theme_file": self.theme_file,
            "draw_grid_lines": self.draw_grid_lines,
            "draw_coordinates": self.draw_coordinates,
            "toroidal": self.toroidal,
            "rows": self.rows,
            "cols": self.cols,
            "cell_size": self.cell_size,
            "sidebar_width": self.sidebar_width,
        }
        with open("conf.json", "w") as file:
            json.dump(content, file)

    def screen_size(self):
        screen_width = self.cols * self.cell_size + self.sidebar_width
        screen_height = self.rows * self.cell_size
        return screen_width, screen_height

    def load(self):
        try:
            with open("conf.json", "r") as file:
                conf = json.load(file)
                self.theme_file = conf.get("theme_file")
                self.draw_grid_lines = conf.get("draw_grid_lines")
                self.draw_coordinates = conf.get("draw_coordinates")
                self.toroidal = conf.get("toroidal")
                self.rows = conf.get("rows")
                self.cols = conf.get("cols")
                self.cell_size = conf.get("cell_size")
                self.sidebar_width = conf.get("sidebar_width")
        except FileNotFoundError:
            print("The file 'conf.json' was not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON in 'conf.json'.")

    def load_theme(self):
        theme = self.load_colors_from_json(self.theme_file)
        if theme:
            self.cell_color = theme.get("cell_color")
            self.bg_color = theme.get("bg_color")
            self.grid_color = theme.get("grid_color")
            self.side_bg_color = theme.get("side_bg_color")
            self.font_color = theme.get("font_color")
