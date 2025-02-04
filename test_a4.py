import unittest
import uuid
import os
import shutil
import subprocess
import stat
import grp
import time

def copyFiles(destination, files_list, executable):
    for file in files_list:
        if os.path.isfile(file) : 
            shutil.copy(file,destination)
            if executable:
                new_filename = destination + "/" + file;
                os.system("chmod +x " + new_filename)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        set_of_tests = {"part1" : {"fut" : "script4_1.sh", "aux" :["rand_data.csv"]},
                        "part2" : {"fut" : "script4_2.sh", "aux" :["suspect.txt","processed.txt"]},
                        "part3" : {"fut" : "script4_3.sh", "aux" :["start_process_tree.sh"]}}
        cls.test = set_of_tests
        #Create temp directory
        uidString = str(uuid.uuid4()) 
        cls.test_directory = "/tmp/Assignment4_"+uidString;
        os.mkdir(cls.test_directory)
        print("The test directory is :" + cls.test_directory)
        
        #check shell
        cls.shell = "/usr/bin/bash"
        cls.assertTrue(os.path.isfile(cls.shell), "/usr/bin/bash not found." + 
           "Operating System may not be correct. Consider using Cloud 9")
        
        #copy files to temp directory
        for test in set_of_tests:
            shutil.copy(cls.test[test]["fut"],cls.test_directory)
            for file in cls.test[test]["aux"]:
                if os.path.isfile(file):
                    shutil.copy(file,cls.test_directory)
                    new_filename = cls.test_directory +"/" + file
                else:                    
                    assert("Setup failed, file" + "Does not exist")
                    
        os.chdir(cls.test_directory)
    
    @classmethod
    def tearDown(cls):
        #shutil.rmtree(cls.test_directory)
        pass
    
        
        
    def test_script4_1(self):
         
        test_script = self.test["part1"]["fut"]
        print(f"testing {test_script}")
        #run script
        cpi = subprocess.run(["/usr/bin/bash", test_script, "rand_data.csv","4"], capture_output=True, text=True)
        print("Output to stdout")
        print(cpi.stdout)
        print("Output to stderr")
        print(cpi.stderr)
        
        expected = ["First Name,Last Name,Adjusted Score",
                    "YoYo,Rubics,90.21",
                    "Mariko,Sama,73.92",
                    "Nakajima,Rocky,71.38",
                    "Francheska,Frita,66.43"]
        
        output = cpi.stdout.strip().split("\n")
        self.assertTrue(len(expected) == len(output),"Output not the correct length")
        for line_num in range(len(output)):
            self.assertTrue(output[line_num] == expected[line_num], 
                            "output does not match expected output")
    
    def test_script4_2(self):
        test_script = self.test["part2"]["fut"]        
        print(f"testing {test_script}")
        self.assertTrue(test_script,"Script not found")
        
        #run script
        cpi = subprocess.run(["/usr/bin/bash", test_script, self.test["part2"]["aux"][0],
                              self.test["part2"]["aux"][1],], capture_output=True, text=True)
        print("Output to stdout")
        print(cpi.stdout)
        print("Output to stderr")
        print(cpi.stderr)

        expected = ["2367",
                    "2126",
                    "1111"]
        output = cpi.stdout.strip().split("\n")
        self.assertTrue(len(expected) == len(output),"Output not the correct length")
        for line in expected:
            occurances = output.count(line)
            self.assertTrue(output.count(line) == 1,  f"{line} has {occurances} when there should be 1")
            

    def test_script4_3(self):
        test_script = self.test["part3"]["fut"]
        print(f"testing {test_script}")
        for data_file in self.test["part3"]["aux"]:
            self.assertTrue(os.path.isfile(data_file),"Data file not found")
        
        #1.start background process
        running_script = subprocess.Popen(["bash","start_process_tree.sh"])
        parent_id = running_script.pid
        print("The parent id is:" + str(parent_id))
        #bad practice, but wait for 1 second before checking continueing.
        #otherwise next line runs before all processes are created.

        print("Sleeping for a second")
        time.sleep(1)
        
        #2.get list of backgroun processes
        #capture process id of children process.
        cpi = subprocess.run(["ps","-f","--ppid",str(parent_id)], capture_output=True, text=True)
        block = cpi.stdout.strip().split("\n")
        table = [];
        for line in block[1:]:
            row = line.split()
            id_idx = 1
            cmd_idx = 7
            arg1_idx = 8
            arg2_idx = 9
            if(len(row) > 9):
                row = [row[id_idx], row[cmd_idx]+ " " + row[arg1_idx] + " " + row[arg2_idx]]
                table.append(row);

        #run user script
        cpi = subprocess.run(["/usr/bin/bash",test_script,str(parent_id)], capture_output=True, text=True);
        print("stdout:")
        user_output = cpi.stdout
        print(user_output)
        
        print("stderr:")
        print(cpi.stderr)
        #check if processes have been terminated
        for process in table:
            print("checking process " + process[0])
            output = subprocess.run(["ps", "--pid" , str(process[0]) ], capture_output = True, text = True)
            data = output.stdout.strip().split("\n")            
            self.assertTrue(len(data) == 1,"Process: " + str(process[0]) + " was not terminated for command " + process[1])
        
        #check if parent still exists
        parent = subprocess.run(["ps", "-l","--pid" , str(parent_id) ], capture_output = True, text = True)        
        rows = parent.stdout.strip().split("\n")
        self.assertTrue(len(rows) > 1,"Parent process was terminated")

        #check for zombie state
        data = rows[1].split(" ")
        self.assertTrue(data[1] != "Z", "Parent process was terminated")
        
        
        
        
        #check output
        lineTable = user_output.strip().split("\n")
        userTable = {} #look up table for process ids
        for line in lineTable:
            row = line.split(",")
            userTable[str(row[0]).strip()] = row
        
        for process in table:
            key = str(process[0]).strip() 
            if  key in userTable:
                self.assertTrue(len(userTable[key]) > 1 , "Something is wrong with the format of your table")
                self.assertTrue(userTable[key][1] == process[1],"Commands do not match for process." +
                "Your command: " + userTable[key][1] +". Expected: " + process[1])
            else:
                self.assertTrue(False,"Did not find process id" + str(process[0]) + " in table for command" + process[1])
        
        
        running_script.kill()
        outs, errs = running_script.communicate()
        time.sleep(1)

if __name__ == '__main__':
   unittest.main()