import messagestack as ms
import azuremessage_pb2

azuremessage = azuremessage_pb2.AzureMessage()
messagestack = azuremessage_pb2.AzureMessageStack()

for i in range(3):
    ms.AddMessage(messagestack)

ms.WriteMessageStack(messagestack)