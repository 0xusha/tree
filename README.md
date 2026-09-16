# OpenCV Animated Proposal Scene

This is a Python project that uses OpenCV to procedurally draw a blooming tree and animate a proposal scene. 

The script uses a recursive function to draw the tree branch by branch, simulating growth. It uses a vibrant red and orange color palette for the blossoms. Once the tree finishes drawing, it reveals a scene with two characters constructed entirely out of basic OpenCV shapes (lines, circles, ellipses), followed by a continuous animation of falling petals.

## Requirements

You will need Python installed on your system, along with OpenCV and NumPy. You can install the required dependencies using pip:

```bash
pip install opencv-python numpy

Usage
Run the script from your terminal or command prompt:

Bash
python tree.py

Controls
The animation will start automatically.

To exit the program at any time during the drawing or the falling petal animation, make sure the OpenCV window is active and press the ESC key.
