""" This will retrieve the contents of the local files/azuremessagestack.bin and display as a pandas dataframe, formatted
    into a terminal friendly table."""

import messagestack as ms

newobj = ms.ReadMessageStack()
print(ms.CreatePandasFrame(newobj))
