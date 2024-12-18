# Plant Tracker



### Challenges Faced
#### Cleaning the Data
- Tensor Flow is great, but it does not support all file types. To combat this, I am not sure if it was an orthodox method, but I:
    - Sorted all files not supported by TF: https://stackoverflow.com/questions/68191448/unknown-image-file-format-one-of-jpeg-png-gif-bmp-required
    - The used `os.remove` to take out any images that would cause issues training the model.
- Some data was incorrect:
    - Sourced from this Kaggle dataset: https://www.kaggle.com/datasets/kacpergregorowicz/house-plant-species
    - It contained some images that were "roughly" associated with the houseplant
        - I.e. "aloe vera" had a bottle of aloe vera product instead of the houseplant