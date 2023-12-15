from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, Draw, rdFMCS, rdDepictor
from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem.Fingerprints import FingerprintMols
from IPython.display import display
from PIL import Image
from io import StringIO
import requests
from base64 import b64decode
import pandas as pd
from mordred import Calculator, descriptors, WienerIndex, ZagrebIndex
import statsmodels.api as sm
import param
import time
import matplotlib.pyplot as plt
from rdkit.Chem.Draw import IPythonConsole

print("""
    This library helps users explore specific chemical features, including finding similarity, chirality,
    bond types, double bond stereochemistry, and common substructures and chirality.

    For more information, refer to the documentation available in the following link:
    https://docs.google.com/document/d/1AqRdpTBIaBZEBkiAnuuzMNLSqoenK4yL/edit?usp=sharing&ouid=118019681680310111518&rtpof=true&sd=true

    The source code for this project is available on GitHub:
    https://github.com/Ahmed212517329/pubcem.git

    For inquiries, you can contact the author:
    Author: Ahmed Alhilal
    Email: aalhilal@kfu.edu.sa

    Functions Summary:

    1. `qspr_analysis(csv_file_path, dependent_variable_column)`: Performs QSPR analysis on a CSV file, calculates molecular descriptors, saves results in a CSV file, and provides a model summary.

    2. `display_active_chemicals_by_assay_aid(Assay_Aid)`: Displays active chemicals based on Assay ID.

    3. `display_inactive_chemicals_by_assay_aid(Assay_Aid)`: Displays inactive chemicals based on Assay ID.

    4. `retrieve_active_cids_by_assay_aid(Assay_Aid)`: Retrieves active compound CIDs based on Assay ID.

    5. `retrieve_inactive_cids_by_assay_aid(Assay_Aid)`: Retrieves inactive compound CIDs based on Assay ID.

    6. `retrieve_active_sids_by_assay_aid(Assay_Aid)`: Retrieves active sample SIDs based on Assay ID.

    7. `retrieve_inactive_sids_by_assay_aid(Assay_Aid)`: Retrieves inactive sample SIDs based on Assay ID.

    8. `virtual_screening(file_path, *Smiles)`: Performs virtual screening on a file with specified SMILES strings.

    9. `display_maximum_common_substructure(*Smiles)`: Displays the maximum common substructure of a list of molecular structures.

    10. `display_chirality(*Smiles)`: Displays chiral centers in molecular structures.

    11. `display_double_bond_stereochemistry(*Smiles)`: Identifies and prints the stereochemistry of double bonds in molecular structures.

    12. `highlight_difference(mol1, mol2)`: Generates an image highlighting the differences between two molecular structures.

    13. `draw_list_of_smiles(*Smiles)`: Draws a list of SMILES representations.

    14. `display_gasteiger_charges(*Smiles)`: Displays Gasteiger charges for a list of molecular structures.

    15. `display_bond_type_and_stereochemistry(*Smiles)`: Identifies and prints the bond type and stereochemistry for each bond in molecular structures.

    16. `display_double_bond_Stereochemistry(*Smiles)`: Identifies and prints the stereochemistry of double bonds in molecular structures.

    17. `mark_substructure(substructure_smiles, *Smiles)`: Marks atoms in molecular structures that match a given substructure represented by SMILES.

    18. `check_for_substructure(substructure_pattern, *Smiles)`: Checks if a substructure is present in a list of compounds.

    19. `display_morgan_score_topological(smile_a, smile_b)`: Displays the topological Morgan score for two SMILES strings.

    20. `delete_substructure(substructure, *Smiles)`: Deletes a specified substructure from a list of compounds.

    21. `Intro()`: Displays information about the library, including documentation and contact details.
        """)


