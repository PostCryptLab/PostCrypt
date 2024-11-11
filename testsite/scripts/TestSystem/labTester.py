# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import nbformat as nbformat
import sys
import glob
import types

test_info = []
students_info = []
test_names = []

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Bad arguments")
        exit()

    # master_nb_name = "McEliece"

    master_nb_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "helloworld")

    isSingleNb = False

    dir_name = sys.argv[1]
    if not os.path.isdir(sys.argv[1]):
        isSingleNb = True

    master_nb_path = master_nb_name + "_private.ipynb"
    master_nb = nbformat.read(master_nb_path, as_version=4)

    for cell in master_nb["cells"]:
        metadata = cell['metadata']
        if "cell_type" in metadata and metadata["cell_type"] == "test":
            # print(metadata)
            test_names.append(metadata["cell_name"])
            test_info.append([0, 0, 0])

        if cell["cell_type"] == "code":
            try:
                exec(cell['source'])
            except:
                print("Failed to execute cell: ")
                print(cell["code"])

    tests_func = []
    for name in test_names:
        eval(f"tests_func.append({name})")

    if isSingleNb:
        nb_names = [dir_name]
    else:
        nb_names = glob.glob(f"{dir_name}/*.ipynb")

    if not isSingleNb:
        print("Students summary: ")
    else:
        print("Student test summary: ")

    for student_idx, file_name in enumerate(nb_names):
        try:

            nb = nbformat.read(file_name, as_version=4)
            cells = nb['cells']
            for cell in cells:
                metadata = cell['metadata']
                # print(cell)
                if cell['cell_type'] == "code":
                    try:
                        exec(cell['source'])
                    except RuntimeError as e:
                        print("Failed to execute cell: ")

                        print(cell["code"])
                        # TODO cell replacement
                        # if "cell_name" in metadata["cell"]:
                        #     print("Try to replace cell")

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

    if not isSingleNb:
        print("Tests summary: ")
        for i, test in enumerate(test_info):
            print(f"{test_names[i]}: Successes-{test[0]}, Failed-{test[1]}, Skipped-{test[2]}")
else:
    print(__name__)