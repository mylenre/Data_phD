function prep_defmod(varargin)
% convert .msh files from Gmsh to defmod input format
%
% input is the structure containing parameter values
% either in workspace or as a file
%
% Daniel Juncu 2014


%% load parameters

switch nargin
    case 0
        evalin('base','if exist(''p'',''var'');temp=p; else; error(''no input found''); end;assignin(''caller'',''p'',temp)')
    case 1
        
        if isa(varargin{1},'struct')
            p = varargin{1};
        elseif isa(varargin{1},'char')
            try
                load(varargin{1})
            catch
                load(['parameters/' varargin{1}])
            end
        end        
end

%eval('caller','hengill_layered_and_ellipse_parm')



force_bcs = p.force_bcs;
n_materials = p.n_layers + p.n_ellipsoids + p.n_faults;
n_layers = p.n_layers;
d_layers = p.d_layers;
layer_priority = p.layer_priority;

n_ellipsoids = p.n_ellipsoids;
ellipsoid_x = p.ellipsoid_x;
ellipsoid_y = p.ellipsoid_y;
ellipsoid_z = p.ellipsoid_z;
ellipsoid_center = p.ellipsoid_center;

n_faults = p.n_faults;
fault_corners_lon = p.fault_corners_lon;
fault_corners_lat = p.fault_corners_lat;


element_type = p.element_type;
nDim = p.nDim;
dt = p.dt;
mshFile = p.mshFile;
inpFile = p.inpFile;

solver_type = p.solver_type;
guess = p.guess;
num_constrain_eqns = p.num_constrain_eqns;
num_traction_eqns = p.num_traction_eqns;
num_sides_with_abcs = p.num_sides_with_abcs;
total_time = p.total_time;
output_frequency = p.output_frequency;
output_displacement_style = p.output_displacement_style;

youngs_modulus = p.youngs_modulus;
poissons_ratio = p.poissons_ratio;
viscosity_coefficient = p.viscosity_coefficient;
power_law_exponent = p.power_law_exponent;
density = p.density;

if strcmp(solver_type,'implicit-p')
    hydraulic_conductivity = p.hydraulic_conductivity;
    biots_coefficient = p.biots_coefficient;
    porosity = p.porosity;
    fluid_bulk_modulus = p.fluid_bulk_modulus; 
end

% material parameters for multiple layers

if n_materials > 1
    if length(youngs_modulus) == 1
        youngs_modulus = repmat(youngs_modulus,n_materials,1);
    elseif length(youngs_modulus) ~= n_materials
        error('Youngs modulus: wrong size of input parameter')
    end
    
    if length(poissons_ratio) == 1
        poissons_ratio = repmat(poissons_ratio,n_materials,1);
    elseif length(poissons_ratio) ~= n_materials
        error('Poissons ratio: wrong size of input parameter')
    end
    
    if length(viscosity_coefficient) == 1
        viscosity_coefficient = repmat(viscosity_coefficient,n_materials,1);
    elseif length(viscosity_coefficient) ~= n_materials
        error('Viscosity coefficient: wrong size of input parameter')
    end
    
    if length(power_law_exponent) == 1
        power_law_exponent = repmat(power_law_exponent,n_materials,1);
    elseif length(power_law_exponent) ~= n_materials
        error('Power law exponent: wrong size of input parameter')
    end
    
    if length(density) ==1
        density = repmat(density,n_materials,1);
    elseif length(density) ~= n_materials
        error('Density: wrong size of input parameter')
    end
    
    if strcmp(solver_type,'implicit-p')
        if size(hydraulic_conductivity,1) == 1
            hydraulic_conductivity = repmat(hydraulic_conductivity,n_materials,1);
        elseif size(hydraulic_conductivity,1) ~= n_materials
            error('Hydraulic conductivity: wrong size of input parameter')            
        end
        
        if length(biots_coefficient) == 1
            biots_coefficient = repmat(biots_coefficient,n_materials,1);
        elseif length(biots_coefficient) ~= n_materials
            error('Biots coefficient: wrong size of input parameter')
        end
        
        if length(porosity) == 1
            porosity = repmat(porosity,n_materials,1);
        elseif length(porosity) ~= n_materials
            error('Porosity: wrong size of input parameter')
        end
        
        if length(fluid_bulk_modulus) == 1
            fluid_bulk_modulus = repmat(fluid_bulk_modulus,n_materials,1);
        elseif length(fluid_bulk_modulus) ~= n_materials
            error('Fluid bulk modulus: wrong size of input parameter')
        end
    end
end