def display_active_chemicals_by_assay_aid(aid):
    """
    Retrieves inactive compound CIDs from a specified assay and displays the common substructure.

    Parameters:
    - aid (int): Assay ID.

    Returns:
    - str: URL of the inactive compound CID data.
    """

    study_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{aid}/cids/txt?cids_type=active"
    url = requests.get(study_url)
    cids = url.text.split()
    str_cid = ",".join(str(x) for x in cids)

    compound_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{str_cid}/property/IsomericSMILES/txt"
    res = requests.get(compound_url)
    ms = res.text.split()
    molecules = list(map(Chem.MolFromSmiles, ms))
    grid_image = Chem.Draw.MolsToGridImage(molecules, subImgSize=(400, 400))
    display(grid_image)

    mcs_result = rdFMCS.FindMCS(molecules, threshold=0.7)
    common_substructure = Chem.MolFromSmarts(mcs_result.smartsString)

    print("The common substructure for these CIDs:")
    display(common_substructure)
    return compound_url


def display_inactive_chemicals_by_assay_aid(aid):
    """
    Retrieves inactive compound CIDs from a specified assay and displays the common substructure.

    Parameters:
    - aid (int): Assay ID.

    Returns:
    - str: URL of the inactive compound CID data.
    """

    study_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{aid}/cids/txt?cids_type=inactive"
    url = requests.get(study_url)
    cids = url.text.split()
    str_cid = ",".join(str(x) for x in cids)

    compound_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{str_cid}/property/IsomericSMILES/txt"
    res = requests.get(compound_url)
    ms = res.text.split()
    molecules = list(map(Chem.MolFromSmiles, ms))
    grid_image = Chem.Draw.MolsToGridImage(molecules, subImgSize=(400, 400))
    display(grid_image)

    mcs_result = rdFMCS.FindMCS(molecules, threshold=0.7)
    common_substructure = Chem.MolFromSmarts(mcs_result.smartsString)

    print("The common substructure for these CIDs:")
    display(common_substructure)
    return compound_url





def retrieve_active_cids_by_assay_aid(assay_id):
    """
    Fetches and prints the active compound CIDs for a given assay ID.

    Parameters:
    - assay_id (int): Assay ID for PubChem.

    Returns:
    - str: URL for active compounds.
    """
    rdDepictor.SetPreferCoordGen(True)
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True

    assay_id = str(assay_id)
    active_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{assay_id}/cids/txt?cids_type=active"
    response = requests.get(active_url)
    active_cids = response.text.split()

    print("Active compound CIDs:\n", active_cids)
    return active_url


def retrieve_inactive_cids_by_assay_aid(assay_id):
    """
    Fetches and prints the inactive compound CIDs for a given assay ID.

    Parameters:
    - assay_id (int): Assay ID for PubChem.

    Returns:
    - str: URL for inactive compounds.
    """
    rdDepictor.SetPreferCoordGen(True)
    Draw.DrawingOptions.minFontSize = 20

    assay_id = str(assay_id)
    inactive_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{assay_id}/cids/txt?cids_type=inactive"
    response = requests.get(inactive_url)
    inactive_cids = response.text.split()

    print("Inactive compound CIDs:\n", inactive_cids)
    return inactive_url


def retrieve_active_sids_by_substance_aid(substance_id):
    """
    Fetches and prints the active sample IDs (SIDs) for a given substance ID.

    Parameters:
    - substance_id (int): Substance ID for PubChem.

    Returns:
    - str: URL for active SIDs.
    """
    # Your drawing options or other settings here
    substance_id = str(substance_id)
    active_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{substance_id}/sids/txt?sids_type=active"
    response = requests.get(active_url)
    active_sids = response.text.split()

    print("Active sample SIDs:\n", active_sids)
    return active_url

def retrieve_inactive_sids_by_substance_aid(substance_id):
    """
    Fetches and prints the inactive sample IDs (SIDs) for a given substance ID.

    Parameters:
    - substance_id (int): Substance ID for PubChem.

    Returns:
    - str: URL for inactive SIDs.
    """
    # Your drawing options or other settings here
    substance_id = str(substance_id)
    inactive_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{substance_id}/sids/txt?sids_type=inactive"
    response = requests.get(inactive_url)
    inactive_sids = response.text.split()

    print("Inactive sample SIDs:\n", inactive_sids)
    return inactive_url

