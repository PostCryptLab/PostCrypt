import copy

import nbformat as nbformat

def process_code_block(code, metadata):
    new_code_cell = ""
    is_config = False
    is_implement = False
    is_visible = True
    config = ""
    offset = ""
    for line in code.split("\n"):
        # print(line)
        if "#Config" in line:
            config = ""
            is_config = True
            continue
        if "#Implement" in line:
            offset = line.split("#Implement")[0]
            is_implement = True
            continue

        if "#End" in line:
            if is_config:
                is_config = False
                for conf in config.split("\n"):
                    record = conf.split("=")
                    if record[0] == "CELLTYPE":
                        metadata["cell_type"] = record[1].strip("\"")
                    if record[0] == "CELLNAME":
                        metadata["cell_name"] = record[1].strip("\"")
                    if record[0] == "TESTCELL":
                        metadata["test_cell"] = record[1].strip("\"")
                    if record[0] == "VISIBLE":
                        if record[1] == "False":
                            is_visible = False

            if is_implement:
                is_implement = False
                new_code_cell += offset + "#Implement me\n" + offset + "raise NotImplementedError"
            continue

        if is_config:
            config += line + "\n"
            continue
        if is_implement:
            continue

        new_code_cell += line + "\n"

    if not is_visible:
        return ""
    return new_code_cell

def format_notebook(input_path, lab_name):
    """Format a notebook and create public/private versions."""
    master_nb = nbformat.read(input_path, as_version=4)
    master_nb_private = copy.deepcopy(master_nb)

    for i, cell in enumerate(master_nb["cells"]):
        if cell['cell_type'] == 'code':
            try:
                cell["source"] = process_code_block(cell["source"], cell['metadata'])
                master_nb_private["cells"][i]["metadata"] = copy.deepcopy(cell['metadata'])
            except:
                pass

    # Create private version
    private_path = f"{lab_name}_private.ipynb"
    nbformat.write(master_nb_private, private_path, version=4)

    # Remove empty cells and create public version
    master_nb["cells"] = [cell for cell in master_nb["cells"] 
                         if not (cell["cell_type"] == "code" and cell["source"] == "")]
    public_path = f"{lab_name}_pub.ipynb"
    nbformat.write(master_nb, public_path, version=4)
    
    return public_path, private_path

if __name__ == '__main__':
    nb_name = "helloworld"
    master_nb_path = nb_name + ".ipynb"
    format_notebook(master_nb_path, nb_name)



