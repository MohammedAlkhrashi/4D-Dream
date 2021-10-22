# Forked from https://github.com/yy1lab/Lyrics-Conditioned-Neural-Melody-Generation
# Paper: https://arxiv.org/pdf/1908.05551.pdf

import numpy as np
import tensorflow as tf

# import midi_statistics
from .midi_statistics import tune_song
from . import utils
import os
from gensim.models import Word2Vec


def melody_from_lyrics(lyrics, filename='test.mid'):
    syll_model_path = "./enc_models/syllEncoding_20190419.bin"
    word_model_path = "./enc_models/wordLevelEncoder_20190419.bin"
    syllModel = Word2Vec.load(syll_model_path)
    wordModel = Word2Vec.load(word_model_path)
    length_song = len(lyrics)
    cond = []

    print(lyrics)

    for i in range(20):
        if i < length_song:

            print(lyrics[i][0])
            try:
                syll2Vec = syllModel.wv[lyrics[i][0]]
                word2Vec = wordModel.wv[lyrics[i][1]]
            except:
                print('AAAA')
                syll2Vec = syllModel.wv['a']
                word2Vec = wordModel.wv['WORD']
            cond.append(np.concatenate((syll2Vec, word2Vec)))
        else:
            cond.append(np.concatenate((syll2Vec, word2Vec)))

    flattened_cond = []
    for x in cond:
        for y in x:
            flattened_cond.append(y)

    model_path = "./saved_gan_models/saved_model_best_overall_mmd"
    # model_path = './saved_gan_models/saved_model_end_of_training'

    x_list = []
    y_list = []

    with tf.Session(graph=tf.Graph()) as sess:
        tf.saved_model.loader.load(sess, [], model_path)
        graph = tf.get_default_graph()
        keep_prob = graph.get_tensor_by_name("model/keep_prob:0")
        input_metadata = graph.get_tensor_by_name("model/input_metadata:0")
        input_songdata = graph.get_tensor_by_name("model/input_data:0")
        output_midi = graph.get_tensor_by_name("output_midi:0")
        feed_dict = {}
        feed_dict[keep_prob.name] = 1.0
        condition = []
        feed_dict[input_metadata.name] = condition
        feed_dict[input_songdata.name] = np.random.uniform(size=(1, 20, 3))
        condition.append(np.split(np.asarray(flattened_cond), 20))
        feed_dict[input_metadata.name] = condition
        generated_features = sess.run(output_midi, feed_dict)
        sample = [x[0, :] for x in generated_features]
        sample = tune_song(utils.discretize(sample))
        midi_pattern = utils.create_midi_pattern_from_discretized_data(
            sample[0:length_song]
        )
        destination = f"../melody/{filename}"
        midi_pattern.write(destination)

        print("done")

