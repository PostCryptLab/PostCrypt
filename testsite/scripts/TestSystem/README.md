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

"code" cell could contain implemented blocks.
<Code>#Implement...#End</Code> 
This blocks is missing in public notebook version and have to be implemented. 

Example intro cell:
<Code>
#Config
CELLNAME="student_info"
CELLTYPE="student_info"
#End
#Student musi uzupełnić poniższe danne, w przypadku braku/błedu w nr albuma praca studenta nie zostanie zaliczona.
#Prosimy uzupełniać kod wyłącznie w wyznaczonych komórkach z komentarzem Implement me.
NAME=""
NRALBUM=""
</Code>

Example config for a code cell:
<Code>
#Config
CELLNAME=""
CELLTYPE="code"
#End
</Code>

Example config for a test cell:
<Code>
#Config
CELLTYPE="test"
CELLNAME="< a test function name>"
TESTCELL=""
VISIBLE=False
#End
</Code>
