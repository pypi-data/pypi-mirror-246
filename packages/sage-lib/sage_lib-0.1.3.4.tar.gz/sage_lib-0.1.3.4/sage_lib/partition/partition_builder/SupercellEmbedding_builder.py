try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del sys

try:
    from sage_lib.input.structure_handling_tools.AtomPosition import AtomPosition
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AtomPosition: {str(e)}\n")
    del sys
    
try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    import os
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing os: {str(e)}\n")
    del sys

class SupercellEmbedding_builder(PartitionManager):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)
        self.AtomPositionManager_constructor = AtomPosition

        self._unitcell = None
        self._defect_supercell_relax = None
        self._defect_supercell_unrelax = None
        
        self._defect_supercell_unrelax_Np1 = None
        self._supercell_Nlayer = None

        self.read_dict = {
                'VASP':'read_POSCAR',
                'PDB':'read_PDB',
                'ASE':'read_ASE',
                'XYZ':'read_XYZ',
                'AIMS':'read_AIMS',
                    }

    def read_unitcell(self, file_location:str=None, file_name:str=None, source:str='VASP'):
        self.read(file_location=file_location, file_name=file_name, atributte='_unitcell', source=source)

    def read_defect_supercell_relax(self, file_location:str=None, file_name:str=None, source:str='VASP'):
        self.read(file_location=file_location, file_name=file_name, atributte='_defect_supercell_relax', source=source)

    def read_defect_supercell_unrelax(self, file_location:str=None, file_name:str=None, source:str='VASP'):
        self.read(file_location=file_location, file_name=file_name, atributte='_defect_supercell_unrelax', source=source)

    def read(self, file_location:str=None, file_name:str=None, atributte=None, source:str='VASP', verbose:bool=False):
        if file_name is None:
            file_location, file_name = os.path.split(file_location)
        file_location = '.' if file_location == '' else file_location
        self.file_location = file_location
        self.loadStoreManager(self.AtomPositionManager_constructor, f'{file_name}', f'{atributte}', f'{self.read_dict[source.upper()]}', verbose)

    @property
    def supercell_Nlayer(self, ):
        '''
        '''
        # Asegúrate de que no haya división por cero o por NaN
        safe_divide = np.divide(self._defect_supercell_unrelax.latticeVectors, self.unitcell.latticeVectors, out=np.zeros_like(self._defect_supercell_unrelax.latticeVectors), where=self.unitcell.latticeVectors!=0)

        # Procesamiento posterior
        rounded_vector = np.nan_to_num(safe_divide, nan=0).round().flatten()
        rounded_vector = rounded_vector[rounded_vector != 0]  # Filtrar ceros

        # 
        if np.all(rounded_vector == rounded_vector[0]):
            # 
            self._supercell_Nlayer = int(rounded_vector[0])
        else:
            # 
            raise ValueError("Los elementos del vector no son todos iguales.")

        return self._supercell_Nlayer


    def make_supercell_embedding(self, ):
        self._defect_supercell_unrelax_Np1 = AtomPosition()
        self.generate_onion_layer()
        self.correct_defect_structure()
        self.add_inner_structure()

    def correct_defect_structure(self, ):
        catomPositions_fractional_before_wrap = self.defect_supercell_unrelax_Np1.atomPositions_fractional 
        #self.defect_supercell_relax.wrap()
        fractional_correction = np.round(self._defect_supercell_relax.atomPositions_fractional - self._defect_supercell_unrelax.atomPositions_fractional)
        self._defect_supercell_relax.set_atomPositions_fractional( self._defect_supercell_relax.atomPositions_fractional - fractional_correction )

    def add_inner_structure(self, ):
        for inner_atom_label, inner_atom_position in zip(self.defect_supercell_relax.atomLabelsList, self.defect_supercell_relax.atomPositions):
            self._defect_supercell_unrelax_Np1.add_atom( atomLabels=inner_atom_label, atomPosition=inner_atom_position, )

    def generate_onion_layer(self, repeat:np.array=np.array([1,1,1], dtype=np.int64), supercell_Nlayer:int=None ):
        """
        Generate a supercell from a given unit cell in a crystalline structure.

        Parameters:
        - repeat (list): A list of three integers (nx, ny, nz) representing the number of times the unit cell is replicated 
                            along the x, y, and z directions, respectively.

        Returns:
        - np.array: An array of atom positions in the supercell.
        """
        supercell_Nlayer = supercell_Nlayer if isinstance(supercell_Nlayer, int) else self.supercell_Nlayer

        # Extract lattice vectors from parameters
        a, b, c = self.unitcell.latticeVectors
        nx, ny, nz = repeat

        # Generate displacement vectors
        displacement_vectors = [a * i + b * j + c * k for i in range(supercell_Nlayer+nx) for j in range(supercell_Nlayer+ny) for k in range(supercell_Nlayer+nz) if i>=supercell_Nlayer or j>=supercell_Nlayer or k>=supercell_Nlayer]
        
        # Replicate atom positions and apply displacements
        atom_positions = np.array(self.unitcell.atomPositions)
        supercell_positions = np.vstack([atom_positions + dv for dv in displacement_vectors])


        # Replicate atom identities and movement constraints
        supercell_atomLabelsList = np.tile(self.unitcell.atomLabelsList, len(displacement_vectors) )
        supercell_atomicConstraints = np.tile(self.unitcell.atomicConstraints, (len(displacement_vectors), 1))

        self._defect_supercell_unrelax_Np1._atomLabelsList = supercell_atomLabelsList
        self._defect_supercell_unrelax_Np1._atomicConstraints = supercell_atomicConstraints
        self._defect_supercell_unrelax_Np1._atomPositions = supercell_positions
        self._defect_supercell_unrelax_Np1._latticeVectors = self.unitcell._latticeVectors*(np.array(repeat) + supercell_Nlayer)
        self._defect_supercell_unrelax_Np1._atomPositions_fractional = None
        self._defect_supercell_unrelax_Np1._atomCount = None
        self._defect_supercell_unrelax_Np1._atomCountByType = None
        self._defect_supercell_unrelax_Np1._fullAtomLabelString = None

        return True

    def export_defect_supercell_unrelax_Np1(self, source:str='VASP', file_location:str=None):
        self.defect_supercell_unrelax_Np1.export(source='AIMS', file_location=file_location)

'''
path = '/home/akaris/Documents/code/Physics/VASP/v6.2/files/POSCAR/Cristals/Chris/new'
SEb = SupercellEmbedding_builder()
SEb.read_unitcell(file_location='/home/akaris/Documents/code/Physics/VASP/v6.2/files/POSCAR/Cristals/Chris/new', file_name='111_unitcell.in', source='AIMS')
SEb.read_defect_supercell_unrelax(file_location='/home/akaris/Documents/code/Physics/VASP/v6.2/files/POSCAR/Cristals/Chris/new', file_name='222_unrelax.in', source='AIMS')
SEb.read_defect_supercell_relax(file_location='/home/akaris/Documents/code/Physics/VASP/v6.2/files/POSCAR/Cristals/Chris/new', file_name='222_relax.in', source='AIMS')

SEb.make_supercell_embedding()
SEb.export_defect_supercell_unrelax_Np1(source='AIMS', file_location=path+'/out.in')
'''

