Bryonna Crowley
CMPSC 441/GAME 450 - Artificial Intelligence SP2023
Final Project


1. Abstract
        This final project for the artificial intelligence and advanced game programming class builds on concepts and implementations learned throughout the year to create one cohesive game. It includes several AI components that either procedurally generate or optimize game content. The game also includes currency and travel cost, and has new loss conditions– running out of money, being unable to afford any available path, and being defeated in battle. The additional AI method that I chose is text-to-image image generation.
2. AI Components
1. Terrain/landscape
2. GA System
3. Journal image generation


3. Problems Solved
        The AI used to generate terrain solves the problem of needing unique, interesting, and realistic terrain for the landscape of the game world. It uses Perlin Noise to procedurally generate terrain based on input such as octaves and seed. Octaves affect how often extreme zones like mountains or deep valleys occur, while seed affects the way the generated data is randomized. 
        The GA System uses AI to train the cities to be more realistically spread out on the landscape’s terrain. It takes elevation into account and trains the generated set of cities based on how high or low each city’s elevation is, as well as how close each city is to each other city. The optimal set of spread out cities are trained using a pygad fitness model. The three factors of extreme low elevation, extreme high elevation, and density are examined and either rewarded or penalized for their current state. After the fitness level has been altered by these rewards and penalties, the fitness model iterates over the spread of cities again, attempting to create a more optimal geography that will fetch the highest possible fitness score.
        The technique I used for the journal image generation was to install the big-sleep library and all necessary supporting libraries such as Pytorch and CUDA. The image generator has a large list of input parameters that can be altered to change the outcome of the function call, however I had to keep my parameters extremely conservative as I only have 4GB of VRAM on my Surface Laptop Studio. I unfortunately chose AMD for my PC when I built it a few years ago, so the laptop with NVIDIA is my best choice for machine learning with images. Due to these challenges, I set my input parameters to a low image size (256), a relatively small number of iterations (500), and a very small num_of_cutouts (32). To save myself some time, I also scaled epochs back to 5 from the default of 20. I set the image generation to happen only upon each successful completion of battle, as there would not be much to journal if the player does not encounter battle, and there would be nothing to journal if the player lost the game. The output of the image generation is saved to the root folder of the project, and my test run image can be found in the folder on GitHub. This use of AI solves the problem of generating an interactive story to immerse the player into the world that they are exploring. 


4. Appendix
        I did not use ChatGPT, but did extensively google things related to the image generation library I chose to use, big-sleep, since it took a bit of trial and error to get working with my laptop GPU.