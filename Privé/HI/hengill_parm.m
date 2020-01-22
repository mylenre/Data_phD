% DEFMOD input parameters

% special features
p.force_bcs = 1;
p.constraint_eqns = 0;

% horizontal layering 
p.n_layers = 3; % number of layers
p.d_layers =  [-1.5; -2]; % interface depths (should be negative, as should be z-coordinates from gmsh)

% keep elements of certain type only
% 4: 4-node tetrahedron
p.element_type = 'tet';

% number of dimensions
p.nDim = 3;

% time-step size
p.dt = 7e5;

% input file
p.mshFile = 'mesh/hng_rotate.msh';

% ouptut file (defmod input file)
p.inpFile = 'input/input.inp';

% inp file parameters

% line 1
p.solver_type = 'implicit-p';
p.guess = 40; % guess for number of elements a node corresponds to
% line2
p.num_materials = 3;
p.num_constrain_eqns = 0;
p.num_traction_eqns = 0;
p.num_sides_with_abcs = 0;
% line3
p.total_time = 3.16e7;
p.output_frequency = 1;
p.output_displacement_style = 1; %(total (1) or delta (0))

% material parameters
p.youngs_modulus = 5e10;
p.poissons_ratio = 0.3;
p.viscosity_coefficient = 1.0e25;
p.power_law_exponent = 0.2;
p.density = 3000;
p.hydraulic_conductivity = [1.0E-14 1E-10 1E-14];
p.biots_coefficient = 0.25;
p.porosity = 0.05;
p.fluid_bulk_modulus = 1.2e9; 

% injection/extraction
p.pump_start = 0;
p.pump_end = 3.16e7;

