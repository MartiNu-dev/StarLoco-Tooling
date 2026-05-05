import pymysql
import sys
import re
from pathlib import Path
from collections import defaultdict
from config import DB_CONFIG


TYPE_HINTS = {
    "0": "generique",
    "1": "interaction_npc",
    "2": "item",
    "3": "item",
    "4": "position_ou_lieu",
    "5": "special",
    "6": "monster",
    "7": "monster",
    "9": "interaction_npc",
    "10": "special",
    "11": "special",
    "12": "item",
}

INDEX_DIR = Path(__file__).resolve().parent / "indexes_dofus_retro"
ITEM_INDEX_FILE = INDEX_DIR / "Objets.txt"
MONSTER_INDEX_FILE = INDEX_DIR / "Monstres.txt"
INTERACTIVE_INDEX_FILE = INDEX_DIR / "Interactives.txt"
DIALOGUE_NPC_FILE = INDEX_DIR / "dialogue_npc.txt"
DIALOGUE_PLAYER_FILE = INDEX_DIR / "dialogue_joueur.txt"


def compact_text(value: str, max_len: int = 120):
    if value is None:
        return ""
    text = re.sub(r"\s+", " ", str(value)).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def parse_pair(raw: str):
    if not raw:
        return None
    chunks = [x.strip() for x in str(raw).split(",")]
    if len(chunks) != 2:
        return None
    if not chunks[0].isdigit() or not chunks[1].isdigit():
        return None
    return int(chunks[0]), int(chunks[1])


def parse_step_ids(raw: str):
    if not raw:
        return []
    values = []
    for token in str(raw).replace(";", ",").split(","):
        token = token.strip()
        if token and token.lstrip("-").isdigit():
            values.append(int(token))
    return values


def parse_description_ints(raw: str):
    if not raw:
        return []
    left = str(raw).split("]")[0]
    return [int(x) for x in re.findall(r"\d+", left)]


def parse_simple_index(path: Path):
    mapping = {}
    if not path.exists():
        return mapping

    pattern = re.compile(r"^\s*(\d+)\s*-\s*(.+?)\s*$")
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            match = pattern.match(line)
            if not match:
                continue
            mapping[int(match.group(1))] = match.group(2).strip()
    return mapping


def decode_dialogue_expression(raw: str):
    if not raw:
        return ""

    parts = re.findall(r'"((?:\\.|[^"\\])*)"', raw)
    if parts:
        text = "".join(parts)
    else:
        text = raw

    text = (
        text.replace("\\n", " ")
        .replace("\\r", " ")
        .replace("\\t", " ")
        .replace("\\'", "'")
        .replace('\\"', '"')
    )
    return re.sub(r"\s+", " ", text).strip()


def parse_dialogue_index(path: Path, prefix: str):
    mapping = {}
    if not path.exists():
        return mapping

    pattern = re.compile(rf"^\s*{re.escape(prefix)}\[(\d+)\]\s*=\s*(.+?)\s*;\s*$")
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            match = pattern.match(line)
            if not match:
                continue
            text_id = int(match.group(1))
            mapping[text_id] = decode_dialogue_expression(match.group(2))
    return mapping


