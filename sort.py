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
        if file.is_dir():
            if not file.name in ["images", "video", "documents", "audio", "archives"]:
                sort_folder(f"{path}/{file.name}")
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
                    # trzeba usupełnić o rozpakowywanie
                    dest_folder_name = "/archives/"
            if os.path.exists(f"{path}{dest_folder_name}{file_name}{ext}"):
                for i in range(1, 1000000):
                    if not os.path.exists(f"{path}{dest_folder_name}{file_name} ({i}){ext}"):
                        file_name += f" ({i})"
                        break
            try:
                os.renames(f"{path}/{file.name}", f"{path}{dest_folder_name}{file_name}{ext}")
            except FileExistsError:
                print(f"File {file_name}{ext} has not been copied, because too many files with that name already exist in the destination directory.")
                continue
def normalize(name: str) -> str:
    normalized_name = name.translate(polish_chars) # zmieniam polskie znaki na łacińskie odpowiedniki 
   
    # zmieniam inne niedozwolone w nazwie znaki na znak _
    normalized_name = re.sub(r"\W+", "_", normalized_name)

    return normalized_name
    

def main():
    sort_folder(get_path())

if __name__ == "__main__":
    main()



