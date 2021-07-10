import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


print("Running Tests for Uniprot Class")
os.system(currentdir + "\\Uniprot_tests.py")
print("")
print("Running Tests for NCBI Class")
os.system(currentdir + "\\NCBI_tests.py")
print("")
print("Running Tests for Annot_Reader Class")
os.system(currentdir + "\\Annot_Reader_Tests.py")
print("")
print("Running Tests for Utility Functions")
os.system(currentdir + "\\utils_testing.py")