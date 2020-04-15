//

lcf = 1.;
lcc = 5.;

z1=-2.995;
z2=-3.005;

radius=5.;

// cell size factors
d1 = 1.; // phi direction
d2 = 1./6.; // r direction

cylSize = (0.5)^0.5*radius;
//cylYSize = ;
//cylZSize = -10.0;

domXSize = 60.0;
domYSize = 60.0;
domZSize = -20.0;

/// TOP OF DOMAIN
// central point
Point(1) =  {0., 0., 0., lcc};

// cylinder points
Point(2) = {cylSize, cylSize,  0., lcc} ;
Point(3) = {-cylSize, cylSize, 0., lcc} ;
Point(4) = {-cylSize,  -cylSize, 0., lcc} ;
Point(5) = {cylSize,  -cylSize, 0., lcc} ;

// outer cylinder points
Point(6) = {domXSize/2., domYSize/2.,  0., lcc} ;
Point(7) = {-domXSize/2., domYSize/2., 0., lcc} ;
Point(8) = {-domXSize/2.,  -domYSize/2., 0., lcc} ;
Point(9) = {domXSize/2.,  -domYSize/2., 0., lcc} ;

// Inner circle
Circle(1) = {2, 1, 3};
Circle(2) = {3, 1, 4};
Circle(3) = {4, 1, 5};
Circle(4) = {5, 1, 2};
// outer box
Line(5) = {6, 7};
Line(6) = {7, 8};
Line(7) = {8, 9};
Line(8) = {9, 6};
// connection lines
Line(9) = {2,6};
Line(10) = {3,7};
Line(11) = {4,8};
Line(12) = {5,9};


/// TOP OF CYLINDER
// central point
Point(11) =  {0., 0., z1, lcc};

// cylinder points
Point(12) = {cylSize, cylSize, z1, lcc} ;
Point(13) = {-cylSize, cylSize, z1, lcc} ;
Point(14) = {-cylSize,  -cylSize, z1, lcc} ;
Point(15) = {cylSize,  -cylSize, z1, lcc} ;


// outer cylinder points
Point(16) = {domXSize/2., domYSize/2.,  z1, lcc} ;
Point(17) = {-domXSize/2., domYSize/2., z1, lcc} ;
Point(18) = {-domXSize/2.,  -domYSize/2.,z1, lcc} ;
Point(19) = {domXSize/2.,  -domYSize/2., z1, lcc} ;

// Inner circle
Circle(21) = {12, 11, 13};
Circle(22) = {13, 11, 14};
Circle(23) = {14, 11, 15};
Circle(24) = {15, 11, 12};
// outer circle
Line(25) = {16, 17};
Line(26) = {17, 18};
Line(27) = {18, 19};
Line(28) = {19, 16};
// connection lines
Line(29) = {12,16};
Line(30) = {13,17};
Line(31) = {14,18};
Line(32) = {15,19};

/// BOTTOM OF CYLINDER
// central point
Point(21) =  {0., 0., z2, lcc};

// cylinder points
Point(22) = {cylSize, cylSize,  z2, lcc} ;
Point(23) = {-cylSize, cylSize, z2, lcc} ;
Point(24) = {-cylSize,  -cylSize, z2, lcc} ;
Point(25) = {cylSize,  -cylSize, z2, lcc} ;

// outer cylinder points
Point(26) = {domXSize/2., domYSize/2.,  z2, lcc} ;
Point(27) = {-domXSize/2., domYSize/2., z2, lcc} ;
Point(28) = {-domXSize/2.,  -domYSize/2., z2, lcc} ;
Point(29) = {domXSize/2.,  -domYSize/2., z2, lcc} ;

// Inner circle
Circle(41) = {22, 21, 23};
Circle(42) = {23, 21, 24};
Circle(43) = {24, 21, 25};
Circle(44) = {25, 21, 22};
// outer box
Line(45) = {26, 27};
Line(46) = {27, 28};
Line(47) = {28, 29};
Line(48) = {29, 26};
// connection lines
Line(49) = {22,26};
Line(50) = {23,27};
Line(51) = {24,28};
Line(52) = {25,29};


/// BOTTOM OF DOMAIN
// central point
Point(31) =  {0., 0., domZSize, lcc};

// cylinder points
Point(32) = {cylSize, cylSize, domZSize, lcc} ;
Point(33) = {-cylSize, cylSize, domZSize, lcc} ;
Point(34) = {-cylSize,  -cylSize, domZSize, lcc} ;
Point(35) = {cylSize,  -cylSize, domZSize, lcc} ;


// outer cylinder points
Point(36) = {domXSize/2., domYSize/2.,  domZSize, lcc} ;
Point(37) = {-domXSize/2., domYSize/2., domZSize, lcc} ;
Point(38) = {-domXSize/2.,  -domYSize/2.,domZSize, lcc} ;
Point(39) = {domXSize/2.,  -domYSize/2., domZSize, lcc} ;

