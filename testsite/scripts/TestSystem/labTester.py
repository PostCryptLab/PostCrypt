# This is a sample Python script.
import os.path
import nbformat
import sys
import glob
import types
import numpy as np
import math

class LabTester:
    def __init__(self, lab_name, test_dir=None):
        if test_dir is None:
            self.base_dir = os.path.dirname(lab_name)
            self.lab_name = os.path.basename(os.path.dirname(lab_name))
        else:
            self.base_dir = test_dir
            self.lab_name = lab_name
        self.test_dir = test_dir
        self.test_info = []
        self.students_info = []
        self.test_names = []
        self.tests_func = []
        
    def run_tests(self, single_lab_path = None):
        # Get the base directory - either test_dir or the directory of the lab file

        # Look for master notebook in the base directory
        master_nb_path = os.path.join(self.base_dir, f"{self.lab_name}_private.ipynb")
        
        # Read and execute master notebook
        master_nb = nbformat.read(master_nb_path, as_version=4)

        # Extract tests from master notebook
        for cell in master_nb["cells"]:
            metadata = cell['metadata']
            if "cell_type" in metadata and metadata["cell_type"] == "test":
                self.test_names.append(metadata["cell_name"])
                self.test_info.append([0, 0, 0])

            if cell["cell_type"] == "code":
                # print(cell['source'])
                try:
                    exec(cell['source'])
                except Exception as e:
                    print("Failed to execute cell")
                    print(e)

        # Collect test functions
        for name in self.test_names:
            eval(f"self.tests_func.append({name})")

        results = []
        
        if self.test_dir is None:
            if single_lab_path is None:
                raise SyntaxError("Wrong argument expression there is no path to single labolatory")
            # Single notebook testing
            return self._test_notebook(single_lab_path)
        else:
            # Get all notebooks in directory except private and public versions
            nb_names = glob.glob(f"{self.test_dir}/*.ipynb")
            nb_names = [nb for nb in nb_names if not (
                nb.endswith('_private.ipynb') or 
                nb.endswith('_pub.ipynb')
            )]
            
            # Test each notebook
            for student_idx, file_name in enumerate(nb_names):
                result = self._test_notebook(file_name)
                if result:
                    results.append(result)
                    
        return results

    def _test_notebook(self, file_name):
        try:
            nb = nbformat.read(file_name, as_version=4)
            cells = nb['cells']
            student_info = ["Unknown", ""]
            
            # Execute cells and collect student info
            for cell in cells:
                metadata = cell['metadata']
                if cell['cell_type'] == "code":
                    try:
                        exec(cell['source'], globals())
                    except Exception as e:
                        print(cell['source'])
                        print("Failed to execute cell2", e)

                if "cell_type" in metadata and metadata["cell_type"] == "student_info":
                    try:
                        student_info = [eval("NAME"), eval("NRALBUM")]
                    except:
                        student_info = ["Failed to read student name", ""]

            # Run tests
            success_cnt, fail_cnt, skip_cnt = 0, 0, 0
            test_results = []

            for i, test in enumerate(self.tests_func):
                try:
                    test()
                    success_cnt += 1
                    self.test_info[i][0] += 1
                    test_results.append((self.test_names[i], "Success"))
                except AssertionError:
                    fail_cnt += 1
                    self.test_info[i][1] += 1
                    test_results.append((self.test_names[i], "Failed"))
                except RuntimeError or NotImplementedError:
                    skip_cnt += 1
                    self.test_info[i][2] += 1
                    test_results.append((self.test_names[i], "Skipped"))

            
            return {
                'student_name': student_info[0],
                'student_id': student_info[1],
                'file_name': os.path.basename(file_name),
                'success_count': success_cnt,
                'fail_count': fail_cnt,
                'skip_count': skip_cnt,
                'total_tests': len(self.tests_func),
                'test_results': test_results
            }

        except Exception as e:
            print(f"Error with notebook: {file_name}", e)
            return None

    def get_test_summary(self):
        return [(self.test_names[i], *self.test_info[i]) 
                for i in range(len(self.test_names))]

# Maintain compatibility with command line usage
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Bad arguments")
        exit()

    dir_name = sys.argv[1]
    is_single_nb = not os.path.isdir(sys.argv[1])
    
    tester = LabTester("helloworld", None if is_single_nb else dir_name)
    results = tester.run_tests()
    
    if is_single_nb:
        print("Student test summary: ")
    else:
        print("Students summary: ")
        
    for result in results:
        if result:
            print(f"Summary for {result['student_name']}: "
                  f"Successes-{result['success_count']}/{result['total_tests']}, "
                  f"Failed-{result['fail_count']}/{result['total_tests']}, "
                  f"Skipped-{result['skip_count']}/{result['total_tests']}")
    
    if not is_single_nb:
        print("\nTests summary: ")
        for name, success, failed, skipped in tester.get_test_summary():
            print(f"{name}: Successes-{success}, Failed-{failed}, Skipped-{skipped}")