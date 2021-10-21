class LyricsGenerator:
    def __init__(self) -> None:
        pass

    def generate(self):
        return [
            "A calm summer day",
            "And the soft rosy lights are red with rain",
            "Bright as the days these low butterflies play",
            "Across the east the yellow daisies lain",
            "Hopeless the raging tempest of night's woe",
            "Within the shadowless, eternal skies",
            "Amid this soft transporting light of snow",
            "A baleful light of morn, a seething eye"
        ]

    def __call__(self):
        return self.generate()