if n_ellipsoids > 1
    if length(ellipsoid_x) == 1
        ellipsoid_x = repmat(ellipsoid_x,n_ellipsoids,1);
    end
    
    if length(ellipsoid_y) == 1
        ellipsoid_y = repmat(ellipsoid_y,n_ellipsoids,1);
    end
    
    if length(ellipsoid_z) == 1
        ellipsoid_z = repmat(ellipsoid_z,n_ellipsoids,1);
    end
    
    if size(ellipsoid_center,1) == 1
        ellipsoid_center = repmat(ellipsoid_center,n_ellipsoids,1);
    end
    
end
    


if force_bcs 
    % injection/extraction
    pump_start = p.pump_start;
    pump_end = p.pump_end;
    pump_inc = p.pump_increment;
end

% catch some problems with the input

if n_layers > 1 && n_layers ~= (length(d_layers) + 1)
    error('INPUT ERROR: Wrong number of layers?')
end
    
% if n_layers + n_ellipsoid ~= n_materials
%     error('INPUT ERROR: number of material/layers/ellipsoids problem')
% end


%% load .msh
fid = fopen(mshFile,'r');
msh = textscan(fid,'%f%f%f%f%f%f%f%f%f','CommentStyle','$');
fclose(fid);

if strcmp(element_type,'tet')
    elmnt_no = 4;
    elmnt_name = 'Tetrahedrons';
    nodes_per_elmnt = 4;
else
    error('wrong element type');
end

n_nodes = msh{1,1}(2);
n_elements = msh{1,1}(n_nodes+3);

%% get elements and their corresponding nodes

for i = 1:length(msh)
    elements(:,i) = msh{1,i}(n_nodes+4:end);
end


% remove wrong element types
elements((elements(:,2) ~= elmnt_no),:) = [];
p.msh=msh;

% check in which material layer the nodes are
node_material = ones(n_nodes,1);

node_depths = msh{1,4}(3:n_nodes+2);
d_layers = [0; d_layers; min(node_depths)];


if n_layers > 1
    for i = 1:n_layers                 
        inLayer = (node_depths < d_layers(i) & node_depths >= d_layers(i+1)); 
        node_material(inLayer) = i;
    end
end

