"""
Je Commence par  l'in terface à travers fastapi permettant de recevoir le fichier uploader via une requête POST.

Je vais créer un point de terminaison qui acceptera les fichiers téléchargés et les enregistrera sur le serveur.
"""

import aiofiles
import os


# import des bibliothèques nécessaires
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse


# je précise le repertoire dans lequel mon fichier serait enregistré
FILE_DIRECTORY = "/home/blessed/Documents/projet_church/project/ingestion/uploads/"
os.makedirs(FILE_DIRECTORY, exist_ok=True)

# je crée mon instance de l'application FastAPI
inst_app = FastAPI()


# maintenant, je crée le point de terminaison pour l'upload du fichier
@inst_app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
	"""
	Cette fonction gère l'upload d'un fichier via une requête POST. et il
	n'accepte que un pdf
	Args:
			file (UploadFile): Le fichier téléchargé via le formulaire.
	"""

	# je construis le chemin du fichier à enregistrer
	file_path = os.path.join(FILE_DIRECTORY, file.filename)

	# je lis les premiers octets du fichier pour vérifier son type
	header = await file.read(16)
	# je remets le curseur au début du fichier
	await file.seek(0)

	# je vérifie si le fichier est un PDF en vérifiant son en-tête
	if not header.startswith(b"%PDF"):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Seuls les fichiers PDF sont acceptés.",
		)

	# je sauvegarde le fichier sur le serveur
	async with aiofiles.open(file_path, "wb") as monfichier:
		# je cree une boucle pour ecrire le fichier par morceaux
		while  True  :
			contenu = await file.read (1024 * 1024)  # lire par morceaux de 1 Mo
			if not contenu :
				break
			await monfichier.write (contenu)
	return {"filename": file.filename, "message": "Fichier téléchargé avec succès"}
# je crée une page HTML simple pour tester l'upload via un formulaire
@inst_app.get("/upload", response_class=HTMLResponse)
async def upload_form():

	"""Renvoie un formulaire HTML pour télécharger un fichier."""
	return """
		<html lang="fr">
		<head>
		<meta charset="utf-8"/>
		<title>Upload — fond unique</title>
		<meta name="viewport" content="width=device-width,initial-scale=1"/>
		<style>
			html,body{height:100%;margin:0;}
			body{
			/* Image du background */
			background-image: url('https://picsum.photos/id/1018/1920/1080');
			background-size: cover;
			background-position: center;
			background-attachment: fixed; /* fond constant lors du scroll */
			font-family: Inter, Arial, Helvetica, sans-serif;
			}
			.center {min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;}
			.card{background:rgba(255,255,255,0.92);padding:22px;border-radius:10px;max-width:720px;width:94%;box-shadow:0 8px 24px rgba(0,0,0,0.14);text-align:center;}
			input[type="file"]{margin-top:12px;}
			.note{font-size:0.9rem;color:#333;margin-top:12px;}
			#result{margin-top:12px;font-weight:600;}
		</style>
		</head>
		<body>
		<div class="center">
			<div class="card" role="main">
			<h1>Uploader votre fichier</h1>
			<form id="uploadForm" action="/uploadfile/" enctype="multipart/form-data" method="post">
				<input name="file" type="file" required />
				<br/><br/>
				<input type="submit" value="Uploader" />
			</form>

			<div id="result" aria-live="polite"></div>

			<br>
			<p class="note">Ou utilisez <a href="/docs">/docs</a> (Swagger).</p>
			</div>
		</div>


		<script>
			const form = document.getElementById('uploadForm');
			const result = document.getElementById('result');

			form.addEventListener('submit', async (e) => {
			e.preventDefault();
			result.textContent = 'Envoi en cours...';
			result.style.color = '#333';

			try {
				const formData = new FormData(form);
				const resp = await fetch('/uploadfile/', { method: 'POST', body: formData });
				const data = await resp.json();

				if (resp.ok) {
				// afficher le message de succès voulu
				result.textContent = 'Fichier traité avec succès' + (data.filename ? ' — ' + data.filename : '');
				result.style.color = 'green';
				} else {
				// FastAPI erreur -> { detail: ... } ou message personnalisé
				result.textContent = data.detail || data.message || 'Erreur lors de l\\'upload';
				result.style.color = 'crimson';
				}
			} catch (err) {
				result.textContent = 'Erreur réseau : ' + err.message;
				result.style.color = 'crimson';
			}
			});
		</script>
		</body>
		</html>
	"""
# je crée une route racine pour vérifier que l'API fonctionne
@inst_app.get("/")
async def root():
	return {
		"status": "ok",
		"message": "API en route. "
		"Utilisez POST /uploadfile/ pour téléverser un fichier.",
	}