def extract_speaker_name(text: str):
    if not text:
        return None

    patterns = [
        r"\bje suis\s+([^,.!;:\n]+)",
        r"\bbonjour,\s*je suis\s+([^,.!;:\n]+)",
        r"\bje m'appelle\s+([^,.!;:\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip(" .,!;:-")
            if value:
                return value
    return None


def fallback_monster_pairs(obj):
    # Certains objectifs (surtout type 6/7) encodent plusieurs monstres dans description.
    if str(obj.get("type")) not in {"6", "7"}:
        return []
    numbers = parse_description_ints(obj.get("description"))
    if len(numbers) < 2 or len(numbers) % 2 != 0:
        return []
    pairs = []
    for i in range(0, len(numbers), 2):
        pairs.append((numbers[i], numbers[i + 1]))
    return pairs


class ObjectiveResolver:
    def __init__(self, conn, objective_rows):
        self.conn = conn
        self.objective_rows = objective_rows

        self.items = {}
        self.monsters = {}
        self.interactives = {}
        self.quest_names = {}
        self.npc_templates = {}
        self.npc_question_text = {}
        self.objective_to_quests = defaultdict(list)

        self.idx_items = parse_simple_index(ITEM_INDEX_FILE)
        self.idx_monsters = parse_simple_index(MONSTER_INDEX_FILE)
        self.idx_interactives = parse_simple_index(INTERACTIVE_INDEX_FILE)
        self.idx_dialogue_npc = parse_dialogue_index(DIALOGUE_NPC_FILE, "D.q")
        self.idx_dialogue_player = parse_dialogue_index(DIALOGUE_PLAYER_FILE, "D.a")

        self._load_maps()

    def _fetch_id_name_map(self, table: str, id_col: str, name_col: str, ids: set[int]):
        if not ids:
            return {}
        placeholders = ",".join(["%s"] * len(ids))
        query = f"SELECT {id_col} AS id, {name_col} AS name FROM {table} WHERE {id_col} IN ({placeholders});"
        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(sorted(ids)))
            rows = cursor.fetchall()
        return {int(row["id"]): str(row["name"]) for row in rows}

    def _load_maps(self):
        objective_ids = set()
        npc_ids = set()
        item_ids = set()
        monster_ids = set()
        interactive_ids = set()
        quest_data_ids = set()
        question_ids = set()

        for obj in self.objective_rows:
            objective_ids.add(int(obj["id"]))

            npc_id = int(obj.get("npc") or 0)
            if npc_id > 0:
                npc_ids.add(npc_id)

            item = parse_pair(obj.get("item"))
            if item and item[0] > 0:
                item_ids.add(item[0])

            monster = parse_pair(obj.get("monster"))
            if monster and monster[0] > 0:
                monster_ids.add(monster[0])

            for mid, _qty in fallback_monster_pairs(obj):
                if mid > 0:
                    monster_ids.add(mid)

            quest_data = int(obj.get("quest_data") or 0)
            if quest_data > 0:
                quest_data_ids.add(quest_data)
                interactive_ids.add(quest_data)

            desc_ids = parse_description_ints(obj.get("description"))
            if desc_ids:
                if str(obj.get("type")) in {"1", "9"}:
                    npc_ids.add(desc_ids[0])
                elif str(obj.get("type")) in {"2", "3", "12"} and len(desc_ids) >= 2:
                    npc_ids.add(desc_ids[0])
                    item_ids.add(desc_ids[1])
                elif str(obj.get("type")) in {"6", "7"}:
                    for i in range(0, len(desc_ids) - 1, 2):
                        monster_ids.add(desc_ids[i])

        self.items = self._fetch_id_name_map("item_template", "id", "name", item_ids)
        self.monsters = self._fetch_id_name_map("monsters", "id", "name", monster_ids)
        self.interactives = self._fetch_id_name_map("interactive_objects_data", "id", "`Name IO`", interactive_ids)
        self.quest_names = self._fetch_id_name_map("quest", "id", "nom", quest_data_ids)

        if npc_ids:
            placeholders = ",".join(["%s"] * len(npc_ids))
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT id, initQuestion FROM npc_template WHERE id IN ({placeholders});",
                    tuple(sorted(npc_ids)),
                )
                for row in cursor.fetchall():
                    npc_id = int(row["id"])
                    init_question = row.get("initQuestion")
                    self.npc_templates[npc_id] = init_question
                    if str(init_question).lstrip("-").isdigit() and int(init_question) >= 0:
                        question_ids.add(int(init_question))

        question_ids.update([n for n in npc_ids if n > 0])
        if question_ids:
            placeholders = ",".join(["%s"] * len(question_ids))
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID, description FROM npc_questions WHERE ID IN ({placeholders});",
                    tuple(sorted(question_ids)),
                )
                for row in cursor.fetchall():
                    self.npc_question_text[int(row["ID"])] = row["description"]

        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id, nom, objectives FROM quest WHERE objectives IS NOT NULL AND objectives <> '';")
            for row in cursor.fetchall():
                ids = parse_step_ids(row.get("objectives"))
                for objective_id in ids:
                    if objective_id in objective_ids:
                        self.objective_to_quests[objective_id].append((int(row["id"]), row["nom"]))

    def resolve_item(self, item_id: int):
        return self.items.get(item_id) or self.idx_items.get(item_id)

    def resolve_monster(self, monster_id: int):
        return self.monsters.get(monster_id) or self.idx_monsters.get(monster_id)

    def resolve_interactive(self, interactive_id: int):
        return self.interactives.get(interactive_id) or self.idx_interactives.get(interactive_id)

    def resolve_quest(self, quest_id: int):
        return self.quest_names.get(quest_id)

    def resolve_player_dialogue(self, text_id: int):
        return self.idx_dialogue_player.get(text_id)

    def resolve_npc(self, npc_id: int):
        if npc_id <= 0:
            return None

        if npc_id in self.npc_templates:
            init_question = self.npc_templates[npc_id]
            question_id = None
            if str(init_question).lstrip("-").isdigit() and int(init_question) >= 0:
                question_id = int(init_question)

            text = None
            if question_id is not None:
                text = self.npc_question_text.get(question_id) or self.idx_dialogue_npc.get(question_id)

            if text:
                name = extract_speaker_name(text)
                if name:
                    return f"{name} (initQuestion={question_id})"
                return f"initQuestion={question_id} | {compact_text(text)}"

            if question_id is not None:
                return f"initQuestion={question_id}"
            return "template_npc_sans_dialogue"

        text = self.npc_question_text.get(npc_id) or self.idx_dialogue_npc.get(npc_id)
        if text:
            name = extract_speaker_name(text)
            if name:
                return f"{name} (question={npc_id})"
            return f"question={npc_id} | {compact_text(text)}"

        return None

    def resolve_quest_data(self, value: int):
        if value <= 0:
            return None

        labels = []
        quest_name = self.resolve_quest(value)
        if quest_name:
            labels.append(f"quest#{value}={quest_name}")

        interactive = self.resolve_interactive(value)
        if interactive:
            labels.append(f"interactive#{value}={interactive}")

        item_name = self.resolve_item(value)
        if item_name:
            labels.append(f"item#{value}={item_name}")

        monster_name = self.resolve_monster(value)
        if monster_name:
            labels.append(f"monster#{value}={monster_name}")

        if not labels:
            return None
        return " | ".join(labels)

    def resolve_description_hints(self, obj):
        numbers = parse_description_ints(obj.get("description"))
        if not numbers:
            return []

        hints = []
        t = str(obj.get("type"))
        if t in {"1", "9"} and numbers:
            npc_id = numbers[0]
            npc_info = self.resolve_npc(npc_id)
            if npc_info:
                hints.append(f"desc_npc={npc_id} ({npc_info})")
        elif t in {"2", "3", "12"} and len(numbers) >= 2:
            npc_id, item_id, *rest = numbers
            npc_info = self.resolve_npc(npc_id)
            item_name = self.resolve_item(item_id)
            qty = rest[0] if rest else None
            parts = [f"desc_npc={npc_id}"]
            if npc_info:
                parts[-1] += f" ({npc_info})"
            item_text = f"desc_item={item_id}"
            if item_name:
                item_text += f" ({item_name})"
            parts.append(item_text)
            if qty is not None:
                parts.append(f"desc_qty={qty}")
            hints.extend(parts)
        elif t in {"6", "7"} and len(numbers) >= 2:
            pairs = []
            for i in range(0, len(numbers) - 1, 2):
                monster_id, qty = numbers[i], numbers[i + 1]
                monster_name = self.resolve_monster(monster_id)
                if monster_name:
                    pairs.append(f"{monster_id} ({monster_name}) x{qty}")
                else:
                    pairs.append(f"{monster_id} x{qty}")
            if pairs:
                hints.append("desc_monsters=" + ", ".join(pairs))
        else:
            dialogue_hits = []
            for value in numbers:
                player_text = self.resolve_player_dialogue(value)
                if player_text:
                    dialogue_hits.append(f"{value}='{compact_text(player_text, 80)}'")
            if dialogue_hits:
                hints.append("desc_dialogues=" + "; ".join(dialogue_hits[:5]))

        return hints


