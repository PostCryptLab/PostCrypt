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

    # print(metadata)
    if not is_visible:
        return ""
    return new_code_cell


if __name__ == '__main__':
    master_nb_path = "helloworld.ipynb"
    master_nb = nbformat.read(master_nb_path, as_version=4)
    master_nb_private = copy.deepcopy(master_nb)

    for i, cell in enumerate(master_nb["cells"]):
        metadata = cell['metadata']
        # print(metadata)
        if cell['cell_type'] == 'code':
            try:
                cell["source"] = process_code_block(cell["source"], cell['metadata'])
                master_nb_private["cells"][i]["metadata"] = copy.deepcopy(cell['metadata'])
                # print(metadata)
                # print(master_nb_private["cells"][i]["metadata"])
                if cell["source"] == "":
                    pass
                    # master_nb["cells"].remove(cell)
            except:
                pass
        # master_nb_private["cells"][i]["metadata"] = cell['metadata']

    nbformat.write(master_nb_private, "helloworld_private.ipynb", version=4)

    for i, cell in enumerate(master_nb["cells"]):
        # print(cell)
        if cell["cell_type"] == "code" and cell["source"] == "":
            master_nb["cells"].remove(cell)
        # print(cell["metadata"])

    nbformat.write(master_nb, "helloworld_pub.ipynb", version=4)



