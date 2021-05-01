# [Parametric Drone Design Software] :airplane:
by [Gyaase Ohemeng] (<pds [at]  KNUST [dot] edu>)


## Overview
This is a Python project  for parametric aircraft design that employs the use various libraries to assit int the conceptual design of fixed-wing rc aircraft and design validation

It is simply a collection of various libraries and work arounds to enable quick 3D modelling of aircraft and estimating various parameters for design validation** 

It uses:

*[Tigl](https://dlr-sc.github.io/tigl/) for geometry generation
*Datcom  for stability and control derivaives estimation(Very Problemtic) 
*[Trimesh] (https://github.com/mikedh/trimesh) to estimate momnents of inertia and center of mass
*[Aerosandbox](https://github.com/peterdsharpe/AeroSandbox) for determining aerodynamic coefficients,and alos for stability and control deriavtives
This is merely a means to help imporve my skills and understanding aircraft design.I have by ,no means, figured anything out :sweat_smile: **Hop on if you want to help or you have suggestios as to how to make is better cool**.


![Design Image](/images/5.jpg)
*Sample Geometry Designed*


![Design Image](/images/2.jpg)
*Sample Geometry Designed*

## Getting Started

### Installation and Tutorials

*First download the code from this repository or clone it
*Then install all dependencies with `pip install .`
*Make sure you are running on Python 3.7.*


### Usage
The "main" script is located in "run-point".
Please email me your "specification.json" file if you manage to come up with cool designs.:smile:
####Note
Design is split into two categories;
*Conventional for simple designs
*Unconventional for complex designs

## Future Goals
*I hope to fully Comment the code with detailed descriptions :sweat_smile:
*I would like to possible get a better library  or create one to increase the fidelity of the simulations(Aerodyamic simluations)
*Add drag and Drop funtionality
*Posssible come up with a better design for the UI :sweat_smile:
*If Have any features in mind ,contact me:smiley:


## Bugs
Please, please report all bugs by sending me an email at [Kojogyaase@gmail.com] or create an issue 

Please note that, while the entirety of the codebase should be cross-platform compatible, it has only been tested on Windows 10 in Python 3.7 


## License

MIT License

Copyright (c) 2021 Gyaase Ohemeng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