def fetch_steps_map(conn, objective_rows):
    step_ids = set()
    for row in objective_rows:
        for step_id in parse_step_ids(row.get("quest_step")):
            if step_id > 0:
                step_ids.add(step_id)

    if not step_ids:
        return {}

    placeholders = ",".join(["%s"] * len(step_ids))
    with conn.cursor() as cursor:
        cursor.execute(
            f"SELECT id, name, description, xp, kamas FROM quest_step WHERE id IN ({placeholders}) ORDER BY id ASC;",
            tuple(sorted(step_ids)),
        )
        rows = cursor.fetchall()
    return {row["id"]: row for row in rows}


def format_objective(obj, steps_map, resolver: ObjectiveResolver):
    type_hint = TYPE_HINTS.get(str(obj["type"]), "inconnu")
    item = parse_pair(obj.get("item"))
    monster = parse_pair(obj.get("monster"))
    step_ids = parse_step_ids(obj.get("quest_step"))

    print(
        f"\n[Objective {obj['id']}] type={obj['type']} ({type_hint}) "
        f"npc={obj['npc']} quest_data={obj['quest_data']} validationType={obj['validationType']}"
    )

    npc_id = int(obj.get("npc") or 0)
    if npc_id > 0:
        npc_info = resolver.resolve_npc(npc_id)
        if npc_info:
            print(f"  npc_info={npc_info}")

    if item:
        item_name = resolver.resolve_item(item[0])
        if item_name:
            print(f"  item_id={item[0]} ({item_name}) quantite={item[1]}")
        else:
            print(f"  item_id={item[0]} quantite={item[1]}")

    if monster:
        monster_name = resolver.resolve_monster(monster[0])
        if monster_name:
            print(f"  monster_id={monster[0]} ({monster_name}) quantite={monster[1]}")
        else:
            print(f"  monster_id={monster[0]} quantite={monster[1]}")
    elif str(obj.get("type")) in {"6", "7"}:
        fallback_pairs = fallback_monster_pairs(obj)
        if fallback_pairs:
            compact = ", ".join(
                [
                    f"{mid} ({resolver.resolve_monster(mid)}) x{qty}" if resolver.resolve_monster(mid) else f"{mid}x{qty}"
                    for mid, qty in fallback_pairs
                ]
            )
            print(f"  monsters={compact} (from description)")

    quest_data_value = int(obj.get("quest_data") or 0)
    if quest_data_value > 0:
        quest_data_hint = resolver.resolve_quest_data(quest_data_value)
        if quest_data_hint:
            print(f"  quest_data_resolve={quest_data_hint}")

    description_hints = resolver.resolve_description_hints(obj)
    for hint in description_hints:
        print(f"  {hint}")

    if obj.get("description"):
        print(f"  description={obj['description']}")
    print(f"  quest_step_raw={obj['quest_step']}")

    if step_ids:
        labels = []
        for step_id in step_ids:
            step = steps_map.get(step_id)
            if step:
                labels.append(f"{step_id}:{step['name']}")
            else:
                labels.append(str(step_id))
        print(f"  steps={', '.join(labels)}")

    quests = resolver.objective_to_quests.get(int(obj["id"]), [])
    if quests:
        quest_labels = ", ".join([f"{qid}:{qname}" for qid, qname in quests])
        print(f"  quests={quest_labels}")


