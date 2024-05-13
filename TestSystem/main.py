# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import nbformat as nbformat
import sys

tests = []
test_names = []
test_run = ""

def tests_run(tests_func):
    success_cnt, fail_cnt, skip_cnt = 0,0,0
    for i, test in enumerate(tests_func):
        print()
        try:
            test()
            success_cnt+=1
        except AssertionError as e:
            fail_cnt += 1
        except RuntimeError:
            skip_cnt += 1

    print(f"Summary: Success-{success_cnt}/{len(tests_func)}, Failed-{fail_cnt}/{len(tests_func)}, Skipped-{skip_cnt}/{len(tests_func)}")
    return success_cnt, fail_cnt, skip_cnt


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nb = nbformat.read('helloworld.ipynb', as_version=4)
    print(nb)
    cells = nb['cells']
    for cell in cells:
        metadata = cell['metadata']
        print(metadata)
        if "test" in metadata and metadata["test"] == True:
            test_names.append(metadata['test_name'])
            tests.append(cell['source'])
        elif "test_run" in metadata and metadata["test_run"] == True:
            test_run = cell['source']

        elif cell['cell_type'] == "code":
            # try:
            exec(cell['source'])
            # except:
            #     pass

    # exec(tests)
    tests_func = []
    for test in tests:
        exec(test)
    for name in test_names:
        exec(f"tests_func.append({name})")
    print(tests_func)
    tests_run(tests_func)
