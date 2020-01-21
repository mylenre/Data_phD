w = 1000;
h = 800;
d = 100;
t = 3;
r= 2;
l = 500;
s = 25; 
lc = 30;
lm = 10;
lf = t/1.5;

// reservoir 
Point(1) = {0, 0, 0, lc};
Point(2) = {w, 0,  0, lc} ;
Point(3) = {w, h, 0, lm};
Point(4) = {0, h, 0, lm} ;

// mined seam
Point(5) = {0, h-d, 0, lf} ;
Point(6) = {0, h-d+t, 0, lf} ;
Point(7) = {w, h-d-100+t, 0, lf} ;
Point(8) = {w, h-d-100, 0, lf} ;

Point(9) = {0, h-d-s, 0, lf} ;
Point(10) = {0, h-d-s+t, 0, lf} ;
Point(11) = {w, h-d-100-s+t, 0, lf} ;
Point(12) = {w, h-d-100-s, 0, lf} ;

// wells injections points
Point(100) = {w-(w+l)/2, h-d+t/2-25, 0, lf} ;
Point(101) = {w-(w-l)/2, h-d+t/2-75, 0, lf} ;

// shaft area

Point(102) = {w-(w+l)/2+r/2, h, 0, lm} ;
Point(103) = {w-(w+l)/2+r/2, h-d+t-25, 0, lf} ;
Point(104) = {w-(w+l)/2-r/2, h, 0, lm} ;
Point(105) = {w-(w+l)/2-r/2, h-d+t-25, 0, lf} ;

Point(106) = {w-(w-l)/2-r/2, h, 0, lm} ;
Point(107) = {w-(w-l)/2-r/2, h-d+t-75, 0, lf} ;
Point(108) = {w-(w-l)/2+r/2, h, 0, lm} ;
Point(109) = {w-(w-l)/2+r/2, h-d+t-75, 0, lf} ;

Line(1) = {4, 104};
Line(2) = {102, 104};
Line(3) = {102, 106};
Line(4) = {106, 108};
Line(5) = {108, 3};
Line(6) = {3, 7};
Line(7) = {7, 8};
Line(8) = {8, 11};
Line(9) = {11, 12};
Line(10) = {12, 2};
Line(11) = {2, 1};
Line(12) = {1, 9};
Line(13) = {9, 10};
Line(14) = {10, 5};
Line(15) = {5, 6};
Line(16) = {6, 4};
Line(17) = {6, 105};
Line(18) = {105, 103};
Line(19) = {103, 107};
Line(20) = {107, 109};
Line(21) = {109, 7};
Line(22) = {8, 5};
Line(23) = {10, 11};
Line(24) = {12, 9};
Line(25) = {104, 105};
Line(26) = {102, 103};
Line(27) = {106, 107};
Line(28) = {108, 109};

// top left
Line Loop(1) = {1, 25, -17, 16}; Plane Surface(1) = {1};
// top middle
Line Loop(2) = {3, 27, -19, -26}; Plane Surface(2) = {2};
//top right
Line Loop(3) = {5, 6, -21, -28}; Plane Surface(3) = {3};
// shafts left
Line Loop(4) = {2, 25, 18, -26}; Plane Surface(4) = {4};
//shaft right
Line Loop(5) = {4, 28, -20, -27}; Plane Surface(5) = {5};
// seams 1
Line Loop(6) = {17, 18, 19, 20, 21, 7, 22, 15}; Plane Surface(6) = {6};
// middle
Line Loop(7) = {22, -14, 23, -8}; Plane Surface(7) = {7};
//seam 2
Line Loop(8) = {23, 9, 24, 13}; Plane Surface(8) = {8};
//bottom
Line Loop(9) = {24, -12, -11, -10}; Plane Surface(9) = {9};

Physical Surface(1) = {1,2,3};
Physical Surface(2) = {7};
Physical Surface(3) = {9};
Physical Surface(4) = {4,5};
Physical Surface(5) = {6,8};

Point {100, 101} In Surface {6};
