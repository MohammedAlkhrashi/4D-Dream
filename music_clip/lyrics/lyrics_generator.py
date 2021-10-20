class LyricsGenerator:
    def __init__(self) -> None:
        pass

    def generate(self):
        return [
            "Love is the dear heart amid the flowers",
            "Sweet as a light in a beating meadow",
            "Hurried by her from her earthly hour",
            "Hopeless the raging tempest of her woe",
        ]

    def __call__(self):
        return self.generate()
