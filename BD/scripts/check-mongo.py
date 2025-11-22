from BD.services import MongoDBService

def main():
    db = MongoDBService().db

    # Show O*NET raw counts
    occ_count = db["onet_occupation_data"].count_documents({})
    print("Total O*NET occupations:", occ_count)

    # Now test app-level collections
    print("\n------ APP ROLES ------")
    print("Total roles:", db["roles"].count_documents({}))
    print("Sample:", db["roles"].find_one())

    print("\n------ APP SKILLS ------")
    print("Total skills:", db["skills"].count_documents({}))
    print("Sample:", db["skills"].find_one())

if __name__ == "__main__":
    main()
