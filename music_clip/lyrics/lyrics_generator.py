class LyricsGenerator:
    def __init__(self) -> None:
        pass

    def generate(self):
        return ["This is fire", "Under the sky", "on the beach"]

    def __call__(self):
        return self.generate()
