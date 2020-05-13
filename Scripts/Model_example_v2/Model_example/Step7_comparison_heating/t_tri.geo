cl=0.1;
Point(1)={0,0,0,cl};
Point(2)={2,0,0,cl};
Point(3)={0,0,2.5,cl};
Point(4)={1,0,2.5,cl};
Point(5)={2,0,2.5,cl};
Line(1)={1,2};
Line(2)={2,5};
Line(3)={5,4};
Line(4)={4,3};
Line(5)={3,1};
Line Loop(1)={1,2,3,4,5};

Point(11)={0,0,5,cl};
Point(12)={2,0,5,cl};
Line(11)={11,12};
Line(12)={12,5};
Line(14)={3,11};
Line Loop(11)={11,12,3,4,14};

Plane Surface(1)={1};
Plane Surface(11)={11};
Physical Surface(1)={1};
Physical Surface(2)={11};