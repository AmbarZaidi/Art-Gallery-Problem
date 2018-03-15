# Vertex-Guard-Problem
Solving the Art Gallery Problem for N distinct planar points given in CCW order, using the DCEL Data Structure, where the guards appear stationary at vertices only. (Vertex Guard Problem).
Implementation in Python 3, uses 'tkinter' module for GUI display of output. 

###Input
  - # of Planar points followed by line separated 2D points (space separated)
  - Note:
      We dont have to repeat the first point at the end in the input so as to complete the polygon. It is taken automatically.

###Output
  - 1. Triangulated Regions represented by Triangle # and Vertices in a GUI ('tkinter' module in Python) 	
  - 2. Appropriate Debug and Program State Messages
  - 3. Guard Locations represented by colors.

###Compile Instructions
  - python3 ArtGalleryProblem.py < input > output

###Important Notes
Following are the assumptions that are followed throughout.
  1. POLYGON is assumed to be simple.
  2. Have used 'tkinter' module for graphical view of the Triangulated Regions. Occasionally, have to replace     'tkinter' by 'Tkinter' throughout.
  3. Have utilised DCEL structure to represent the points, edges and the plane in general.
  4. For Triangulation, have used Ear-Cutting Triangulation Algorithm which locates 'ears' and subsequently     triangulates them

	