// Inner circle
Circle(61) = {32, 31, 33};
Circle(62) = {33, 31, 34};
Circle(63) = {34, 31, 35};
Circle(64) = {35, 31, 32};
// outer circle
Line(65) = {36, 37};
Line(66) = {37, 38};
Line(67) = {38, 39};
Line(68) = {39, 36};
// connection lines
Line(69) = {32,36};
Line(70) = {33,37};
Line(71) = {34,38};
Line(72) = {35,39};

/// VERTICAL CONNECTIONS
Line(81) = {2, 12}; Line(91) = {12, 22}; Line(101) = {22, 32};
Line(82) = {3, 13}; Line(92) = {13, 23}; Line(102) = {23, 33};
Line(83) = {4, 14}; Line(93) = {14, 24}; Line(103) = {24, 34};
Line(84) = {5, 15}; Line(94) = {15, 25}; Line(104) = {25, 35};
Line(85) = {6, 16}; Line(95) = {16, 26}; Line(105) = {26, 36};
Line(86) = {7, 17}; Line(96) = {17, 27}; Line(106) = {27, 37};
Line(87) = {8, 18}; Line(97) = {18, 28}; Line(107) = {28, 38};
Line(88) = {9, 19}; Line(98) = {19, 29}; Line(108) = {29, 39};


/// SURFACES
// Inner circle
Line Loop(1) = {1, 2, 3, 4}; Surface(2) = {1}; 
Line Loop(3) = {21, 22, 23, 24}; Surface(4) = {3}; 
Line Loop(5) = {41, 42, 43, 44}; Surface(6) = {5}; 
Line Loop(7) = {61, 62, 63, 64}; Surface(8) = {7}; 
// outer areas
// top of domain
Line Loop(9) = {9, 5, -10, -1}; Surface(10) = {9};
Line Loop(11) = {10, 6, -11, -2}; Surface(12) = {11};
Line Loop(13) = {11, 7, -12, -3}; Surface(14) = {13};
Line Loop(15) = {12, 8, -9, -4}; Surface(16) = {15};
// top of cylinder
Line Loop(17) = {29, 25, -30, -21}; Surface(18) = {17};
Line Loop(19) = {30, 26, -31, -22}; Surface(20) = {19};
Line Loop(21) = {31, 27, -32, -23}; Surface(22) = {21};
Line Loop(23) = {32, 28, -29, -24}; Surface(24) = {23};
// bottom of cylinder
Line Loop(25) = {49, 45, -50, -41}; Surface(26) = {25};
Line Loop(27) = {50, 46, -51, -42}; Surface(28) = {27};
Line Loop(29) = {51, 47, -52, -43}; Surface(30) = {29};
Line Loop(31) = {52, 48, -49, -44}; Surface(32) = {31};
// bottom of domain
Line Loop(33) = {69, 65, -70, -61}; Surface(34) = {33};
Line Loop(35) = {70, 66, -71, -62}; Surface(36) = {35};
Line Loop(37) = {71, 67, -72, -63}; Surface(38) = {37};
Line Loop(39) = {72, 68, -69, -64}; Surface(40) = {39};

// areas on side of inner cylinder (top part)
Line Loop(41) = {1, 82, -21, -81}; Surface(42) = {41};
Line Loop(43) = {2, 83, -22, -82}; Surface(44) = {43};
Line Loop(45) = {3, 84, -23, -83}; Surface(46) = {45};
Line Loop(47) = {4, 81, -24, -84}; Surface(48) = {47};
// areas on side of inner cylinder (cylinder part)
Line Loop(49) = {21, 92, -41, -91}; Surface(50) = {49};
Line Loop(51) = {22, 93, -42, -92}; Surface(52) = {51};
Line Loop(53) = {23, 94, -43, -93}; Surface(54) = {53};
Line Loop(55) = {24, 91, -44, -94}; Surface(56) = {55};
// areas on side of inner cylinder (bottom part)
Line Loop(57) = {41, 102, -61, -101}; Surface(58) = {57};
Line Loop(59) = {42, 103, -62, -102}; Surface(60) = {59};
Line Loop(61) = {43, 104, -63, -103}; Surface(62) = {61};
Line Loop(63) = {44, 101, -64, -104}; Surface(64) = {63};

// areas on outer sides (top part)
Line Loop(65) = {5, 86, -25, -85}; Surface(66) = {65};
Line Loop(67) = {6, 87, -26, -86}; Surface(68) = {67};
Line Loop(69) = {7, 88, -27, -87}; Surface(70) = {69};
Line Loop(71) = {8, 85, -28, -88}; Surface(72) = {71};
// areas on outer sides (cylinder part)
Line Loop(73) = {25, 96, -45, -95}; Surface(74) = {73};
Line Loop(75) = {26, 97, -46, -96}; Surface(76) = {75};
Line Loop(77) = {27, 98, -47, -97}; Surface(78) = {77};
Line Loop(79) = {28, 95, -48, -98}; Surface(80) = {79};
// areas on outer sides (bottom part)
Line Loop(81) = {45, 106, -65, -105}; Surface(82) = {81};
Line Loop(83) = {46, 107, -66, -106}; Surface(84) = {83};
Line Loop(85) = {47, 108, -67, -107}; Surface(86) = {85};
Line Loop(87) = {48, 105, -68, -108}; Surface(88) = {87};

