#!/bin/bash

# Chemin vers le projet Django (ajusté pour mission1Backend)
PROJECT_DIR="/home/heil/Desktop/Projet e-RANIS/Mission1-Eranis/mission1Backend"
MANAGE_PY="$PROJECT_DIR/manage.py"
VENV_ACTIVATE="$PROJECT_DIR/../venv/bin/activate"

# Vérifier si l'environnement virtuel existe
if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "Erreur : L'environnement virtuel n'a pas été trouvé à $VENV_ACTIVATE"
    echo "Vérifiez le chemin ou créez un environnement virtuel avec :"
    echo "cd $PROJECT_DIR/.. && python3 -m venv venv"
    exit 1
fi

# Vérifier si manage.py existe
if [ ! -f "$MANAGE_PY" ]; then
    echo "Erreur : manage.py n'a pas été trouvé à $MANAGE_PY"
    exit 1
fi

# Créer un fichier Python temporaire pour insérer les données
TEMP_SCRIPT="/tmp/populate_categories_sous_domaines.py"

# Écrire le script Python dans le fichier temporaire
cat << EOF > $TEMP_SCRIPT
from profils.models import Categorie, SousDomaine

# Données à insérer
domaines_freelance = [
    {
        "categorie": "Services techniques",
        "sous_domaines": [
            "Plomberie", "Électricité bâtiment", "Maçonnerie", "Menuiserie bois",
            "Menuiserie aluminium", "Peinture bâtiment", "Mécanique auto",
            "Mécanique moto", "Carrelage", "Soudure", "Entretien de groupes électrogènes",
            "Réparation d'appareils électroménagers", "Pose de faux plafonds",
            "Installation de caméras de surveillance", "Pose de climatiseurs"
        ]
    },
    {
        "categorie": "Beauté & soins",
        "sous_domaines": [
            "Coiffure hommes", "Coiffure femmes", "Tresses africaines",
            "Coloration et soin capillaire", "Maquillage professionnel", "Esthétique",
            "Massage", "Manicure / pédicure", "Soins de peau (acné, etc.)",
            "Extension de cils / ongles", "Tatouage artistique", "Spa à domicile"
        ]
    },
    {
        "categorie": "Éducation & rédaction",
        "sous_domaines": [
            "Cours de soutien scolaire (primaire, collège, lycée)",
            "Préparation aux concours (ENAM, ENS, etc.)", "Aide à la rédaction de mémoires",
            "Aide à la rédaction de rapports de stage", "Correction et relecture",
            "Traduction (FR-EN, EN-FR)", "Cours de langues (anglais, français, allemand)",
            "Cours d'informatique de base", "Cours de programmation",
            "Formation bureautique (Word, Excel, PowerPoint)"
        ]
    },
    {
        "categorie": "Numérique & IT",
        "sous_domaines": [
            "Développement web (vitrine, e-commerce)", "Développement mobile (Android/iOS)",
            "Infographie / design graphique", "Design UI/UX", "Montage vidéo",
            "Photographie professionnelle", "Création de contenus visuels (affiches, flyers)",
            "Community management", "Création de logos et chartes graphiques",
            "Gestion de campagnes publicitaires (Facebook, Google)", "Référencement SEO",
            "Maintenance de sites web", "Formation informatique"
        ]
    },
    {
        "categorie": "Livraison & commerce",
        "sous_domaines": [
            "Livraison à moto (documents, repas, colis)",
            "Livraison interurbaines (Express Union, agences)", "Vente de vêtements",
            "Vente de chaussures", "Vente de téléphones/accessoires",
            "Vente de produits cosmétiques", "Vente de produits alimentaires secs (arachide, riz, huile)",
            "Livraison de gaz domestique", "Courses pour particuliers ou entreprises",
            "Gestion de boutiques en ligne (Facebook/Instagram)"
        ]
    },
    {
        "categorie": "Restauration",
        "sous_domaines": [
            "Préparation de plats traditionnels (ndolè, eru, etc.)", "Cuisine à domicile",
            "Traiteurs pour événements", "Livraison de repas au bureau",
            "Préparation de jus naturels", "Snack mobile (télé-brazzas, sandwichs, beignets-haricot)",
            "Vente de pâtisseries", "Grillades (poisson, porc, brochettes)"
        ]
    },
    {
        "categorie": "Mode & couture",
        "sous_domaines": [
            "Couture homme sur mesure", "Couture femme sur mesure",
            "Création de sacs, accessoires et pochettes", "Broderie traditionnelle",
            "Sérigraphie sur tee-shirts", "Stylisme personnalisé", "Création de perles",
            "Transformation et ajustement de vêtements"
        ]
    },
    {
        "categorie": "Art & événementiel",
        "sous_domaines": [
            "Animation DJ", "Animateur/présentateur d’événements", "Photographe de mariage",
            "Tournage et montage de vidéos d'événements", "Création de clips musicaux",
            "Groupes de danse / ballet traditionnel", "Influenceurs / créateurs de contenu (TikTok, Instagram)",
            "Décoration de salles", "Maître de cérémonie", "Vente/location de matériel d'événement"
        ]
    },
    {
        "categorie": "Agriculture & élevage",
        "sous_domaines": [
            "Agriculteur (maïs, manioc, arachide, etc.)", "Éleveur (poules, porcs, moutons)",
            "Pisciculture", "Transformation de produits agricoles (farines locales)",
            "Vente de produits frais (œufs, légumes, etc.)", "Livraison de produits agro",
            "Apiculture (miel local)", "Fertilisants bio artisanaux"
        ]
    },
    {
        "categorie": "Services domestiques",
        "sous_domaines": [
            "Ménage à domicile", "Baby-sitting", "Repassage à domicile",
            "Blanchisserie (ramassage/livraison)", "Aide aux personnes âgées",
            "Cuisine de maison", "Jardinage"
        ]
    }
]

# Supprimer les données existantes (optionnel, décommentez si nécessaire)
# Categorie.objects.all().delete()
# SousDomaine.objects.all().delete()

# Insérer les catégories et sous-domaines
for domaine in domaines_freelance:
    categorie, created = Categorie.objects.get_or_create(nom=domaine['categorie'])
    for sous_domaine_nom in domaine['sous_domaines']:
        SousDomaine.objects.get_or_create(nom=sous_domaine_nom, categorie=categorie)

print("Données insérées avec succès !")
EOF

# Activer l'environnement virtuel
source "$VENV_ACTIVATE"

# Vérifier si l'activation a réussi
if [ $? -ne 0 ]; then
    echo "Erreur : Impossible d'activer l'environnement virtuel à $VENV_ACTIVATE"
    exit 1
fi

# Exécuter le script Python via manage.py shell
python "$MANAGE_PY" shell < $TEMP_SCRIPT

# Vérifier si l'exécution a réussi
if [ $? -ne 0 ]; then
    echo "Erreur : Échec de l'exécution de manage.py shell"
    rm $TEMP_SCRIPT
    exit 1
fi

# Supprimer le fichier temporaire
rm $TEMP_SCRIPT

echo "Population des tables Categorie et SousDomaine terminée."