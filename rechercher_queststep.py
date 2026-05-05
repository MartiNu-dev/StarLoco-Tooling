import pymysql
import sys
from collections import defaultdict
from rechercher_questobjective import print_results as print_objective_results
from config import DB_CONFIG


def print_row(title: str, row: dict):
    print(f"\n=== {title} ===")
    for key, value in row.items():
        print(f"{key}: {value}")


def list_types():
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT type, COUNT(*) AS total
                FROM quest_objective
                GROUP BY type
                ORDER BY total DESC, type ASC;
                """
            )
            results = cursor.fetchall()

            if not results:
                print("Aucun type trouve dans quest_objective.")
                return

            print("\n=== TYPES DE QUEST STEP (quest_objective.type) ===")
            for row in results:
                print(f"- {row['type']} ({row['total']})")
    finally:
        conn.close()


def get_step(step_id: int):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM quest_step WHERE id = %s;", (step_id,))
            step = cursor.fetchone()

            if not step:
                print(f"Aucun quest_step trouve pour ID={step_id}")
                return

            print_row("QUEST STEP", step)

            cursor.execute(
                """
                SELECT *
                FROM quest_objective
                WHERE FIND_IN_SET(%s, REPLACE(quest_step, ';', ',')) > 0
                ORDER BY id ASC;
                """,
                (str(step_id),),
            )
            objectives = cursor.fetchall()

            if objectives:
                print("\n=== OBJECTIFS LIES ===")
                for obj in objectives:
                    print(
                        f"[{obj['id']}] type={obj['type']} "
                        f"quest_data={obj['quest_data']} "
                        f"description={obj['description']}"
                    )
            else:
                print(f"Aucun objectif lie au quest_step {step_id}")

    finally:
        conn.close()


def search_steps_by_type(type_query: str):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM quest_objective
                WHERE type = %s
                ORDER BY type ASC, id ASC;
                """,
                (type_query,),
            )
            objectives = cursor.fetchall()

            # Fallback pratique si l'utilisateur donne un fragment de type.
            if not objectives:
                cursor.execute(
                    """
                    SELECT *
                    FROM quest_objective
                    WHERE type LIKE %s
                    ORDER BY type ASC, id ASC;
                    """,
                    (f"%{type_query}%",),
                )
                objectives = cursor.fetchall()

            if not objectives:
                print(f"Aucun quest step trouve pour le type '{type_query}'")
                return

            by_type = defaultdict(list)
            for obj in objectives:
                by_type[obj["type"]].append(obj)

            print(f"\n=== RESULTATS POUR TYPE '{type_query}' ===")
            for objective_type, rows in by_type.items():
                print(f"\n--- TYPE: {objective_type} ({len(rows)}) ---")
                for obj in rows:
                    print(
                        f"[Objective {obj['id']}] quest_data={obj['quest_data']} "
                        f"quest_step={obj['quest_step']} "
                        f"npc={obj['npc']} "
                        f"validationType={obj['validationType']}"
                    )
                    if obj.get("description"):
                        print(f"  description={obj['description']}")
                    if obj.get("item") and obj["item"] != "0":
                        print(f"  item={obj['item']}")
                    if obj.get("monster") and obj["monster"] != "0":
                        print(f"  monster={obj['monster']}")

            step_ids = set()
            for obj in objectives:
                raw = (obj.get("quest_step") or "").replace(";", ",")
                for candidate in raw.split(","):
                    candidate = candidate.strip()
                    if candidate.isdigit():
                        step_ids.add(int(candidate))

            if step_ids:
                placeholders = ",".join(["%s"] * len(step_ids))
                cursor.execute(
                    f"SELECT * FROM quest_step WHERE id IN ({placeholders}) ORDER BY id ASC;",
                    tuple(sorted(step_ids)),
                )
                steps = cursor.fetchall()

                print("\n=== QUEST STEPS ASSOCIES ===")
                for step in steps:
                    print(
                        f"[{step['id']}] name={step['name']} "
                        f"xp={step['xp']} kamas={step['kamas']} "
                        f"description={step['description']}"
                    )

    finally:
        conn.close()