def print_results(title: str, objectives):
    if not objectives:
        print("Aucun objectif trouve.")
        return

    conn = pymysql.connect(**DB_CONFIG)
    try:
        steps_map = fetch_steps_map(conn, objectives)
        resolver = ObjectiveResolver(conn, objectives)
    finally:
        conn.close()

    print(f"\n=== {title} ===")
    print(f"Total: {len(objectives)}")

    by_type = defaultdict(int)
    for obj in objectives:
        by_type[str(obj["type"])] += 1

    stats = ", ".join([f"type {t}={c}" for t, c in sorted(by_type.items(), key=lambda x: x[0])])
    print(f"Repartition: {stats}")

    for obj in objectives:
        format_objective(obj, steps_map, resolver)


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
            rows = cursor.fetchall()

            print("\n=== TYPES QUEST OBJECTIVE ===")
            for row in rows:
                hint = TYPE_HINTS.get(str(row["type"]), "inconnu")
                print(f"- type {row['type']}: {row['total']} ({hint})")
    finally:
        conn.close()


def get_objective(objective_id: int):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM quest_objective WHERE id = %s;", (objective_id,))
            row = cursor.fetchone()

        if not row:
            print(f"Aucun quest_objective pour ID={objective_id}")
            return

        print_results(f"QUEST OBJECTIVE {objective_id}", [row])
    finally:
        conn.close()


