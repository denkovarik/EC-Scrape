import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import shutil
import xlwings as xw
import pandas as pd
from classes.Annot_Reader import *


class Annot_Reader_tests(unittest.TestCase):
    """
    Runs all tests for the Uniprot class.
    """          
    def test_write(self):
        """
        Tests Annot_Reader class on writing a value to a cell in the excel 
        sheet
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' + 'test_genome_annotation.xls'
        cpy = currentdir + '\\test_files\\' + 'test_genome_annotation_write.xls'
        self.assertTrue(os.path.isfile(cpy))
        # Construct an Annot_Reader
        reader = Annot_Reader(orig, cpy, 0)
        write_row = 3
        write_col = "function"
        val = reader.read(write_row, write_col)
        val += " Modified++"
        reader.write(val, write_row, write_col)
        exp = "DNA polymerase IV (EC 2.7.7.7) Modified++"
        del(reader)
        validator = Annot_Reader(cpy, cpy, 0)
        self.assertTrue(validator.read(write_row, write_col) == exp)
        
        
    def test_init(self):
        """
        Tests the initialization of the Annot_Reader object.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xls"
        shifted = currentdir + '\\test_files\\'
        shifted += 'test_genome_annotation_shifted_data_frame.xls'
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        self.assertFalse(os.path.isfile(cpy))
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        # Construct an Annot_Reader
        reader = Annot_Reader(orig, cpy, 0)
        self.assertTrue(reader.dest == cpy)
        self.assertTrue(reader.header['start row'] == 1)
        self.assertTrue(reader.cols['function'] == 'H')
        del(reader)
        # Reload singleton class
        reader = Annot_Reader(orig, orig, 0)
        self.assertTrue(reader.dest == orig)
        # Loading file with shifted data frame
        self.assertTrue(os.path.isfile(shifted))
        del(reader)
        reader = Annot_Reader(shifted, shifted, 0)
        self.assertTrue(reader.instance.dest == shifted)
        self.assertTrue(reader.header['start row'] == 3)
        self.assertTrue(reader.cols['function'] == 'K')
    
        
    def test_read_cell(self):
        """
        Tests Annot_Reader on reading a cell from the excel sheet
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xls"
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        self.assertFalse(os.path.isfile(cpy))
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        reader = Annot_Reader(orig, cpy, 0)
        exp = "DNA polymerase IV (EC 2.7.7.7)"
        self.assertTrue(reader.read(3, 'function') == exp)
        
        
    def test_cols(self):
        """
        Tests Annot_Reader.int_2_col on its ability to convert an int
        to a supported excel column label.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        self.assertTrue(Annot_Reader.col_labels[1] == "A")
        self.assertTrue(Annot_Reader.col_labels[26] == "Z")
        self.assertTrue(Annot_Reader.col_labels[27] == "AA")
        self.assertTrue(Annot_Reader.col_labels[28] == "AB")
        self.assertTrue(Annot_Reader.col_labels["A"] == 1)
        self.assertTrue(Annot_Reader.col_labels["Z"] == 26)
        self.assertTrue(Annot_Reader.col_labels["AA"] == 27)
        self.assertTrue(Annot_Reader.col_labels["AB"] == 28)
        
        
    def test_modify_annot(self):
        """
        Tests modifying a single cell in an excel sheet.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        pass
           
        
    def test_copy(self):
        """
        Justs tests copying an excel file.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xls"
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        self.assertFalse(os.path.isfile(cpy))
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        
        
    def test_execution(self):
        """
        Tests the ability of the Annot_Reader_tests class to run a test.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()