def find_by_description(description: str):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description FROM quest_step WHERE name LIKE %s OR description LIKE %s ORDER BY id ASC;",
                (f"%{description}%", f"%{description}%"),
            )
            steps = cursor.fetchall()

            cursor.execute(
                "SELECT id, type, description, quest_step FROM quest_objective WHERE description LIKE %s OR type LIKE %s ORDER BY id ASC;",
                (f"%{description}%", f"%{description}%"),
            )
            objectives = cursor.fetchall()

            if steps:
                print(f"\n=== QUEST STEPS MATCHING '{description}' ===")
                for step in steps:
                    print(f"[{step['id']}] {step['name']} -> {step['description']}")

            if objectives:
                print(f"\n=== OBJECTIFS MATCHING '{description}' ===")
                for obj in objectives:
                    print(
                        f"[{obj['id']}] type={obj['type']} "
                        f"quest_step={obj['quest_step']} "
                        f"description={obj['description']}"
                    )

            if not steps and not objectives:
                print(f"Aucun resultat pour '{description}'")

    finally:
        conn.close()


def translate_type(type_value: int, lang:str='fr') -> str:
    if lang == 'en':
        type_mapping = {
            1: "TALK_TO_NPC",
            2: "GIVE_ITEM",
            3: "KILL_MONSTER",
            4: "COLLECT_ITEM",
            5: "EXPLORE_AREA",
            6: "ESCORT_NPC",
            7: "DEFEAT_BOSS",
            8: "USE_OBJECT",
            9: "DELIVER_ITEM",
            10: "CRAFT_ITEM",
        }
    else:
        type_mapping = {
            1: "PARLER_A_NPC",
            2: "DONNER_ITEM",
            3: "TUE_MONSTRE",
            4: "COLLECTER_ITEM",
            5: "EXPLORER_ZONE",
            6: "ESCORTER_NPC",
            7: "DEFAIT_BOSS",
            8: "UTILISER_OBJET",
            9: "LIVRER_ITEM",
            10: "CRAFT_ITEM",
        }
    return type_mapping.get(type_value, f"UNKNOWN_TYPE_{type_value}")

def find_steps_by_quest_id(quest_id: int):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT steps, objectives FROM quest WHERE id = %s ORDER BY id ASC;",
                (quest_id,),
            )
            results = cursor.fetchall()
            #format de steps : "1;2;3" ou null

            if results:
                steps_str = results[0]["steps"] or ""
                objectives_str = results[0]["objectives"] or ""

                step_ids = set()
                for part in steps_str.split(";"):
                    part = part.strip()
                    if part.isdigit():
                        step_ids.add(int(part))

                objective_ids = set()
                for part in objectives_str.split(";"):
                    part = part.strip()
                    if part.isdigit():
                        objective_ids.add(int(part))

                if step_ids:
                    placeholders = ",".join(["%s"] * len(step_ids))
                    cursor.execute(
                        f"SELECT id, name FROM quest_step WHERE id IN ({placeholders}) ORDER BY id ASC;",
                        tuple(sorted(step_ids)),
                    )
                    steps = cursor.fetchall()
                    print(f"\n=== QUEST STEPS POUR QUEST ID={quest_id} ===")
                    for step in steps:
                        print(f"[{step['id']}] {step['name']}")

                if objective_ids:
                    placeholders = ",".join(["%s"] * len(objective_ids))
                    cursor.execute(
                        f"SELECT * FROM quest_objective WHERE id IN ({placeholders}) ORDER BY id ASC;",
                        tuple(sorted(objective_ids)),
                    )
                    objectives = cursor.fetchall()
                    print_objective_results(f"OBJECTIFS POUR QUEST ID={quest_id}", objectives)
                        

    finally:
        conn.close()



def print_usage():
    print("Usage:")
    print("  python rechercher_queststep.py types")
    print("  python rechercher_queststep.py type <type>")
    print("  python rechercher_queststep.py step <step_id>")
    print("  python rechercher_queststep.py chercher <texte>")
    print("  python rechercher_queststep.py quest <quest_id>")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "types":
        list_types()
    elif mode == "type":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        search_steps_by_type(sys.argv[2])
    elif mode == "step":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        get_step(int(sys.argv[2]))
    elif mode == "chercher":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        find_by_description(sys.argv[2])
    elif mode == "quest":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        find_steps_by_quest_id(int(sys.argv[2]))
    else:
        print_usage()
        sys.exit(1)

