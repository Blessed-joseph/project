"""
Je Commence par  l'in terface à travers fastapi permettant de recevoir le fichier uploader via une requête POST.

Je vais créer un point de terminaison qui acceptera les fichiers téléchargés et les enregistrera sur le serveur.
"""

# import des bibliothèques nécessaires
from fastapi import FastAPI, File, UploadFile
import aiofiles
import os


# je crée mon instance de l'application FastAPI

inst_app = FastAPI()
# je précise le repertoire dans lequel mon fichier serait enregistré

FILE_DIRECTORY = "/home/blessed/Documents/Projet_church/ingestion/uploads/"

# je verifie bien que c'est le bon repertoire, si ce n'est pas le bon, je signale une erreur avec pytest (rappel)
os.makedirs(FILE_DIRECTORY, exist_ok=True)


# maintenant, je crée le point de terminaison pour l'upload du fichier
@inst_app.post("/uploadfile/")
# je definis la fonction asynchrome pour gerer l'upload du fichier
async def upload_file(file: UploadFile = File(...)):
    """_summary_

    Args:
        file (UploadFile, optional): _description_. Defaults to File(...).
    """

    # je construis le chemin du fichier à enregistrer
    file_path = os.path.join(FILE_DIRECTORY, file.filename)

    # comme le fichier est un pdf, je vais essayer de l'ouvrir pour tester sinon on envoie une erreur
    #  en utilisant pytest
    async with aiofiles.open(file_path, "wb") as monfichier:
        content = await file.read()
        await monfichier.write(content)

    return {
        "filename": file.filename,
        "message": "Fichier téléchargé avec succès"
        }
