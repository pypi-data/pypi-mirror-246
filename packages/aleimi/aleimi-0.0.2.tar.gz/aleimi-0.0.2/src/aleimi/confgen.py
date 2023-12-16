#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO
# Toma de un archivo .smi los SMILES, genera la cant de conformeros seleccionados
# e imprime tanto los .sdf con todos los conformeros como .mop para optimizar en MOPAC
# con el nivel de teoria seleccionado.


from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import pandas as pd
import os
from typing import List

#      CHECKING geometry degeneracy
# La primera iteracion que corre por i busca que este optimizada la estructura
# La segunda busca que no se geometricamente la misma estructura
#Pueda suceder que alguna idx cumpla que no es geometricamente la misma estructura
#y no la ve el segundo ciclo
#pero el primero cuando llegue a ella la vera y tomara su id
# =============================================================================
def confgen(mol:Chem.rdchem.Mol, rdkit_d_RMSD:float, numConfs:int, rdkit_numThreads:float = 0, UFF:bool = False):
    """Generate conformers stochastically for mol and filter them out based on geometrical and energetic criterions.

    Parameters
    ----------
    mol : Chem.rdchem.Mol
        The RDKit molecule for which the stochastic conformations will be generated.
    rdkit_d_RMSD : float
        RMSD to filter out redundant conformations, geometric filter.
    numConfs : int
        Maximum number of conformation to generate
    rdkit_numThreads : float, optional
        Number of CPUs to use, by default 0 (use all)
    UFF : bool, optional
        If True a classical mechanical optimization will be performed, by default False

    Returns
    -------
    tuple
        * RDKit molecule with conformations, the hydrogens are always added.
        * Index of conformer to use.
        * List of classic energies if UFF = True, if not, a list of None values with length, number of conformers.
    """
    molecule = Chem.AddHs(mol)
    ids = AllChem.EmbedMultipleConfs(molecule, numConfs=numConfs, numThreads=rdkit_numThreads)
    if UFF:
        opt = AllChem.UFFOptimizeMoleculeConfs(molecule, numThreads=rdkit_numThreads, ignoreInterfragInteractions=False, maxIters=500) # The result is a list a containing 2-tuples: (not_converged, energy) for each conformer. If not_converged is 0, the minimization for that conformer converged.

        print('Calculando RMSD ...')
        rmsd_reject = set()
        opt_reject = set()
        rmsd_no_reject= set()
        no_opt=0
        ids=list(ids)
        for i in ids:

            if opt[i][0]==1:
                no_opt +=1
                opt_reject.add(ids[i])
            else:
                for idx in ids:
                    if i < idx:
                        RMSD = AllChem.GetConformerRMS(molecule, i, idx, prealigned=True)
                        if RMSD <= rdkit_d_RMSD:
                            if opt[i][1] < opt[idx][1]:
                                rmsd_reject.add(ids[i])
                                rmsd_no_reject.add(ids[idx])
                            else:
                                rmsd_reject.add(ids[idx])
                                rmsd_no_reject.add(ids[i])

        reject = opt_reject.union(rmsd_reject)
        if len(rmsd_reject) !=0:
            print(f'Los confórmeros con Id {rmsd_reject} no se imprimirán en el .mop por ser iguales (Según el error de RMSD = {rdkit_d_RMSD}) a {rmsd_no_reject} respectivamente y menos favorables energéticamente que los últimos mencionados.')
        if len(opt_reject) !=0:
            print(f'Los confórmeros con Id {opt_reject} no se imprimirán en el .mop pues no lograron ser optimizados.')
        to_use = list(set(ids) - reject)
        return molecule, to_use, [item[1] for item in opt]# Here I am creating a list of tuple (molecule, energy)
    else:

        print('Calculando RMSD ...')
        rmsd_reject = set()
        rmsd_no_reject= set()
        ids=list(ids)
        for i in ids:
            for idx in ids:
                if i < idx:
                    RMSD = AllChem.GetConformerRMS(molecule, i, idx, prealigned=True)
                    if RMSD <= rdkit_d_RMSD:
                        rmsd_reject.add(ids[i])
                        rmsd_no_reject.add(ids[idx])


        if len(rmsd_reject) !=0:
            print(f'Los confórmeros con Id {rmsd_reject} no se imprimirán en el .mop por ser iguales (Según el error de RMSD = {rdkit_d_RMSD}) a {rmsd_no_reject} respectivamente y menos favorables energéticamente que los últimos mencionados.')

        to_use = list(set(ids) - rmsd_reject)
        return molecule, to_use, len(ids)*[None] # Because I did not optimize, then I add None

