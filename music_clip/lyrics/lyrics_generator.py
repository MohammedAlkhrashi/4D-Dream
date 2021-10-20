class LyricsGenerator:
    def __init__(self) -> None:
        pass

    def generate(self):
        return ["This is fire", "Under the night's sky", "With you baby"]

    def __call__(self):
        return self.generate()
