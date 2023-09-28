import sys
import os
import shutil
import re

# files = os.scandir("C:/Projects/GoIT_homeworks/6/Bałagan")
# for file in files:
#     if file.is_file():
#         print(file.path)
# shutil.move("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/Nowy/lis.pdf")
# os.replace("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/Nowy/lis.pdf")
# os.rename("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/Nowy/lis.pdf")
# os.renames("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/New/lis.pdf")

# os.makedirs("Bałagan/Test")
# os.rmdir("C:/Projects/GoIT_homeworks/6/Bałagan/Test")

# słownik polskich znaków, używany w funkcji normalize, zawiera polskie znaki, które będę zamieniał na odpowiedniki łacińskie
polish_chars = {
        ord('ą'): 'a', ord('Ą'): 'A',
        ord('ć'): 'c', ord('Ć'): 'C',
        ord('ę'): 'e', ord('Ę'): 'E',
        ord('ł'): 'l', ord('Ł'): 'L',
        ord('ń'): 'n', ord('Ń'): 'N',
        ord('ó'): 'o', ord('Ó'): 'O',
        ord('ś'): 's', ord('Ś'): 'Ś',
        ord('ź'): 'z', ord('Ż'): 'Z',
        ord('ż'): 'z', ord('Ż'): 'Z',   
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
            #usuwanie pustych katalogów
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
                        print(f"Directory {dir_name} has not been copied, because too many directories with that name already exist.")
                        continue
                    
                sort_folder(dir_path)
        
        # działania na plikach
        else:
            file_name, ext = os.path.splitext(file.name)
            file_name = normalize(file_name)
            dest_folder_name = ""
            match ext:
                case ".jpeg" | ".png" | ".jpg" | ".svg":
                   dest_folder_name = "/images/"
                case ".avi" | ".mp4" | ".mov" | ".mkv":
                    dest_folder_name = "/video/"
                case ".doc" | ".docx" | ".txt" | ".pdf" | ".xlsx" | "pptx":
                    dest_folder_name = "/documents/"
                case ".mp3" | ".ogg" | ".wav" | ".amr":
                    dest_folder_name = "/audio/"
                case ".zip" | ".gz" | ".tar":
                    dest_folder_name = "/archives/"
                    shutil.unpack_archive(f"{path}/{file.name}", f"{path}{dest_folder_name}{file_name}/") # archiwum jest od razu rozpakowywane do folderu archives/"nazwa archiwum bez rozszerzenia"

            dest_path = set_dest_path(f"{path}{dest_folder_name}", file_name, ext)

            try:
                os.renames(f"{path}/{file.name}", dest_path)
            except FileExistsError:
                print(f"File {file_name}{ext} has not been copied, because too many files with that name already exist in the destination directory.")
                continue


def normalize(name: str) -> str:
    normalized_name = name.translate(polish_chars) # zmieniam polskie znaki na łacińskie odpowiedniki na podstawie dict: polish_chars
    normalized_name = re.sub(r"\W+", "_", normalized_name) # zmieniam inne niedozwolone w nazwie znaki na znak _
    return normalized_name
    

def set_dest_path(path: str, file_name: str, ext="") -> str:
    if os.path.exists(f"{path}{file_name}{ext}"): # sprawdzam, czy dany plik / katalog już nie istnieje w dest_folder
        for i in range(1, 1000000): 
            if not os.path.exists(f"{path}{file_name}_{i}{ext}"): # jeśli plik / katalog już istnieje w kolejnych wersjach w dest_folder ...
                file_name += f"_{i}" # dodaje do jego nazwy "_i" gdzie i to pierwsza wolna liczba od 1 do 1000000
                break
    return f"{path}{file_name}{ext}"


def main():
    sort_folder(get_path())

if __name__ == "__main__":
    main()



