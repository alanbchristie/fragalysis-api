from fragalysis_api import Validate, Align, set_up, to_fragalysis_dir
# from .align import Align
# from .validate import Validate
from fragalysis_api.xcimporter.conversion_pdb_mol import set_up
import os

# from shutil import rmtree
import argparse
from sys import exit


def xcimporter(in_dir, out_dir, target, validate=False):
    """Formats a lists of PDB files into fragalysis friendly format.
    1. Validates the naming of the pdbs.
    2. It aligns the pdbs (_bound.pdb file).
    3. It cleans the pdbs (removes solvents and ions).
    4. Splits the pdbs into ligands (.mol, .sdf and .pdb formats) and protein files (_apo.pdb file).
    5. Orders all the files into the correct directory structure required for fragalysis.

    :param user_id: data ID given to the input. Should be present in in_dir.
    :param in_dir: Directory containing data ID directories.
    :param out_dir: Directory containing processed pdbs (will be created if it doesn't exists).
    :return:
    """
    if validate:
        validation = Validate(in_dir)

        if not bool(validation.is_pdbs_valid):
            print("Input files are invalid!!")
            exit()

        if not validation.does_dir_exist:
            exit()

        if not validation.is_there_a_pdb_in_dir:
            exit()

    pdb_list = []

    for file in os.listdir(in_dir):
        pdb_list.append(os.path.join(in_dir, file))

    print(pdb_list)

    print("Making output directories")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
        os.makedirs(os.path.join(out_dir, "tmp"))

    print("Aligning protein structures")
    structure = Align(in_dir, pdb_ref="")
    structure.align(os.path.join(out_dir, "tmp"))

    aligned_list = [
        os.path.join(out_dir, "tmp", x)
        for x in os.listdir(os.path.join(out_dir, "tmp"))
    ]

    print("Identifying ligands")
    for i in aligned_list:
        try:
            new = set_up(target_name=target, infile=i, out_dir=out_dir)
        except AssertionError:
            print(i, "is not suitable, please consider removal or editing")
            for file in os.listdir(os.path.join(out_dir, "tmp")):
                if str(i) in file:
                    os.remove(os.path.join(out_dir, "tmp", str(file)))

    # to_fragalysis_dir(in_dir, os.path.join(out_dir, 'tmp'))

    # rmtree(os.path.join(out_dir, 'tmp'))
    print("Files are now in a fragalysis friendly format!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('-id', '--user_id', required=True,
    #                     help='Description for foo argument')
    parser.add_argument(
        "-i",
        "--in_dir",
        default=os.path.join("..", "..", "data", "xcimporter", "input"),
        help="Input directory",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out_dir",
        default=os.path.join("..", "..", "data", "xcimporter", "output"),
        help="Output directory",
        required=True,
    )
    parser.add_argument(
        "-v", "--validate", action="store_true", default=False, help="Validate input"
    )
    parser.add_argument("-t", "--target", help="Target name", required=True)
    args = vars(parser.parse_args())

    # user_id = args['user_id']
    in_dir = args["in_dir"]
    out_dir = args["out_dir"]
    validate = args["validate"]
    target = args["target"]

    if in_dir == os.path.join("..", "..", "data", "xcimporter", "input"):
        print("Using the default input directory ", in_dir)
    if out_dir == os.path.join("..", "..", "data", "xcimporter", "output"):
        print("Using the default input directory ", out_dir)

    xcimporter(in_dir=in_dir, out_dir=out_dir, target=target, validate=validate)
