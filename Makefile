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

# Analyse statique du code avec pylint
lint:
	pylint --disable=R,C ingestion/main.py

# Lancer l'application FastAPI
run:
	python -m uvicorn ingestion.main:inst_app --reload

# Exécuter un test spécifique
one-test:
	python -m pytest -vv ingestion/tests/test_main.py::test_directory_creation 

# # Nettoyer les fichiers temporaires
# clean:
#     find . -type f -name "*.pyc" -delete
#     find . -type d -name "__pycache__" -exec rm -rf {} +

# Tout exécuter : installation, formatage, linting, tests
all: install format lint test