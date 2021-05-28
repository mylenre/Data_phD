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

// wells injections points
Point(100) = {w-(w+l)/2, h-d-s-13+t/2, 0, lf} ;
Point(101) = {w-(w-l)/2, h-d-70+t/2, 0, lf} ;

// shaft area

Point(102) = {w-(w+l)/2+r/2, h, 0, lm} ;
Point(103) = {w-(w+l)/2+r/2, h-d+t-10, 0, lf} ;
Point(104) = {w-(w+l)/2-r/2, h, 0, lm} ;
Point(105) = {w-(w+l)/2-r/2, h-d+t-10, 0, lf} ;

Point(106) = {w-(w-l)/2-r/2, h, 0, lm} ;
Point(107) = {w-(w-l)/2-r/2, h-d+t-70, 0, lf} ;
Point(108) = {w-(w-l)/2+r/2, h, 0, lm} ;
Point(109) = {w-(w-l)/2+r/2, h-d+t-70, 0, lf} ;

Point(110) = {20, 800, 0, 1.0};
Point(111) = {24, 800, 0, 1.0};
Point(112) = {50, 800, 0, 1.0};
Point(113) = {54, 800, 0, 1.0};

Point(114) = {w-(w+l)/2-r/2, h-d-10, 0, lf} ;
Point(115) = {w-(w+l)/2+r/2, h-d-10, 0, lf} ;
Point(116) = {w-(w+l)/2-r/2, h-d-s-10, 0, lf} ;
Point(117) = {w-(w+l)/2+r/2, h-d-s-10, 0, lf} ;

Line(6) = {3, 7};
Line(7) = {7, 8};
Line(8) = {8, 11};
Line(9) = {11, 12};
Line(10) = {12, 2};
Line(11) = {2, 1};
Line(16) = {1, 4};
Line(17) = {6, 105};
Line(18) = {105, 103};
Line(19) = {103, 107};
Line(20) = {107, 109};
Line(21) = {109, 7};
Line(25) = {104, 105};
Line(26) = {102, 103};
Line(27) = {106, 107};
Line(28) = {108, 109};
Line(32) = {6, 113};
Line(33) = {3, 108};
Line(34) = {108, 106};
Line(35) = {106, 102};
Line(36) = {102, 104};
Line(37) = {104, 113};
Line(38) = {113, 112};
Line(39) = {112, 111};
Line(40) = {111, 110};
Line(41) = {110, 4};
Line(42) = {8, 115};
Line(43) = {114, 5};
Line(44) = {5, 112};
Line(45) = {110, 9};
Line(46) = {12, 9};
Line(47) = {111, 10};
Line(48) = {10, 116};
Line(49) = {117, 11};
Line(50) = {114, 116};
Line(51) = {117, 115};
Line(52) = {114, 115};
Line(53) = {116, 117};

// top and bottom
Line Loop(54) = {37, -32, 17, -25}; Plane Surface(55) = {54};
Line Loop(56) = {35, 26, 19, -27}; Plane Surface(57) = {56};
Line Loop(58) = {33, 28, 21, -6}; Plane Surface(59) = {58};
Line Loop(60) = {41, -16, -11, -10, 46, -45}; Plane Surface(61) = {60};
Physical Surface(62) = {55, 57, 59, 61};

//middle
Line Loop(63) = {39, 47, 48, -50, 43, 44}; Plane Surface(64) = {63};
Line Loop(65) = {42, -51, 49, -8}; Plane Surface(66) = {65};
Physical Surface(67) = {64, 66};

//shafts
Line Loop(68) = {36, 25, 18, -26};Plane Surface(69) = {68};
Line Loop(70) = {52, -51, -53, -50};Plane Surface(71) = {70};
Line Loop(72) = {34, 27, 20, -28};Plane Surface(73) = {72};
Physical Surface(74) = {69, 71, 73};

// seams
Line Loop(75) = {32, 38, -44, -43, 52, -42, -7, -21, -20, -19, -18, -17};Plane Surface(76) = {75};
Line Loop(77) = {40, 45, -46, -9, -49, -53, -48, -47}; Plane Surface(78) = {77};
Physical Surface(79) = {76,78};

Point {100} In Surface {78};
Point {101} In Surface {76};