def virtual_screening(file_path, *colnames):
    # Convert variable number of column names to a list
    col_names = list(colnames)

    # Read the input file into a pandas DataFrame
    df_act = pd.read_csv(file_path, sep=" ", names=col_names)
    smiles_act = df_act['smiles'].tolist()

    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    cids_hit = {}

    # Loop through the input smiles and perform similarity search against PubChem
    for idx, mysmiles in enumerate(smiles_act):
        mydata = {'smiles': mysmiles}

        # Similarity Search against PubChem
        url = f"{prolog}/compound/fastsimilarity_2d/smiles/cids/txt"
        res = requests.post(url, data=mydata)

        if res.status_code == 200:
            cids = [int(x) for x in res.text.split()]
        else:
            # Handle errors during the PubChem request
            print(f"Error at {idx}: {df_act.loc[idx, 'id']} {mysmiles}")
            print(res.status_code)
            print(res.content)

        # Update the dictionary with hit counts for each CID
        for mycid in cids:
            cids_hit[mycid] = cids_hit.get(mycid, 0) + 1
        time.sleep(0.2)

    # Exclude the query compounds from the hits
    cids_query = {}
    for idx, mysmiles in enumerate(smiles_act):
        mydata = {'smiles': mysmiles}
        url = f"{prolog}/compound/fastidentity/smiles/cids/txt?identity_type=same_connectivity"
        res = requests.post(url, data=mydata)

        if res.status_code == 200:
            cids = [int(x) for x in res.text.split()]
        else:
            # Handle errors during the PubChem request
            print(f"Error at {idx}: {df_act.loc[idx, 'id']} {mysmiles}")
            print(res.status_code)
            print(res.content)

        # Update the dictionary with query CID counts
        for mycid in cids:
            cids_query[mycid] = cids_query.get(mycid, 0) + 1
        time.sleep(0.2)

    # Remove query compounds from the hit dictionary
    for mycid in cids_query.keys():
        cids_hit.pop(mycid, None)

    # Filtering out non-drug-like compounds
    chunk_size = 100
    if len(cids_hit) % chunk_size == 0:
        num_chunks = len(cids_hit) // chunk_size
    else:
        num_chunks = len(cids_hit) // chunk_size + 1

    cids_list = list(cids_hit.keys())
    csv = ""

    # Loop through chunks and retrieve additional properties from PubChem
    for i in range(num_chunks):
        idx1 = chunk_size * i
        idx2 = chunk_size * (i + 1)
        cids_str = ",".join(map(str, cids_list[idx1:idx2]))
        url = f"{prolog}/compound/cid/{cids_str}/property/HBondDonorCount,HBondAcceptorCount,MolecularWeight,XLogP,CanonicalSMILES,IsomericSMILES/csv"
        res = requests.get(url)

        # Append results to CSV variable
        if i == 0:
            csv = res.text
        else:
            csv += "\n".join(res.text.split()[1:]) + "\n"

        time.sleep(0.2)

    # Downloaded data (in CSV) are loaded into a pandas data frame
    csv_file = StringIO(csv)
    df_raw = pd.read_csv(csv_file, sep=",")

    # Lipinski's rule of five criteria
    df = df_raw[(df_raw['HBondDonorCount'] <= 5) &
                (df_raw['HBondAcceptorCount'] <= 10) &
                (df_raw['MolecularWeight'] <= 500) &
                (df_raw['XLogP'] < 5)]

    # Draw the structures of the top 10 compounds
    print("The top 10 unique compounds that satisfy all criteria of Lipinski's rule of five")
    cids_top = df.sort_values(by=['HitFreq', 'CID'], ascending=False).head(10).CID.tolist()

    mols = []
    for mycid in cids_top:
        mysmiles = df[df.CID == mycid].IsomericSMILES.item()
        mol = Chem.MolFromSmiles(mysmiles)
        Chem.FindPotentialStereoBonds(mol)
        mols.append(mol)

    mylegends = [f"CID {x}" for x in cids_top]
    img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(400, 400), legends=mylegends)
    display(img)

    # Extract unique compounds in terms of canonical SMILES
    canonical_smiles = df.CanonicalSMILES.unique()
    idx_to_include = []

    for mysmiles in canonical_smiles:
        myidx = df[df.CanonicalSMILES == mysmiles].index.to_list()[0]
        idx_to_include.append(myidx)

    df['Include'] = 0
    df.loc[idx_to_include, 'Include'] = 1

    cids_top_unique = df[df['Include'] == 1].sort_values(by=['HitFreq', 'CID'], ascending=False).head(10).CID.tolist()

    # Draw the top 10 unique compounds
    print("The top 10 unique compounds in terms of canonical SMILES")
    mols = []

    for mycid in cids_top_unique:
        mysmiles = df[df.CID == mycid].IsomericSMILES.item()
        mol = Chem.MolFromSmiles(mysmiles)
        Chem.FindPotentialStereoBonds(mol)
        mols.append(mol)

    mylegends = [f"CID {x}" for x in cids_top_unique]
    img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(400, 400), legends=mylegends)
    display(img)

    # Saving molecules in files
    for idx, mycid in enumerate(cids_top_unique):
        if idx == 3:
            break

        mysmiles = df[df['CID'] == mycid].IsomericSMILES.item()
        mymol = Chem.MolFromSmiles(mysmiles)
        mymol = Chem.AddHs(mymol)
        AllChem.EmbedMolecule(mymol)
        AllChem.MMFFOptimizeMolecule(mymol)

        filename = f"{file_path}_lig{idx}_{mycid}.mol"
        Chem.MolToMolFile(mymol, filename)

    df.to_csv('Virtual_Screening.csv', index=False)
    print("Now, you can find 'Virtual_Screening.csv' in your device")

    return df.to_csv('Virtual_Screening.csv')


