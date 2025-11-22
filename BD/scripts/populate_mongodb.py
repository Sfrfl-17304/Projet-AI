# BD/scripts/populate_mongodb.py
from collections import defaultdict
from typing import Dict, List

from BD.services import MongoDBService
from BD.models import Skill, Role, RequiredSkill


def map_importance_to_priority(score: float) -> str:
    """Convert O*NET importance score (0–5) into a priority label."""
    if score >= 4.0:
        return "critical"
    if score >= 3.0:
        return "high"
    if score >= 2.0:
        return "medium"
    return "low"


def map_level_to_difficulty(level: float) -> str:
    """Convert O*NET level score (0–7) into a difficulty label."""
    if level >= 4.0:
        return "expert"
    if level >= 3.0:
        return "advanced"
    if level >= 2.0:
        return "intermediate"
    return "beginner"


def build_skills(db) -> Dict[str, Skill]:
    """
    Build Skill objects from onet_skills collection.

    We aggregate by Element ID:
    - average importance (Scale ID = 'IM')
    - average level (Scale ID = 'LV')
    """
    skills_collection = db["onet_skills"]
    aggregates: Dict[str, Dict] = {}

    for row in skills_collection.find({}):
        element_id = row["Element ID"]
        name = row["Element Name"]
        scale = row["Scale ID"]
        value_raw = row.get("Data Value", "") or "0"
        try:
            value = float(value_raw)
        except ValueError:
            value = 0.0

        agg = aggregates.setdefault(
            element_id,
            {
                "name": name,
                "importance": [],
                "level": [],
            },
        )

        if scale == "IM":
            agg["importance"].append(value)
        elif scale == "LV":
            agg["level"].append(value)

    skills: Dict[str, Skill] = {}
    for element_id, agg in aggregates.items():
        imp = sum(agg["importance"]) / len(agg["importance"]) if agg["importance"] else 0.0
        lvl = sum(agg["level"]) / len(agg["level"]) if agg["level"] else 0.0

        difficulty = map_level_to_difficulty(lvl)
        popularity = int(min(max(imp / 5 * 100, 0), 100))
        if imp >= 3.5:
            demand = "very_high"
        elif imp >= 2.5:
            demand = "high"
        elif imp >= 1.5:
            demand = "medium"
        else:
            demand = "low"

        skill = Skill(
            id=element_id,
            name=agg["name"],
            category="onet_skill",
            description=agg["name"],
            difficulty=difficulty,
            learning_time_hours=int(lvl * 40) if lvl else 40,
            prerequisites=[],
            related_skills=[],
            resources=[],
            popularity_score=popularity,
            demand_level=demand,
        )
        skills[element_id] = skill

    return skills


def build_roles(db, skills_by_id: Dict[str, Skill]) -> List[Role]:
    """
    Build Role objects from O*NET occupations + skills + tasks + technologies.

    - Role.name        ← Occupation Title
    - Role.description ← Occupation Description
    - Role.category    ← SOC major group (first 2 digits)
    - required_skills  ← top importance skills for that occupation
    - responsibilities ← up to 10 task statements
    - tools            ← technologies / tools from Technology Skills.txt
    """
    occ_col = db["onet_occupation_data"]
    skills_col = db["onet_skills"]
    tasks_col = db["onet_task_statements"]
    tech_col = db["onet_technology_skills"]

    # Map occ -> top skills
    occ_skills: Dict[str, List[RequiredSkill]] = defaultdict(list)

    # Use Scale ID = 'IM' (importance) to rank skills per occupation
    for row in skills_col.find({"Scale ID": "IM"}):
        code = row["O*NET-SOC Code"]
        element_id = row["Element ID"]
        value_raw = row.get("Data Value", "") or "0"
        try:
            imp = float(value_raw)
        except ValueError:
            imp = 0.0

        skill = skills_by_id.get(element_id)
        if not skill:
            continue

        occ_skills[code].append(
            RequiredSkill(
                skill_id=skill.id,
                skill_name=skill.name,
                proficiency_level=map_level_to_difficulty(imp),
                priority=map_importance_to_priority(imp),
            )
        )

    # Keep top 15 skills by importance per occupation
    priority_order = ["low", "medium", "high", "critical"]

    for code, reqs in occ_skills.items():
        occ_skills[code] = sorted(
            reqs,
            key=lambda rs: priority_order.index(rs.priority),
            reverse=True,
        )[:15]

    # Map occ -> tasks (up to 10 descriptions)
    occ_tasks: Dict[str, List[str]] = defaultdict(list)
    for row in tasks_col.find({}):
        code = row["O*NET-SOC Code"]
        task = row.get("Task", "").strip()
        if not task:
            continue
        if len(occ_tasks[code]) < 10:
            occ_tasks[code].append(task)

    # Map occ -> tools/technologies
    occ_tools: Dict[str, List[str]] = defaultdict(list)
    for row in tech_col.find({}):
        code = row["O*NET-SOC Code"]
        tool = (
            row.get("Commodity Title")
            or row.get("Example")
            or row.get("Technology Title")
            or ""
        ).strip()
        if tool and tool not in occ_tools[code]:
            occ_tools[code].append(tool)

    roles: List[Role] = []

    for occ in occ_col.find({}):
        code = occ["O*NET-SOC Code"]
        name = occ["Title"]
        desc = occ["Description"]

        # Use SOC major group (first 2 digits) as category label
        if "-" in code:
            major = code.split("-")[0]
            category = f"SOC-{major}"
        else:
            category = "O*NET"

        role = Role(
            name=name,
            description=desc,
            category=category,
            required_skills=occ_skills.get(code, []),
            average_salary="N/A",        # can be filled later from another dataset
            growth_rate="N/A",
            experience_level="N/A",
            responsibilities=occ_tasks.get(code, []),
            tools=occ_tools.get(code, []),
            industries=[],
        )
        roles.append(role)

    return roles


def main():
    mongo = MongoDBService()
    db = mongo.db

    # Clean old app collections
    db["roles"].delete_many({})
    db["skills"].delete_many({})
    db["learning_resources"].delete_many({})

    # 1) Build skills from O*NET
    skills_by_id = build_skills(db)
    for skill in skills_by_id.values():
        mongo.insert_skill(skill)

    # 2) Build roles from O*NET + the skills we just built
    roles = build_roles(db, skills_by_id)
    for role in roles:
        mongo.insert_role(role)

    mongo.close()
    print(f"Inserted {len(skills_by_id)} skills and {len(roles)} roles from O*NET.")


if __name__ == "__main__":
    main()
