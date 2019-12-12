import os
import unittest
from fragalysis_api import set_up


class Conversion_test(unittest.TestCase):

    def test_open_file(self):
        """
        pdb file opens and checks that correct number of lines
        """
        new = set_up("5q1j", 'anna')
        assert len(new.pdbfile) == 6779

    def test_make_directory(self):
        """
        tests that directory to receive results has been created
        """
        new = set_up("5q1j", 'anna')
        assert os.path.isdir(new.RESULTS_DIRECTORY)

    def test_hets_and_cons(self):
        """
        tests that the correct number of heteroatoms and conect lines have been found
        """
        new = set_up("5q1j", 'anna')
        assert len(new.hetatms) == 326 and len(new.conects) == 24

    def test_remove_nonligs(self):
        """
        tests that solvents and ions from crystallography have been removed
        """
        new = set_up("5q1j", 'anna')
        assert len(new.final_hets) == 11

    def test_wanted_ligs(self):
        """
        tests that the ligand identifiers at the top of the pdb file have been found
        """
        new = set_up("5q1j", 'anna')
        assert len(new.wanted_ligs) != None

    def test_make_mol_objs(self):
        """
        tests that a molecular object has been made made for each ligand
        """
        new = set_up("5qj7", 'anna')
        assert len(new.mol_lst) == 4

    def test_make_pdb_file(self):
        """
        tests that a pdb file has been made for a particular ligand with the correct number of lines (HETATM & CONECT)
        """
        new = set_up("5qj7", 'anna')
        file = open(new.RESULTS_DIRECTORY + "/5qj7_JMM_A_303.pdb").readlines()
        assert len(file) == 36

    def test_make_mol_file(self):
        """
        tests that a mol file has been made with the correct number of lines
        """
        new = set_up("5qj7", 'anna')
        file = open(new.RESULTS_DIRECTORY + "/5qj7_JMM_A_303_mol.mol").readlines()
        assert len(file) == 43

    def test_make_sdf_file(self):
        """
        test that a sdf file has been made that incorporates the different mol objects
        """
        new = set_up("5qj7", 'anna')
        file = open(new.RESULTS_DIRECTORY +"/5qj7_out.sdf").readlines()
        assert len(file) == 176


if __name__ == '__main__':
    unittest.main()