def qspr_analysis(csv_file_path, dependent_variable_column):
    # Create descriptor instances
    zagreb_index1 = ZagrebIndex.ZagrebIndex(version=1)
    zagreb_index2 = ZagrebIndex.ZagrebIndex(version=2)
    wiener_index = WienerIndex.WienerIndex()

    # Read the CSV file into a pandas dataframe
    df = pd.read_csv(csv_file_path)

    # Create lists to store calculated results
    result_Wiener = []
    result_Z1 = []
    result_Z2 = []

    # Iterate through each row of the CSV data
    for index, row in df.iterrows():
        SMILE = row['SMILES']
        mol = Chem.MolFromSmiles(SMILE)

        # Calculate descriptor values
        result_Wiener.append(wiener_index(mol))
        result_Z1.append(zagreb_index1(mol))
        result_Z2.append(zagreb_index2(mol))

    # Add the calculated results to the dataframe
    df['Wiener'] = result_Wiener
    df['Z1'] = result_Z1
    df['Z2'] = result_Z2

    # Save the dataframe as a CSV file
    output_csv_path = f"{csv_file_path}_W_Z1_Z2_qspr_analysis_results.csv"
    df.to_csv(output_csv_path, index=False)
    display(df)
    # Perform QSPR analysis
    independent_variables = ["MW", "Wiener", "Z1", "Z2"]
    X = df[independent_variables]        # select our independent variables
    X = sm.add_constant(X)               # add an intercept to our model
    y = df[[dependent_variable_column]]  # select the dependent variable
    model = sm.OLS(y, X).fit()            # set up our model

    # Save the model summary to a text file
    output_text_path = f"{csv_file_path}_W_Z1_Z2__model_summary.txt"
    with open(output_text_path, "w") as text_file:
        text_file.write(model.summary().as_text())
        print(model.summary())

    print(f"\n***Results saved to:\n- CSV file: {output_csv_path}\n- Model summary text file: {output_text_path}")


    return

