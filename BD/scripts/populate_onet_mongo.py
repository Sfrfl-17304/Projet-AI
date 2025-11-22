# BD/scripts/populate_onet_mongo.py
from pathlib import Path
from typing import Dict
import csv

from pymongo import MongoClient
from BD.config import MONGO_URL, MONGO_DB_NAME

# Folder that contains all the O*NET *.txt files
# Adjust if your folder name is slightly different.
DATA_DIR = Path(__file__).resolve().parents[1] / "txt" / "OnsetDATA"

# Map file name -> MongoDB collection name
FILE_MAP: Dict[str, str] = {
    "Occupation Data.txt": "onet_occupation_data",
    "Abilities.txt": "onet_abilities",
    "Abilities to Work Activities.txt": "onet_abilities_to_work_activities",
    "Abilities to Work Context.txt": "onet_abilities_to_work_context",
    "Alternate Titles.txt": "onet_alternate_titles",
    "Basic Interests to RIASEC.txt": "onet_basic_interests_to_riasec",
    "Content Model Reference.txt": "onet_content_model_reference",
    "DWA Reference.txt": "onet_dwa_reference",
    "Education, Training, and Experience.txt": "onet_education_training_and_experience",
    "Education, Training, and Experience Categories.txt": "onet_education_training_and_experience_categories",
    "Emerging Tasks.txt": "onet_emerging_tasks",
    "Interests.txt": "onet_interests",
    "Interests Illustrative Activities.txt": "onet_interests_illustrative_activities",
    "Interests Illustrative Occupations.txt": "onet_interests_illustrative_occupations",
    "IWA Reference.txt": "onet_iwa_reference",
    "Job Zones.txt": "onet_job_zones",
    "Job Zone Reference.txt": "onet_job_zone_reference",
    "Level Scale Anchors.txt": "onet_level_scale_anchors",
    "Read Me.txt": "onet_read_me",
    "RIASEC Keywords.txt": "onet_riasec_keywords",
    "Sample of Reported Titles.txt": "onet_sample_of_reported_titles",
    "Scales Reference.txt": "onet_scales_reference",
    "Skills.txt": "onet_skills",
    "Skills to Work Activities.txt": "onet_skills_to_work_activities",
    "Skills to Work Context.txt": "onet_skills_to_work_context",
    "Survey Booklet Locations.txt": "onet_survey_booklet_locations",
    "Task Categories.txt": "onet_task_categories",
    "Task Ratings.txt": "onet_task_ratings",
    "Task Statements.txt": "onet_task_statements",
    "Technology Skills.txt": "onet_technology_skills",
    "Tools Used.txt": "onet_tools_used",
    "UNSPSC Reference.txt": "onet_unspsc_reference",
    "Work Activities.txt": "onet_work_activities",
    "Work Context.txt": "onet_work_context",
    "Work Context Categories.txt": "onet_work_context_categories",
    "Work Styles.txt": "onet_work_styles",
    "Work Values.txt": "onet_work_values",
}

def load_txt_file(path: Path):
    """Yield each row in a O*NET text file as a dict."""
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            # Clean keys/values a bit
            clean = { (k or "").strip(): (v or "").strip() for k, v in row.items() if k }
            if clean:
                yield clean

def main():
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB_NAME]

    for filename, collection_name in FILE_MAP.items():
        file_path = DATA_DIR / filename
        if not file_path.exists():
            print(f"[WARN] Missing file: {file_path}")
            continue

        col = db[collection_name]
        col.delete_many({})  # clear old data

        docs = list(load_txt_file(file_path))
        if docs:
            col.insert_many(docs)

        print(f"[OK] {filename} -> {collection_name} ({len(docs)} documents)")

    print("Done loading O*NET files.")
    client.close()

if __name__ == "__main__":
    main()
