import json                        # lets us read the list of models from a .json file
from agent import setup, test_model  # the same test that agent.py runs on its own


if __name__ == "__main__":
    setup()

    # Read the list of models. The file holds categories, and each category holds models.
    with open("available_models.json", encoding="utf-8") as file:
        categories = json.load(file)

    for category in categories:
        for model in category["models"]:
            print("=" * 60)
            print("Testing:", model["name"], "(" + model["id"] + ")")
            print("=" * 60)

            # If one model fails (busy, removed, etc.), show the error and keep going
            try:
                test_model(model["id"])
            except Exception as error:
                print("Error:", error)

            print()
