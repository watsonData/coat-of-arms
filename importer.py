import os
import pandas as pd
import json
from config import CONTACT_URL, CONTACT_EMAIL

mode = "canton"  # 'canton' or 'gde'

if not os.path.exists(f"data/{mode}"):
    os.makedirs(f"data/{mode}")

query = {
    "canton": """
        SELECT DISTINCT ?id ?coa_url WHERE {
            ?item p:P31 [ps:P31 wd:Q23058];
                    wdt:P395 ?id;
                    wdt:P94 ?coa.

            # Get the direct URL from the Wikimedia Commons file
            BIND(CONCAT('https://commons.wikimedia.org/w/index.php?title=Special:Redirect/file/', REPLACE(STR(?coa), 'http://commons.wikimedia.org/wiki/Special:FilePath/', ''), '&width=200') AS ?coa_url)
        }
    """,
    "gde": """
        SELECT DISTINCT ?id ?coa_url WHERE {
            ?item p:P31 [ps:P31 wd:Q70208];
                    wdt:P771 ?id;
                    wdt:P94 ?coa.

            # Get the direct URL from the Wikimedia Commons file
            BIND(CONCAT('https://commons.wikimedia.org/w/index.php?title=Special:Redirect/file/', REPLACE(STR(?coa), 'http://commons.wikimedia.org/wiki/Special:FilePath/', ''), '&width=200') AS ?coa_url)
        }
    """,
}

if not os.path.exists(f"data/{mode}/coats_of_arms.csv"):
    from graphly.api_client import SparqlClient

    wikidata = SparqlClient("https://query.wikidata.org/sparql")

    wikidata.HEADERS["User-Agent"] = (
        f"User-Agent: WatsonCOABot/0.0 ({CONTACT_URL}; {CONTACT_EMAIL}) zazuko-graphly/0.1"
    )

    current_query = query[mode]

    result = wikidata.send_query(current_query)

    result.to_csv(f"data/{mode}/coats_of_arms.csv", index=False)

df_coats_of_arms = pd.read_csv(f"data/{mode}/coats_of_arms.csv").drop_duplicates(
    subset=["id"]
)

if not os.path.exists(f"data/{mode}/png"):
    os.makedirs(f"data/{mode}/png")

if not os.path.exists(f"data/{mode}/current_coas.json"):
    with open(f"data/{mode}/current_coas.json", "w") as f:
        f.write("{}")

with open(f"data/{mode}/current_coas.json", "r") as f:
    current_coas = json.load(f)

    for i, row in df_coats_of_arms.iterrows():
        id = row["id"].lower() if mode == "canton" else str(int(row["id"]))

        if mode == "canton":
            row["id"] = row["id"].lower()

        if (
            not os.path.exists(f"data/{mode}/png/{row['id']}.png")
            or current_coas.get(id) != row["coa_url"]
            or os.path.getsize(f"data/{mode}/png/{row['id']}.png") == 0
        ):
            print(row["id"], row["coa_url"])
            if not os.path.exists(f"data/{mode}/png/{row['id']}.png"):
                print("not exists")
            if current_coas.get(id) != row["coa_url"]:
                print("not equal")
            if not os.system(
                f"wget -O data/{mode}/png/{row['id']}.png \"{row['coa_url']}\" -q -U \"WatsonCOABot/0.0 ({CONTACT_URL}; {CONTACT_EMAIL}) zazuko-graphly/0.1\""
            ):
                current_coas[id] = row["coa_url"]
                print(f"Downloaded {row['id']}")
            else:
                print(f"Failed to download {row['id']}")
                os.system(f"rm data/{mode}/png/{row['id']}.png")

    with open(f"data/{mode}/current_coas.json", "w") as f:
        json.dump(current_coas, f, indent=2)
