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

