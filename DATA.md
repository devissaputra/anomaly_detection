# Data

This project uses scikit-learn's Optical Recognition of Handwritten Digits dataset.

- 1,797 images
- 8 × 8 grayscale pixels
- 64 numerical features after flattening
- 10 digit classes

Source documentation: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html

Digit 0 is treated as the novelty class. The model is trained only on digits 1 through 9, while digit-0 examples remain available for evaluation.
