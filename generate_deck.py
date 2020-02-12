import genanki
import os
import subprocess
from pathlib import Path

# Parameters
SOURCE_DIR = "./source"
OUTPUT_DIR = "./output"

TEMPOS = [60, 80, 100, 120]

# Generation
def find_source_files():
    source_filenames = [f for f in os.listdir(SOURCE_DIR)]
    source_files = [get_source_file_metadata(f) for f in source_filenames]

    return source_files

def get_source_file_metadata(filename):
    filename_without_extension = Path(filename).stem
    parts = filename_without_extension.split("_")

    page = int(parts[0])
    size = parts[1]
    x = int(size.split("x")[0])
    y = int(size.split("x")[1])

    name = " ".join(parts[2:])

    return {"source_filename": os.path.join(SOURCE_DIR, filename), "basename": filename_without_extension, "page": page, "x": x, "y": y, "name": name}

def assign_page_count(source_files):
    source_files = sorted(source_files, key = lambda f: f["page"])

    source_files_with_page_count = [source_files[0]]
    source_files_with_page_count[0]["page_count"] = 0

    for file in source_files[1:]:
        if file["name"] == source_files_with_page_count[-1]["name"]:
            new_page_count = source_files_with_page_count[-1]["page_count"] + 1
        else:
            new_page_count = 0

        source_files_with_page_count.append(file)
        source_files_with_page_count[-1]["page_count"] = new_page_count

    return source_files_with_page_count


def generate_exercise_data_for_file(source_file):
    normalised_name = f"{os.path.join(OUTPUT_DIR, Path(source_file['source_filename'].replace(' ', '')).stem)}-%d.png"

    x_crop = 100 / source_file["x"]
    y_crop = 100 / source_file["y"]
    crop_settings = f"{y_crop}%x{x_crop}%"

    subprocess.run(["convert", source_file["source_filename"], "-crop", crop_settings, normalised_name])

    exercise_numbers = []
    for i in range(1, source_file["x"] + 1):
        for j in range(0, source_file["y"]):
            exercise_numbers.append(i + source_file["x"] * j)

    file_number_to_exercise_number = zip(range(0, len(exercise_numbers)), exercise_numbers)

    return [{"name": f"{source_file['name']} {exercise[1]}", "filename": f"{os.path.join(OUTPUT_DIR, Path(source_file['source_filename'].replace(' ', '')).stem)}-{exercise[0]}.png", "basename": f"{source_file['basename']}-{exercise[0]}.png"} for exercise in file_number_to_exercise_number]

def generate_package(exercise_data):
    deck = genanki.Deck(
        1593336103, # Consistent deck ID for Anki
        "Stick Control for the Snare Drummer"
    )

    model = genanki.Model(
        1593336103,
        "Drum rudiment",
        fields=[
            {"name": "Rudiment"},
            {"name": "Tempo"},
            {"name": "Image"}
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Rudiment}}<br>{{Tempo}}bpm<br>{{Image}}",
                "afmt": "{{FrontSide}}"
            }
        ]
    )

    deck.add_model(model)

    for exercise in exercise_data:
        for tempo in TEMPOS:
            deck.add_note(genanki.Note(
                model = model,
                fields = [exercise["name"], str(tempo), f'<img src="{exercise["basename"]}">']
            ))

    package = genanki.Package(deck)
    package.media_files = [exercise["filename"] for exercise in exercise_data]

    return package

# From https://coderwall.com/p/rcmaea/flatten-a-list-of-lists-in-one-line-in-python
# (but should be in the stdlib)
def flatten(l):
    return [y for x in l for y in x]

def main():
    source_files = assign_page_count(find_source_files())
    print(source_files)
    exercise_data = flatten([generate_exercise_data_for_file(f) for f in source_files])

    package = generate_package(exercise_data)
    package.write_to_file("snare_control.apkg")

if __name__ == "__main__":
    main()
