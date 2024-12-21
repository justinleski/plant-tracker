# Plant Tracker



### Challenges Faced
#### Cleaning the Data
- Tensor Flow is great, but it does not support all file types. To combat this, I am not sure if it was an orthodox method, but I:
    - Sorted all files not supported by TF: https://stackoverflow.com/questions/68191448/unknown-image-file-format-one-of-jpeg-png-gif-bmp-required
    - The used `os.remove` to take out any images that would cause issues training the model.
- Some data was incorrect:
    - Sourced from this [Kaggle dataset](https://www.kaggle.com/datasets/kacpergregorowicz/house-plant-species)
    - It contained some images that were "roughly" associated with the houseplant
        - I.e. "aloe vera" had a bottle of aloe vera product instead of the houseplant

### Training the Model (Accuracy)
- My first iteration of the model is relatively accurate, but could use some improvements.
    - I just added random contrast to emulate differences in cameras, lighting conditions, and plant health states.
#### Pipelining
- While training the model and attempting to use it in my app, I came to realize that my model just predefined the expected image size using `InputLayer`, however, this posed a problem as it required all of the images fed to the model to be $128 \times 128$ which made the pipeline difficult for my first fullstack application
- To combat this hiccup, I first tried to create **proxy** to process the image before it was fed to model, but this would require extra set-up and more code to handle the images
    - Instead, I opted to retrain the model with some slight modifications *and* the ability to resize the images
    - This made the model easier to deploy with less middleman work

### Connecting the Front and Back End
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving) allows for easy deployment of models.