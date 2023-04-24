# Measure-colour-patches

Python script that uses Pygame to automate the unbelievably tedious task of measuring individual colour patches.

Set the path of the image you want to use and set the path to where you would like the CSV saved.
Set the number of rows and columns you need and the script will place a point at every intersection.
Set the point size variable and the script will average the RGB values of every pixel within that point (to avoid errornous noise values) and output the averaged, normalised rgb value to the CSV. 
The corner points shape the grid using bilinear interp but all other points have local control.
Press "s" to save the CSV once you have placed the points where you want them.
<img width="1141" alt="measure-colour-patches" src="https://user-images.githubusercontent.com/51723444/234099935-05ec1e7e-0b61-4744-9c27-ee3ce9dd834f.png">
