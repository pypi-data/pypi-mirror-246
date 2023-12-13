# Pixel Perfect

A versatile Python package leveraging TensorFlow's machine learning model for efficient image comparisons. Designed to seamlessly integrate with Selenium, it empowers developers with powerful tools for UI validations, making it a valuable asset for automated testing and visual verification in web applications.

## Installation

You can install pixel_perfect using pip:

```bash
pip install pixel_perfect 
```

## Usage: Image Comparison

The `image_similarity` method allows you to compare two images and receive a boolean value indicating whether the images are similar or not. The comparison is performed with a default threshold of 0.1, providing a balance between strictness and leniency. You can customize the threshold by adjusting the value.


```python
from pixel_perfect import image_similarity 

# Provide paths to the images for comparison
image_path1 
image_path2

# Compare the images with default threshold
isImageSimilar = image_similarity(image_path1, image_path2)

# Compare the images with custom threshold
isImageSimilar = image_similarity(image_path1, image_path2, 1)
```

You can utilize the `image_similarity_score` method to compare two images and obtain the similarity score. Here's a simple example:

```python
from pixel_perfect import image_similarity 

# Provide paths to the images for comparison
image_path1 
image_path2

# Compare the images
similarity_score = image_similarity(image_path1, image_path2)
```
