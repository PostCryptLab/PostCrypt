# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import nbformat as nbformat
# import sys
import glob
import types

test_info = []
students_info = []
test_names = []

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    master_nb_path = "helloworld.ipynb"
    master_nb = nbformat.read(master_nb_path, as_version=4)

    for cell in master_nb["cells"]:
        metadata = cell['metadata']
        if "cell_type" in metadata and metadata["cell_type"] == "test":
            test_names.append(metadata["test_name"])
            test_info.append([0, 0, 0])
            try:
                exec(cell['source'])
            except:
                print("Failed to execute cell: ")
                print(cell["code"])

    tests_func = []
    for name in test_names:
        eval(f"tests_func.append({name})")

    dir_name = "lab1"
    nb_names = glob.glob(f"{dir_name}/*.ipynb")

    print("Students summary: ")

    for student_idx, file_name in enumerate(nb_names):
        try:

            nb = nbformat.read(file_name, as_version=4)
            cells = nb['cells']
            for cell in cells:
                metadata = cell['metadata']

                if cell['cell_type'] == "code":
                    try:
                        exec(cell['source'])
                    except:
                        print("Failed to execute cell: ")
                        print(cell["code"])

                if "cell_type" in metadata and metadata["cell_type"] == "student_info":
                    code_cell = cell["source"]
                    try:
                        students_info.append([eval("NAME"), eval("NRALBUM")])
                    except:
                        students_info.append(["Failed to read student name", ""])

            success_cnt, fail_cnt, skip_cnt = 0, 0, 0

            for i, test in enumerate(tests_func):
                try:
                    test()
                    success_cnt += 1
                    test_info[i][0] += 1
                    print(f"{test_names[i]} - Success")
                except AssertionError as e:
                    fail_cnt += 1
                    test_info[i][1] += 1
                    print(f"{test_names[i]} - Failed")
                except RuntimeError:
                    skip_cnt += 1
                    test_info[i][2] += 1
                    print(f"{test_names[i]} - Skipped")

            print(
                f"Summary for {students_info[student_idx][0]}: Successes-{success_cnt}/{len(tests_func)},"
                f" Failed-{fail_cnt}/{len(tests_func)}, Skipped-{skip_cnt}/{len(tests_func)}")
        except RuntimeError as e:
            print(f"Error with notebook: {file_name}")

    print("Tests summary: ")
    for i, test in enumerate(test_info):
        print(f"{test_names[i]}: Successes-{test[0]}, Failed-{test[1]}, Skipped-{test[2]}")