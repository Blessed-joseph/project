from extraction.extract_info import extraire_infos


# je donne au programme le chemin vers le fichier pdf


def main():
    # le chemin du fichier à traiter
    pdf_path = (
        "/home/blessed/Documents/projet_church/project/uploads/DAILY MANNA_2026.pdf"
    )
    infos = extraire_infos(pdf_path)

    texte = infos.get("key_verse")
    # print(texte)



if __name__ == "__main__":
    main()