def search_by_npc(npc_id: int):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quest_objective WHERE npc = %s ORDER BY id ASC;",
                (npc_id,),
            )
            rows = cursor.fetchall()

        print_results(f"OBJECTIFS LIES AU NPC {npc_id}", rows)
    finally:
        conn.close()


def search_by_item(item_id: int, qty: int | None = None):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            if qty is None:
                cursor.execute(
                    "SELECT * FROM quest_objective WHERE item LIKE %s ORDER BY id ASC;",
                    (f"{item_id},%",),
                )
            else:
                cursor.execute(
                    "SELECT * FROM quest_objective WHERE item = %s ORDER BY id ASC;",
                    (f"{item_id},{qty}",),
                )
            rows = cursor.fetchall()

        suffix = f" x{qty}" if qty is not None else ""
        print_results(f"OBJECTIFS PAR ITEM {item_id}{suffix}", rows)
    finally:
        conn.close()


def search_by_monster(monster_id: int, qty: int | None = None):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            if qty is None:
                cursor.execute(
                    """
                    SELECT *
                    FROM quest_objective
                    WHERE monster LIKE %s
                       OR description REGEXP %s
                    ORDER BY id ASC;
                    """,
                    (f"{monster_id},%", f"(^|[^0-9]){monster_id},[0-9]+([^0-9]|$)"),
                )
            else:
                cursor.execute(
                    """
                    SELECT *
                    FROM quest_objective
                    WHERE monster = %s
                       OR description REGEXP %s
                    ORDER BY id ASC;
                    """,
                    (f"{monster_id},{qty}", f"(^|[^0-9]){monster_id},{qty}([^0-9]|$)"),
                )
            rows = cursor.fetchall()

        suffix = f" x{qty}" if qty is not None else ""
        print_results(f"OBJECTIFS PAR MONSTER {monster_id}{suffix}", rows)
    finally:
        conn.close()


def search_by_type(type_query: str):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quest_objective WHERE type = %s ORDER BY id ASC;",
                (type_query,),
            )
            rows = cursor.fetchall()

            if not rows:
                cursor.execute(
                    "SELECT * FROM quest_objective WHERE type LIKE %s ORDER BY id ASC;",
                    (f"%{type_query}%",),
                )
                rows = cursor.fetchall()

        print_results(f"OBJECTIFS DE TYPE '{type_query}'", rows)
    finally:
        conn.close()


