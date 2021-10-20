from music_clip.common import cd_into_folder
from music_clip.melody_generation import melody_from_lyrics
import pyphen
import re


def get_syllables(sentence):
    pyphen.language_fallback("en_US_variant1")
    dic = pyphen.Pyphen(lang="en_US")
    sentence = re.sub(r"[^\w]", " ", sentence)
    sentence = sentence.lower()

    out = []
    for word in sentence.split():
        for syllable in dic.inserted(word).split("-"):
            out.append([syllable, word])

    return out


class MusicGenerator:
    def __init__(self) -> None:
        pass

    def generate_initial_melody(self, lyrics):
        syllables = get_syllables(" ".join(lyrics))
        with cd_into_folder("music_clip/melody_generation"):

            # Forked from https://github.com/yy1lab/Lyrics-Conditioned-Neural-Melody-Generation
            melody_from_lyrics(syllables)

    def harmonize_melody(self):
        pass

