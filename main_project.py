import pymongo
from colorama import Fore, Style
from random import randint, choice, sample
from bson import ObjectId
import re
client = pymongo.MongoClient('mongodb://localhost:27017/') #з'єднання з сервером

current_db = client["cats-gallery"]

collection_c = current_db['cats-collection']

list_collection = []

cat_names = ["Whiskers", "Luna","Simba", "Mittens", "Shadow", "Bella", "Oliver", "Ginger", "Luna", "Max", "Cleo", "Tigger",
    "Chloe", "Leo", "Misty", "Felix"]

features = ["любить погріб","муркоче нічим теплише","завжди веселка зранку","завжди під ногами","вірний помічник на кухні",
    "завжди випросить смаколик","майстер камуфляжу","любить крісло більше за все","грає з усім, що рухається","любить поспати на сонці",
    "майстер масажу","вміє відкривати двері","завжди в пошуку пригод","любить кульки-миші","має золотисте серце"]


for i in range(10):
    if collection_c.count_documents({}) == 10:
        break

    cat_obj = {
        "name": choice(cat_names),
        "age": randint(1, 12),
        "features": sample(features, 3)
    }

    collection_c.insert_one(cat_obj)

"""
функція обробки виключень
"""


def printing_collection(coll):
    try:
        coll_data = list(coll.find())
        print(f"\n{Fore.LIGHTYELLOW_EX}>>> All documents in collection - '{coll.name}'{Style.RESET_ALL}")
        count = 1
        if not coll_data:
            print(f"There isn't any document :3 ----> ERROR")
            return []
        else:
            for document in coll_data:
                print(f"\t{count} ---> 📁 {document}")
                count += 1
            return coll_data
    except Exception as e:
        print(f"An error occurred while fetching documents: {e}")
        return None


def finding_object(coll):
    try:
        cat_name = input("Type cat's name: ")
        coll_data = list(coll.find({"name": cat_name}))

        print(f"\n{Fore.LIGHTYELLOW_EX}>>> Result:{Style.RESET_ALL}")

        if not coll_data:
            print(f"{Fore.RED}Cat -'{cat_name}'- not found in the database.{Style.RESET_ALL}")
        else:
            count = 1
            for document in coll_data:
                print(f"\t{count} ---> 📁 {document}")
                count += 1
        return coll_data
    except Exception as e:
        print(f"An error occurred while finding object: {e}")
        return None


def update_info(ex):
    try:
        user_input_number_of_doc = int(input(
            f"\nType the number of document you want to update{Fore.LIGHTGREEN_EX}[To exit print --> exit/close]{Style.RESET_ALL}: "))
        if user_input_number_of_doc <= 0 or user_input_number_of_doc > len(ex):
            print(f"Invalid document number. Please enter a number between 1 and {len(ex)}.")
            return

        document_to_update = ex[user_input_number_of_doc - 1]
        years_to_update = int(input(f"\nYou are changing age for document [№{user_input_number_of_doc}]\n>>> "))
        filter = {"_id": document_to_update["_id"]}
        new_values = {"$set": {"age": years_to_update}}
        if collection_c.update_one(filter, new_values):
            print(f"{Fore.CYAN}Document was updated!{Style.RESET_ALL}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred while updating info: {e}")


def add_new_feature(ex):
    try:
        user_input_number_of_doc = int(input(
            f"\nType the number of document you want to update{Fore.LIGHTGREEN_EX}[To exit print --> exit/close]{Style.RESET_ALL}: "))
        if user_input_number_of_doc <= 0 or user_input_number_of_doc > len(ex):
            print(f"Invalid document number. Please enter a number between 1 and {len(ex)}.")
            return

        document_to_update = ex[user_input_number_of_doc - 1]
        add_new_feature = input(f"\nYou are adding new feature :3 for document [№{user_input_number_of_doc}]\n>>> ")

        current_features = document_to_update.get("features", [])
        current_features.append(add_new_feature)

        filter = {"_id": document_to_update["_id"]}
        new_values = {"$set": {"features": current_features}}

        if collection_c.update_one(filter, new_values):
            print(f"{Fore.CYAN}Document was updated!{Style.RESET_ALL}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred while adding new feature: {e}")


def delete_record(ex):
    try:
        user_input_number_of_doc = int(input(
            f"\nType the number of document you want to delete{Fore.LIGHTGREEN_EX}[To exit print --> exit/close]{Style.RESET_ALL}: "))
        if user_input_number_of_doc <= 0 or user_input_number_of_doc > len(ex):
            print(f"Invalid document number. Please enter a number between 1 and {len(ex)}.")
            return

        document_to_delete = ex[user_input_number_of_doc - 1]

        filter = {"_id": document_to_delete["_id"]}

        if collection_c.delete_one(filter):
            print(f"{Fore.CYAN}Document was deleted!{Style.RESET_ALL}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred while deleting record: {e}")


def delete_all_records(coll):
    try:
        confirmation = input("Are you sure you want to delete all documents? (yes/no): ").lower()
        if confirmation == "yes":
            result = coll.delete_many({})
            print(f"{Fore.RED}----> {result.deleted_count} documents deleted.{Style.RESET_ALL}")
        elif confirmation == "no":
            print("Deletion cancelled.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    except Exception as e:
        print(f"An error occurred while deleting all records: {e}")


print("Hello! Welcome to Cats gallery :)")
while True:
    user_input = input("\n1.Exit/close\n2.Show all records\n3.Find a cat\n"
          "4.Update cat's age\n5.Add new feature for cat\n6.Delete cat's record\n7.Delete all records\n>>> ")
    if user_input == "1":
        print("Goodbye! Have a nice day :)")
        break

    if user_input == "2":
        printing_collection(collection_c)

    if user_input == "3":
        finding_object(collection_c)

    if user_input == "4":
        ex = finding_object(collection_c)
        if len(ex) != 0:
            update_info(ex)
        else:
            break
    if user_input == "5":
        ex = finding_object(collection_c)
        if len(ex) != 0:
            add_new_feature(ex)
        else:
            break

    if user_input == "6":
        ex = finding_object(collection_c)
        if len(ex) != 0:
            delete_record(ex)
        else:
            break

    if user_input == "7":
        ex = printing_collection(collection_c)
        if len(ex) != 0:
            delete_all_records(collection_c)
        else:
            break




