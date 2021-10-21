# Red Rosy Rain

# Lyrics

# Music

# Video
To generate the music video from the given lyrics we use CLIP and BigGAN with the help of Big Sleep to create a text-to-image generation model. The model takes some text description as input and tries to generates an image that fits that given description starting from a random image where the image 'fitness' improves with each training step.

 We utilize the fact that the model outputs an image after every training step, by making each image into its own video frame, this technique allows us to create the music videos. We do this for each verse of the lyrics but instead of initializing from a random image, we use the previous verse's output image. This gives the generated video natural and aesthetically pleasing transitions between the frames and the verses. 
 
A limitation of the model is that it outputs relatively small images that are not suitable for high-quality video generation. To overcome this problem we use DCNN Super-Resolution models to upscale the images from 512x512 to 2048x2048 without noticeable quality loss. 
