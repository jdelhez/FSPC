//+
d = 0.1;
//+
Point(1) = {0, 0, 0, d};
//+
Point(2) = {6, 0, 0, d};
//+
Point(3) = {6, 1, 0, d};
//+
Point(4) = {0, 1, 0, d};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Surface(1) = {1};
//+
Physical Curve("Boundary") = {1, 3};
//+
Physical Curve("Inlet") = {4};
//+
Physical Curve("Outlet") = {2};
//+
Physical Surface("Fluid") = {1};
//+
Physical Curve("FSInterface") = {1,3}; ??? 
//+
Transfinite Surface{1};
