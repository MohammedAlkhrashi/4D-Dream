from .musicautobot.numpy_encode import *
from .musicautobot.utils.file_processing import process_all, process_file
from .musicautobot.config import *
from .musicautobot.music_transformer import *
from .musicautobot.multitask_transformer import *
from .musicautobot.numpy_encode import stream2npenc_parts
from .musicautobot.utils.setup_musescore import setup_musescore
from music21 import midi

class MusicAutobot:
	def __init__(self):
		# Config
		config = multitask_config();

		# Location of your midi files
		midi_path =  Path('data/midi')

		# Location of saved datset
		data_path = Path('data/numpy')
		data_save_name = 'musicitem_data_save.pkl'
		
		self.data = MusicDataBunch.empty(data_path)
		self.vocab = self.data.vocab

		pretrained_path = data_path/'pretrained'/'MultitaskSmallKeyC.pth'
		# pretrained_path.parent.mkdir(parents=True, exist_ok=True)
		# download_url(pretrained_url, dest=pretrained_path)

		self.learn = multitask_model_learner(self.data, pretrained_path=pretrained_path)

		

	def add_harmony(self, melody_path="music_clip/melody"):
		files = get_files(melody_path, recurse=True, extensions='.mid')
		for f in files:
			if f.name == 'new.mid':
				midi_file = f

		

		item = MusicItem.from_file(midi_file, self.data.vocab)

		dur_melody = item.mask_duration()

		new_rhythm = self.learn.predict_mask(dur_melody
		, temperatures=(0.8,0.8), top_k=40, top_p=0.6
		)
		output_midi = midi.translate.streamToMidiFile(new_rhythm.stream)
		output_midi.open('music_clip/music/output/rhythm_remix.mid', 'wb')
		output_midi.write()
		output_midi.close()

		note_item = new_rhythm.mask_pitch();
		new_pitch = self.learn.predict_mask(note_item, temperatures=(1.4, 1))
		output_midi = midi.translate.streamToMidiFile(new_pitch.stream)
		output_midi.open('music_clip/music/output/pitch_remix.mid', 'wb')
		output_midi.write()
		output_midi.close()
		

		empty_chords = MusicItem.empty(self.vocab, seq_type=SEQType.Chords)
		pred_chord = self.learn.predict_s2s(input_item=new_pitch, target_item=empty_chords)

		combined = MultitrackItem(new_pitch, pred_chord)
		output_midi = midi.translate.streamToMidiFile(combined.stream)
		output_midi.open('music_clip/music/output/music.mid', 'wb')
		output_midi.write()
		output_midi.close()

	def autocomplete(self, music_path='music_clip/music/output'):
		files = get_files(music_path, recurse=True, extensions='.mid')
		for f in files:
			if f.name == 'music.mid':
				midi_file = f

		item = MusicItem.empty(self.data.vocab)

		pitch_temp = 1.4 # randomness of melody
		tempo_temp = 1.0 # randomness or rhythm
		top_k = 40
		_, full = self.learn.predict_nw(item, temperatures=(pitch_temp, tempo_temp), top_k=top_k, top_p=0.5, min_bars=64)

		output_midi = midi.translate.streamToMidiFile(full.stream)
		output_midi.open('music_clip/music/output/cont_music.mid', 'wb')
		output_midi.write()
		output_midi.close()





