w = 1000; // width area
h = -700; // height area
d = 100; // depth seam
t = 3; // thickness seams
l = 100; // distance separation wells
s = 25; // distance separation seams
lc = 20;
lf = t/2;
i = 0;
j = 0;
x = 0 ;
y = 0;
offset=20;
nbBox = 4;
nbpoints=nbBox*4-3;
slope = 10;
lBox=100;
hBox=-50;
dlBox = 50;
dhBox = hBox;

// reservoir 
Point(1) = {0, 0, 0, lc};
Point(2) = {w, 0,  0, lc} ;
Point(3) = {w, h, 0, lc};
Point(4) = {0, h, 0, lc} ;

// mined area

For x In {10:10+nbpoints:4}

  
  Point(x) = {i*dlBox+offset, i*dhBox, 0, lf} ;
  Point(x+1) = {i*dlBox+offset+lBox, i*dhBox, 0, lf} ; 
  Point(x+2) = {i*dlBox+offset+lBox, i*dhBox+hBox, 0, lf} ;
  Point(x+3) = {i*dlBox+offset, i*dhBox+hBox, 0, lf} ;

  i += 1 ;

EndFor

// roadways
Point(200) = {220, -125, 0, lf};
Point(201) = {220, -130,  0, lf} ;
Point(202) = {800, -125, 0, lf};
Point(203) = {800, -130, 0, lf} ;

Point(204) = {270, -175, 0, lf};
Point(205) = {270, -180,  0, lf} ;
Point(206) = {800, -175, 0, lf};
Point(207) = {800, -180, 0, lf} ;

// well
Point(210) = {700, 0, 0, lf};
Point(211) = {708, 0,  0, lf} ;
Point(212) = {700, -300, 0, lf};
Point(213) = {708, -300, 0, lf} ;

// well intersection
Point(220) = {700, -125, 0, lf};
Point(221) = {708, -125,  0, lf} ;
Point(222) = {700, -130, 0, lf};
Point(223) = {708, -130, 0, lf} ;

Point(224) = {700, -175, 0, lf};
Point(225) = {708, -175,  0, lf} ;
Point(226) = {700, -180, 0, lf};
Point(227) = {708, -180, 0, lf} ;


//roadways
Line(34) = {200, 220};
Line(35) = {220, 222};
Line(36) = {222, 201};
Line(37) = {201, 200};
Line Loop(38) = {34, 35, 36, 37};
Plane Surface(39) = {38};

Line(40) = {204, 224};
Line(41) = {224, 226};
Line(42) = {226, 205};
Line(43) = {205, 204};
Line Loop(44) = {40, 41, 42, 43};
Plane Surface(45) = {44};

// mining areas 
Line(6) = {10, 11};
Line(7) = {11, 12};
Line(8) = {12, 14};
Line(9) = {14, 13};
Line(10) = {13, 10};
Line(12) = {12, 15};
Line(13) = {15, 16};
Line(14) = {16, 18};
Line(15) = {18, 17};
Line(16) = {17, 14};
// Line(17) = {16, 19};
// Line(18) = {19, 20};
// Line(19) = {20, 22};
// Line(20) = {22, 21};
// Line(21) = {21, 18};
// Line(22) = {20, 23};
// Line(23) = {23, 24};
// Line(24) = {24, 25};
// Line(25) = {25, 22};

Line Loop(26) = {6, 7, 8, 9, 10};
Plane Surface(27) = {26};
Line Loop(28) = {8, -16, -15, -14, -13, -12};
Plane Surface(29) = {28};
// Line Loop(30) = {14, -21, -20, -19, -18, -17};
// Plane Surface(31) = {30};
// Line Loop(32) = {19, -25, -24, -23, -22};
// Plane Surface(33) = {32};

// mining areas (including roadways)
Line(46) = {16, 19};
Line(47) = {19, 200};
Line(48) = {201, 20};
Line(49) = {20, 22};
Line(50) = {22, 21};
Line(51) = {21, 18};
Line(52) = {20, 23};
Line(53) = {23, 204};
Line(54) = {205, 24};
Line(55) = {24, 25};
Line(56) = {25, 22};
Line Loop(57) = {14, -51, -50, -49, -48, 37, -47, -46};
Plane Surface(58) = {57};
Line Loop(59) = {49, -56, -55, -54, 43, -53, -52};
Plane Surface(60) = {59};

// well
Line(61) = {210, 220};
Line(62) = {222, 224};
Line(63) = {226, 212};
Line(64) = {212, 213};
Line(65) = {213, 227};
Line(66) = {227, 225};
Line(67) = {225, 223};
Line(68) = {223, 221};
Line(69) = {221, 211};
Line(70) = {211, 210};
Line Loop(77) = {70, 61, 35, 62, 41, 63, 64, 65, 66, 67, 68, 69};
Plane Surface(78) = {77};

// reservoir
Line(71) = {1, 10};
Line(72) = {11, 210};
Line(73) = {211, 2};
Line(74) = {2, 3};
Line(75) = {3, 4};
Line(76) = {4, 1};

//top
Line Loop(81) = {72, 61, -34, -47, -46, -13, -12, -7};
Plane Surface(82) = {81};

//middle
Line Loop(83) = {36, 48, 52, 53, 40, -62};
Plane Surface(84) = {83};

//bottom
Line Loop(79) = {71, 6, 72, -70, 73, 74, 75, 76};
Plane Surface(80) = {79,38,44,26,28,57,59,77,81,83};