def qspr_analysis_2(csv_file_path, dependent_variable_column, descriptor_types):
    # Create descriptor instances based on user's choice
    descriptor_instances = []
    for descriptor_type in descriptor_types:
        if descriptor_type == "z1":
            descriptor_instances.append(ZagrebIndex.ZagrebIndex(version=1))
        elif descriptor_type == "z2":
            descriptor_instances.append(ZagrebIndex.ZagrebIndex(version=2))
        elif descriptor_type == "w":
            descriptor_instances.append(WienerIndex.WienerIndex())
        else:
            raise ValueError(f"Invalid descriptor type '{descriptor_type}'. Choose 'z1', 'z2', or 'w'.")

    # Read the CSV file into a pandas dataframe
    df = pd.read_csv(csv_file_path)

    # Create lists to store calculated results
    for descriptor_type, descriptor_instance in zip(descriptor_types, descriptor_instances):
        result_descriptor = []

        # Iterate through each row of the CSV data
        for index, row in df.iterrows():
            SMILE = row['SMILES']
            mol = Chem.MolFromSmiles(SMILE)

            # Calculate descriptor values
            result_descriptor.append(descriptor_instance(mol))

        # Add the calculated results to the dataframe
        df[descriptor_type.capitalize()] = result_descriptor

    # Save the dataframe as a CSV file
    output_csv_path = f"{csv_file_path}_qspr_analysis_results.csv"
    df.to_csv(output_csv_path, index=False)
    display(df)
    # Perform QSPR analysis
    independent_variables = ["MW"] + [desc.capitalize() for desc in descriptor_types]
    X = df[independent_variables]        # select our independent variables
    X = sm.add_constant(X)               # add an intercept to our model
    y = df[[dependent_variable_column]]  # select the dependent variable
    model = sm.OLS(y, X).fit()            # set up our model

    # Save the model summary to a text file
    output_text_path = f"{csv_file_path}_model_summary.txt"
    with open(output_text_path, "w") as text_file:
        text_file.write(model.summary().as_text())
        print(model.summary())

    print(f"\n***Results saved to:\n- CSV file: {output_csv_path}\n- Model summary text file: {output_text_path}")
    return