# =============================================================================
#exportar las imagenes de la mejor manera posible. en columnas de 1,2,3,4 o 5
# =============================================================================

def makeimg(mols:List[Chem.rdchem.Mol], **keywords):
    """Simple function to create a picture of the input molecules.
    The file ``used_mols.png`` will be createad.

    Parameters
    ----------
    mols : List[Chem.rdchem.Mol]
        list of molecules
    """

    ms = [mol for mol in mols if mol is not None]
    _ = [AllChem.Compute2DCoords(m) for m in ms]

    cant = len(ms)
    if cant==1:
        best=1
    else:
        div = range(2,6)
        tup = [[i - cant%i,i] for i in div]

        for t in tup:
            if t[0] == t[1]:
                t[0] = 0

        minimum_rest = min(tup, key=lambda x: x[0])
        for t in tup:
            if t[0] == minimum_rest[0] and t[1]>minimum_rest[1]:
                minimum_rest = t
        best = minimum_rest[1]

    if 'legends' in keywords:
        legends = keywords['legends']
    else:
        legends = [f'Mol: {x+1}' for x in range(len(ms))]

    img=Draw.MolsToGridImage(ms,molsPerRow=best,subImgSize=(700,700), legends=legends)
    if len(ms) > 1:
        img.save('used_mols.png')
    else:
        img.save(f'{legends[0]}.png')



