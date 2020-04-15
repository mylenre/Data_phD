/*
* 06-Apr-2015
*/
lcf = 0.15;
lcc = 4.0;

xSize = 40.0;
ySize = 40.0;
zSize = -20.0;

Point(1) =  {0., 0., 0., lcc};
Point(2) = {xSize, 0.,  0., lcc} ;
Point(3) = {xSize, ySize, 0., lcc} ;
Point(4) = {0.,  ySize, 0., lcc} ;


// locations for mesh refinement
Point(11) = { 6.7816, 24.5825, -1.5000, lcf} ;
Point(12) = { 7.3148, 33.0360, -1.5000, lcf} ;
Point(13) = { 6.7816, 24.5825, 0, lcf/2.} ;
Point(14) = { 7.3148, 33.0360, 0, lcf/2.} ;
Point(15) = { 6.7816, 24.5825, 0.1, lcf} ;
Point(16) = { 7.3148, 33.0360, 0.1, lcf} ;
Point(17) = { 6.7816, 24.5825, 0.2, lcf} ;
Point(18) = { 7.3148, 33.0360, 0.2, lcf} ;
Point(19) = { 6.7816, 24.5825, 0.3, lcf} ;
Point(20) = { 7.3148, 33.0360, 0.3, lcf} ;
Point(21) = { 7.0482, 28.80925, 0, lcf/2. } ;
Point(22) = { 7.0482, 28.80925, 0.1, lcf} ;
Point(23) = { 7.0482, 28.80925, 0.2, lcf} ;
Point(24) = { 7.0482, 28.80925, 0.3, lcf} ;

//connect corner points
Line(1) = {1,2} ;
Line(2) = {3,2} ;
Line(3) = {3,4} ;
Line(4) = {4,1} ;

//surface areas
Line Loop(1) = {4,1,-2,3} ;
Plane Surface(1) = {1};

Extrude {0,0,zSize} {
    Surface{1};
}

Physical Volume(1) = {1};

// refine mesh locally using attractor field
Field[1] = Attractor;
Field[1].NodesList = {11:24};
Field[2] = Threshold;
Field[2].IField = 1;
Field[2].LcMin = lcf;
Field[2].LcMax = lcc;
Field[2].DistMin = 2.;
Field[2].DistMax = 15.;

// Use minimum of all the fields as the background field
Field[3] = Min;
Field[3].FieldsList = {2};
Background Field = 3;

// Do not extend the elements sizes from the boundary inside the domain
Mesh.CharacteristicLengthExtendFromBoundary = 1;

Rotate {{ 0, 0, 1}, { 0, 0, 0}, Pi*30.0/180.} {
    Volume{1};
}