def display_maximum_common_substructure(*args):
    """
    Finds and displays the maximum common substructure (MCS) of a list of molecular structures.

    Parameters:
    - *args (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    # Initialize an empty list to store converted SMILES strings
    str_list = []

    # Iterate through the input arguments
    for x in args:
        if type(x) is str or type(x) is int:
            # Convert to string and append to the list
            str_list.append(str(x))
        elif type(x) is list:
            # If the argument is a list, iterate through its elements and convert to strings
            for m in x:
                str_list.append(str(m))
        else:
            # If the argument is neither string nor integer, assume it is an iterable and convert its elements to strings
            for m in x:
                str_list.append(str(m))

    # Convert SMILES strings to RDKit molecules
    mols = [Chem.MolFromSmiles(i) for i in str_list]

    # Find the Maximum Common Substructure (MCS)
    if len(mols) > 0:
        result = rdFMCS.FindMCS(mols)
        mcs_mol = Chem.MolFromSmarts(result.smartsString)
        # Display the MCS
        display(Draw.MolToImage(mcs_mol, legend="MCS1"))


def display_chirality(*compounds):
    """
    Displays chiral centers in molecular structures represented by SMILES strings.

    Parameters:
    - *compounds (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True

    for compound in compounds:
        smiles_str = str(compound)
        mol = Chem.MolFromSmiles(smiles_str)
        chiral_centers = Chem.FindMolChiralCenters(mol, force=True, includeUnassigned=True, useLegacyImplementation=True)
        print(chiral_centers)
        display(mol)

def display_double_bond_stereochemistry(*compounds):
    """
    Identifies and prints the stereochemistry of double bonds in molecular structures represented by SMILES strings.

    Parameters:
    - *compounds (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True

    for compound in compounds:
        smiles_str = str(compound)
        mol = Chem.MolFromSmiles(smiles_str)
        display(mol)

        for bond in mol.GetBonds():
            print(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx(), bond.GetBondType(), bond.GetStereo())


    return



def highlight_difference(mol1, mol2):
    """
    Generates an image highlighting the differences between two molecular structures represented by SMILES strings.

    Parameters:
    - mol1 (str): SMILES string of the first molecule.
    - mol2 (str): SMILES string of the second molecule.

    Returns:
    - PIL.Image.Image: Image highlighting the differing atoms in the two molecules.
    """
    # Convert SMILES strings to RDKit molecules
    mol1 = Chem.MolFromSmiles(mol1)
    mol2 = Chem.MolFromSmiles(mol2)

    # Find the Maximum Common Substructure (MCS) between the two molecules
    mcs = rdFMCS.FindMCS([mol1, mol2])
    mcs_mol = Chem.MolFromSmarts(mcs.smartsString)

    # Identify atoms in mol1 not present in the MCS
    match1 = mol1.GetSubstructMatch(mcs_mol)
    target_atm1 = [atom.GetIdx() for atom in mol1.GetAtoms() if atom.GetIdx() not in match1]

    # Identify atoms in mol2 not present in the MCS
    match2 = mol2.GetSubstructMatch(mcs_mol)
    target_atm2 = [atom.GetIdx() for atom in mol2.GetAtoms() if atom.GetIdx() not in match2]

    # Generate and return an image highlighting the differing atoms in both molecules
    return Draw.MolsToGridImage([mol1, mol2], highlightAtomLists=[target_atm1, target_atm2])

def draw_list_of_smiles(*args):
    """
    Generates a grid image displaying molecular structures from a list of SMILES strings and/or integers.

    Parameters:
    - *args (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - PIL.Image.Image: Grid image displaying the molecular structures.
    """
    # Initialize an empty list to store converted SMILES strings
    str_list = []

    # Iterate through the input arguments
    for x in args:
        if type(x) is str or type(x) is int:
            # Convert to string and append to the list
            str_list.append(str(x))
        elif type(x) is list:
            # If the argument is a list, iterate through its elements and convert to strings
            for m in x:
                str_list.append(str(m))

    # Convert SMILES strings to RDKit molecules
    mol_list = [Chem.MolFromSmiles(smiles) for smiles in str_list]

    # Generate and return a grid image of the molecular structures
    grid_image = Chem.Draw.MolsToGridImage(mol_list)
    return grid_image



def display_gasteiger_charges(*args):
    """
    Calculates and displays Gasteiger charges for atoms in molecular structures represented by SMILES strings.

    Parameters:
    - *args (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True


    # Initialize an empty list to store converted SMILES strings
    str_list = []

    # Iterate through the input arguments
    for x in args:
        if type(x) is str or type(x) is int:
            # Convert to string and append to the list
            str_list.append(str(x))
        elif type(x) is list:
            # If the argument is a list, iterate through its elements and convert to strings
            for m in x:
                str_list.append(str(m))
        else:
            # If the argument is neither string nor integer, assume it is an iterable and convert its elements to strings
            for m in x:
                str_list.append(str(m))

    # Iterate through the list of SMILES strings
    for i in str_list:
        # Convert SMILES string to RDKit molecule
        mol = Chem.MolFromSmiles(i)

        # Calculate Gasteiger charges for the atoms in the molecule
        AllChem.ComputeGasteigerCharges(mol)

        # Display the molecule with Gasteiger charges as atom notes
        display(mol)

        # Create a copy of the molecule to add atom notes
        mol_with_notes = Chem.Mol(mol)
        for atom in mol_with_notes.GetAtoms():
            charge_label = '%.2f' % (atom.GetDoubleProp("_GasteigerCharge"))
            atom.SetProp('atomNote', charge_label)

        # Display the molecule with Gasteiger charges as atom notes
        display(mol_with_notes)
    return



def display_bond_type_and_stereochemistry(*compounds):
    """
    Identifies and prints the bond type and stereochemistry for each bond in molecular structures represented by SMILES strings.

    Parameters:
    - *compounds (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True

    # Initialize an empty list to store converted SMILES strings
    str_list = []

    # Iterate through the input arguments
    for x in compounds:
        if type(x) is str or type(x) is int:
            # Convert to string and append to the list
            str_list.append(str(x))
        elif type(x) is list:
            # If the argument is a list, iterate through its elements and convert to strings
            for m in x:
                str_list.append(str(m))
        else:
            # If the argument is neither string nor integer, assume it is an iterable and convert its elements to strings
            for m in x:
                str_list.append(str(m))

    # Iterate through the list of SMILES strings
    for i in str_list:
        # Convert SMILES string to RDKit molecule
        mol = Chem.MolFromSmiles(i)

        # Display the molecule
        display(mol)

        # Iterate through the bonds and print bond type and stereochemistry
        for bond in mol.GetBonds():
            bond_type = bond.GetBondType()
            stereo_info = bond.GetStereo()

            # Check if the bond is a double bond and print stereochemistry if present
            if bond_type == Chem.BondType.DOUBLE:
                print(
                    f"Double Bond ({bond.GetBeginAtomIdx()}-{bond.GetEndAtomIdx()}): {bond_type}, Stereochemistry: {stereo_info}")
            else:
                print(
                    f"Bond ({bond.GetBeginAtomIdx()}-{bond.GetEndAtomIdx()}): {bond_type}, Stereochemistry: {stereo_info}")
    return

def display_double_bond_Stereochemistry(*compounds):
    """
    Identifies and prints the stereochemistry of double bonds in molecular structures represented by SMILES strings.

    Parameters:
    - *compounds (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True

    for compound in compounds:
        smiles_str = str(compound)
        mol = Chem.MolFromSmiles(smiles_str)
        display(mol)

        for bond in mol.GetBonds():
            print(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx(), bond.GetBondType(), bond.GetStereo())
    return


def mark_substructure(substructure_smiles, *molecules):
    """
    Marks atoms in molecular structures that match a given substructure represented by SMILES.

    Parameters:
    - substructure_smiles (str): SMILES string representing the substructure to mark.
    - *molecules (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    # Initialize an empty list to store converted SMILES strings
    str_list = []

    # Iterate through the input arguments
    for x in molecules:
        if type(x) is str or type(x) is int:
            # Convert to string and append to the list
            str_list.append(str(x))
        elif type(x) is list:
            # If the argument is a list, iterate through its elements and convert to strings
            for m in x:
                str_list.append(str(m))
        else:
            # If the argument is neither string nor integer, assume it is an iterable and convert its elements to strings
            for m in x:
                str_list.append(str(m))

    # Convert substructure SMILES to RDKit molecule
    substructure = Chem.MolFromSmarts(substructure_smiles)

    # Iterate through the list of SMILES strings
    for i in str_list:
        # Convert SMILES string to RDKit molecule
        mol = Chem.MolFromSmiles(i)

        # Get substructure matches and mark specific atoms
        matches = mol.GetSubstructMatches(substructure)
        for match in matches:
            for atom_index in match:
                mol.GetAtomWithIdx(atom_index)

        # Display the marked molecule
        display(mol)
    return



def check_for_substructure(substructure_pattern, *compounds):
    """
    Check if a substructure is present in a list of compounds.

    Parameters:
    - substructure_pattern (str): SMARTS pattern representing the substructure to check.
    - *compounds (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - list: List of tuples containing compound information and a boolean value indicating whether the substructure is present.
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True

    results = []

    for compound in compounds:
        smiles_str = str(compound)
        mol = Chem.MolFromSmiles(smiles_str)
        pattern = Chem.MolFromSmarts(substructure_pattern)
        has_substructure = mol.HasSubstructMatch(pattern)
        result_info = (smiles_str, has_substructure)
        results.append(result_info)

    print("Results:")
    for result_info in results:
        smiles, has_substructure = result_info
        status = "has" if has_substructure else "does not have"
        print(f"{smiles}: {status} the substructure")

    return results




def display_gasteiger_charges(*compounds):
    """
    Computes and displays Gasteiger charges for atoms in molecular structures represented by SMILES strings.

    Parameters:
    - *compounds (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True

    for compound in compounds:
        if isinstance(compound, str):
            mol = Chem.MolFromSmiles(compound)
            AllChem.ComputeGasteigerCharges(mol)

            mol_copy = Chem.Mol(mol)
            for atom in mol_copy.GetAtoms():
                lbl = '%.2f' % (atom.GetDoubleProp("_GasteigerCharge"))
                atom.SetProp('atomNote', lbl)
            display(mol_copy)

        elif isinstance(compound, list):
            for smiles_str in compound:
                mol = Chem.MolFromSmiles(smiles_str)
                AllChem.ComputeGasteigerCharges(mol)

                mol_copy = Chem.Mol(mol)
                for atom in mol_copy.GetAtoms():
                    lbl = '%.2f' % (atom.GetDoubleProp("_GasteigerCharge"))
                    atom.SetProp('atomNote', lbl)
                display(mol_copy)


    return


def display_morgan_score_topological(smile_a, smile_b):
    """
    Compares molecular fingerprints for given SMILES strings using atom pair, Morgan, and topological fingerprints.

    Parameters:
    - smile_a (str): SMILES string for the first compound.
    - smile_b (str): SMILES string for the second compound.

    Returns:
    - None
    """
    Draw.DrawingOptions.addAtomIndices = True
    Draw.DrawingOptions.addStereoAnnotation = True


    ms = [Chem.MolFromSmiles(smile_a), Chem.MolFromSmiles(smile_b)]
    fig = Draw.MolsToGridImage(ms[:], molsPerRow=2, subImgSize=(400, 200))
    display(fig)

    radius = 2

    fpatom = [Pairs.GetAtomPairFingerprintAsBitVect(x) for x in ms]

    print("Atom pair score: {:8.4f}".format(DataStructs.TanimotoSimilarity(fpatom[0], fpatom[1])))

    fpmorg = [Chem.AllChem.GetMorganFingerprint(ms[0], radius, useFeatures=True),
              Chem.AllChem.GetMorganFingerprint(ms[1], radius, useFeatures=True)]

    fptopo = [FingerprintMols.FingerprintMol(x) for x in ms]

    print("Morgan score: {:11.4f}".format(DataStructs.TanimotoSimilarity(fpmorg[0], fpmorg[1])))
    print("Topological score: {:3.4f}".format(DataStructs.TanimotoSimilarity(fptopo[0], fptopo[1])))
    return


def delete_substructure(substructure, *compounds):
    """
    Deletes a specified substructure from given molecular structures and displays the modified structures.

    Parameters:
    - substructure (str): SMILES string representing the substructure to be deleted.
    - *compounds (variable arguments): SMILES strings and/or integers representing molecular structures.

    Returns:
    - None
    """

    # Convert various input types to a list of SMILES strings
    smiles_list = [str(x) for x in compounds]

    # Display the substructure to be deleted
    print("Substructure to be deleted:")
    substructure_mol = Chem.MolFromSmiles(substructure)
    display(substructure_mol)

    print("\nProcessing...")

    # Display original and modified molecular structures
    for smiles in smiles_list:
        original_mol = Chem.MolFromSmiles(smiles)

        # Display original molecular structure
        print("\nOriginal Molecular Structure:")
        display(original_mol)

        # Display modified molecular structure after deleting substructure
        pattern = Chem.MolFromSmarts(substructure)
        modified_mol = AllChem.DeleteSubstructs(original_mol, pattern)

        print("\nMolecular Structure After Deleting Substructure:")
        display(modified_mol)

    return

