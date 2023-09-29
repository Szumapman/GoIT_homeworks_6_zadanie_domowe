import sys
import os
import shutil
import re
import datetime

# import cowsay # dodatkowa bilioteka wymagająca instalacji (pip install cowsay) używana do wyświetlenia końcowych informacji

# pomocniczy słownik polskich znaków, używany w funkcji normalize, zawiera polskie znaki, które będą zamieniane na odpowiedniki łacińskie
polish_chars = {
    ord("ą"): "a",
    ord("Ą"): "A",
    ord("ć"): "c",
    ord("Ć"): "C",
    ord("ę"): "e",
    ord("Ę"): "E",
    ord("ł"): "l",
    ord("Ł"): "L",
    ord("ń"): "n",
    ord("Ń"): "N",
    ord("ó"): "o",
    ord("Ó"): "O",
    ord("ś"): "s",
    ord("Ś"): "Ś",
    ord("ź"): "z",
    ord("Ż"): "Z",
    ord("ż"): "z",
    ord("Ż"): "Z",
}
# pomocnicze słowniki do przechowywania danych o przetwarzanych plikach
extensions = {
    "images": set(),
    "documents": set(),
    "audio": set(),
    "video": set(),
    "archives": set(),
    "unsorted": set(),
}
paths = {
    "images": [],
    "documents": [],
    "audio": [],
    "video": [],
    "archives": [],
    "unsorted": [],
}


def get_path():
    exit_help = f"Stars program with command like: {sys.argv[0]} /user/folder_to_sort/ (path to folder you want to sort)."
    if len(sys.argv) < 2:
        sys.exit(f"Too few command-line arguments.\n{exit_help}")
    elif len(sys.argv) > 2:
        sys.exit(f"Too many command line arguments.\n{exit_help}")
    folder_path = sys.argv[1]
    if os.path.exists(os.path.dirname(folder_path)):
        return folder_path
    sys.exit(f"{folder_path} is not a proper folder path.\n{exit_help}")

def sort_folder(path):
    files = os.scandir(path)
    for file in files:
        # sprawdzam czy to katalog, jeśli tak to normalizuję jego nazwę i rekurencyjnie wywołuję funkcję sort_folder
        if file.is_dir():
            # usuwanie pustych katalogów
            temp_list = list(os.scandir(file.path))
            if len(temp_list) == 0:
                os.rmdir(file.path)

            if not file.name in ["images", "video", "documents", "audio", "archives"]:
                dir_name = normalize(file.name)
                dir_path = f"{path}/{dir_name}"
                try:
                    os.renames(f"{path}/{file.name}", dir_path)
                except FileExistsError:
                    # jeśli katalog o takiej nazwie już istniał ustawiam nową nazwę katalogu
                    dir_path = set_dest_path(f"{path}/", dir_name)
                    try:
                        os.renames(f"{path}/{file.name}", dir_path)
                    except:
                        print(
                            f"Directory {dir_name} has not been copied, because too many directories with that name already exist."
                        )
                        continue

                sort_folder(dir_path)

        # działania na plikach
        else:
            file_name, ext = os.path.splitext(file.name)
            file_name = normalize(file_name)
            file_type = ""
            match ext:
                case ".jpeg" | ".png" | ".jpg" | ".svg":
                    file_type = "images"
                case ".avi" | ".mp4" | ".mov" | ".mkv":
                    file_type = "video"
                case ".doc" | ".docx" | ".txt" | ".pdf" | ".xlsx" | "pptx":
                    file_type = "documents"
                case ".mp3" | ".ogg" | ".wav" | ".amr":
                    file_type = "audio"
                case ".zip" | ".gz" | ".tar":
                    file_type = "archives"
                    # archiwum jest od razu rozpakowywane do folderu archives/"nazwa archiwum bez rozszerzenia"
                    shutil.unpack_archive(
                        f"{path}/{file.name}", f"{path}/{file_type}/{file_name}/"
                    )
                case _:
                    file_type = "unsorted"

            # przenoszę pliki (z wyjątkiem tych o nieuwzględnianych rozszerzeniach) do odpowiednich katalogów
            if file_type != "unsorted":
                dest_path = set_dest_path(f"{path}/{file_type}/", file_name, ext)
                try:
                    os.renames(f"{path}/{file.name}", dest_path)
                except FileExistsError:
                    print(
                        f"File {file_name}{ext} has not been copied, because too many files with that name already exist in the destination directory."
                    )
                    continue

            # dodaje informacje o ścieżkach obrabianych plików i ich rozszerzeniach do słowników paths i extensions
            if paths.get(file_type) != None:
                temp_list = paths.get(file_type)
                if file_type == "unsorted":
                    temp_list.append(f"{path}/{file_type}/{file.name}")
                else:
                    temp_list.append(
                        f"{path}/{file_type}/{file.name} has moved to: {dest_path}"
                    )
                paths.update({file_type: temp_list})
            if extensions.get(file_type) != None:
                temp_set = extensions.get(file_type)
                temp_set.add(ext)
                extensions.update({file_type: temp_set})

            

def normalize(name: str) -> str:
    # zmieniam polskie znaki na łacińskie odpowiedniki na podstawie dict: polish_chars
    normalized_name = name.translate(polish_chars)
    # zmieniam inne niedozwolone w nazwie znaki na znak _
    normalized_name = re.sub(r"\W+", "_", normalized_name)
    return normalized_name
    

def set_dest_path(path: str, file_name: str, ext="") -> str:
    # sprawdzam, czy dany plik / katalog już nie istnieje w dest_folder
    if os.path.exists(f"{path}{file_name}{ext}"):
        # jeśli plik / katalog już istnieje w kolejnych wersjach w dest_folder dodaje do jego nazwy "_i" gdzie i to pierwsza wolna liczba od 1 do 1000000
        for i in range(1, 1000000):
            if not os.path.exists(f"{path}{file_name}_{i}{ext}"):
                file_name += f"_{i}"
                break
    return f"{path}{file_name}{ext}"

def create_report(path):
    now = datetime.datetime.now()
    with open(path, "a") as fo:
        fo.write(f"{3*'>'} Activity report - {now.strftime('%Y-%m-%d %H:%M:%S')}:\n")
        fo.write(f"Extensions of checked files by category:\n")
        no_transfered_data = True
        for key, values in extensions.items():
            if len(values) > 0:
                no_transfered_data = False
                values = list(values)
                fo.write(f"{key}: {' | '.join(values)};\n")
        if no_transfered_data:
            fo.write(f"{3*'-'}")
        fo.write(f"\nFiles sorted by category:\n")
        for key, values in paths.items():
            if len(values) > 0:
                no_transfered_data = False
                fo.write(f"{key}:\n")
                for value in values:
                    fo.write(f"{value};\n")
        if no_transfered_data:
            fo.write(f"{3*'-'}")
        fo.write(f"\n{5*'-'} The end {5*'-'}\n\n")

# # dodatkowe informacje wyświetlane w konsoli na zakończenie programu - wymaga import cowsay
# def end_info(path):
#     report_file, _ = sys.argv[0].rsplit("/", maxsplit=1)
#     report_file += f"/report.txt"
#     cowsay.tux(f"I've sorted your files in {path}.\nReport file is here: {report_file}")


def main():
    path = get_path()
    sort_folder(path)
    create_report("report.txt")
    # end_info(path)


if __name__ == "__main__":
    main()