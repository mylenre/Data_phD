// created by bhe_setup_tool
// project name: BHE2

// geometry parameters
width = 300;
length = 300;
box_start = 100;
box_length = 100;
box_width = 100;
z = -150;

// element sizes
elem_size_box = 1;
elem_size_corner = 20;


// bounding box
Point(1) = { box_width/2.0, box_start, 0.0, elem_size_box};
Point(2) = {-box_width/2.0, box_start, 0.0, elem_size_box};
Point(3) = {-box_width/2.0, box_start + box_length, 0.0, elem_size_box};
Point(4) = { box_width/2.0, box_start + box_length, 0.0, elem_size_box};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

Transfinite Surface {1};
Transfinite Line {3, 1, 4, 2} = 51 Using Progression 1;
Recombine Surface {1};


// model boundaries
Point(12) = {-width/2.0, 0.0, 0.0, elem_size_corner};
Point(13) = { width/2.0, 0.0, 0.0, elem_size_corner};
Point(14) = { width/2.0, length, 0.0, elem_size_corner};
Point(15) = {-width/2.0, length, 0.0, elem_size_corner};
Line(12) = {12, 13};
Line(13) = {13, 14};
Line(14) = {14, 15};
Line(15) = {15, 12};
Line Loop(2) = {12, 13, 14, 15};
Plane Surface(2) = {2, 1};

// Transfinite Surface {2};
// Transfinite Line {15, 12, 13, 14} = 31 Using Progression 1;
// Recombine Surface {2};


Extrude {0, 0, z} { 
	  Surface{2, 1}; Layers{ {30}, {1} }; Recombine;
	}
	Coherence;
    
Physical Volume(1) = {1, 2};

