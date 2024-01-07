#!/usr/bin/env python
# coding: utf-8

import azuremessage_pb2
import pandas as pd
from tabulate import tabulate


def PromptForField(azuremessage):
    """This creates a new azuremessage within an existing AzureMessageStack object"""
    azuremessage.name = input("Enter a name: ")
    azuremessage.id = int(input("Enter ID: "))
    azuremessage.subscription = input("Enter subscription: ")
    azuremessage.sku = input("Enter SKU: ")
    azuremessage.reservation = input("Enter Reservation: ")


def AddMessage(messagestack):
    PromptForField(messagestack.azuremessage.add())


def WriteMessageStack(messagestack):
    with open("./binfile/azuremessagestack.bin", "wb") as file:
        file.write(messagestack.SerializeToString())


def ReadMessageStack():
    with open("./binfile/azuremessagestack.bin", "rb") as file:
        outobj = azuremessage_pb2.AzureMessageStack()
        outobj.ParseFromString(file.read())
    return outobj


def DisplayMessageStack(message_stack):
    for item in message_stack.azuremessage:
        print(f"Name: {item.name}")


def CreatePandasFrame(messagestack):
    data = []
    for azure_message in messagestack.azuremessage:
        data.append(
            {
                "id": azure_message.id,
                "name": azure_message.name,
                "subscription": azure_message.subscription,
                "sku": azure_message.sku,
                "reservation": azure_message.reservation,
            }
        )

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


def DisplayTabulatedData(df):
    print(tabulate(df, headers="keys", tablefmt="grid"))