def search_by_data(data_id: int, qty: int | None = None):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            if qty is None:
                cursor.execute(
                    """
                    SELECT *
                    FROM quest_objective
                    WHERE quest_data = %s
                       OR item LIKE %s
                       OR monster LIKE %s
                       OR description REGEXP %s
                    ORDER BY id ASC;
                    """,
                    (data_id, f"{data_id},%", f"{data_id},%", f"(^|[^0-9]){data_id},[0-9]+([^0-9]|$)"),
                )
            else:
                cursor.execute(
                    """
                    SELECT *
                    FROM quest_objective
                    WHERE item = %s
                       OR monster = %s
                       OR description REGEXP %s
                    ORDER BY id ASC;
                    """,
                    (f"{data_id},{qty}", f"{data_id},{qty}", f"(^|[^0-9]){data_id},{qty}([^0-9]|$)"),
                )
            rows = cursor.fetchall()

        if qty is None:
            print_results(f"OBJECTIFS PAR DATA {data_id}", rows)
        else:
            print_results(f"OBJECTIFS PAR DATA {data_id} x{qty}", rows)
    finally:
        conn.close()


def search_text(text: str):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM quest_objective
                WHERE description LIKE %s
                   OR type LIKE %s
                   OR item LIKE %s
                   OR monster LIKE %s
                ORDER BY id ASC;
                """,
                (f"%{text}%", f"%{text}%", f"%{text}%", f"%{text}%"),
            )
            rows = cursor.fetchall()

        print_results(f"OBJECTIFS MATCHING '{text}'", rows)
    finally:
        conn.close()


def parse_int(value: str, label: str):
    if not value.lstrip("-").isdigit():
        print(f"{label} doit etre un entier: {value}")
        sys.exit(1)
    return int(value)


def print_usage():
    print("Usage:")
    print("  python rechercher_questobjective.py types")
    print("  python rechercher_questobjective.py type <type>")
    print("  python rechercher_questobjective.py objectif <objective_id>")
    print("  python rechercher_questobjective.py npc <npc_id>")
    print("  python rechercher_questobjective.py item <item_id> [quantite]")
    print("  python rechercher_questobjective.py monster <monster_id> [quantite]")
    print("  python rechercher_questobjective.py data <data_id> [quantite]")
    print("  python rechercher_questobjective.py chercher <texte>")


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
        search_by_type(sys.argv[2])
    elif mode == "objectif":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        get_objective(parse_int(sys.argv[2], "objective_id"))
    elif mode == "npc":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        search_by_npc(parse_int(sys.argv[2], "npc_id"))
    elif mode == "item":
        if len(sys.argv) not in (3, 4):
            print_usage()
            sys.exit(1)
        item_id = parse_int(sys.argv[2], "item_id")
        qty = parse_int(sys.argv[3], "quantite") if len(sys.argv) == 4 else None
        search_by_item(item_id, qty)
    elif mode == "monster":
        if len(sys.argv) not in (3, 4):
            print_usage()
            sys.exit(1)
        monster_id = parse_int(sys.argv[2], "monster_id")
        qty = parse_int(sys.argv[3], "quantite") if len(sys.argv) == 4 else None
        search_by_monster(monster_id, qty)
    elif mode == "data":
        if len(sys.argv) not in (3, 4):
            print_usage()
            sys.exit(1)
        data_id = parse_int(sys.argv[2], "data_id")
        qty = parse_int(sys.argv[3], "quantite") if len(sys.argv) == 4 else None
        search_by_data(data_id, qty)
    elif mode == "chercher":
        if len(sys.argv) != 3:
            print_usage()
            sys.exit(1)
        search_text(sys.argv[2])
    else:
        print_usage()
        sys.exit(1)
