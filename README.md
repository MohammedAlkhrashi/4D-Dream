# Final Results
 [Video 1](https://www.youtube.com/watch?v=UFmA7bWlP1k) (Artathon Submission)
 
 [Video 2](https://www.youtube.com/watch?v=OoNonzv85IM)
 

# 4D-Dream (AI Artathon 2021)
A fully AI-generated artistic piece that features all the components needed for a music video; the music, lyrics, and video clip. The lyrics can be composed manually or through the use of an AI. In our case, we generated a poem as our lyrics using Google's Verse by Verse model.

To produce our video clip we enhanced existing state-of-the-art methods for text-to-image generation to create an innovative 'text-to-video' generation method or more specifically 'lyrics-to-music video'. This technique can produce extremely artistic and awe-inspiring videos that relate directly to the input text or lyrics.  

The lyrics are also fed into a music generation model that outputs a complimentary, singable, musical piece, saving you the hard work of melodizing any form of poetic verse.




# Lyrics Generation
Although we could have used any string for our lyrics input, we chose to use Google's Verse by Verse to generate a poem we could use to take out as much human involvement in the final piece as possible. 
# Music Generation
Given any piece of text, the music generation model ensures the "singability" of the resulting musical composition by breaking down the text to its syllables and establishing a 1-to-1 correspondence between them and the notes of the melody. This was achieved by creating a new MIDI file with random notes in the key of C repeated the same number as the syllable count (C because the model was only trained on music in the key of C). Then, making use of MusicAutobot, which is built on the transformer architecture (particularly Transformer-XL), we remix the pitch, rhythm, and then add harmony to output a complete musical piece.
# Video Generation
To generate the music video from the given lyrics we use CLIP and BigGAN with the help of Big Sleep to create a text-to-image generation model. The model takes some text description as input and tries to generate an image that fits that given description starting from a random image where the image 'fitness' improves with each training step.

We utilize the fact that the model outputs an image after every training step, by making each image into its own video frame, this technique allows us to create the text-to-video model. We do this for each verse of the lyrics but instead of initializing from a random image, we use the previous verse's output image. This grants the generated video natural and aesthetically pleasing transitions between the frames and the verses.

A limitation of the model is that it outputs relatively small images that are not suitable for high-quality video generation. To overcome this problem we use DCNN Super-Resolution models to upscale the images from 512x512 to 2048x2048 without noticeable quality loss.

# Resources Used
The Combination of BigGAN and Open AI's CLIP was used to create the text-to-image model that generated all the frames of the video.
[https://github.com/lucidrains/big-sleep](https://github.com/lucidrains/big-sleep)


Generating the music for remixing pitch/rhythm and harmonizing
(http://musicautobot.com/)

FSRCNN a CNN Super Resolution model that was used to upscale (4x) the frames of the video.
[https://arxiv.org/abs/1608.00367](https://arxiv.org/abs/1608.00367)



[Google' Verse by Verse model to generate the lyrics of the poem.](https://sites.research.google/versebyverse/)
