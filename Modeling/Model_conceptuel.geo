w = 1000;
h = 700;
d = 100;
t = 3;
l = 100;
s = 25; 
lc = 20;
lf = t/2;
i = 0;
j = 0;
x = 0 ;
y = 0;


// reservoir 
Point(1) = {0, 0, 0, lc};
Point(2) = {w, 0,  0, lc} ;
Point(3) = {w, h, 0, lc};
Point(4) = {0, h, 0, lc} ;

// mined seam
Point(5) = {0, h-d, 0, lf} ;
Point(6) = {0, h-d+t, 0, lf} ;
Point(7) = {w, h-d+t, 0, lf} ;
Point(8) = {w, h-d, 0, lf} ;

Point(9) = {0, h-d-s, 0, lf} ;
Point(10) = {0, h-d-s+t, 0, lf} ;
Point(11) = {w, h-d-s+t, 0, lf} ;
Point(12) = {w, h-d-s, 0, lf} ;

// wells
Point(100) = {w-(w+l)/2, h-d+t/2, 0, lf} ;
Point(101) = {w-(w-l)/2, h-d+t/2, 0, lf} ;
Point(102) = {w-(w+l)/2, h, 0, lc} ;
Point(103) = {w-(w-l)/2, h, 0, lc} ;

For x In {104:122}

  i += 1 ;
  
  Point(x) = {w-(w-l)/2, h-d/20*i, 0, lf} ;

EndFor

For y In {123:141}

  j += 1 ;
  
  Point(y) = {w-(w+l)/2, h-d/20*j, 0, lf} ;

EndFor


Line(1) = {4, 6};
Line(2) = {6, 5};
Line(3) = {5, 10};
Line(4) = {10, 9};
Line(5) = {9, 1};
Line(6) = {1, 2};
Line(7) = {2, 12};
Line(8) = {12, 11};
Line(9) = {11, 8};
Line(10) = {8, 7};
Line(11) = {7, 3};
Line(12) = {3, 103};
Line(13) = {103, 102};
Line(14) = {102, 4};
Line(15) = {6, 7};
Line(16) = {8, 5};
Line(17) = {10, 11};
Line(18) = {12, 9};

Line Loop(19) = {14, 1, 15, 11, 12, 13}; Plane Surface(20) = {19};
Line Loop(21) = {15, -10, 16, -2}; Plane Surface(22) = {21};
Line Loop(23) = {16, 3, 17, 9}; Plane Surface(24) = {23};
Line Loop(25) = {17, -8, 18, -4}; Plane Surface(26) = {25};
Line Loop(27) = {18, 5, 6, 7}; Plane Surface(28) = {27};

Point {100,101} In Surface {22};
Point {102:141} In Surface {20};

Physical Surface(29) = {20};
Physical Surface(30) = {24};
Physical Surface(31) = {28};
Physical Surface(32) = {22, 26};

Field[1] = Attractor;
Field[1].NodesList = {102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141};

Field[2] = Threshold;
Field[2].DistMax = 4;
Field[2].DistMin = 2;
Field[2].IField = 1;
Field[2].LcMax = 20;
Field[2].LcMin = 1.5;

Field[3] = Min;
Field[3].FieldsList = {2};
Background Field = 3;

