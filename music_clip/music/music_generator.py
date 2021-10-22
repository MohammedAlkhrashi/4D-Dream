from music_clip.common import cd_into_folder
from music_clip.melody_generation import melody_from_lyrics
from .music_autobot import MusicAutobot
import pyphen
import re
import mido
from random import choice

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
        self.autobot = MusicAutobot()
        # autobot.add_harmony()

    def generate_initial_melody(self, lyrics):
        transitions = []
        melody = mido.MidiFile()
        melody.add_track()
        melody.add_track()
        
        melody.tracks[0] = mido.MidiTrack([
            mido.MetaMessage('set_tempo', tempo=500000, time=0),
            mido.MetaMessage('time_signature', numerator=4, denominator=4,
                        clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0),
            mido.MetaMessage('end_of_track', time=1)]
        )

        note_count = len(get_syllables(" ".join(lyrics)))
        print('NOTE COUNT', note_count)
        for i in range(note_count):
            note = choice([67, 69, 71, 72, 74, 76, 77, 79, 81, 83])
            melody.tracks[1].append(
                mido.Message('note_on', channel=0, note=note, velocity=100, time=0)
            )
            melody.tracks[1].append(
                mido.Message('note_on', channel=0, note=note, velocity=0, time=480)
            )
        melody.save('music_clip/melody/new.mid')
        # with cd_into_folder("music_clip/melody_generation"):
        #     # Forked from https://github.com/yy1lab/Lyrics-Conditioned-Neural-Melody-Generation
        #     syllables = get_syllables(lyrics[0])
        #     melody_from_lyrics(syllables, filename='a.mid')
        #     for line in lyrics:
        #         syllables = get_syllables(line)
        #         melody_from_lyrics(syllables, filename='b.mid')
        #         transition = self.append_melody(
        #             '../melody/a.mid', '../melody/b.mid')
        #         transitions.append(transition)
        #     print(transitions)
        # return transition

    def harmonize_melody(self):
        self.autobot.add_harmony()

    def append_melody(self, a_path, b_path):
        a_melody = mido.MidiFile(a_path)
        b_melody = mido.MidiFile(b_path)
        new_melody = mido.MidiFile()
        new_melody.add_track()
        new_melody.add_track()
        new_melody.add_track()
        new_melody.tracks[0] = a_melody.tracks[0]
        new_melody.tracks[1] = a_melody.tracks[1]

        # new_melody.tracks[2].append(mido.Message('note_on', note=last_note.note, time=last_note.time, velocity=0))
        for msg in b_melody.tracks[1]:
            new_melody.tracks[1].append(msg)

        s = 0
        for msg in new_melody.tracks[1]:
            s += msg.time

        new_melody.save(a_path)

        return s
