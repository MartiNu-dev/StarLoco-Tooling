import pymysql
import sys
from config import DB_CONFIG


def get_npc_question(question_id: int):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM npc_questions WHERE id = %s;"
            cursor.execute(sql, (question_id,))
            result = cursor.fetchone()

            if result:
                print("\n=== NPC QUESTION ===")
                for k, v in result.items():
                    print(f"{k}: {v}")

            if result and result["responses"]:
                response_ids = [int(x) for x in result["responses"].split(";") if x]

                with conn.cursor() as cursor:
                    sql = f"""
                    SELECT * FROM npc_reponses_actions
                    WHERE id IN ({','.join(['%s'] * len(response_ids))})
                    """
                    cursor.execute(sql, response_ids)
                    responses = cursor.fetchall()

                    print("\n=== RESPONSES ===")
                    for r in responses:
                        print(f"[{r['ID']}] {r['nom']} (type={r['type']} args={r['args']})")


            else:
                print(f"Aucune réponse trouvée pour ID={question_id}")

    finally:
        conn.close()

def get_npc_reponse(reponse_id: int):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM npc_reponses_actions WHERE id = %s;"
            cursor.execute(sql, (reponse_id,))
            result = cursor.fetchone()

            if result:
                print("\n=== REPONSE ===")
                for k, v in result.items():
                    print(f"{k}: {v}")
                
                #print associated uestions
                with conn.cursor() as cursor:
                    sql = f"""
                    SELECT * FROM npc_questions
                    WHERE FIND_IN_SET(%s, REPLACE(responses, ';', ',')) > 0
                    """
                    cursor.execute(sql, (reponse_id,))
                    questions = cursor.fetchall()

                    if questions:
                        print("\n=== QUESTIONS ASSOCIÉES ===")
                        for q in questions:
                            print(f"[{q['ID']}] {q['description']} (responses={q['responses']})") 
                    else:
                        print("Aucune question associée trouvée.")

            else:
                print(f"Aucune reponse trouvée pour ID={reponse_id}")

    finally:
        conn.close()

#une fonction pour trouver l'id de la question ou réponse en fonction d'un morceau de description donnée
def find_id_by_description(description: str, type:str):
    conn = pymysql.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cursor:
            if type == "question":
                sql = "SELECT id, description FROM npc_questions WHERE description LIKE %s;"
            elif type == "reponse":
                sql = "SELECT id, nom AS description FROM npc_reponses_actions WHERE nom LIKE %s;"
            else:
                print("Type must be 'question' or 'reponse'")
                return

            cursor.execute(sql, (f"%{description}%",))
            results = cursor.fetchall()

            if results:
                print(f"\n=== IDs matching '{description}' for {type} ===")
                for r in results:
                    print(f"ID: {r['id']}\nDescription : {r['description']}\n")
            else:
                print(f"Aucune {type} trouvée pour la description '{description}'")

    finally:
        conn.close()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reponses_possible_dialogue.py <question|reponse> <question_id>")
        sys.exit(1)

    if sys.argv[1] == "question":
        question_id = int(sys.argv[2])
        get_npc_question(question_id)

    elif sys.argv[1] == "reponse":
        reponse_id = int(sys.argv[2])
        get_npc_reponse(reponse_id)

    elif sys.argv[1] == "chercher":
        description = sys.argv[2]
        find_id_by_description(description, "question")
        find_id_by_description(description, "reponse")

    else:
        print("Usage: python reponses_possible_dialogue.py <question|reponse> <question_id>")
        sys.exit(1)
