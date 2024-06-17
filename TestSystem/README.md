Cell Config Documentation

Cell config at the beggining of the cell always opens with #Config and ends with #End

#Config
...
#End

Possible config fields
- CELLNAME (cell id)
- CELLTYPE (could be "student_info", "code" or "test")
- TESTCELL (test config, contains "code" cell id. This test starts immediatly after execution "code" cell with this id) WORK IN PROGRESS
- VISIBLE (test config, could be True of False. If True is selected, this "test" cell remains in public notebook)

"student_info" cell contains additional information fields such as:
- NAME
- NRALBUM