// connector areas (top part)
Line Loop(89) = {9, 85, -29, -81}; Surface(90) = {89};
Line Loop(91) = {10, 86, -30, -82}; Surface(92) = {91};
Line Loop(93) = {11, 87, -31, -83}; Surface(94) = {93};
Line Loop(95) = {12, 88, -32, -84}; Surface(96) = {95};
// connector areas (cylinder part)
Line Loop(97) = {29, 95, -49, -91}; Surface(98) = {97};
Line Loop(99) = {30, 96, -50, -92}; Surface(100) = {99};
Line Loop(101) = {31, 97, -51, -93}; Surface(102) = {101};
Line Loop(103) = {32, 98, -52, -94}; Surface(104) = {103};
// connector areas (bottom part)
Line Loop(105) = {49, 105, -69, -101}; Surface(106) = {105};
Line Loop(107) = {50, 106, -70, -102}; Surface(108) = {107};
Line Loop(109) = {51, 107, -71, -103}; Surface(110) = {109};
Line Loop(111) = {52, 108, -72, -104}; Surface(112) = {111};

// Volumes (top)
Surface Loop(113) = {10, 90, 66, 18, 92, 42}; Volume(114) = {113};
Surface Loop(115) = {12, 92, 68, 20, 94, 44}; Volume(116) = {115};
Surface Loop(117) = {14, 94, 70, 22, 96, 46}; Volume(118) = {117};
Surface Loop(119) = {16, 96, 72, 24, 90, 48}; Volume(120) = {119};
Surface Loop(121) = {2, 4, 42, 44, 46, 48}; Volume(122) = {121};
// Volumes (cylinder slice)
Surface Loop(123) = {18, 98, 74, 26, 100, 50}; Volume(124) = {123};
Surface Loop(125) = {20, 100, 76, 28, 102, 52}; Volume(126) = {125};
Surface Loop(127) = {22, 102, 78, 30, 104, 54}; Volume(128) = {127};
Surface Loop(129) = {24, 104, 80, 32, 98, 56}; Volume(130) = {129};
Surface Loop(131) = {4, 6, 50, 52, 54, 56}; Volume(132) = {131};
// Volumes (bottom slice)
Surface Loop(133) = {26, 106, 82, 34, 108, 58}; Volume(134) = {133};
Surface Loop(135) = {28, 108, 84, 36, 110, 60}; Volume(136) = {135};
Surface Loop(137) = {30, 110, 86, 38, 112, 62}; Volume(138) = {137};
Surface Loop(139) = {32, 112, 88, 40, 106, 64}; Volume(140) = {139};
Surface Loop(141) = {6, 8, 58, 60, 62, 64}; Volume(142) = {141};

//// LINE RESOLUTIONS
n1 = domXSize/2./d1; // resolution in phi direction
n2 = domXSize/4./d2; // resolution in r direction
nzt = 15; // 18 before
nzs = 5;
nzb = 15;

// Inner circle
Transfinite Line {1, 2, 3, 4} = n1;
Transfinite Line {21, 22, 23, 24} = n1;
Transfinite Line {41, 42, 43, 44} = n1;
Transfinite Line {61, 62, 63, 64} = n1;
// Outer Limit
Transfinite Line {5, 6, 7, 8} = n1;
Transfinite Line {25, 26, 27, 28} = n1;
Transfinite Line {45, 46, 47, 48} = n1;
Transfinite Line {65, 66, 67, 68} = n1;
// Connecting lines
Transfinite Line {9, 10, 11, 12, 29, 30, 31, 32, 49, 50, 51, 52, 69, 70, 71, 72} = n2 Using Progression 1.1; // was 1.1 before
// vertical lines
//top
Transfinite Line {81, 82, 83, 84, 85, 86, 87, 88} = nzt Using Bump 0.01; // was .01
//slice
Transfinite Line {91, 92, 93, 94, 95, 96, 97, 98} = nzs Using Bump 1.;
// bottom
Transfinite Line {101,102, 103, 104, 105, 106, 107, 108} = nzb Using Progression 1.6; // was 1.6

Transfinite Surface "*";
Recombine Surface "*";
Transfinite Volume "*";

//Physical Surface("top") = {2, 10, 12, 14, 16};
//Physical Surface("topofcyl") = {4, 18, 20, 22, 24};
//Physical Surface("botofcyl") = {6, 26, 28, 30, 32};
//Physical Surface("bottom") = {8, 32, 34, 36, 38};
//Physical Surface("sides") = {30, 32, 34, 36};
Physical Volume("all") = {114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142};


