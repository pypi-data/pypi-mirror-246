import csv
import json

def demander_type_de_fichier():
    
    # Demander à l'utilisateur de choisir le type de fichier
    choix = input("Veuillez choisir le type de fichier (csv, json, text): ").lower()
        
    # Vérifier le choix de l'utilisateur
    if choix == 'csv' :
        print('pour faire des manu sur un fichier csv appeler la method,"csv_files() "')
    elif choix == 'text' :
        print('pour faire des manu sur un fichier txt appeler la method,"txt_file()"')
    elif choix == 'json':
        print('pour faire des manu sur un fichier json appeler la method,"json_fichier()"')   
    else :
        print("Choix invalide. Veuillez choisir parmi 'csv', 'json' ou 'text'.")

#les fichier -(txt) :

def txt_file() :
    mode = input("-pour créer un fichier: taper 'x'\n-pour lire un fichier: taper 'r'\n-pour écrire dans un fichier: taper 'w'\n-pour ajouter a un fichier: taper 'a' ").lower()
    if mode == 'r' : 
        fichier = input("entrer le nom de fichier avec l'extention")
        lecture_mode = input("pour lire tous le contenu taper: 't'\npour lire le premier ligne taper: 'l'\npour lire le premier charactere taper: 'ch'").lower()
        if lecture_mode == 't' :
            f = open(fichier,"r")
            read_file = f.read()
            print(read_file)
            f.close()
            return f"succed"
        elif lecture_mode == 'l' :
            f = open(fichier,"r")
            read_line = f.readline()
            print(read_line)
            f.close() 
            return f"succed"
        elif lecture_mode == 'ch' :
            nbr_ch = int(input('entre le nombre des caractere tu va lire'))
            f = open(fichier,"r")
            read_ch = f.read(nbr_ch)
            print(read_ch)
            f.close()
            return f"succed"
        else :
            print("Choix invalide. Veuillez choisir parmi 't', 'l' ou 'ch'.")    
    elif mode == 'a' :
        fichier = input("entrer le nom de fichier avec l'extention")
        contenu = input('entrer le contenu tu va ajouter ou fichier')
        f = open(fichier,"a")
        f.write(contenu)
        f.close()
        return f"le text est ajouté."
    elif mode == 'w' :
        fichier = input("entrer le nom de fichier avec l'extention")
        content = input('entrer le contenu tu va ajouter ou fichier')
        f = open(fichier,"w")
        f.write(content)
        f.close()
        return f"le text est ajouté,est le precedent text est supprimé."
    elif mode == 'x' :
        fichier = input("entrer le nom de fichier avec l'extention")
        nom_fichier = input('entrer le nom de fichier tu va créer avec l"extention')
        f = open(nom_fichier,'x')
        f.close()
        return f"le fichier est créer."
    else :
        print("Choix invalide. Veuillez choisir parmi 'r', 'a', 'w' ou 'x'.")

#les fichier -(csv) :

def csv_files() :
    mode = input("-pour créer un fichier: taper 'x'\n-pour lire un fichier: taper 'r'\n-pour écrire dans un fichier: taper 'w'\n-pour ajouter a un fichier: taper 'a' ").lower()
    if mode == 'r' : 
        fichier = input("entrer le nom de fichier csv avec l'extention")
        lecture_mode = input("pour lire tous le contenu taper: 't'\npour lire le contenu comme un dict taper: 'dict'").lower()
        if lecture_mode == 't' :
            f = open(fichier,'r')
            lecteurCSV = csv.reader(f,delimiter=";")
            for i in lecteurCSV :
               print(i)
            f.close()
            return f"succed"
        elif lecture_mode == 'dict' :
            f = open(fichier,'r')
            lecteurCSV = csv.DictReader(f,delimiter=";")
            for i in lecteurCSV :
               print(i)
            f.close()
            return f"succed"
        else :
            print("Choix invalide. Veuillez choisir parmi 't', 'l' ou 'ch'.")    
    elif mode == 'a' :
        fichier = input("entrer le nom de fichier avec l'extention")
        numero_ligne = int(input('entrer le nombre des ligne tu va ajouter'))
        for j in range(numero_ligne) :
            f = open(fichier,'a')
            lecteurCSV = csv.writer(f,delimiter=";")
            print('noté bien que le contenu csv sera ecrire comme sa.["khalidi","hind","11"]')
            contenu_lignes = input('entrer la ligne',i+1)
            lecteurCSV.writerow([contenu_lignes])
            f.close()     
        return f"le contenu est ajouté."
    elif mode == 'w' :
        fichier = input("entrer le nom de fichier avec l'extention")
        numero_ligne = int(input('entrer le nombre des ligne tu va ajouter'))
        for j in range(numero_ligne) :
            f = open(fichier,'a')
            lecteurCSV = csv.writer(f,delimiter=";")
            print('noté bien que le contenu csv sera ecrire comme sa.["khalidi","hind","11"]')
            contenu_lignes = input('entrer la ligne',i+1)
            lecteurCSV.writerow([contenu_lignes])
            f.close()
        return f"le text est ajouté,est le precedent text est supprimé."
    elif mode == 'x' :
        nom_fichier = input('entrer le nom de fichier tu va créer avec l"extention')
        f = open(nom_fichier,'x')
        f.close()
        return f"le fichier est créer."
    else :
        print("Choix invalide. Veuillez choisir parmi 'r', 'a', 'w' ou 'x'.") 

#les fichier -(json) :
    
def json_fichier():
    mode = input("-pour créer un fichier: taper 'x'\n-pour lire un fichier: taper 'r'\n-pour écrire dans un fichier: taper 'w'\n-pour ajouter a un fichier: taper 'a' ").lower()
    if mode == 'r' : 
        fichier = input("entrer le nom de fichier json avec l'extention")
        f = open(fichier,'r')
        lecteurjson = json.loads(f.read())
        for i in lecteurjson :
            print(i)
        f.close()
        return f"succed"
    elif mode == 'a' :
        fichier = input("entrer le nom de fichier avec l'extention")
        f = open(fichier,'a')
        contenu_json = input('entrer le contenu')
        f.write(json.dumps(contenu_json))
        f.close()     
        return f"le contenu est ajouté."
    elif mode == 'w' :
        fichier = input("entrer le nom de fichier avec l'extention")
        f = open(fichier,'a')
        contenu_json = input('entrer le contenu')
        f.write(json.dumps(contenu_json))
        f.close()
        return f"le text est ajouté,est le precedent text est supprimé."
    elif mode == 'x' :
        nom_fichier = input('entrer le nom de fichier tu va créer avec l"extention')
        f = open(nom_fichier,'x')
        f.close()
        return f"le fichier est créer."
    else :
        print("Choix invalide. Veuillez choisir parmi 'r', 'a', 'w' ou 'x'.")
    
