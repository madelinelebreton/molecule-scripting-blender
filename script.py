#------------------------------------------------------------#
#       Script for building molecules in Blender             #
#       Madeline LeBreton, adapted from Jakob Kibsgaard      #
#------------------------------------------------------------#

import bpy
import numpy
import math
import numpy as np
import re
import csv

#------------------------------------------------------------#  
# write the correct path to your molecule file
file = open('path/to/molecule.sdf', 'r')mol=file.read()

# Clear old objects
context = bpy.context
scene = context.scene

for c in scene.collection.children:
    scene.collection.children.unlink(c)
 
for block in bpy.data.collections:
    if block.users == 0:
        bpy.data.collections.remove(block)

for block in bpy.data.objects:
    if block.users == 0:
        bpy.data.objects.remove(block)

for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)

for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

for block in bpy.data.textures:
    if block.users == 0:
        bpy.data.textures.remove(block)

for block in bpy.data.images:
    if block.users == 0:
        bpy.data.images.remove(block)
        
#------------------------------------------------------------#    
# Support functions

def makeCylinder(startV,endV):

  dx = endV[0] - startV[0]
  dy = endV[1] - startV[1]
  dz = endV[2] - startV[2]    
  dist = math.sqrt(dx**2 + dy**2 + dz**2)

  bpy.ops.mesh.primitive_cylinder_add(
      vertices=64,
      radius = 0.2, 
      depth = dist,
      location = (dx/2 + startV[0], dy/2 + startV[1], dz/2 + startV[2])   
  ) 

  phi = math.atan2(dy, dx) 
  theta = math.acos(dz/dist) 

  bpy.context.object.rotation_euler[1] = theta 
  bpy.context.object.rotation_euler[2] = phi 

def makeHalfCylinder(startV,endV):
    diffV = (endV)-(startV)
    return makeCylinder(startV,startV+diffV/2)

# Return the rotation matrix associated with counterclockwise rotation about the given axis by theta radians.
def rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2)
    b, c, d = -axis * math.sin(theta / 2)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

#------------------------------------------------------------#
# Open .mol file 
rows = mol.split('\n')
count_line = rows[3].strip() # Counts line
counts = re.split('\s+', count_line.strip())
count_atoms = int(counts[0])
count_bonds = int(counts[1])
atoms = rows[4:4+count_atoms]
bonds = rows[4+count_atoms:4+count_atoms+count_bonds]

# Create lists for atoms and bonds
atomV = []
atomName = []
bondV1 = []
bondV2 = []
bondName1 = []
bondName2 = []
bondType = []

# Center molecule in (0,0,0)
x_offset = float(re.split('\s+',atoms[0].strip())[0])
y_offset = float(re.split('\s+',atoms[0].strip())[1])
z_offset = float(re.split('\s+',atoms[0].strip())[2])

# Append atoms to list
for i in atoms:
    fields = re.split('\s+', i.strip())
    atomV.append([float(fields[0])-x_offset ,float(fields[2])-z_offset ,float(fields[1])-y_offset]*1)
    atomName.append(fields[3])

# Rotate atoms 
atomV = np.dot(atomV, rotation_matrix([1,0,0], np.radians(90)))

# Append bonds to list
for i in bonds:
    fields = re.split('\s+', i.strip())
    id1 = int(fields[0])-1
    id2 = int(fields[1])-1
    bondV1.append(atomV[id1])
    bondV2.append(atomV[id2])
    bondName1.append(atomName[id1])
    bondName2.append(atomName[id2])
    bondType.append(int(fields[2]))
 
#------------------------------------------------------------#
# Plot to Blender 
bondV1 = np.asarray(bondV1)
bondV2 = np.asarray(bondV2)

# Make collections for atoms and bonds
AtomsCollection = bpy.data.collections.new('AtomsCollection')
bpy.context.scene.collection.children.link(AtomsCollection)
BondsCollection = bpy.data.collections.new('BondsCollection')
bpy.context.scene.collection.children.link(BondsCollection)


for i in range(len(atomV)):
# Make atoms as spheres
    if atomName[i] == 'H':
        r=.75
    else:
        r=1
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, location=atomV[i], radius=.75*r)
    atom = bpy.context.selected_objects[0]
    atom.modifiers.new(name="Subsurface", type='SUBSURF')
    atom.modifiers["Subsurface"].render_levels = 4
    
    # Add material according to element
    mat = bpy.data.materials.get(atomName[i])
    atom.data.materials.append(mat)
    
    atom.name = atomName[i]+'_atom'
    bpy.context.scene.collection.objects.unlink(atom)
    AtomsCollection.objects.link(atom) 
    
# Make bonds
for i in range(len(bondV1)):
    VectorDiff = bondV2[i]-bondV1[i]
    # Use cross product to make vector perpendicular to bond direction and z-axis
    delta = np.cross([VectorDiff[0],VectorDiff[1],VectorDiff[2]],[0,0,1])
    norm = np.linalg.norm(delta)
    delta = delta/norm*0.15
    
    for j in range(bondType[i]): 
        # Make first half of bond
        makeHalfCylinder(bondV1[i]-delta*(bondType[i]-1-2*j),bondV2[i]-delta*(bondType[i]-1-2*j))
        bond = bpy.context.selected_objects[0]
        mat = bpy.data.materials.get(bondName1[i])
        bond.data.materials.append(mat)       
        bond.name = bondName1[i]+'_bond'
        bpy.context.scene.collection.objects.unlink(bond)    
        BondsCollection.objects.link(bond) 
        # Make second half of bond    
        makeHalfCylinder(bondV2[i]-delta*(bondType[i]-1-2*j),bondV1[i]-delta*(bondType[i]-1-2*j))
        bond = bpy.context.selected_objects[0]
        mat = bpy.data.materials.get(bondName2[i])
        bond.data.materials.append(mat)
        bond.name = bondName2[i]+'_bond'
        bpy.context.scene.collection.objects.unlink(bond)    
        BondsCollection.objects.link(bond)

