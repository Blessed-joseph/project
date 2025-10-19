import os


from ingestion.main import FILE_DIRECTORY as file_directory

def test_directory_creation():

    # je verifie si le repertoire existe belle et bien
    assert os.path.exists(file_directory), f"Le répertoire {file_directory} n'a pas été créé."
    # je verifie si c'est bien un repertoire
    assert os.path.isdir(file_directory), f"{file_directory} existe mais ce n'est pas un répertoire."


