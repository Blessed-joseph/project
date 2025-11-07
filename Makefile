.PHONY: install test format lint run all clean

# Installation des dépendances
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

# Exécution des tests avec pytest
test:
	python -m pytest -vv --cov=ingestion --cov-report=term-missing ingestion/tests

# Formatage du code avec Black

format:
	black ingestion/*.py
	black extraction/*.py

# Analyse statique du code avec ruff# Analyse statique du code avec ruff (et garde pylint en option)
ruff:
	ruff check ingestion --fix
	ruff check extraction --fix

lint: ruff
	pylint --disable=R,C ingestion/*.py
# 	on le fait pour tout les fichier py dans le  repertoire 
	pylint --disable=R,C extraction/*.py

# Lancer l'application FastAPI
run:
# 	python -m uvicorn ingestion.main:inst_app --reload
# 	 j'exécute le fichier main de extraction pour avoir mon pdf
	python -m extraction.extract

# Exécuter un test spécifique
one-test:
	python -m pytest -vv ingestion/tests/test_main.py::test_directory_creation 

# # Nettoyer les fichiers temporaires
# clean:
#     find . -type f -name "*.pyc" -delete
#     find . -type d -name "__pycache__" -exec rm -rf {} +

# Tout exécuter : installation, formatage, linting, tests
all: install format lint test