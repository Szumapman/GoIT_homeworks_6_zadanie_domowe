import sys
import os
import shutil
import re
import datetime

# additional library requiring installation (pip install cowsay) used to display final information 
import cowsay # you can comment out this line if you don't want to use cowsay


def get_path() -> str:
    """
    The function checks whether the user has entered an additional parameter on the command line in the form of a path to the directory he wants to sort out. 
    If not, the program terminates, telling the user what the run command should look like with the additional parameter included. 
    If the path is correct (leads to the directory) it is returned as a string.

    :rtype: str
    """
    exit_help = f"Stars program with command like: {sys.argv[0]} /user/folder_to_sort/ (path to folder you want to sort)."
    if len(sys.argv) < 2:
        sys.exit(f"Too few command-line arguments.\n{exit_help}")
    elif len(sys.argv) > 2:
        sys.exit(f"Too many command line arguments.\n{exit_help}")
    folder_path = sys.argv[1] 
    if os.path.exists(os.path.dirname(folder_path)) and os.path.isdir(folder_path):
        return folder_path
    sys.exit(f"{folder_path} is not a proper folder path.\n{exit_help}")
        
def sort_folder(path):
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
    # lista plików i katalogów znajdujących się w danym katalogu
    files = list(os.scandir(path))
    for file in files:
        # sprawdzam czy to katalog, jeśli tak to normalizuję jego nazwę i rekurencyjnie wywołuję funkcję sort_folder
        if file.is_dir():
            # usuwanie pustych katalogów
            temp_list = list(os.scandir(file.path))
            if len(temp_list) == 0:
                os.rmdir(file.path)
            # pominięcie katalogów która są wykluczone z sortowania
            if not file.name in ["images", "video", "documents", "audio", "archives"]:
                dir_name = normalize(file.name)
                dir_path = f"{path}/{dir_name}"
                # sprawdzam, czy nastąpiła zmiana nazwy katalogu po uzyciu funkcji normalize i jeśli tak przenoszę zawartość do katalogu z nową nazwą
                if dir_name != file.name:
                    #sprawdzam czy w katalogu nie istnieje już katalog który kolidowałby z nową nazwą, jeśli tak dodaje numerowaną wersję
                    for entry in files:
                        if dir_name == entry.name:
                            dir_path = set_dest_path(f"{path}/", dir_name)
                
                    # przenoszę zawartość katalogu ze zmienioną nazwą
                    try:
                        os.renames(f"{path}/{file.name}", dir_path)
                    except FileExistsError:
                        print(
                            f"Directory {dir_name} has not been copied, because too many directories with that name already exist."
                        )
                        continue

                # rekurencyjne wywołanie funkcji dla niepustych katalogów        
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
            
    # dodaje informacje do raportu
    create_report(extensions, paths, path)

            

def normalize(name: str) -> str:
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

def create_report(extensions: dict, paths: dict, path: str):
    # sprawdzam, czy w danym katalogu będą informacje do zapisania w raporcie
    contain_data_to_report = False
    for value in extensions.values():
        if len(value) > 1:
            contain_data_to_report = True
    # jeśli są dane do zapisu zapisuję je
    if contain_data_to_report:      
        now = datetime.datetime.now()
        with open(report_file, "a") as fo:
            fo.write(f"{3*'>'} Activity report for directory: {path} - {now.strftime('%Y-%m-%d %H:%M:%S')}:\n")
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
            fo.write(f"\n{20*'-'}\n\n")

# # dodatkowe informacje wyświetlane w konsoli na zakończenie programu - wymaga import cowsay
def end_info(path: str) -> str:
    # nazwa pliku z raportem (domyślnie raport jest zapisywany w folderze programu)
    report_file = "report.txt" 
    report_file_path, _ = sys.argv[0].rsplit("/", maxsplit=1)
    return f"{report_file_path}/{report_file}"


def main():
    path = get_path()
    sort_folder(path)
    cowsay.tux(f"I've sorted your files in {path}.\nReport file is here: {end_info(path)}") # you can comment out this line if you don't want to use cowsay
    # print(f"I've sorted your files in {path}.\nReport file is here: {end_info(path)}") # uncomment this line if not using cowsay


if __name__ == "__main__":
    main()