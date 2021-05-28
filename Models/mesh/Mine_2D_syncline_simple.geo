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
Point(3) = {w, h, 0, lc};
Point(4) = {0, h, 0, lc} ;

// mined seam
Point(5) = {160, h-d, 0, lf} ;
Point(6) = {164, h-d+t, 0, lf} ;
Point(7) = {w, h-d-100+t, 0, lf} ;
Point(8) = {w, h-d-100, 0, lf} ;

Point(9) = {140, h-d-s, 0, lf} ;
Point(10) = {144, h-d-s+t, 0, lf} ;
Point(11) = {w, h-d-100-s+t, 0, lf} ;
Point(12) = {w, h-d-100-s, 0, lf} ;

Point(110) = {20, 800, 0, 1.0};
Point(111) = {24, 800, 0, 1.0};
Point(112) = {50, 800, 0, 1.0};
Point(113) = {54, 800, 0, 1.0};

// wells injections points
Point(100) = {w-(w+l)/2, h-d-s-13+t/2, 0, lf} ;
Point(101) = {w-(w-l)/2, h-d-70+t/2, 0, lf} ;



// reservoir
Line(1) = {1, 2};
Line(2) = {2, 12};
Line(3) = {12, 11};
Line(4) = {11, 8};
Line(5) = {8, 7};
Line(6) = {7, 3};
Line(7) = {3, 113};
Line(8) = {113, 112};
Line(9) = {112, 111};
Line(10) = {111, 110};
Line(11) = {110, 4};
Line(12) = {4, 1};

// seam 1
Line(13) = {113, 6};
Line(14) = {6, 7};
Line(15) = {8, 5};
Line(16) = {5, 112};

// seam 2
Line(17) = {111, 10};
Line(18) = {10, 11};
Line(19) = {12, 9};
Line(20) = {9, 110};

//seam 1
Line Loop(21) = {8, -16, -15, 5, -14, -13};
Plane Surface(22) = {21};

//seam 2
Line Loop(23) = {3, -18, -17, 10, -20, -19};
Plane Surface(24) = {23};

//middle
Line Loop(25) = {16, 9, 17, 18, 4, 15};
Plane Surface(26) = {25};

//top
Line Loop(29) = {13, 14, 6, 7};
Plane Surface(30) = {29};

// reservoir 
Line Loop(27) = {20, 11, 12, 1, 2, 19};
Plane Surface(28) = {27};

//Line Loop(27) = {7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6};
//Plane Surface(28) = {27, 21, 23, 58};

Point {100} In Surface {24};
Point {101} In Surface {22};

Physical Surface(1) = {22,24}; // seam
Physical Surface(2) = {26}; // middle
Physical Surface(3) = {28, 30}; // undisrubed rock