if any(n_ellipsoids)
    load('mesh/theta') 
    load('mesh/origin')
    R = [cos(theta) -sin(theta); sin(theta) cos(theta)];
    
    ellipsoid_center_local = llh2local(ellipsoid_center',origin);
    ellipsoid_center_local_rot = ellipsoid_center_local' * R;
    ellipsoid_center_local_rot = [ellipsoid_center_local_rot ellipsoid_center(:,3)];
    
    for i = 1:n_ellipsoids
        inBody = inEllipsoid(msh{1,2}(3:n_nodes+2),msh{1,3}(3:n_nodes+2),msh{1,4}(3:n_nodes+2),ellipsoid_x(i),ellipsoid_y(i),ellipsoid_z(i),ellipsoid_center_local_rot(i,:));        
        node_material(inBody) = n_layers + i;
    end
    
end

if any(layer_priority)
    for i = 1:length(layer_priority)
        tmp_layer_id = layer_priority(i); 
        
        if tmp_layer_id == 1
            inLayer = (node_depths <= d_layers(tmp_layer_id) & node_depths >= d_layers(tmp_layer_id+1)); 
        else
            inLayer = (node_depths < d_layers(tmp_layer_id) & node_depths >= d_layers(tmp_layer_id+1)); 
        end
        
        node_material(inLayer) = tmp_layer_id;
    end
end   


% nodes within fault structure
node_x = msh{1,2}(3:n_nodes+2);
node_y = msh{1,3}(3:n_nodes+2);


if any(n_faults)    
    fault_local = llh2local([fault_corners_lon; fault_corners_lat; zeros(size(fault_corners_lat))],origin);
    fault_local_rot = fault_local' * R;    
    
    inFault = inpolygon(node_x,node_y, fault_local_rot(:,1),fault_local_rot(:,2));        
    node_material(inFault) = n_layers + n_ellipsoids +1;    
end
        
        
% write the associated nodes for each element
element_nodes = ones(length(elements),5);
element_nodes(:,1:nodes_per_elmnt) = elements(:,end-nodes_per_elmnt+1:end);

% associate element with material layer
element_nodes(:,nodes_per_elmnt+1) = node_material(element_nodes(:,1));


%% NODES
switch solver_type
       
    case 'implicit-p'
        nodes = ones(n_nodes,7);
        
        for i = 1:3
            nodes(:,i) = msh{1,i+1}(3:n_nodes+2);
        end
        
                
        % boundaries       
        
        % fix boundaries
        x_Bnd = [min(nodes(:,1)) max(nodes(:,1))];
        y_Bnd = [min(nodes(:,2)) max(nodes(:,2))];
        z_Bnd = [max(nodes(:,3)) min(nodes(:,3))];
        
        % adjust boundary displacement BC's        
        % 0 - Fixed     1 - Free
        nodes((nodes(:,3) == z_Bnd(1)),nDim+1:nDim+nDim) = 1;
        nodes((nodes(:,3) == z_Bnd(2)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,2) == y_Bnd(1)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,2) == y_Bnd(2)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,1) == x_Bnd(1)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,1) == x_Bnd(2)),nDim+1:nDim+nDim) = 0;
        
        % pressure BC's
        % 0 - Flow      1 - No Flow
        nodes((nodes(:,3) == z_Bnd(1)),2*nDim+1) = 1;
        nodes((nodes(:,3) == z_Bnd(2)),2*nDim+1) = 0;
        nodes((nodes(:,2) == y_Bnd(1)),2*nDim+1) = 0;
        nodes((nodes(:,2) == y_Bnd(2)),2*nDim+1) = 0;
        nodes((nodes(:,1) == x_Bnd(1)),2*nDim+1) = 0;
        nodes((nodes(:,1) == x_Bnd(2)),2*nDim+1) = 0;
        
        
    case 'implicit'
        nodes = zeros(n_nodes,6);
        
        for i = 1:3
            nodes(:,i) = msh{1,i+1}(3:n_nodes+2);
        end
        
        % boundaries
        % fix boundaries
        x_Bnd = [min(nodes(:,1)) max(nodes(:,1))];
        y_Bnd = [min(nodes(:,2)) max(nodes(:,2))];
        z_Bnd = [max(nodes(:,3)) min(nodes(:,3))];
        
        % adjust boundary conditions
        nodes((nodes(:,3) == z_Bnd(1)),nDim+1:nDim+nDim) = 1;
        nodes((nodes(:,3) == z_Bnd(2)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,2) == y_Bnd(1)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,2) == y_Bnd(2)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,1) == x_Bnd(1)),nDim+1:nDim+nDim) = 0;
        nodes((nodes(:,1) == x_Bnd(2)),nDim+1:nDim+nDim) = 0;
        
end



%% well locations

if force_bcs
    %holeFile = 'mesh/data/pumping_hh_full.csv';
    load('mesh/holeFile');
    holeFile = ['mesh/',holeFile];
    
    BH_fsize = getFileWidth(holeFile,2);    
    BH_formatString = ['%5s',repmat('%f',1,BH_fsize)];
    
    fid = fopen(holeFile,'r');        
    holes = textscan(fid,BH_formatString,'headerlines',2,'whitespace','\t');
    fclose(fid);
    
    load('mesh/holeCoords');
    
    nForceBCs = size(holeCoords,1);
    

    
    % fid = fopen('pumps.loc','w+');
    % for i = 1:length(holeCoords)
    %     varName = strcat('Point(',num2str(i+8),')');
    %     fprintf(fid,'%s = { %6.4f, %6.4f, %6.4f, lc} ;\n', varName,holeCoords(i,:));
    % end    
    
    
    % total length of pumping force BC's
    nYrs = BH_fsize - 4;
    nHoles = size(holeCoords,1);
    nForceBCs = nHoles*nYrs;
    
    holeNodes = zeros(nHoles,1);    
    
    holeCoords
    
    % finde nodes closest to the hole coordinates
    for i = 1:nHoles
        distance = sqrt((holeCoords(i,1) - nodes(:,1)).^2 + (holeCoords(i,2) - nodes(:,2)).^2 + ...
            (holeCoords(i,3) - nodes(:,3)).^2);              
        holeNodes(i) = find(distance==min(distance)); 
        %min(distance)
    end
    p.holeNodes = holeNodes;
    holeNodes = repmat(holeNodes,nYrs,1);
        
    holeData = zeros(nForceBCs,7);
    holeData(:,1) = holeNodes;
    
    for i = 1:nYrs
        
        i1 = 1 + nHoles * (i-1);
        i2 = nHoles * i;
        
        % pump rates: convert kg/yr to m^3/s and multiply by the timestep
        holeData(i1:i2,5) = 1e6*holes{1,4+i} * (1/(24*3600*365.25)) * dt;
        holeData(i1:i2,6) = (i-1) * pump_inc; % start of pumping time
        holeData(i1:i2,7) = i*pump_inc; % end of pumping time
        
    end
    
    %noPumping = holeData(:,5)==0
    holeData(holeData(:,5)==0,:) = [];
    nForceBCs = size(holeData,1);
    
    