def main(suppl:str, numConfs:int = 10, rdkit_d_RMSD:float = 0.2, UFF:bool = False, rdkit_numThreads:int = 0, mopac_keywords:str =  'PM7 precise ef xyz geo-ok t=3h THREADS = 2') -> List[str]: #EPS=78.4
    """Generate conformers stochastically for the supplied molecules and filter them out based on geometrical and energetic criterions.

    Parameters
    ----------
    suppl : str
        Path for the molecule file. It could be:.pdb, .mol2, .mol, .sdf, .smi. In case of .smi you can define several SMILES.
        and for all of them the configuration will be generated.
        TODO: do the same for sdf files
    numConfs : int, optional
        Maximum number of conformation to generate, by default 10
    rdkit_d_RMSD : float, optional
        RMSD to filter out redundant conformations, geometric filter, by default 0.2
    UFF : bool, optional
        If True a classical mechanical optimization will be performed, by default False
    rdkit_numThreads : int, optional
        Number of CPUs to use, by default 0 (use all)
    mopac_keywords : str, optional
        This is head of a .mop file, basically a definition of the sei-empirical job. Check
        the `MOPAC Documentation <http://openmopac.net/>`_ for more information , by default 'PM7 precise ef xyz geo-ok t=3h THREADS = 2'

    Returns
    -------
    List[str]
        List of names of the used molecules

    Raises
    ------
    ValueError
        If in the .smi there are invalid SMILES
    ValueError
        If the extension of molecule is not: .pdb, .mol2, .mol, .sdf or .smi.
    ValueError
        If the molecule was not understood by RDKit
    """

    name, ext = os.path.splitext(os.path.basename(suppl))
    print('Resumen\n')
    if ext == ".smi":
        with open(suppl, 'rt') as file:
            smiles = file.readlines()

        # =============================================================================
        #    Comprobamos que los SMILES esten bien
        # expuestas con la funcion molfilter y exportamos .sdf
        # =============================================================================
        Errors_mols = []
        for i, item in enumerate(smiles):
            try:
                Chem.MolFromSmiles(item).GetNumAtoms()
            except:
                Errors_mols.append(i+1)
        if len(Errors_mols) !=  0:
            raise ValueError(f'Las moléculas con Ids: {Errors_mols} no son estructuras SMILES correctas para RDKit. Por favor, retirelas del .smi.')


        mols = [(f'conf_{name}_{i+1}', Chem.MolFromSmiles(smile)) for (i,smile) in enumerate(smiles)]
    elif ext == '.pdb':
        mols = [(f"conf_{name}", Chem.MolFromPDBFile(suppl))]
    elif ext == '.mol2':
        mols = [(f"conf_{name}", Chem.MolFromMol2File(suppl))]
    # elif ext == '.mol':
    #     mols = [(f"conf_{name}", Chem.MolFromMolFile(suppl))]
    elif ext in ['.mol', '.sdf']:
        mols = [(f"conf_{name}", Chem.MolFromMolFile(suppl))]
    else:
        raise ValueError(f'The structure must be one of the following extensions: .pdb, .mol2, .mol, .sdf, .smi. {suppl} was provided')

    if None in [mol[1] for mol in mols]:
        raise ValueError(f"{suppl} is not understanded by RDKit")




    # =============================================================================
    # Generamos conformaciones que cumplen con las condiciones de rmsd
    # expuestas con la funcion molfilter y exportamos .sdf
    # =============================================================================

    makeimg([mol[1] for mol in mols], legends = [mol[0] for mol in mols])
    for (i, mol) in enumerate(mols):

        print(f'Se están generando {numConfs} conformaciones para la molécula con Id = {i+1}...')

        molecule, index, opt = confgen(mol[1], rdkit_d_RMSD, numConfs, rdkit_numThreads = rdkit_numThreads, UFF = UFF)
        natoms = molecule.GetNumAtoms()

        sdf_writer = Chem.SDWriter(f"{mol[0]}.sdf")
        for idx in index:
            sdf_writer.write(molecule, confId=idx)
        sdf_writer.close()
        print(f'{mol[0]}:  {len(index)}/{numConfs}')

    # =============================================================================
    #     Generando los .mop
    # =============================================================================


        print(f"Archivos de salida: {mol[0]}.sdf, {mol[0]}.mop")

        # TODO Change this part to work properlly with the attribute _Name of the molecule
        with open(f"{mol[0]}.sdf", 'rt') as file:
            lines = file.readlines()

        final=open(f"{mol[0]}.mop",'w')

        #Toma los valores reales que se usaron para imprimir el .sdf y asi buscar los opt de verdad, pq si se elimino una estructura tengo que tenerlo en cuenta
        cont = 0 #Lo inicializao en -1 pq la cantidad de veces que se encontrara la palabra RDKit coincide con la cantidad con el len(to_use[0])
        #todo esto para que en el .mop me saque el valor de energia optenido en la optimizacion
        for k, line in enumerate(lines):
            if 'RDKit          3D' in line:

                chunk = lines[(k+3):(k+3+(natoms))]
                sliced = []
                for c in chunk:
                    sliced.append(c.split())
                df = pd.DataFrame(sliced)
                to_print = df[[3, 0, 1, 2]]
                final.write(mopac_keywords+'\n')
                try:
                    comments = f"{mol[0]}   E_UFF = {round(float(opt[index[cont]]), 3)}"
                except:
                    comments = f"{mol[0]}   E_UFF = {opt[index[cont]]}"
                final.write(comments+'\n')
                final.write('CELL: %d\n' % (cont+1))
                to_print.to_string(final, header=False, index=False)
                final.write('\n0\n')
                cont += 1
        print('Número de átomos: %d\n'% (natoms))
        final.close()
    mol_names = [mol[0] for mol in mols]
    return mol_names


if __name__ == '__main__':
    pass