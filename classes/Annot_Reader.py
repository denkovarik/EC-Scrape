import shutil
import xlwings as xw
import pandas as pd
import os, io, sys, inspect
import time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class Annot_Reader():
    """
    Class to read and write to a genome annotation.
    """
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    col_labels = {1 : "A", "A" : 1, 2 : "B", "B" : 2, 3 : "C", "C" : 3, 4 : "D", "D" : 4, 5 : "E", "E" : 5, 6 : "F", "F" : 6, 7 : "G", "G" : 7, 8 : "H", "H" : 8, 9 : "I", "I" : 9, 10 : "J", "J" : 10, 11 : "K", "K" : 11, 12 : "L", "L" : 12, 13 : "M", "M" : 13, 14 : "N", "N" : 14, 15 : "O", "O" : 15, 16 : "P", "P" : 16, 17 : "Q", "Q" : 17, 18 : "R", "R" : 18, 19 : "S", "S" : 19, 20 : "T", "T" : 20, 21 : "U", "U" : 21, 22 : "V", "V" : 22, 23 : "W", "W" : 23, 24 : "X", "X" : 24, 25 : "Y", "Y" : 25, 26 : "Z", "Z" : 26, 27 : "AA", "AA" : 27, 28 : "AB", "AB" : 28, 29 : "AC", "AC" : 29, 30 : "AD", "AD" : 30, 31 : "AE", "AE" : 31, 32 : "AF", "AF" : 32, 33 : "AG", "AG" : 33, 34 : "AH", "AH" : 34, 35 : "AI", "AI" : 35, 36 : "AJ", "AJ" : 36, 37 : "AK", "AK" : 37, 38 : "AL", "AL" : 38, 39 : "AM", "AM" : 39, 40 : "AN", "AN" : 40, 41 : "AO", "AO" : 41, 42 : "AP", "AP" : 42, 43 : "AQ", "AQ" : 43, 44 : "AR", "AR" : 44, 45 : "AS", "AS" : 45, 46 : "AT", "AT" : 46, 47 : "AU", "AU" : 47, 48 : "AV", "AV" : 48, 49 : "AW", "AW" : 49, 50 : "AX", "AX" : 50, 51 : "AY", "AY" : 51, 52 : "AZ", "AZ" : 52, 53 : "BA", "BA" : 53, 54 : "BB", "BB" : 54, 55 : "BC", "BC" : 55, 56 : "BD", "BD" : 56, 57 : "BE", "BE" : 57, 58 : "BF", "BF" : 58, 59 : "BG", "BG" : 59, 60 : "BH", "BH" : 60, 61 : "BI", "BI" : 61, 62 : "BJ", "BJ" : 62, 63 : "BK", "BK" : 63, 64 : "BL", "BL" : 64, 65 : "BM", "BM" : 65, 66 : "BN", "BN" : 66, 67 : "BO", "BO" : 67, 68 : "BP", "BP" : 68, 69 : "BQ", "BQ" : 69, 70 : "BR", "BR" : 70, 71 : "BS", "BS" : 71, 72 : "BT", "BT" : 72, 73 : "BU", "BU" : 73, 74 : "BV", "BV" : 74, 75 : "BW", "BW" : 75, 76 : "BX", "BX" : 76, 77 : "BY", "BY" : 77, 78 : "BZ", "BZ" : 78, 79 : "CA", "CA" : 79, 80 : "CB", "CB" : 80, 81 : "CC", "CC" : 81, 82 : "CD", "CD" : 82, 83 : "CE", "CE" : 83, 84 : "CF", "CF" : 84, 85 : "CG", "CG" : 85, 86 : "CH", "CH" : 86, 87 : "CI", "CI" : 87, 88 : "CJ", "CJ" : 88, 89 : "CK", "CK" : 89, 90 : "CL", "CL" : 90, 91 : "CM", "CM" : 91, 92 : "CN", "CN" : 92, 93 : "CO", "CO" : 93, 94 : "CP", "CP" : 94, 95 : "CQ", "CQ" : 95, 96 : "CR", "CR" : 96, 97 : "CS", "CS" : 97, 98 : "CT", "CT" : 98, 99 : "CU", "CU" : 99, 100 : "CV", "CV" : 100, 101 : "CW", "CW" : 101, 102 : "CX", "CX" : 102, 103 : "CY", "CY" : 103, 104 : "CZ", "CZ" : 104, 105 : "DA", "DA" : 105, 106 : "DB", "DB" : 106, 107 : "DC", "DC" : 107, 108 : "DD", "DD" : 108, 109 : "DE", "DE" : 109, 110 : "DF", "DF" : 110, 111 : "DG", "DG" : 111, 112 : "DH", "DH" : 112, 113 : "DI", "DI" : 113, 114 : "DJ", "DJ" : 114, 115 : "DK", "DK" : 115, 116 : "DL", "DL" : 116, 117 : "DM", "DM" : 117, 118 : "DN", "DN" : 118, 119 : "DO", "DO" : 119, 120 : "DP", "DP" : 120, 121 : "DQ", "DQ" : 121, 122 : "DR", "DR" : 122, 123 : "DS", "DS" : 123, 124 : "DT", "DT" : 124, 125 : "DU", "DU" : 125, 126 : "DV", "DV" : 126, 127 : "DW", "DW" : 127, 128 : "DX", "DX" : 128, 129 : "DY", "DY" : 129, 130 : "DZ", "DZ" : 130, 131 : "EA", "EA" : 131, 132 : "EB", "EB" : 132, 133 : "EC", "EC" : 133, 134 : "ED", "ED" : 134, 135 : "EE", "EE" : 135, 136 : "EF", "EF" : 136, 137 : "EG", "EG" : 137, 138 : "EH", "EH" : 138, 139 : "EI", "EI" : 139, 140 : "EJ", "EJ" : 140, 141 : "EK", "EK" : 141, 142 : "EL", "EL" : 142, 143 : "EM", "EM" : 143, 144 : "EN", "EN" : 144, 145 : "EO", "EO" : 145, 146 : "EP", "EP" : 146, 147 : "EQ", "EQ" : 147, 148 : "ER", "ER" : 148, 149 : "ES", "ES" : 149, 150 : "ET", "ET" : 150, 151 : "EU", "EU" : 151, 152 : "EV", "EV" : 152, 153 : "EW", "EW" : 153, 154 : "EX", "EX" : 154, 155 : "EY", "EY" : 155, 156 : "EZ", "EZ" : 156, 157 : "FA", "FA" : 157, 158 : "FB", "FB" : 158, 159 : "FC", "FC" : 159, 160 : "FD", "FD" : 160, 161 : "FE", "FE" : 161, 162 : "FF", "FF" : 162, 163 : "FG", "FG" : 163, 164 : "FH", "FH" : 164, 165 : "FI", "FI" : 165, 166 : "FJ", "FJ" : 166, 167 : "FK", "FK" : 167, 168 : "FL", "FL" : 168, 169 : "FM", "FM" : 169, 170 : "FN", "FN" : 170, 171 : "FO", "FO" : 171, 172 : "FP", "FP" : 172, 173 : "FQ", "FQ" : 173, 174 : "FR", "FR" : 174, 175 : "FS", "FS" : 175, 176 : "FT", "FT" : 176, 177 : "FU", "FU" : 177, 178 : "FV", "FV" : 178, 179 : "FW", "FW" : 179, 180 : "FX", "FX" : 180, 181 : "FY", "FY" : 181, 182 : "FZ", "FZ" : 182, 183 : "GA", "GA" : 183, 184 : "GB", "GB" : 184, 185 : "GC", "GC" : 185, 186 : "GD", "GD" : 186, 187 : "GE", "GE" : 187, 188 : "GF", "GF" : 188, 189 : "GG", "GG" : 189, 190 : "GH", "GH" : 190, 191 : "GI", "GI" : 191, 192 : "GJ", "GJ" : 192, 193 : "GK", "GK" : 193, 194 : "GL", "GL" : 194, 195 : "GM", "GM" : 195, 196 : "GN", "GN" : 196, 197 : "GO", "GO" : 197, 198 : "GP", "GP" : 198, 199 : "GQ", "GQ" : 199, 200 : "GR", "GR" : 200, 201 : "GS", "GS" : 201, 202 : "GT", "GT" : 202, 203 : "GU", "GU" : 203, 204 : "GV", "GV" : 204, 205 : "GW", "GW" : 205, 206 : "GX", "GX" : 206, 207 : "GY", "GY" : 207, 208 : "GZ", "GZ" : 208, 209 : "HA", "HA" : 209, 210 : "HB", "HB" : 210, 211 : "HC", "HC" : 211, 212 : "HD", "HD" : 212, 213 : "HE", "HE" : 213, 214 : "HF", "HF" : 214, 215 : "HG", "HG" : 215, 216 : "HH", "HH" : 216, 217 : "HI", "HI" : 217, 218 : "HJ", "HJ" : 218, 219 : "HK", "HK" : 219, 220 : "HL", "HL" : 220, 221 : "HM", "HM" : 221, 222 : "HN", "HN" : 222, 223 : "HO", "HO" : 223, 224 : "HP", "HP" : 224, 225 : "HQ", "HQ" : 225, 226 : "HR", "HR" : 226, 227 : "HS", "HS" : 227, 228 : "HT", "HT" : 228, 229 : "HU", "HU" : 229, 230 : "HV", "HV" : 230, 231 : "HW", "HW" : 231, 232 : "HX", "HX" : 232, 233 : "HY", "HY" : 233, 234 : "HZ", "HZ" : 234, 235 : "IA", "IA" : 235, 236 : "IB", "IB" : 236, 237 : "IC", "IC" : 237, 238 : "ID", "ID" : 238, 239 : "IE", "IE" : 239, 240 : "IF", "IF" : 240, 241 : "IG", "IG" : 241, 242 : "IH", "IH" : 242, 243 : "II", "II" : 243, 244 : "IJ", "IJ" : 244, 245 : "IK", "IK" : 245, 246 : "IL", "IL" : 246, 247 : "IM", "IM" : 247, 248 : "IN", "IN" : 248, 249 : "IO", "IO" : 249, 250 : "IP", "IP" : 250, 251 : "IQ", "IQ" : 251, 252 : "IR", "IR" : 252, 253 : "IS", "IS" : 253, 254 : "IT", "IT" : 254, 255 : "IU", "IU" : 255, 256 : "IV", "IV" : 256, }
    
    
    class __Annot_Reader():
        def __init__(self, src=None, dest=None, sheet=0, visible=False, \
                 load_filepath=None):
            """
            Initializes an instance of the Annot_Reader class.
                
            :param self: An instance of the __Annote_Reader class.
            :param src: The filepath for the original genome annotation
            :param dest: The filepath for the modified genome annotation
            :param sheet: The excel sheet to grab
            :param visible: Param indicating if sheet is visible
            :param load_filepath: The filepath of the job to load
            """
            # Class instance variables
            self.df = None      
            self.app = None
            self.book = None
            self.wks = None
            self.ws = None
            self.src = src
            self.dest = dest
            self.sheet = sheet
            self.header = {}
            self.function = {}
            self.nt_seq = {}
            self.cols = {}
            self.rows = set(())
            self.visible = False
            
            if load_filepath is not None:
                self.load_job(load_filepath)
            else:
                self.open(src, dest, sheet, visible)
            
        
        def __del__(self):
            """
            Destroys an instance of the __Annote_Reader class.
            
            :param self: An instance of the Annot_Reader class.
            """
            dirpath = currentdir + '\\saved_jobs\\'
            filename = 'autosave_job.txt'
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
            path = dirpath + filename
            if len(self.rows) > 0:
                self.save_job(path)
            self.close()
                        
            
        def __str__(self):
            """
            Converts the instance of the __Annote_Reader class to a string
            
            :param self: The on instance of the singleton class.
            """
            return self.dest
                            
                
        def close(self):
            """
            Closes the excel file.
            
            :param self: An instance of the Annot_Reader class.
            """
            # Close the book and the app
            if self.book is not None:
                #Save
                self.book.save(self.dest)
                book = self.book
                self.book = None
                book.close()
            if self.app is not None:
                app = self.app
                self.app = None
                app.quit()
            # Init all vars to None    
            self.df = None      
            self.app = None
            self.book = None
            self.wks = None
            self.ws = None
            self.src = None
            self.dest = None
            self.sheet = None
            self.header = {}
            self.function = {}
            self.nt_seq = {}
            self.cols = {}
            
            
        def load_job(self, filepath):
            """
            Loads a job from file
            
            :param self: An instance of the __Annote_Reader class
            :param filepath: The filepath of the job to load
            """
            # Validate the results
            f = open(filepath, 'r')
            txt = f.read()
            f.close()
            txt = txt.split("\n")
            src = txt[0].strip()
            dest = txt[1].strip()
            sheet = int(txt[2].strip())
            visible = False
            if txt[3].strip() == "True":
                visible = True   
            for i in range(3, len(txt)):
                if len(txt[i]) > 0 and txt[i][0].isdigit():
                    row = str(txt[i].strip())
                    row = int(row)
                    self.rows.add(row)
            self.open(src, dest, sheet, visible)
                
                
        def open(self, src, dest, sheet, visible):
            """
            Opens an instance of the Annot_Reader class and initializes 
            instance variables.
            
            :param self: An instance of the __Annote_Reader class.
            :param src: The filepath to the source file
            :param dest: The filepath to the destination filepath
            :sheet: The sheet to read
            :param visible: Param indicating if sheet is visible
            """
            self.visible = visible
            if src != dest:
                # Create the new file dest
                if os.path.isfile(dest):
                    os.remove(dest)
                # Now copy the file
                shutil.copyfile(src, dest)
                if not os.path.isfile(src):
                    raise Exception("Could not create file " + dest)
            # Read the file with pandas
            self.df = pd.read_excel(dest)        
            self.app = xw.App(visible=visible)
            self.book = xw.Book(dest)
            self.wks = xw.sheets
            self.ws = self.wks[sheet]
            for r in range(self.df.shape[0]):
                for c in range(self.df.shape[1]):
                    cell = str(Annot_Reader.col_labels[c+1]) + str(r+1)
                    cell = str(cell)
                    val = self.ws.range(cell).value
                    if val == "function":
                        self.cols['function'] = Annot_Reader.col_labels[c + 1]
                        self.header["start row"] = r + 1
                    if val == "nucleotide_sequence":
                        self.cols['nucleotide_sequence'] \
                            = Annot_Reader.col_labels[c + 1]
                            
    
        def save_job(self, filepath):
            """
            Saves the progress of the current working job.
            
            :param self: An instance of the Annot_Reader class
            :param filepath: The filepath to save the job to.
            """
            if self.src is None or self.dest is None or self.sheet is None:
                return 
            f = open(filepath, 'w')
            f.write(self.src)
            f.write("\n")
            f.write(self.dest)
            f.write("\n")
            f.write(str(self.sheet))
            f.write("\n")
            f.write(str(self.visible))
            f.write("\n")
            for row in self.rows:
                f.write(str(row))
                f.write("\n")
            f.close()
                   
                   
    instance = None
    
    def __init__(self, src=None, dest=None, sheet=0, visible=False, \
                 load_filepath=None):
        """
        Initializes an instance of the Annot_Reader class.
            
        :param self: An instance of the Annote_Reader class.
        :param src: The filepath for the original genome annotation
        :param dest: The filepath for the modified genome annotation
        :param sheet: The excel sheet to grab
        :param visible: Param indicating if sheet is visible
        :param load_filepath: The filepath of the job to load
        """
        if Annot_Reader.instance is not None:
            del(Annot_Reader.instance)
        Annot_Reader.instance = Annot_Reader.__Annot_Reader(src, dest, sheet, visible, load_filepath)
            
            
    def __del__(self):
        """
        Destroys an instance of the __Annote_Reader class.
            
        :param self: An instance of the Annot_Reader class.
        """
        path = 'C:\\Users\\1985937\\Documents\\BI_Sum_2021\\EC-Scrape\\'
        path += 'saved_jobs\\autosave_job.txt'
        if Annot_Reader.instance is not None:
            if Annot_Reader.instance is not None \
            and len(self.instance.rows) > 0:
                Annot_Reader.instance.save_job(path)
            Annot_Reader.instance.close()
            
    
    def __getattr__(self, name):
        """
        Overloaded python function of attribute accessing
        
        :param self: The instance of the Annot_Reader
        :param name: The attribute to access.
        """
        return getattr(self.instance, name)
        
        
    def compile_rows(self, keywords):
        """
        Compiles a list of rows to blast.
        
        :param self: The instance of the Annot_Reader
        :param keywords: The keywords to match on
        """
        for ind in self.instance.df.index:
            entry = self.instance.df['function'][ind]
            if Annot_Reader.matches_keywords(entry, keywords) \
            and not Annot_Reader.has_ec(entry):
                self.rows.add(ind)
        
        
    @staticmethod
    def has_ec(word):
        """
        Determines if a string has an EC number contained in it. This 
        function looks for the following string patterns.
            
        :param word: A string to determine if is an EC number or not.
        """
        word = word.strip()
        word = word.lower()
        words = word.split(" ")
        # Search for "ec" keyword
        for i in range(len(words)):
            if words[i] == "ec" and len(words) > i:
                if Annot_Reader.is_ec(words[i+1]):
                    return True
            if words[i] == "ec:" and len(words) > i:
                if Annot_Reader.is_ec(words[i+1]):
                    return True
            if words[i] == "(ec" and len(words) > i:
                if Annot_Reader.is_ec(words[i+1]):
                    return True
            if words[i] == "(ec:" and len(words) > i:
                if Annot_Reader.is_ec(words[i+1]):
                    return True
        return False
        
        
    @staticmethod
    def is_ec(word):
        """
        Determines if 'word' is an ec number or not.
            
        :param word: A string to determine if is an EC number or not.
        """
        word = word.strip()
        # Remove '(' characters
        s = 0
        while s != -1:
            s = word.find("(")
            if s != -1:
                if s < len(word) - 2:
                    word = word[s+1:]
                else:
                    word = word[:s]
        # Remove ')' characters
        s = 0
        while s != -1:
            s = word.find(")")
            if s != -1:
                if s < len(word) - 2:
                    word = word[s+1:]
                else:
                    word = word[:s]
            
        # The string must be non-empty
        if len(word) == 0:
            return False
        # Must be a single word
        if word.find(" ") != -1:
            return False
        # First character must be a digit
        if not word[0].isdigit():
            return False
        # Must have 3 periods
        if word.count('.') != 3:
            return False
        # The last character must be a digit or -
        if not word[len(word)-1].isdigit() and word[len(word)-1] != '-':
            return False
        # Make sure digits seperate the periods
        if word.find("..") > 0:
            return False
        # Make sure every character is either a digit, -, or .
        for i in word:
            if i.isdigit():
                pass
            elif i == '-':
                pass
            elif i == '.':
                pass
            else:
                return False
        return True
        
        
    @staticmethod
    def matches_keywords(txt, keywords):
        """
        Determines if 'txt' matches a list of keywords given it. Keywords is 
        a list of dictionaries containing 2 values. The "Not" entry value 
        is used to indicate if a string is expected to have the keyword or 
        not, while the "Keyword" entry value is the keyword itself.
        
        :param txt: The string to match the keywords to
        :param keywords: The keywords to search for in txt as a list of 
                         tuples.
        """
        txt = txt.lower()
        for key in keywords:
            temp = txt.split(" ")
            found = (txt.find(key['Keyword'].lower()) != -1)
            if found == key['Not']:
                return False
        return True
        
        
    def read(self, row, col):
        """
        Read and returns a value from the loaded excel sheet.
        
        :param self: An instance of the Annot_Reader class
        :param row: The row to read
        :param col: The column to read
        """
        return self.df[col][row]
        
        
    def save_job(self, filepath):
        """
        Saves the progress of the current working job.
        
        :param self: An instance of the Annot_Reader class
        :param filepath: The filepath to save the job to.
        """
        self.instance.save_job(filepath)
        
        
    def write(self, val, row, col):
        """
        Writes a value to the loaded excel sheet.
        
        :param self: An instance of the Annot_Reader class
        :param val: The value to write
        :param row: The row to read
        :param col: The column to read
        """
        cell = self.instance.cols[col] + \
            str(row + self.header['start row'] + 1)
        cell = str(cell)
        self.instance.ws.range(cell).value = val
        #Save
        self.instance.book.save(self.dest)