else
    nForceBCs = 0;

end
    

%% check for unused nodes


%check if all nodes are used in elements
unused_nodes = ismember([1:length(nodes)],element_nodes);

if any(find(unused_nodes==0))
    fprintf('WARNING: Node %u unused\n',find(unused_nodes==0))
end

% THIS WAS A MILLION TIMES SLOWER
% for i = 1:100%length(nodes)%     
%     if ~any(find(element_nodes(:,:)==i))
%         fprintf('WARNING: Node %u unused\n',i)
%     end
% end




%% write data
%dlmwrite('mesh.out',element_nodes,' ');
%dlmwrite('mesh.out',nodes,'delimiter',' ','-append');

if force_bcs
    
    fid = fopen('mesh/pumps.out','w+');
    for i = 1:nForceBCs
        fprintf(fid,'%u %u %u %u %3.2e %u %3.2e\n', holeData(i,:));
    end
    
end

% create .inp file for defmod
fid = fopen(inpFile,'w+');

fprintf(fid,'%s %s %u ! solver_type element_type guess_no_of_elements_per_node\n\n%u %u %u %u %u %u %u ! no_of_elements no_of_nodes\n\n%4.3e %3.2e %u %u\n\n',...
    solver_type,element_type,guess,length(elements),...
    n_nodes, n_materials, num_constrain_eqns, nForceBCs, num_traction_eqns,...
    num_sides_with_abcs,total_time,dt,output_frequency,output_displacement_style);

for i = 1:length(element_nodes)
    fprintf(fid,'%u %u %u %u %u\n', element_nodes(i,:)); % element_node_1  element_node_2  element_node_3  element_node_4  material_id
end

switch solver_type
    
    case 'implicit-p'
        
        for i = 1:length(nodes)
                fprintf(fid,'%7.4f %7.4f %6.4f %u %u %u %u\n', nodes(i,:)); % nodes:  x-coord. / y-coord. / z. coord / x BC / y BC / z BC / p BC (a bc flag of 0 means fixed and 1 means free)
        end
        
        for i = 1:n_materials
            
            fprintf(fid,'\n%2.1e %3.2f %3.2e %3.2f %5.1f %2.1e %2.1e %2.1e %3.2f %3.2f %2.1e',...
                youngs_modulus(i), poissons_ratio(i), viscosity_coefficient(i), power_law_exponent(i),...
                density(i), hydraulic_conductivity(i,:), biots_coefficient(i), porosity(i), fluid_bulk_modulus(i));  
            
        end
        
        fprintf(fid,'\n\n');
        
        if force_bcs
            for i = 1:nForceBCs
                fprintf(fid,'%u %u %u %u %4.3e %4.3e %4.3e\n', holeData(i,:));
            end
        end
        
    case 'implicit'
        
        for i = 1:length(nodes)
            fprintf(fid,'%7.4f %7.4f %6.4f %u %u %u \n', nodes(i,:)); % nodes:  x-coord. / y-coord. / z. coord / x BC / y BC / z BC  (a bc flag of 0 means fixed and 1 means free)
        end
        
        
        for i = 1:n_materials
            fprintf(fid,'\n%2.1e %3.2f %3.2e %3.2f %5.1f ',...
                youngs_modulus(i), poissons_ratio(i), viscosity_coefficient(i), power_law_exponent(i), ...
                density(i));  
        end
        
        fprintf(fid,'\n\n');        
   
end

% if force_bcs
%     figure(1)
%     plot(holeCoords(:,1),holeCoords(:,2),'.')
% end

if n_materials > 1
    figure(1)
    scatter3(nodes(:,1),nodes(:,2),nodes(:,3),5,node_material)
end

p.n_nodes = n_nodes;
p.n_elements = length(elements);
p.node_material = node_material;
p.element_nodes = element_nodes;

assignin('base','p',p)

% figure(2)
% scatter3(holeCoords(:,1),holeCoords(:,2),holeCoords(:,3),5)

fprintf('============== Defmod input file has been created ============\n')
fprintf('Number of Elements: %u\n',length(elements))
fprintf('Number of Nodes: %u\n',n_nodes)
fprintf('Time-step (seconds): %2.1e\n', dt)
fprintf('Element type: %s\n',elmnt_name)
fprintf('============================================================\n')
