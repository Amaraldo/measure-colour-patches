# Measure-colour-patches

`Measure-colour-patches` is a Python script that automates the usually tedious task of measuring individual color patches from an image. This script uses Pygame and works by averaging the RGB values of every pixel within a specific point (to avoid erroneous noise values), outputting the averaged, normalized RGB values to a CSV file.

## How to Use
1. **Set Image Path** - Specify the path of the image you want to measure.
2. **Set CSV Output Path** - Specify the path where you would like the resulting CSV saved.
3. **Configure Rows and Columns** - Set the number of rows and columns as per your requirements.
4. **Set Point Size** - Customize the point size variable according to your needs.
5. **Save the CSV** - Once you have placed the points where you want them, press "s" to save the CSV.

The corner points shape the grid using bilinear interpolation, while all other points are locally controlled.

![Measure-color-patches](https://user-images.githubusercontent.com/51723444/234099935-05ec1e7e-0b61-4744-9c27-ee3ce9dd834f.png)
