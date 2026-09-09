# Blender Molecule Builder
Python script for generating 3D molecular models in **Blender** from `.mol` or `.sdf` structure files.

The script reads atomic coordinates and bond information from a molecular structure file, then builds the molecule in Blender using spheres for atoms and cylinders for bonds.

## Features

* Import molecular structures from `.mol` / `.sdf` files
* Automatically center and orient molecular coordinates
* Generate 3D atom models with element-specific materials
* Generate single, double, and triple bonds

  
<div align="center">
  <img height="300" alt="NO3R_blenderscripting" src="https://github.com/user-attachments/assets/6d6009ee-57c1-40c2-8a54-cd1f180b7247" />
  <img height="300" alt="NO3R_molecularstructure" src="https://github.com/user-attachments/assets/a180f574-46d1-428f-936b-7367cee9f482" />
  <p><em>After using the script in Blender, molecular models can be visualized and manipulated.</em></p>
</div>

<div align="center">
  <img height="300" alt="NO3R_moleculecnt" src="https://github.com/user-attachments/assets/ed98843e-8970-4eee-8b5c-0e1c64eca36e" />
  <img height="300" alt="NO3R_journalcover" src="https://github.com/user-attachments/assets/2d796d78-f1e9-4491-a44c-15c30d7cc1f9" />
  <p><em>This script was used to illustrate a cover for ACS Catalysis.</em></p>
</div>


## How It Works

The script:

1. Reads the atom and bond information from an `.sdf` file.
2. Extracts atomic coordinates, element names, and bond types.
3. Centers and rotates the molecular structure.
4. Creates spheres representing atoms.
5. Creates cylinders representing bonds.
6. Applies materials based on the elements involved.
7. Organizes the resulting objects into `AtomsCollection` and `BondsCollection`.

## Usage

### 1. Prepare a molecular structure file

Download or create a `.mol` or `.sdf` file for the molecule you want to visualize.

Useful sources include:

* [Crystallography Open Database](https://www.crystallography.net/cod/search.html) — molecular structure files
* [Avogadro](https://avogadro.cc/) — create and edit molecular structures

### 2. Update the file path

In the script, change the input file path:

```python
file = open('path/to/molecule.sdf', 'r')
```

### 3. Set up materials

The script expects Blender materials named according to the element symbols in the structure file (e.g. `H`, `C`, `N`, `O`).

Create or import the appropriate materials before running the script.

### 4. Run in Blender

Open Blender's **Scripting** workspace, load the Python script, and run it.

> **Tip:** Keep the camera and lighting in a separate collection if you are using the script's scene-cleaning code, so they are not deleted when the scene is reset.

## Rendering Tips

* **Cycles:** Higher-quality renders with more realistic lighting, but slower.
* **Eevee:** Faster rendering and useful for previews or iterative work.
* Reduce the render resolution while positioning the camera and materials, then increase it for the final render.
* A transparent background can be enabled through **Render → Film → Transparent**.
* For a white background, use a large plane behind the molecule with an appropriate material.

## Related Resources

This project was developed using techniques from:

* [Jakob Kibsgaard's Blender Course](https://www.kibsgaard-research.com/blender-course)
* [Blender for Scientists](https://www.youtube.com/watch?v=s2M2mMCKpeQ)

## Notes

This project was developed as a tool for creating scientific visualizations of molecular structures in Blender. The script can be adapted for different molecules by changing the input `.mol` or `.sdf` file and adjusting Blender materials and rendering settings.
