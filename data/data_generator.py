import random
import csv



# =========================
# 🗣️ INTRODUCTIONS
# =========================
introductions = [
      # Salutations simples
    "Bonjour, j’aurais besoin d’un renseignement s’il vous plaît",
    "Bonsoir, je vous contacte parce que j’ai une préoccupation",
    "Salut, je voulais me renseigner sur quelque chose",

    # Politesse + demande
    "S’il vous plaît, pouvez-vous m’aider à comprendre",
    "Je vous écris pour avoir des informations précises",
    "J’aimerais bien avoir des explications claires",

    # Confusion / incompréhension
    "Je suis un peu perdu par rapport à tout ça",
    "Franchement je ne comprends pas comment ça fonctionne",
    "Honnêtement je suis un peu confus",
    "Je ne comprends pas trop ce qui se passe chez moi",

    # Frustration / problème
    "Ça fait plusieurs jours que j’ai un problème",
    "Depuis hier j’ai un souci chez moi",
    "Franchement ça commence à m’inquiéter",
    "Je suis vraiment fatigué de cette situation",
    "Ça devient compliqué pour moi en ce moment",

    # Urgence
    "S’il vous plaît c’est assez urgent dans mon cas",
    "J’ai vraiment besoin d’une réponse rapide",
    "C’est important pour moi d’avoir une solution",

    # Contexte personnel
    "Je viens d’emménager et je ne comprends pas encore tout",
    "Je suis nouveau dans la zone et j’ai quelques questions",
    "Je reviens au pays et j’essaie de comprendre le système",

    # Mélange naturel (très humain)
    "Bonjour, excusez-moi de vous déranger mais j’ai une question",
    "Bonsoir, je voulais juste comprendre quelque chose rapidement",
    "Svp, j’ai un petit souci et je ne sais pas quoi faire",

    # Langage local / naturel
    "Grand, j’ai un souci avec ça là",
    "On souffre un peu ici, j’aimerais comprendre",
    "Chef, y a un problème ici chez nous",

    # Cas sans intro (très important)
    "",
    "",
    ""
]

# =========================
# 🌍 CONTEXTES
# =========================
contexts = [
    # 📍 Localisation précise
    "chez moi à Adidogomé",
    "dans mon quartier à Lomé",
    "dans la zone où j’habite actuellement",
    "au niveau de mon secteur ici",
    "dans ma zone de résidence",
    "dans notre quartier ici à Tokoin",
    "chez nous dans le quartier",
    "dans la zone où je viens d’emménager",

    # ⏱️ Temps / durée
    "depuis ce matin",
    "depuis quelques jours déjà",
    "ça fait plusieurs jours maintenant",
    "depuis hier soir",
    "ça dure depuis un bon moment",
    "depuis que je suis rentré à la maison",
    "récemment j’ai commencé à remarquer ça",

    # 🏠 Situation personnelle
    "pour ma maison",
    "dans mon foyer",
    "dans ma concession",
    "chez moi avec ma famille",
    "dans ma nouvelle maison",
    "dans la maison que je viens de louer",
    "pour mon habitation principale",

    # 👨‍👩‍👧‍👦 Composition du foyer
    "pour une famille de 5 personnes",
    "on est plusieurs à la maison",
    "nous sommes une grande famille ici",
    "on est environ 4 à utiliser l’eau",
    "dans un foyer avec plusieurs enfants",

    # 🚰 Technique / compteur / installation
    "au niveau de mon compteur",
    "au niveau de l’installation d’eau",
    "sur mon branchement actuel",
    "au niveau des robinets chez moi",
    "sur toute l’installation dans la maison",
    "par rapport à mon abonnement actuel",

    # 🌍 Retour / déménagement
    "je viens d’emménager ici",
    "je suis nouveau dans cette zone",
    "je reviens au pays récemment",
    "je viens juste de prendre la maison",

    # ⚠️ Problème concret
    "où l’eau ne coule presque pas",
    "où la pression est très faible",
    "où l’eau est un peu sale",
    "où on a souvent des coupures",

    # 🗣️ Langage local / naturel
    "chez nous ici là",
    "dans mon coin ici",
    "là où je suis actuellement",
    "chez moi même ici",

    # 🔀 Contextes mixtes (TRÈS IMPORTANT)
    "chez moi à Adidogomé depuis ce matin",
    "dans mon quartier à Lomé depuis quelques jours",
    "dans ma maison avec ma famille depuis hier",
    "au niveau de mon compteur depuis un moment",
    "chez moi où la pression est très faible depuis plusieurs jours",

    # ❌ Sans contexte (important pour équilibre)
    "",
    "",
    ""
]

# =========================
# 🙏 POLITESSE
# =========================
politeness = [
    "merci",
    "merci beaucoup",
    "svp",
    "s’il vous plaît",
    "je vous remercie",
    "merci d’avance",
    "aidez-moi svp",
    "je compte sur vous",
    "pardon pour le dérangement",
    "veuillez m’aider s’il vous plaît",

    # langage oral
    "merci hein",
    "svp j’ai besoin d’aide",

    "", "", ""
]
sentence_styles = [
    "simple",
    "long",
    "emotion",
    "indirect",
    "broken"
]
# =========================
# 🎯 INTENTS COMPLETS
# =========================
intents = {

"info_generale_tde": [

    # acronymes + nom complet
    "c'est quoi la tde",
    "c'est quoi la société togolaise des eaux",
    "expliquez moi la société togolaise des eaux",
    "je veux comprendre la tde",
    "je veux comprendre la société togolaise des eaux",
    "la tde ça sert à quoi exactement",
    "vous faites quoi exactement à la tde",
    "expliquez moi votre rôle",
    "je veux comprendre vos services",
    "présentez moi la société d’eau",
    "la tde c’est quelle structure au juste",

    # variantes naturelles
    "c’est quoi votre société d’eau exactement",
    "vous êtes le fournisseur d’eau national c’est ça",
    "expliquez moi le service d’eau au togo",
    "qui gère la distribution d’eau ici au togo",
    "c’est quelle structure qui s’occupe de l’eau potable",

    # mélange (très puissant)
    "la tde c’est bien la société togolaise des eaux non",
    "je veux comprendre la tde la société togolaise des eaux exactement",
    "expliquez moi votre rôle en tant que société togolaise des eaux",
    "vous êtes la tde donc la société d’eau du togo c’est ça",

    # formulations longues réalistes
    "bonjour je voudrais comprendre ce qu’est la société togolaise des eaux et quel est son rôle dans la distribution d’eau potable au togo",
    "je suis nouveau ici et j’aimerais savoir ce que fait exactement la tde aussi appelée société togolaise des eaux",
    "svp expliquez moi clairement la société togolaise des eaux ses missions et les services que vous proposez",
    "bonjour je voudrais savoir c'est quoi exactement la tde et quel est votre rôle dans le pays",
    "svp expliquez moi un peu la tde parce que je comprends pas trop vos services",
    "je suis nouveau ici à lomé je veux savoir c’est quoi la tde et ce que vous faites exactement",
    "on m’a parlé de la tde mais j’aimerais comprendre concrètement vos missions",
    "je veux savoir à quoi sert la tde dans notre quotidien",

    # langage local
    "la société d’eau là au togo vous faites quoi exactement",
    "c’est vous qui gérez toute l’eau potable ici au pays",
    "on dit tde tde mais vous faites quoi concrètement",
    "vous êtes les responsables de l’eau dans tout lomé ou bien",
    "expliquez moi un peu votre travail là j’ai pas bien capté",

    # fautes
    "societe togolaise des eau c'est quoi",
    "c quoi la societe des eau au togo",
    "c quoi la tde exactement",
    "expliker moi votre role svp",
    "je veu comprendre vos service",
    "la tde sa sert a quoi",
    "vous faite quoi exactement a la tde",

    # ambiguïtés intéressantes
    "je veux des informations sur votre société",
    "parlez moi un peu de vous",
    "je veux comprendre votre fonctionnement",
    "vous pouvez m’expliquer votre organisation",
    "je veux connaitre vos activités principales",

    # cas avec émotion / frustration
    "honnêtement je ne comprends même pas votre rôle quelqu’un peut m’expliquer",
    "ça fait longtemps que j’entends parler de la tde mais je ne sais toujours pas ce que vous faites",
    "je suis un peu confus pouvez-vous m’expliquer clairement votre mission",
    "aidez moi svp je veux juste comprendre ce que fait la tde",

    # mix complet (très réaliste)
    "bonjour svp je suis un peu perdu je viens d’arriver à lomé et j’aimerais comprendre c’est quoi exactement la societe togolaise des eaux et quels services vous proposez aux habitants",
    "bonsoir ça peut paraitre simple mais je ne comprends pas bien votre rôle est-ce que vous pouvez m’expliquer clairement ce que fait la tde societe togolaise des eaux au quotidien",
    "salut j’aimerais avoir une explication complète sur votre société notamment vos missions vos services et votre importance pour la population"
    
    "comment l’eau est traitée avant distribution",
    "quel est le processus de traitement de l’eau",
    "comment vous purifiez l’eau potable",
    "expliquez-moi comment l’eau devient potable",
    "quelles sont les étapes de traitement de l’eau",
    "vous traitez l’eau comment avant de la distribuer",
    "c’est quoi le traitement de l’eau à la tde",
    "l’eau est nettoyée comment avant d’arriver chez nous",
    "comment vous rendez l’eau potable",

    "je veux comprendre comment vous traitez l’eau avant de la distribuer",
    "l’eau qu’on boit là vous la traitez comment exactement",
    "expliquez-moi comment vous nettoyez l’eau avant qu’on l’utilise",
    "franchement je veux comprendre comment l’eau devient potable chez vous",

    "coment vous traiter leau",
    "leau est traiter comen",
    "je veu savoir comen leau devien potable",

    "je ne veux pas remettre mon eau, je veux comprendre comment elle est traitée",
    "ce n’est pas pour un réabonnement, je veux juste savoir comment l’eau est traitée",

# compréhension générale
    "c’est quoi la société togolaise des eaux",
    "expliquez-moi ce que fait la tde",
    "je veux comprendre votre rôle",
    "présentez-moi votre structure",
    "vous faites quoi exactement à la tde",
    "c’est quoi votre mission principale",
    "je veux savoir à quoi sert la tde",

    # distribution d’eau (coeur de ton besoin)
    "comment vous faites la distribution de l’eau",
    "expliquez-moi comment l’eau est distribuée dans les quartiers",
    "je veux comprendre votre système de distribution d’eau",
    "comment fonctionne la distribution d’eau potable au togo",
    "vous gérez comment l’approvisionnement en eau",
    "comment l’eau arrive dans nos maisons",
    "je veux des explications sur votre mode de distribution d’eau",
    "comment l’eau est acheminée jusqu’aux habitations",
    "vous faites passer l’eau comment jusqu’aux compteurs",
    "le système de distribution d’eau fonctionne comment chez vous",

    # fonctionnement global
    "comment fonctionne votre service au quotidien",
    "je veux comprendre comment vous travaillez",
    "vous organisez comment la gestion de l’eau",
    "comment vous assurez l’approvisionnement en eau potable",
    "c’est quoi votre mode de fonctionnement",
    "vous gérez quoi exactement dans le pays",

    # formulations naturelles longues
    "bonjour je voudrais comprendre comment la société togolaise des eaux fonctionne et comment vous distribuez l’eau dans les quartiers",
    "bonsoir je suis un peu perdu j’aimerais comprendre comment vous faites arriver l’eau potable dans nos maisons",
    "svp pouvez-vous m’expliquer comment vous gérez la distribution d’eau dans les différentes zones",
    "je veux des informations claires sur la façon dont vous organisez l’approvisionnement en eau au togo",
    "je reviens au pays et j’aimerais comprendre comment fonctionne la tde et comment l’eau est distribuée",
    "franchement je veux juste comprendre votre système de distribution d’eau et votre rôle dans la fourniture d’eau",

    # langage local / réaliste
    "vous faites comment pour envoyer l’eau dans les maisons",
    "l’eau là arrive comment chez nous",
    "c’est comment vous distribuez l’eau dans les quartiers",
    "expliquez-moi comment l’eau circule jusqu’à chez nous",
    "vous gérez l’eau comment dans le pays",
    "l’eau vient comment jusqu’au robinet",

    # fautes / bruit
    "coment vous faite la distribution de leau",
    "je veu comprendre comen leau arrive chez nous",
    "expliker moi votre systeme de distribution",
    "c koi la tde et comen elle marche",
    "coment vous gerer leau potable",

    # cas ambigus (important)
    "je veux comprendre comment vous distribuez l’eau sans forcément contacter quelqu’un",
    "ce n’est pas pour faire un branchement je veux juste comprendre comment vous fonctionnez",
    "je ne veux pas m’abonner je veux comprendre comment vous gérez l’eau",
    "expliquez-moi juste votre fonctionnement pas une demande de service",
    "", ""
],

"info_tarif": [

    # 🔹 basique
    "quels sont les tarifs de l’eau",
    "combien coûte l’eau",
    "je veux connaître les prix de l’eau",
    "les tarifs de consommation d’eau",
    "c’est combien l’eau chez vous",

    # 🔹 variantes naturelles
    "combien coûte l’eau par mois en moyenne",
    "je voudrais savoir le prix de l’eau potable",
    "c’est quoi vos tarifs actuels",
    "comment sont fixés les prix de l’eau",
    "vous facturez l’eau comment exactement",

    # 🔹 synonymes importants
    "je veux comprendre la tarification de l’eau",
    "expliquez moi les coûts liés à l’eau",
    "je veux savoir combien je vais payer pour l’eau",
    "comment fonctionne la facturation de l’eau",
    "je veux des détails sur les frais d’eau",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais comprendre comment sont appliqués les tarifs de l’eau potable et combien cela peut me coûter par mois dans ma maison",
    "svp expliquez moi en détail la tarification de l’eau parce que je ne comprends pas comment les prix sont calculés",
    "je souhaite avoir une idée claire du coût de l’eau pour une consommation normale dans un foyer",
    "franchement je suis un peu perdu j’aimerais comprendre combien coûte réellement l’eau chez vous",
    "je veux savoir comment vous calculez les montants à payer pour l’eau chaque mois",

    # 🔹 avec contexte
    "combien coûte l’eau pour une famille de 5 personnes à lomé",
    "je voudrais savoir les tarifs appliqués chez moi à adidogomé",
    "quel est le prix de l’eau dans mon quartier actuellement",
    "combien je peux payer pour l’eau dans ma maison chaque mois",

    # 🔹 ambiguïtés utiles (IMPORTANT)
    "je ne comprends pas les montants qu’on me demande de payer",
    "pourquoi je paie autant pour l’eau",
    "expliquez moi les frais sur ma consommation d’eau",
    "je veux comprendre pourquoi ma facture est élevée",
    "les frais d’eau sont calculés comment",

    # 🔹 langage local / naturel
    "l’eau là vous vendez ça à combien",
    "on paie l’eau comment chez vous",
    "c’est combien l’eau ici à lomé",
    "vos prix d’eau là c’est comment",
    "expliquez moi les prix là j’ai pas compris",

    # 🔹 fautes humaines
    "combien coute leau",
    "c koi les tarif de leau",
    "je veu savoir le prix de leau",
    "expliker moi la facturation de leau",
    "leau sa coute combien",

    # 🔹 mix complet (très réaliste)
    "bonjour je voudrais savoir combien coûte l’eau dans mon quartier parce que je trouve que les montants sont un peu élevés merci",
    "svp je ne comprends pas comment vous calculez les tarifs de l’eau chez moi pouvez-vous m’expliquer clairement",
    "franchement ça devient compliqué pour moi j’aimerais comprendre les prix de l’eau et comment vous facturez",
    "bonsoir je veux une explication complète sur vos tarifs d’eau et les coûts associés à la consommation",
    "salut je veux juste savoir combien je dois prévoir pour l’eau chaque mois dans un foyer normal",

    # 🔹 variations avec TDE explicite
    "quels sont les tarifs de la tde",
    "combien coûte l’eau à la société togolaise des eaux",
    "la tde facture comment l’eau",
    "expliquez moi les tarifs appliqués par la société togolaise des eaux",

    "", ""
],

"simulation_facture": [

    # 🔹 basique
    "combien je vais payer pour une famille de 5 personnes",
    "estimer ma facture d’eau",
    "simulation de consommation eau",
    "je veux prévoir ma facture",
    "combien je peux payer pour l’eau",

    # 🔹 variantes naturelles
    "je voudrais estimer combien je vais payer pour l’eau chaque mois",
    "pouvez-vous me donner une estimation de ma facture d’eau",
    "je veux savoir à combien peut s’élever ma facture",
    "combien je risque de payer pour ma consommation d’eau",
    "je veux avoir une idée du montant de ma facture",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais avoir une estimation de ma facture d’eau pour un foyer moyen afin de mieux prévoir mes dépenses mensuelles",
    "svp aidez moi à estimer combien je pourrais payer pour l’eau dans ma maison chaque mois",
    "je souhaite prévoir ma consommation d’eau et savoir combien cela peut me coûter environ",
    "franchement je veux anticiper mes dépenses pouvez-vous m’aider à simuler une facture d’eau",
    "je voudrais une estimation réaliste de ce que je vais payer en eau selon ma consommation",

    # 🔹 avec contexte (TRÈS IMPORTANT)
    "combien je vais payer pour une famille de 5 personnes à lomé",
    "estimez ma facture pour une maison à adidogomé",
    "je veux savoir combien je vais payer dans mon foyer chaque mois",
    "pour une consommation normale dans ma maison combien ça fait",
    "je voudrais une estimation pour une famille moyenne chez moi",

    # 🔹 consommation + estimation
    "si j’utilise l’eau normalement combien je vais payer",
    "pour une consommation moyenne combien coûte la facture d’eau",
    "si on est 4 à la maison combien on peut payer",
    "combien coûte l’eau pour une utilisation normale",
    "je veux prévoir ma facture selon ma consommation",

    # 🔹 ambiguïtés utiles
    "combien je vais payer environ",
    "donnez moi une idée du montant à payer",
    "je veux savoir à peu près combien ça va coûter",
    "je veux une estimation des frais d’eau",
    "à peu près ça revient à combien",

    # 🔹 langage local / naturel
    "si on est en famille là on peut payer combien pour l’eau",
    "l’eau là ça peut me coûter combien par mois",
    "je veux savoir environ je vais payer combien",
    "on peut estimer ça à combien chez vous",
    "aidez-moi je veux prévoir combien je vais payer",

    # 🔹 fautes humaines
    "estimé ma facture deau",
    "combien je vai payer pour leau",
    "je veu savoir combien sa va me couté",
    "simulation facture deau svp",
    "combien je peut payer environ",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais savoir combien je vais payer pour l’eau dans ma maison sachant qu’on est environ 5 personnes merci",
    "bonsoir je souhaite anticiper mes dépenses pouvez-vous me donner une estimation de ma facture d’eau mensuelle",
    "franchement je suis un peu perdu je veux savoir combien prévoir pour l’eau chaque mois dans mon foyer",
    "salut je veux juste une idée du montant que je vais payer pour l’eau en fonction d’une consommation normale",
    "je veux comprendre combien ça peut me coûter environ pour l’eau dans une famille moyenne",

    # 🔹 avec TDE explicite
    "la tde peut estimer ma facture d’eau",
    "je veux une simulation de facture à la société togolaise des eaux",
    "est-ce que la tde peut me dire combien je vais payer",
    "donnez moi une estimation de facture chez la société togolaise des eaux",

    "", ""
],

"demande_branchement": [

    # 🔹 basique
    "je veux un branchement d’eau",
    "installer un compteur chez moi",
    "faire une demande de raccordement",
    "avoir l’eau à domicile",
    "je veux être connecté à l’eau",

    # 🔹 variantes naturelles
    "je souhaite faire un branchement d’eau pour ma maison",
    "je veux raccorder ma maison au réseau d’eau",
    "je voudrais installer un compteur d’eau",
    "je veux avoir l’eau potable chez moi",
    "je souhaite faire une demande pour avoir l’eau",

    # 🔹 intention claire (TRÈS IMPORTANT)
    "je veux faire une demande de branchement",
    "je veux entamer les démarches pour un raccordement",
    "je suis prêt à faire la demande de branchement",
    "je veux commencer la procédure pour avoir l’eau",
    "je souhaite déposer une demande de branchement",

    # 🔹 phrases longues réalistes
    "bonjour je souhaite faire une demande de branchement d’eau pour ma nouvelle maison et j’aimerais connaître les démarches à suivre",
    "svp je veux installer un compteur d’eau chez moi pouvez-vous m’aider à faire la demande",
    "je viens de construire une maison et je souhaite maintenant faire un raccordement au réseau d’eau potable",
    "franchement j’ai besoin d’eau chez moi je veux savoir comment faire la demande de branchement",
    "je voudrais entamer une procédure pour avoir l’eau à domicile dans mon foyer",

    # 🔹 avec contexte
    "je veux un branchement d’eau chez moi à adidogomé",
    "je souhaite installer l’eau dans ma maison à lomé",
    "je veux faire un raccordement pour mon terrain",
    "je veux avoir l’eau dans mon quartier",
    "je veux un compteur pour ma maison",

    # 🔹 langage local / naturel
    "je veux mettre l’eau chez moi",
    "je veux que l’eau arrive dans ma maison",
    "je veux brancher l’eau chez moi",
    "je veux connecter ma maison à l’eau",
    "aidez-moi à mettre l’eau chez moi",

    # 🔹 ambiguïtés utiles
    "je veux avoir l’eau chez moi comment faire",
    "je veux commencer les démarches pour avoir l’eau",
    "je veux savoir comment faire pour avoir l’eau à domicile",
    "je veux passer à l’action pour avoir l’eau",
    "je veux faire le nécessaire pour avoir l’eau",

    # 🔹 fautes humaines
    "je veu un branchement deau",
    "instaler un compteur chez moi",
    "faire une demande de racordement",
    "je veu avoir leau a domicile",
    "je veu brancher leau chez moi",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je viens de finir ma maison et je souhaite faire une demande de branchement d’eau pour pouvoir avoir l’eau chez moi merci",
    "bonsoir je voudrais installer un compteur d’eau dans ma maison à lomé pouvez-vous m’aider à lancer la procédure",
    "salut j’ai besoin d’eau chez moi maintenant je veux savoir comment faire une demande de raccordement",
    "franchement ça devient urgent pour moi je veux faire le nécessaire pour avoir l’eau à domicile",
    "svp aidez moi je veux entamer une demande de branchement pour ma maison dans mon quartier",

    # 🔹 avec TDE explicite
    "je veux faire une demande de branchement à la tde",
    "je souhaite un raccordement à la société togolaise des eaux",
    "comment faire une demande de branchement à la tde je veux commencer",
    "je veux installer l’eau via la société togolaise des eaux",

    "", ""
],

"info_branchement": [

    # 🔹 basique
    "comment se passe le branchement",
    "les étapes pour avoir l’eau",
    "procédure de raccordement",
    "détails sur le branchement",
    "comment fonctionne un branchement d’eau",

    # 🔹 variantes naturelles
    "comment faire pour avoir un branchement d’eau",
    "quelles sont les étapes pour raccorder une maison à l’eau",
    "expliquez moi la procédure de branchement",
    "comment ça se passe pour installer un compteur d’eau",
    "je veux comprendre comment on obtient l’eau à domicile",

    # 🔹 formulation info (TRÈS IMPORTANT)
    "quelles sont les démarches pour avoir l’eau",
    "comment se déroule la procédure de branchement",
    "pouvez-vous m’expliquer les étapes du raccordement",
    "je voudrais savoir comment faire un branchement d’eau",
    "expliquez moi comment fonctionne le raccordement à l’eau",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais comprendre les différentes étapes pour faire un branchement d’eau dans une maison",
    "svp pouvez-vous m’expliquer en détail la procédure pour obtenir un branchement d’eau potable",
    "je souhaite avoir des informations complètes sur le processus de raccordement à l’eau",
    "franchement je ne comprends pas comment se passe le branchement d’eau pouvez-vous m’expliquer",
    "je veux connaître toutes les étapes nécessaires pour avoir l’eau chez moi",

    # 🔹 avec contexte
    "comment se passe le branchement d’eau chez moi à adidogomé",
    "quelles sont les étapes pour avoir l’eau dans mon quartier",
    "comment raccorder une maison à lomé au réseau d’eau",
    "je veux comprendre la procédure pour une maison",
    "comment faire pour avoir l’eau dans mon foyer",

    # 🔹 ambiguïtés utiles
    "comment faire pour avoir l’eau chez moi",
    "je veux savoir comment avoir l’eau à domicile",
    "expliquez moi comment obtenir l’eau",
    "je veux comprendre les démarches pour avoir l’eau",
    "comment ça marche pour avoir l’eau",

    # 🔹 langage local / naturel
    "on fait comment pour brancher l’eau chez soi",
    "le branchement d’eau là ça se passe comment",
    "comment on fait pour avoir l’eau à la maison",
    "expliquez moi comment l’eau arrive chez les gens",
    "c’est comment on connecte une maison à l’eau",

    # 🔹 fautes humaines
    "coment se passe le branchement deau",
    "procedure de racordement c'est quoi",
    "je veu comprendre comment avoir leau",
    "expliker moi les etapes de branchement",
    "comment fair pour avoir leau chez moi",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais comprendre comment se passe le branchement d’eau pour une maison afin de mieux me préparer merci",
    "bonsoir je souhaite avoir des informations détaillées sur la procédure de raccordement à l’eau potable",
    "salut je veux juste comprendre les étapes pour avoir l’eau chez moi avant de faire une demande",
    "franchement je suis un peu perdu pouvez-vous m’expliquer comment fonctionne le branchement d’eau",
    "svp aidez moi je veux comprendre toute la procédure pour avoir l’eau à domicile",

    # 🔹 avec TDE explicite
    "comment se passe le branchement à la tde",
    "expliquez moi la procédure de raccordement à la société togolaise des eaux",
    "quelles sont les étapes pour avoir l’eau avec la tde",
    "comment fonctionne le branchement chez la société togolaise des eaux",

    "", ""
],

"suivi_demande_branchement": [

    # 🔹 basique
    "suivre ma demande de branchement",
    "où en est mon dossier",
    "statut de ma demande",
    "ma demande est à quel niveau",
    "je veux suivre mon branchement",

    # 🔹 variantes naturelles
    "je voudrais savoir où en est ma demande de branchement",
    "pouvez-vous me dire l’état d’avancement de mon dossier",
    "je veux connaître le statut de ma demande",
    "où en est le traitement de mon branchement",
    "je veux voir l’évolution de ma demande",

    # 🔹 formulation tracking (TRÈS IMPORTANT)
    "ma demande de branchement est rendue où",
    "mon dossier avance comment",
    "est-ce que ma demande a été validée",
    "je veux savoir si mon branchement est en cours",
    "à quelle étape se trouve ma demande",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais savoir où en est ma demande de branchement que j’ai déposée il y a quelques jours",
    "svp pouvez-vous me donner des informations sur l’état d’avancement de mon dossier de raccordement",
    "je souhaite suivre ma demande de branchement pour savoir si elle est en cours de traitement",
    "franchement ça fait un moment que j’ai fait la demande et je voudrais savoir où ça en est",
    "je veux savoir si ma demande de branchement a été prise en compte et à quel niveau elle se trouve",

    # 🔹 avec contexte
    "où en est ma demande de branchement à adidogomé",
    "je veux suivre mon dossier de raccordement à lomé",
    "ma demande pour ma maison est à quel niveau",
    "je veux savoir l’état de mon branchement dans mon quartier",
    "où en est ma demande faite pour mon terrain",

    # 🔹 ambiguïtés utiles
    "ma demande est passée ou pas",
    "je veux savoir si ça avance",
    "mon dossier est traité ou pas encore",
    "est-ce que vous avez commencé ma demande",
    "je veux savoir si ça évolue",

    # 🔹 langage local / naturel
    "mon dossier là ça a avancé ou bien",
    "ma demande là c’est arrivé où",
    "on a fait quoi avec mon branchement",
    "je veux savoir ça a bougé ou pas",
    "ma demande est bloquée ou ça avance",

    # 🔹 fautes humaines
    "ou en est ma demande de branchement",
    "statut de ma demande de racordement",
    "je veu suivre mon dossier",
    "ma demande est a kel niveau",
    "suivie de ma demande deau",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp j’ai fait une demande de branchement il y a quelques jours et je voudrais savoir où en est mon dossier merci",
    "bonsoir je souhaite suivre l’évolution de ma demande de raccordement pour savoir si elle avance",
    "salut je veux juste savoir à quel niveau se trouve ma demande de branchement actuellement",
    "franchement ça fait longtemps que j’attends je veux savoir si ma demande a évolué ou pas",
    "svp aidez moi je veux savoir si mon dossier de branchement est en cours de traitement",

    # 🔹 avec TDE explicite
    "je veux suivre ma demande de branchement à la tde",
    "où en est mon dossier à la société togolaise des eaux",
    "la tde a traité ma demande ou pas",
    "je veux connaître le statut de ma demande à la société togolaise des eaux",

    "", ""
],

"documents_branchement": [

    # 🔹 basique
    "documents pour branchement",
    "pièces à fournir pour raccordement",
    "dossier à constituer",
    "quels papiers pour abonnement",
    "documents nécessaires pour avoir l’eau",

    # 🔹 variantes naturelles
    "quels sont les documents nécessaires pour un branchement d’eau",
    "liste des pièces à fournir pour le raccordement",
    "quels papiers dois-je fournir pour avoir un compteur",
    "de quels documents ai-je besoin pour faire un branchement",
    "donnez-moi la liste des documents pour un branchement",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "quelles sont les pièces justificatives demandées pour un branchement",
    "quel dossier dois-je préparer pour un raccordement",
    "quels documents sont exigés pour une demande de branchement",
    "liste complète des documents à fournir pour un branchement d’eau",
    "quels sont les justificatifs nécessaires pour avoir l’eau",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais connaître la liste complète des documents à fournir pour faire une demande de branchement d’eau",
    "svp pouvez-vous me dire quels papiers sont nécessaires pour constituer un dossier de raccordement à l’eau",
    "je souhaite préparer mon dossier de branchement et j’aimerais savoir quels documents fournir",
    "franchement je veux éviter les allers-retours dites-moi tous les documents nécessaires pour un branchement",
    "je voudrais avoir les détails sur les pièces justificatives demandées pour un branchement d’eau",

    # 🔹 avec contexte
    "quels documents pour un branchement chez moi à adidogomé",
    "liste des pièces à fournir pour ma maison à lomé",
    "quels papiers pour raccorder mon terrain",
    "documents nécessaires pour mon foyer",
    "quels justificatifs pour un branchement dans mon quartier",

    # 🔹 ambiguïtés utiles
    "qu’est-ce qu’on demande pour un branchement",
    "je dois fournir quoi pour avoir l’eau",
    "il faut quels papiers pour être branché",
    "on demande quoi comme documents",
    "je dois préparer quoi comme dossier",

    # 🔹 langage local / naturel
    "pour brancher l’eau là on demande quels papiers",
    "je dois amener quoi comme documents pour avoir l’eau",
    "c’est quels papiers qu’il faut pour le branchement",
    "on donne quoi pour faire le dossier d’eau",
    "quels papiers il faut déposer pour avoir l’eau",

    # 🔹 fautes humaines
    "document pour branchement deau",
    "piece a fournir pour racordement",
    "kel papier pour abonnement eau",
    "je doi fournir koi pour leau",
    "liste des document pour branchement",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je souhaite faire un branchement d’eau et j’aimerais connaître tous les documents nécessaires pour préparer mon dossier merci",
    "bonsoir je voudrais savoir quelles sont les pièces à fournir pour un raccordement à l’eau dans ma maison",
    "salut je veux préparer mon dossier de branchement pouvez-vous me donner la liste complète des documents",
    "franchement je veux tout préparer à l’avance dites-moi quels papiers sont demandés pour un branchement",
    "svp aidez moi je veux savoir quels documents je dois fournir pour avoir l’eau chez moi",

    # 🔹 avec TDE explicite
    "quels documents pour un branchement à la tde",
    "liste des pièces demandées par la société togolaise des eaux pour un branchement",
    "quels papiers fournir à la tde pour avoir l’eau",
    "documents nécessaires pour un branchement à la société togolaise des eaux",

    "", ""
],

"documents_reabonnement": [

    # 🔹 basique
    "documents pour réabonnement",
    "pièces pour remettre l’eau",
    "dossier de réactivation",
    "conditions de réabonnement",
    "documents nécessaires pour réactiver l’eau",

    # 🔹 variantes naturelles
    "quels documents fournir pour un réabonnement",
    "liste des pièces pour remettre l’eau en service",
    "quels papiers pour réactiver mon compteur",
    "de quels documents ai-je besoin pour reprendre l’eau",
    "documents nécessaires pour rouvrir mon abonnement",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "quelles sont les pièces justificatives pour un réabonnement",
    "quel dossier dois-je constituer pour une remise en service",
    "quels documents sont exigés pour réactiver un abonnement d’eau",
    "liste complète des documents pour un réabonnement",
    "quels justificatifs fournir pour une réactivation de compteur",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais connaître la liste des documents nécessaires pour faire un réabonnement d’eau après une coupure",
    "svp pouvez-vous me dire quels papiers sont demandés pour remettre l’eau en service dans mon logement",
    "je souhaite réactiver mon abonnement et j’aimerais savoir quels documents fournir",
    "franchement mon eau a été coupée et je veux savoir quels documents sont nécessaires pour la remettre",
    "je voudrais préparer mon dossier de réabonnement pouvez-vous me donner la liste complète des pièces",

    # 🔹 avec contexte
    "quels documents pour réactiver l’eau chez moi à adidogomé",
    "liste des pièces pour remettre l’eau dans ma maison à lomé",
    "documents nécessaires pour réactiver mon compteur dans mon quartier",
    "quels papiers pour reprendre l’eau dans mon foyer",
    "documents pour remise en service après coupure chez moi",

    # 🔹 ambiguïtés utiles
    "je dois fournir quoi pour remettre l’eau",
    "quels papiers pour reprendre l’eau",
    "on demande quoi pour réactiver l’eau",
    "je dois préparer quoi pour que l’eau revienne",
    "il faut quels documents pour remettre l’eau",

    # 🔹 langage local / naturel
    "pour remettre l’eau là on demande quels papiers",
    "je dois amener quoi pour que l’eau revienne chez moi",
    "c’est quels documents qu’il faut pour remettre l’eau",
    "on donne quoi pour réactiver l’eau",
    "quels papiers il faut déposer pour que l’eau revienne",

    # 🔹 fautes humaines
    "document pour reabonnement deau",
    "piece pour remetre leau",
    "kel papier pour reactiver compteur",
    "je doi fournir koi pour remetre leau",
    "liste des document pour reabonnement",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp mon eau a été coupée et je souhaite faire un réabonnement pouvez-vous me dire quels documents fournir merci",
    "bonsoir je voudrais remettre l’eau en service dans ma maison et j’aimerais connaître les pièces nécessaires",
    "salut je veux réactiver mon compteur pouvez-vous me donner la liste complète des documents à fournir",
    "franchement ça devient compliqué sans eau je veux savoir quels papiers il faut pour remettre l’eau",
    "svp aidez moi je veux préparer mon dossier pour réabonnement et savoir quels documents sont demandés",

    # 🔹 avec TDE explicite
    "quels documents pour un réabonnement à la tde",
    "liste des pièces demandées par la société togolaise des eaux pour remettre l’eau",
    "quels papiers fournir à la tde pour réactiver mon abonnement",
    "documents nécessaires pour réabonnement à la société togolaise des eaux",

    "", ""
],

"documents_resiliation": [

    # 🔹 basique (corrigé)
    "documents pour résiliation",
    "pièces pour arrêter le contrat",
    "quels papiers pour résilier abonnement",
    "documents nécessaires pour résilier",
    "liste des pièces pour résiliation",

    # 🔹 variantes naturelles
    "quels documents fournir pour résilier mon abonnement d’eau",
    "liste des pièces à fournir pour arrêter mon contrat",
    "quels papiers dois-je donner pour résilier l’eau",
    "de quels documents ai-je besoin pour résilier mon abonnement",
    "documents nécessaires pour mettre fin à mon contrat d’eau",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "quelles sont les pièces justificatives pour une résiliation d’abonnement",
    "quel dossier dois-je constituer pour résilier mon contrat",
    "quels documents sont exigés pour une résiliation d’eau",
    "liste complète des documents pour résiliation",
    "quels justificatifs fournir pour mettre fin à un abonnement",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais connaître la liste complète des documents nécessaires pour résilier mon abonnement d’eau",
    "svp pouvez-vous me dire quels papiers sont demandés pour arrêter mon contrat d’eau",
    "je souhaite résilier mon abonnement et j’aimerais savoir quels documents fournir",
    "franchement je veux arrêter mon abonnement dites-moi les documents nécessaires pour la résiliation",
    "je voudrais préparer mon dossier de résiliation pouvez-vous me donner la liste des pièces",

    # 🔹 avec contexte
    "quels documents pour résilier mon abonnement à adidogomé",
    "liste des pièces pour arrêter mon contrat à lomé",
    "documents nécessaires pour résilier dans mon quartier",
    "quels papiers pour arrêter l’eau dans ma maison",
    "documents pour résiliation de mon abonnement dans mon foyer",

    # 🔹 ambiguïtés utiles
    "je dois fournir quoi pour arrêter l’eau",
    "quels papiers pour arrêter mon abonnement",
    "on demande quoi pour résilier",
    "je dois préparer quoi pour arrêter le contrat",
    "il faut quels documents pour résilier",

    # 🔹 langage local / naturel
    "pour arrêter l’eau là on demande quels papiers",
    "je dois amener quoi pour couper mon abonnement",
    "c’est quels documents qu’il faut pour résilier",
    "on donne quoi pour arrêter l’eau",
    "quels papiers il faut déposer pour stopper l’abonnement",

    # 🔹 fautes humaines
    "document pour resiliation deau",
    "piece pour arreter contrat",
    "kel papier pour resilier abonnement",
    "je doi fournir koi pour resilier",
    "liste des document pour resiliation",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je souhaite résilier mon abonnement d’eau pouvez-vous me dire quels documents fournir merci",
    "bonsoir je voudrais arrêter mon contrat d’eau et j’aimerais connaître les pièces nécessaires",
    "salut je veux résilier mon abonnement pouvez-vous me donner la liste complète des documents à fournir",
    "franchement je ne veux plus de l’abonnement dites-moi quels papiers sont demandés pour résilier",
    "svp aidez moi je veux préparer mon dossier pour résiliation et savoir quels documents sont demandés",

    # 🔹 avec TDE explicite
    "quels documents pour résiliation à la tde",
    "liste des pièces demandées par la société togolaise des eaux pour résilier un abonnement",
    "quels papiers fournir à la tde pour arrêter mon contrat",
    "documents nécessaires pour résiliation à la société togolaise des eaux",

    "", ""
],

"documents_generaux": [

    # 🔹 basique
    "quels documents fournissez-vous",
    "types de documents disponibles",
    "liste des documents administratifs",
    "quels sont vos documents",
    "documents disponibles à la tde",

    # 🔹 variantes naturelles
    "quels types de documents proposez-vous",
    "je veux voir la liste de tous les documents disponibles",
    "quels sont les documents que je peux demander",
    "donnez-moi la liste des documents administratifs",
    "je veux connaître tous les documents disponibles",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "quelle est la liste des documents administratifs disponibles",
    "quels documents officiels sont fournis par la société",
    "catalogue des documents disponibles",
    "liste complète des documents accessibles aux clients",
    "quels sont les documents que vous mettez à disposition",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais connaître l’ensemble des documents administratifs que vous proposez à vos clients",
    "svp pouvez-vous me donner la liste complète des documents disponibles à la société togolaise des eaux",
    "je souhaite savoir quels types de documents je peux obtenir auprès de vos services",
    "franchement je veux avoir une idée de tous les documents que vous fournissez aux clients",
    "je voudrais consulter la liste des documents disponibles avant de faire une demande",

    # 🔹 avec contexte
    "quels documents sont disponibles pour les clients à lomé",
    "liste des documents que je peux demander dans mon quartier",
    "documents accessibles pour mon foyer",
    "quels documents sont disponibles pour les abonnés",
    "liste des documents que je peux obtenir chez moi à adidogomé",

    # 🔹 ambiguïtés utiles
    "vous avez quels documents",
    "on peut demander quels papiers chez vous",
    "qu’est-ce que vous fournissez comme documents",
    "je peux avoir quels types de papiers",
    "donnez-moi les documents que vous avez",

    # 🔹 langage local / naturel
    "vous donnez quels papiers aux clients",
    "on peut prendre quels documents chez vous",
    "c’est quels papiers vous avez là",
    "je veux savoir quels documents vous sortez",
    "vous avez quels papiers disponibles",

    # 🔹 fautes humaines
    "kel document vous fournissez",
    "liste des document administratif",
    "document disponible a la tde",
    "je veu voir les document que vous avez",
    "type de document disponible",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais connaître tous les documents que vous proposez aux clients merci",
    "bonsoir je souhaite avoir la liste des documents administratifs disponibles à la tde",
    "salut je veux savoir quels documents je peux obtenir auprès de vous",
    "franchement avant de faire une demande je veux voir tous les documents disponibles",
    "svp aidez moi je veux connaître l’ensemble des documents que vous mettez à disposition",

    # 🔹 avec TDE explicite
    "quels documents sont disponibles à la tde",
    "liste des documents de la société togolaise des eaux",
    "quels papiers la tde fournit aux clients",
    "documents disponibles à la société togolaise des eaux",

    "", ""
],

"demande_document": [

    # 🔹 basique
    "je veux un document",
    "obtenir une facture",
    "avoir un justificatif",
    "demander un papier officiel",
    "je veux récupérer un document",

    # 🔹 variantes naturelles
    "je voudrais obtenir un document",
    "comment avoir ma facture d’eau",
    "je veux récupérer un justificatif",
    "donnez-moi un document officiel",
    "je veux télécharger un document",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite faire une demande de document administratif",
    "comment obtenir un document officiel auprès de vos services",
    "je voudrais recevoir un justificatif de paiement",
    "procédure pour obtenir un document administratif",
    "demande de délivrance d’un document",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais obtenir un document officiel concernant mon abonnement d’eau",
    "svp pouvez-vous m’aider à récupérer ma facture ou un justificatif lié à mon abonnement",
    "je souhaite faire une demande de document administratif pouvez-vous m’indiquer comment faire",
    "franchement j’ai besoin d’un document officiel lié à mon compteur pouvez-vous m’aider",
    "je voudrais avoir accès à un document concernant mon abonnement d’eau",

    # 🔹 avec contexte
    "je veux obtenir un document pour mon abonnement à adidogomé",
    "comment avoir ma facture d’eau à lomé",
    "je veux un justificatif pour mon compteur dans mon quartier",
    "obtenir un document pour mon foyer",
    "je veux récupérer un papier lié à mon abonnement chez moi",

    # 🔹 ambiguïtés utiles
    "je veux un papier",
    "donnez-moi un document",
    "je peux avoir un justificatif",
    "je veux récupérer ça",
    "comment avoir ce document",

    # 🔹 langage local / naturel
    "je veux prendre un papier chez vous",
    "donnez-moi mon document là",
    "je veux un justificatif de mon eau",
    "je peux avoir mon papier",
    "je veux récupérer mon document chez vous",

    # 🔹 fautes humaines
    "je veu un document",
    "obtenir une factur deau",
    "je veu un justificatif",
    "demander un papier officiel",
    "je veu recuperer mon document",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais obtenir un document officiel lié à mon abonnement merci",
    "bonsoir je veux récupérer ma facture d’eau pouvez-vous m’aider",
    "salut je souhaite avoir un justificatif de mon abonnement d’eau",
    "franchement j’ai besoin d’un document officiel pouvez-vous me dire comment faire",
    "svp aidez moi je veux obtenir un document concernant mon abonnement",

    # 🔹 avec TDE explicite
    "je veux obtenir un document à la tde",
    "comment avoir ma facture auprès de la société togolaise des eaux",
    "je veux un justificatif délivré par la tde",
    "demande de document à la société togolaise des eaux",

    "", ""
],

"info_reabonnement": [

    # 🔹 basique
    "comment se réabonner",
    "remettre l’eau après coupure",
    "procédure de réabonnement",
    "comment réactiver mon abonnement",
    "étapes pour remettre l’eau",

    # 🔹 variantes naturelles
    "comment faire pour remettre mon eau en service",
    "comment reprendre mon abonnement d’eau",
    "je veux savoir comment réactiver mon compteur",
    "comment rouvrir mon abonnement d’eau",
    "quelle est la procédure pour remettre l’eau",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "quelle est la procédure de réabonnement après coupure",
    "quelles sont les étapes pour une remise en service de l’eau",
    "comment procéder pour réactiver un abonnement d’eau",
    "processus de réactivation d’un compteur d’eau",
    "démarches à suivre pour un réabonnement",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais savoir comment faire pour remettre l’eau en service après une coupure",
    "svp pouvez-vous m’expliquer les étapes pour réactiver mon abonnement d’eau",
    "je souhaite reprendre mon abonnement et j’aimerais connaître la procédure à suivre",
    "franchement mon eau a été coupée et je veux savoir comment faire pour la remettre",
    "je voudrais comprendre le processus complet pour réactiver mon compteur d’eau",

    # 🔹 avec contexte
    "comment remettre l’eau chez moi à adidogomé après coupure",
    "procédure pour réactiver mon abonnement à lomé",
    "comment reprendre l’eau dans mon quartier",
    "étapes pour remettre l’eau dans mon foyer",
    "comment réactiver mon compteur chez moi",

    # 🔹 ambiguïtés utiles
    "je fais comment pour remettre l’eau",
    "comment faire pour reprendre l’eau",
    "on fait comment pour réactiver",
    "je dois faire quoi pour remettre l’eau",
    "comment ça se passe pour reprendre l’eau",

    # 🔹 langage local / naturel
    "je fais comment pour que l’eau revienne chez moi",
    "on fait comment pour remettre l’eau là",
    "je dois faire quoi pour que l’eau revienne",
    "comment on fait pour réactiver l’eau",
    "c’est comment pour remettre l’eau",

    # 🔹 fautes humaines
    "comment reabonner deau",
    "procedure pour remetre leau",
    "je fai comment pour reactiver",
    "comment remettre leau apres coupur",
    "etape pour reabonnement",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp mon eau a été coupée et je voudrais savoir comment faire pour la remettre merci",
    "bonsoir je souhaite réactiver mon abonnement pouvez-vous m’expliquer la procédure",
    "salut je veux reprendre mon abonnement d’eau dites-moi les étapes à suivre",
    "franchement ça devient compliqué sans eau je veux savoir comment faire pour la remettre",
    "svp aidez moi je veux comprendre comment réactiver mon compteur d’eau",

    # 🔹 avec TDE explicite
    "comment se réabonner à la tde",
    "procédure de réabonnement à la société togolaise des eaux",
    "comment remettre l’eau avec la tde",
    "étapes pour réactiver mon abonnement à la société togolaise des eaux",

    "", ""
],

"resiliation": [

    # 🔹 basique
    "je veux résilier mon abonnement",
    "arrêter mon contrat d’eau",
    "fermer mon compteur",
    "je veux arrêter mon abonnement",
    "résilier mon contrat d’eau",

    # 🔹 variantes naturelles
    "je souhaite mettre fin à mon abonnement d’eau",
    "je veux couper mon abonnement",
    "je ne veux plus de mon abonnement d’eau",
    "je veux arrêter définitivement l’eau",
    "je veux fermer mon abonnement",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite procéder à la résiliation de mon abonnement d’eau",
    "je demande la résiliation de mon contrat",
    "je souhaite mettre fin à mon contrat d’eau",
    "demande de résiliation d’abonnement",
    "procéder à la fermeture de mon compteur d’eau",

    # 🔹 phrases longues réalistes
    "bonjour je souhaite résilier mon abonnement d’eau car je ne suis plus sur place",
    "svp je voudrais arrêter mon contrat d’eau pouvez-vous m’aider",
    "je souhaite mettre fin à mon abonnement car je déménage",
    "franchement je ne veux plus continuer avec cet abonnement d’eau",
    "je voudrais fermer mon compteur d’eau définitivement",

    # 🔹 avec contexte
    "je veux résilier mon abonnement à adidogomé",
    "arrêter mon contrat d’eau à lomé",
    "fermer mon compteur dans mon quartier",
    "résilier mon abonnement pour ma maison",
    "je veux arrêter l’eau dans mon foyer",

    # 🔹 ambiguïtés utiles
    "je veux arrêter l’eau",
    "je ne veux plus d’eau",
    "coupez mon abonnement",
    "je veux stopper mon abonnement",
    "je veux qu’on arrête mon eau",

    # 🔹 langage local / naturel
    "je veux couper l’eau chez moi",
    "arrêtez mon abonnement là",
    "je ne veux plus de l’eau là chez moi",
    "fermez mon compteur pour moi",
    "je veux qu’on coupe mon eau",

    # 🔹 fautes humaines
    "je veu resilier mon abonnement",
    "arreter mon contrat deau",
    "je veu couper mon abonnement",
    "resiliation compteur eau",
    "je ne veu plus de leau",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je souhaite résilier mon abonnement d’eau merci",
    "bonsoir je veux arrêter mon contrat d’eau pouvez-vous m’aider",
    "salut je ne veux plus de mon abonnement d’eau merci de le résilier",
    "franchement je veux arrêter mon abonnement ça ne m’intéresse plus",
    "svp aidez moi je veux mettre fin à mon contrat d’eau",

    # 🔹 avec TDE explicite
    "je veux résilier mon abonnement à la tde",
    "demande de résiliation à la société togolaise des eaux",
    "je souhaite arrêter mon contrat avec la tde",
    "fermer mon compteur à la société togolaise des eaux",

    "", ""
],
"modification_abonnement": [

    # 🔹 basique
    "modifier mon abonnement",
    "changer nom compteur",
    "mettre compteur à mon nom",
    "modifier les informations de mon abonnement",
    "changer le titulaire du compteur",

    # 🔹 variantes naturelles
    "je veux changer le nom sur le compteur",
    "mettre l’abonnement à mon nom",
    "je veux transférer le compteur à mon nom",
    "modifier les informations liées à mon abonnement",
    "je veux mettre à jour mon abonnement",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite procéder à une modification de mon abonnement",
    "demande de changement de titulaire du compteur",
    "je souhaite mettre à jour les informations de mon contrat",
    "procédure de modification d’abonnement",
    "changement de nom sur un abonnement d’eau",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais modifier mon abonnement d’eau et mettre le compteur à mon nom",
    "svp pouvez-vous m’aider à changer le nom du titulaire du compteur",
    "je souhaite transférer l’abonnement à mon nom car j’ai repris la maison",
    "franchement je veux mettre à jour les informations liées à mon abonnement d’eau",
    "je voudrais changer le nom sur le compteur suite à un changement de situation",

    # 🔹 avec contexte
    "mettre le compteur à mon nom à adidogomé",
    "changer le titulaire du compteur à lomé",
    "modifier mon abonnement dans mon quartier",
    "mettre à jour mon abonnement pour ma maison",
    "changer les informations de mon compteur dans mon foyer",

    # 🔹 ambiguïtés utiles
    "je veux changer mon abonnement",
    "modifier les infos du compteur",
    "changer les informations",
    "mettre ça à mon nom",
    "je veux faire une modification",

    # 🔹 langage local / naturel
    "je veux mettre le compteur à mon nom là",
    "changez le nom sur le compteur pour moi",
    "je veux que le compteur soit à mon nom",
    "on peut changer le nom du compteur",
    "je veux modifier les infos de mon abonnement",

    # 🔹 fautes humaines
    "modifier mon abonement",
    "changer nom compteur eau",
    "mettre compteur a mon nom",
    "je veu modifier mon abonnement",
    "changer titulaire compteur",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je souhaite modifier mon abonnement et mettre le compteur à mon nom merci",
    "bonsoir je veux changer le titulaire du compteur pouvez-vous m’aider",
    "salut je veux transférer l’abonnement à mon nom car j’occupe maintenant la maison",
    "franchement je dois mettre à jour mon abonnement d’eau pouvez-vous m’aider",
    "svp aidez moi je veux changer les informations de mon compteur",

    # 🔹 avec TDE explicite
    "modifier mon abonnement à la tde",
    "changement de titulaire du compteur à la société togolaise des eaux",
    "mettre le compteur à mon nom à la tde",
    "modifier les informations de mon abonnement à la société togolaise des eaux",

    "", ""
],

"reclamation_facture": [

    # 🔹 basique
    "ma facture est trop élevée",
    "je ne comprends pas ma facture",
    "erreur de facturation",
    "montant de facture incorrect",
    "facture anormale",

    # 🔹 variantes naturelles
    "ma facture est trop chère",
    "je trouve ma facture d’eau trop élevée",
    "il y a une erreur sur ma facture",
    "je ne comprends pas le montant qu’on m’a facturé",
    "ma facture ne correspond pas à ma consommation",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite contester ma facture d’eau",
    "réclamation concernant une erreur de facturation",
    "le montant de ma facture semble incorrect",
    "je souhaite signaler une anomalie sur ma facture",
    "demande de vérification de ma facture d’eau",

    # 🔹 phrases longues réalistes
    "bonjour ma facture d’eau est vraiment trop élevée ce mois-ci et je ne comprends pas pourquoi",
    "svp je pense qu’il y a une erreur dans ma facture pouvez-vous vérifier",
    "je souhaite contester le montant de ma facture qui me semble anormalement élevé",
    "franchement je ne comprends pas ma facture d’eau elle est trop chère pour moi",
    "je voudrais savoir pourquoi ma facture est aussi élevée alors que je consomme peu",

    # 🔹 avec contexte
    "ma facture est trop élevée à adidogomé",
    "je ne comprends pas ma facture à lomé",
    "erreur sur ma facture dans mon quartier",
    "problème de facturation dans mon foyer",
    "facture anormale chez moi",

    # 🔹 ambiguïtés utiles
    "il y a un problème avec ma facture",
    "ma facture n’est pas normale",
    "ça ne correspond pas",
    "il y a une erreur quelque part",
    "je ne suis pas d’accord avec ma facture",

    # 🔹 langage local / naturel
    "ma facture est trop chère là",
    "je ne comprends pas cette facture là",
    "vous avez exagéré sur ma facture",
    "c’est trop élevé pour moi",
    "il y a un problème sur ma facture là",

    # 🔹 fautes humaines
    "ma factur est trop eleve",
    "je compren pa ma facture",
    "erreur de facturation eau",
    "facture tro cher",
    "montant facture pa normal",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp ma facture d’eau est trop élevée pouvez-vous vérifier merci",
    "bonsoir je ne comprends pas le montant de ma facture pouvez-vous m’expliquer",
    "salut je pense qu’il y a une erreur sur ma facture d’eau",
    "franchement ma facture est trop chère je veux comprendre pourquoi",
    "svp aidez moi ma facture ne correspond pas à ma consommation",

    # 🔹 avec TDE explicite
    "ma facture à la tde est trop élevée",
    "erreur de facturation à la société togolaise des eaux",
    "je ne comprends pas ma facture de la tde",
    "problème sur ma facture avec la société togolaise des eaux",

    "", ""
],

"signaler_coupure": [

    # 🔹 basique
    "il n’y a pas d’eau",
    "coupure d’eau dans ma zone",
    "plus d’eau depuis ce matin",
    "l’eau ne coule plus",
    "absence totale d’eau",

    # 🔹 variantes naturelles
    "je n’ai plus d’eau chez moi",
    "l’eau est complètement coupée",
    "il n’y a plus d’eau dans mon quartier",
    "on n’a pas d’eau depuis plusieurs heures",
    "l’eau ne sort plus du robinet",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite signaler une coupure d’eau",
    "absence d’eau dans ma zone",
    "incident de coupure d’eau",
    "signalement d’une interruption d’alimentation en eau",
    "problème d’approvisionnement en eau",

    # 🔹 phrases longues réalistes
    "bonjour je n’ai plus d’eau chez moi depuis ce matin pouvez-vous vérifier",
    "svp il y a une coupure d’eau dans mon quartier et ça dure depuis plusieurs heures",
    "je souhaite signaler une absence totale d’eau dans ma zone",
    "franchement on n’a plus d’eau depuis hier et ça devient compliqué",
    "je voudrais savoir pourquoi l’eau ne coule plus chez moi",

    # 🔹 avec contexte
    "plus d’eau à adidogomé",
    "coupure d’eau à lomé",
    "absence d’eau dans mon quartier",
    "pas d’eau dans mon foyer",
    "l’eau ne sort plus chez moi",

    # 🔹 ambiguïtés utiles
    "l’eau ne vient pas",
    "il n’y a rien qui sort",
    "ça ne coule pas",
    "plus rien au robinet",
    "l’eau est partie",

    # 🔹 langage local / naturel
    "y a pas d’eau chez moi là",
    "l’eau ne sort pas du tout",
    "on est sans eau ici",
    "l’eau est coupée chez nous",
    "ça ne coule plus du tout",

    # 🔹 fautes humaines
    "ya pa deau",
    "plu deau depuis matin",
    "leau ne coule plu",
    "coupur deau chez moi",
    "pa deau robinet",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp il n’y a pas d’eau chez moi depuis ce matin pouvez-vous vérifier merci",
    "bonsoir on n’a plus d’eau dans notre quartier depuis plusieurs heures",
    "salut l’eau est coupée chez moi pouvez-vous m’aider",
    "franchement ça fait deux jours qu’on n’a pas d’eau ça devient compliqué",
    "svp aidez moi l’eau ne coule plus du tout chez moi",

    # 🔹 avec TDE explicite
    "coupure d’eau à la tde",
    "absence d’eau signalée à la société togolaise des eaux",
    "je n’ai plus d’eau avec la tde",
    "problème de coupure d’eau avec la société togolaise des eaux",

    "", ""
],

"signaler_basse_pression": [

    # 🔹 basique
    "faible pression d’eau",
    "l’eau coule lentement",
    "pression insuffisante",
    "débit d’eau très faible",
    "l’eau sort faiblement",

    # 🔹 variantes naturelles
    "l’eau coule très doucement",
    "le débit d’eau est faible chez moi",
    "il y a de l’eau mais la pression est très faible",
    "l’eau met du temps à sortir",
    "le robinet coule à peine",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite signaler une faible pression d’eau",
    "problème de pression d’eau insuffisante",
    "débit d’eau anormalement faible",
    "signalement de pression d’eau insuffisante",
    "problème de distribution avec faible pression",

    # 🔹 phrases longues réalistes
    "bonjour l’eau coule très lentement chez moi pouvez-vous vérifier la pression",
    "svp il y a de l’eau mais la pression est vraiment trop faible pour une utilisation normale",
    "je souhaite signaler un problème de pression d’eau insuffisante dans ma zone",
    "franchement l’eau sort à peine du robinet et ça devient compliqué",
    "je voudrais savoir pourquoi la pression d’eau est aussi faible chez moi",

    # 🔹 avec contexte
    "faible pression d’eau à adidogomé",
    "l’eau coule lentement à lomé",
    "pression faible dans mon quartier",
    "débit faible dans mon foyer",
    "l’eau sort faiblement chez moi",

    # 🔹 ambiguïtés utiles
    "l’eau ne sort pas bien",
    "ça coule mal",
    "le débit n’est pas normal",
    "l’eau est faible",
    "ça ne coule pas correctement",

    # 🔹 langage local / naturel
    "l’eau sort petit petit",
    "ça coule doucement chez moi",
    "l’eau ne vient pas bien",
    "le robinet donne petit débit",
    "l’eau est faible là",

    # 🔹 fautes humaines
    "faible pression deau",
    "leau coule lenteman",
    "pression insuffisante eau",
    "debit eau faible",
    "leau sort faiblement",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp l’eau coule très lentement chez moi pouvez-vous vérifier merci",
    "bonsoir il y a de l’eau mais la pression est trop faible dans mon quartier",
    "salut l’eau sort à peine du robinet pouvez-vous m’aider",
    "franchement la pression d’eau est trop faible ça devient difficile",
    "svp aidez moi le débit d’eau est vraiment insuffisant chez moi",

    # 🔹 avec TDE explicite
    "faible pression d’eau à la tde",
    "problème de pression avec la société togolaise des eaux",
    "l’eau coule lentement avec la tde",
    "signalement de faible pression à la société togolaise des eaux",

    "", ""
],

 "demande_abonnement": [
    # basiques
    "je veux faire un abonnement",
    "ouvrir un abonnement d’eau",
    "je veux m’abonner à la tde",
    "mettre un abonnement à mon nom",
    "souscrire un contrat d’eau",
    "je veux créer un abonnement chez vous",
    "comment faire pour m’abonner à l’eau",
    "je souhaite prendre un abonnement d’eau",
    "ouvrir un contrat d’eau potable",

    # langage naturel + contexte
    "je viens d’emménager et je veux ouvrir un abonnement d’eau à mon nom",
    "je suis nouveau dans la maison et je voudrais m’abonner à l’eau",
    "je viens de louer une maison et je veux mettre l’abonnement à mon nom",
    "je veux avoir un contrat d’eau pour ma maison",
    "je veux m’inscrire pour utiliser l’eau chez moi",
    "je veux activer un abonnement d’eau dans mon logement",
    "je viens d’arriver et je veux créer mon abonnement d’eau",

    # formulations indirectes
    "quelles sont les démarches pour avoir un abonnement d’eau",
    "comment on fait pour souscrire à un contrat d’eau",
    "c’est quoi la procédure pour ouvrir un abonnement à la tde",
    "expliquez-moi comment m’abonner à l’eau potable",
    "je veux savoir comment obtenir un abonnement d’eau",
    "vous pouvez m’aider à créer un abonnement d’eau",

    # langage local / réaliste
    "je veux prendre l’eau à mon nom chez vous",
    "je veux mettre l’eau sur mon nom là",
    "je veux que le compteur soit à mon nom maintenant",
    "je veux commencer à payer l’eau à mon nom",
    "je veux gérer mon eau moi-même maintenant",
    "je veux être responsable de l’eau chez moi",

    # fautes / bruit
    "je veu mabonner a leau",
    "ouvrire un abonement deau",
    "je ve souscrir un contra deau",
    "je veu metre labonement a mon nom",
    "coment faire un abonement tde",

    # phrases longues réalistes
    "bonjour je viens d’emménager dans une maison à lomé et je voudrais savoir comment faire pour ouvrir un abonnement d’eau à mon nom svp",
    "bonsoir je suis nouveau dans cette zone et je veux m’abonner à l’eau potable pour ma maison pouvez-vous m’expliquer la procédure",
    "svp aidez-moi je viens de louer une maison et je souhaite souscrire un abonnement d’eau mais je ne sais pas comment faire",
    "franchement je suis un peu perdu je veux avoir un abonnement d’eau chez moi et commencer à payer normalement pouvez-vous m’aider",
    "je reviens au pays et je veux mettre l’eau à mon nom dans la maison familiale pouvez-vous me dire comment faire",

    # cas ambigus (important pour robustesse)
    "je veux avoir l’eau chez moi et mettre ça à mon nom",
    "je veux installer l’eau et aussi m’abonner",
    "comment faire pour avoir l’eau et un abonnement en même temps",
    "je veux l’eau chez moi avec un abonnement à mon nom",
],

"signaler_fuite": [

    # 🔹 basique
    "il y a une fuite d’eau",
    "canalisation cassée",
    "eau qui fuit dans la rue",
    "fuite d’eau chez moi",
    "tuyau percé",

    # 🔹 variantes naturelles
    "il y a de l’eau qui s’échappe",
    "une fuite est en train de couler",
    "l’eau coule partout à cause d’une fuite",
    "le tuyau est cassé et l’eau sort",
    "il y a une grosse fuite d’eau",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite signaler une fuite d’eau",
    "signalement d’une canalisation endommagée",
    "fuite d’eau constatée dans ma zone",
    "incident de fuite sur le réseau d’eau",
    "problème de canalisation avec fuite d’eau",

    # 🔹 phrases longues réalistes
    "bonjour il y a une fuite d’eau importante devant chez moi pouvez-vous intervenir",
    "svp une canalisation semble cassée et l’eau coule en continu dans la rue",
    "je souhaite signaler une fuite d’eau dans mon quartier depuis ce matin",
    "franchement il y a beaucoup d’eau qui se perd à cause d’une fuite près de chez moi",
    "je voudrais signaler une fuite d’eau qui dure depuis plusieurs heures",

    # 🔹 avec contexte
    "fuite d’eau à adidogomé",
    "canalisation cassée à lomé",
    "eau qui fuit dans mon quartier",
    "fuite dans ma rue",
    "tuyau cassé près de chez moi",

    # 🔹 ambiguïtés utiles
    "il y a de l’eau partout",
    "ça coule dans la rue",
    "on perd beaucoup d’eau",
    "ça fuit quelque part",
    "l’eau sort du sol",

    # 🔹 langage local / naturel
    "l’eau coule partout là",
    "il y a une fuite chez nous",
    "ça fuit fort dans la rue",
    "l’eau sort du sol là-bas",
    "tuyau gâté l’eau coule",

    # 🔹 fautes humaines
    "fuit deau",
    "canalisation casse eau",
    "leau fuit partout",
    "fuite eau rue",
    "tuyau percer eau",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp il y a une fuite d’eau dans ma rue pouvez-vous intervenir merci",
    "bonsoir une canalisation est cassée et l’eau coule beaucoup dans mon quartier",
    "salut il y a de l’eau qui fuit devant chez moi pouvez-vous vérifier",
    "franchement ça fuit beaucoup et l’eau se perd inutilement",
    "svp aidez moi il y a une grosse fuite d’eau près de chez moi",

    # 🔹 avec TDE explicite
    "fuite d’eau signalée à la tde",
    "canalisation cassée à la société togolaise des eaux",
    "problème de fuite avec la tde",
    "signalement de fuite à la société togolaise des eaux",

    "", ""
],

"signaler_eau_sale": [

    # 🔹 basique
    "l’eau est sale",
    "eau trouble",
    "eau de mauvaise qualité",
    "eau sale qui sort du robinet",
    "eau non potable",

    # 🔹 variantes naturelles
    "l’eau est sale chez moi",
    "l’eau est trouble et pas claire",
    "l’eau a une mauvaise qualité",
    "l’eau est bizarre",
    "l’eau n’est pas propre",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite signaler une mauvaise qualité de l’eau",
    "signalement d’une eau impropre à la consommation",
    "problème de qualité de l’eau distribuée",
    "eau trouble signalée dans ma zone",
    "incident lié à la qualité de l’eau",

    # 🔹 phrases longues réalistes
    "bonjour l’eau qui sort de mon robinet est sale pouvez-vous vérifier",
    "svp l’eau est trouble chez moi et je ne peux pas l’utiliser",
    "je souhaite signaler un problème de qualité de l’eau dans mon quartier",
    "franchement l’eau est sale et ça m’inquiète pour la santé",
    "je voudrais savoir pourquoi l’eau est de mauvaise qualité chez moi",

    # 🔹 avec contexte
    "eau sale à adidogomé",
    "eau trouble à lomé",
    "mauvaise qualité d’eau dans mon quartier",
    "eau sale dans mon foyer",
    "l’eau n’est pas propre chez moi",

    # 🔹 ambiguïtés utiles
    "l’eau est bizarre",
    "l’eau a une couleur étrange",
    "l’eau n’est pas claire",
    "il y a un problème avec l’eau",
    "l’eau ne donne pas confiance",

    # 🔹 langage local / naturel
    "l’eau est sale là",
    "l’eau n’est pas claire du tout",
    "ça sort sale au robinet",
    "l’eau est vraiment mauvaise",
    "on ne peut pas boire cette eau",

    # 🔹 fautes humaines
    "eau sale robinet",
    "leau est trouble",
    "eau movaise qualite",
    "leau pa propre",
    "eau sale chez moi",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp l’eau est sale chez moi pouvez-vous vérifier merci",
    "bonsoir l’eau est trouble dans mon quartier et ça m’inquiète",
    "salut l’eau qui sort du robinet n’est pas propre pouvez-vous m’aider",
    "franchement l’eau est de mauvaise qualité et on ne peut pas la boire",
    "svp aidez moi l’eau est vraiment sale chez moi",

    # 🔹 avec TDE explicite
    "eau sale à la tde",
    "problème de qualité d’eau avec la société togolaise des eaux",
    "eau trouble signalée à la tde",
    "mauvaise qualité d’eau à la société togolaise des eaux",

    "", ""
],

"zone_couverture": [

    # 🔹 basique
    "zones desservies par la tde",
    "est-ce que ma zone est couverte",
    "quartiers alimentés en eau",
    "zones couvertes par la tde",
    "où la tde fournit de l’eau",

    # 🔹 variantes naturelles
    "est-ce que vous fournissez de l’eau dans ma zone",
    "mon quartier est-il desservi en eau",
    "y a-t-il de l’eau dans ma zone",
    "est-ce que la tde couvre mon quartier",
    "je veux savoir si ma zone est alimentée en eau",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite connaître les zones de couverture de la tde",
    "vérification de la couverture en eau dans ma zone",
    "zones desservies par la société togolaise des eaux",
    "information sur la couverture géographique du réseau d’eau",
    "ma localité est-elle incluse dans la zone de distribution",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais savoir si mon quartier est couvert par la tde",
    "svp est-ce que vous fournissez de l’eau dans ma zone à lomé",
    "je souhaite vérifier si ma zone est desservie par le réseau d’eau",
    "franchement je veux savoir si on peut avoir de l’eau dans mon quartier",
    "je voudrais savoir si la tde couvre ma zone d’habitation",

    # 🔹 avec contexte
    "zone couverte à adidogomé",
    "quartiers desservis à lomé",
    "ma zone est-elle couverte",
    "couverture dans mon quartier",
    "eau disponible dans ma zone",

    # 🔹 ambiguïtés utiles
    "est-ce qu’il y a de l’eau dans ma zone",
    "ma zone a de l’eau",
    "vous êtes présents dans mon quartier",
    "est-ce que vous êtes dans ma zone",
    "je peux avoir l’eau ici",

    # 🔹 langage local / naturel
    "vous donnez l’eau dans mon quartier",
    "y a l’eau chez nous avec la tde",
    "ma zone a l’eau ou pas",
    "vous êtes dans mon coin",
    "on peut avoir l’eau ici",

    # 🔹 fautes humaines
    "zone couverture tde",
    "ma zone est couvert eau",
    "quartier desservi eau",
    "tde couvre ma zone",
    "eau disponible zone",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais savoir si ma zone est couverte par la tde merci",
    "bonsoir est-ce que vous fournissez de l’eau dans mon quartier",
    "salut je veux vérifier si ma zone est desservie par votre réseau",
    "franchement je veux savoir si on peut avoir de l’eau dans mon quartier",
    "svp aidez moi à savoir si ma zone est couverte",

    # 🔹 avec TDE explicite
    "zones desservies par la société togolaise des eaux",
    "couverture de la tde dans ma zone",
    "ma zone est-elle couverte par la société togolaise des eaux",
    "présence de la tde dans mon quartier",

    "", ""
],

"eligibilite_branchement": [

    # 🔹 basique
    "est-ce que je peux avoir l’eau chez moi",
    "ma zone est-elle éligible",
    "peut-on installer un compteur ici",
    "est-ce possible d’avoir un branchement",
    "puis-je avoir l’eau à mon domicile",

    # 🔹 variantes naturelles
    "est-ce que ma maison peut être raccordée à l’eau",
    "je peux avoir un compteur chez moi",
    "mon terrain est-il éligible à un branchement",
    "est-ce qu’on peut installer l’eau ici",
    "je veux savoir si je peux avoir l’eau chez moi",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite vérifier l’éligibilité de mon habitation au branchement d’eau",
    "demande de vérification de faisabilité de raccordement",
    "mon logement est-il éligible au réseau d’eau",
    "vérification de l’éligibilité au branchement d’eau potable",
    "possibilité de raccordement au réseau de la société togolaise des eaux",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais savoir si je peux avoir un branchement d’eau chez moi",
    "svp est-ce que ma maison est éligible à un raccordement à l’eau",
    "je souhaite vérifier si je peux installer un compteur dans mon habitation",
    "franchement je veux savoir si je peux avoir l’eau chez moi avant de faire une demande",
    "je voudrais savoir si mon terrain peut être raccordé au réseau d’eau",

    # 🔹 avec contexte
    "éligibilité branchement à adidogomé",
    "je peux avoir l’eau chez moi à lomé",
    "ma maison est-elle éligible dans mon quartier",
    "possibilité de branchement dans mon foyer",
    "je peux installer un compteur ici",

    # 🔹 ambiguïtés utiles
    "je peux avoir l’eau ici",
    "c’est possible d’avoir l’eau",
    "on peut mettre l’eau chez moi",
    "je peux installer l’eau",
    "est-ce que ça marche ici",

    # 🔹 langage local / naturel
    "je peux avoir l’eau chez moi là",
    "on peut mettre compteur ici",
    "je peux avoir l’eau dans ma maison",
    "c’est possible d’avoir l’eau ici",
    "vous pouvez amener l’eau chez moi",

    # 🔹 fautes humaines
    "je peu avoir leau chez moi",
    "eligibilite branchement eau",
    "installer compteur chez moi possible",
    "je veu savoir si jai leau",
    "branchement possible ici",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais savoir si je peux avoir l’eau chez moi merci",
    "bonsoir est-ce que ma maison est éligible à un branchement d’eau",
    "salut je veux vérifier si je peux installer un compteur chez moi",
    "franchement je veux savoir si je peux avoir l’eau ici avant de faire une demande",
    "svp aidez moi à savoir si mon habitation est éligible",

    # 🔹 avec TDE explicite
    "éligibilité au branchement avec la tde",
    "je peux avoir l’eau chez moi avec la société togolaise des eaux",
    "mon habitation est-elle éligible à la tde",
    "possibilité de raccordement à la société togolaise des eaux",

    "", ""
],

"conseil_consommation": [

    # 🔹 basique
    "comment réduire ma consommation d’eau",
    "astuces pour économiser l’eau",
    "optimiser utilisation eau",
    "comment consommer moins d’eau",
    "réduire ma facture d’eau",

    # 🔹 variantes naturelles
    "comment faire pour utiliser moins d’eau",
    "des conseils pour économiser l’eau",
    "je veux réduire ma consommation d’eau",
    "comment mieux gérer ma consommation d’eau",
    "comment éviter de gaspiller l’eau",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite obtenir des conseils pour optimiser ma consommation d’eau",
    "recommandations pour réduire l’utilisation d’eau",
    "bonnes pratiques pour une consommation d’eau responsable",
    "stratégies d’économie d’eau au niveau domestique",
    "conseils pour une gestion efficace de l’eau",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais savoir comment réduire ma consommation d’eau chez moi",
    "svp pouvez-vous me donner des astuces pour économiser l’eau dans mon foyer",
    "je souhaite des conseils pour mieux gérer ma consommation d’eau",
    "franchement ma facture est élevée je veux savoir comment consommer moins d’eau",
    "je voudrais apprendre à utiliser l’eau de manière plus efficace",

    # 🔹 avec contexte
    "réduire consommation eau à adidogomé",
    "économiser l’eau à lomé",
    "consommer moins d’eau dans mon foyer",
    "optimiser l’eau pour une famille de 5 personnes",
    "gestion eau dans mon quartier",

    # 🔹 ambiguïtés utiles
    "comment faire pour l’eau",
    "je peux faire quoi pour l’eau",
    "comment améliorer ma consommation",
    "comment gérer l’eau",
    "je veux utiliser moins",

    # 🔹 langage local / naturel
    "comment faire pour ne pas trop utiliser l’eau",
    "je veux économiser l’eau chez moi",
    "comment on peut réduire l’eau",
    "donnez moi des astuces pour l’eau",
    "comment éviter gaspillage eau",

    # 🔹 fautes humaines
    "reduire consomation eau",
    "astuce economiser eau",
    "optimiser utilisation deau",
    "consomer moin eau",
    "gerer eau maison",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais des conseils pour réduire ma consommation d’eau merci",
    "bonsoir pouvez-vous m’aider à économiser l’eau dans mon foyer",
    "salut je veux savoir comment utiliser moins d’eau chez moi",
    "franchement je cherche des astuces pour réduire ma consommation d’eau",
    "svp aidez moi à mieux gérer mon utilisation d’eau",

    # 🔹 avec TDE explicite
    "conseils de la tde pour économiser l’eau",
    "comment réduire consommation avec la société togolaise des eaux",
    "astuces eau proposées par la tde",
    "gestion consommation eau tde",

    "", ""
],

"info_consommation_moyenne": [

    # 🔹 basique
    "consommation moyenne d’une famille",
    "quantité d’eau utilisée par mois",
    "moyenne consommation eau",
    "combien d’eau consomme une famille",
    "consommation moyenne eau par mois",

    # 🔹 variantes naturelles
    "une famille consomme combien d’eau en moyenne",
    "c’est quoi la consommation normale d’eau",
    "combien d’eau on utilise en général",
    "consommation moyenne d’eau par personne",
    "combien d’eau une maison utilise par mois",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite connaître la consommation moyenne d’eau par foyer",
    "information sur la consommation d’eau mensuelle moyenne",
    "statistiques de consommation d’eau domestique",
    "consommation moyenne d’eau par habitant",
    "données sur l’utilisation moyenne de l’eau",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais savoir combien d’eau une famille consomme en moyenne par mois",
    "svp quelle est la consommation moyenne d’eau pour un foyer normal",
    "je souhaite connaître la quantité d’eau utilisée par une famille de 5 personnes",
    "franchement je veux savoir si ma consommation est normale",
    "je voudrais comparer ma consommation avec la moyenne",

    # 🔹 avec contexte
    "consommation moyenne à lomé",
    "moyenne eau à adidogomé",
    "consommation d’eau dans mon quartier",
    "quantité d’eau pour une famille de 5 personnes",
    "consommation dans mon foyer",

    # 🔹 ambiguïtés utiles
    "on consomme combien d’eau",
    "la moyenne d’eau c’est combien",
    "consommation normale c’est quoi",
    "on utilise combien d’eau",
    "c’est combien en général",

    # 🔹 langage local / naturel
    "une famille utilise combien d’eau",
    "on prend combien d’eau par mois",
    "consommation normale c’est combien",
    "on consomme combien chez nous",
    "c’est combien l’eau en moyenne",

    # 🔹 fautes humaines
    "consomation moyenne eau",
    "quantite eau par mois",
    "moyenne consomation eau",
    "combien eau famille",
    "consomation eau normale",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais savoir la consommation moyenne d’eau pour une famille merci",
    "bonsoir combien d’eau une famille utilise en moyenne par mois",
    "salut je veux connaître la consommation normale d’eau chez un foyer",
    "franchement je veux savoir si ma consommation d’eau est normale",
    "svp aidez moi à comprendre la moyenne de consommation d’eau",

    # 🔹 avec TDE explicite
    "consommation moyenne selon la tde",
    "statistiques de consommation eau société togolaise des eaux",
    "moyenne eau tde",
    "consommation eau selon la société togolaise des eaux",

    "", ""
],

"contact_service_client": [
    # basiques clairs
    "quel est votre numéro",
    "comment vous contacter",
    "où se trouve votre agence",
    "je veux appeler un agent",
    "donnez-moi un contact",
    "numéro du service client tde",
    "comment joindre la tde",
    "je veux parler à un agent tde",
    "où est située votre agence",
    "adresse de votre agence",

    # formulations naturelles
    "je voudrais avoir votre numéro de téléphone pour vous contacter",
    "comment puis-je joindre un agent de la tde rapidement",
    "svp donnez-moi un numéro pour contacter le service client",
    "je veux savoir où se trouve votre bureau à lomé",
    "comment faire pour entrer en contact avec vous",
    "je veux passer à votre agence pour un renseignement",
    "où puis-je vous trouver physiquement",

    # langage local / réaliste
    "je peux vous appeler comment",
    "donnez-moi votre numéro là",
    "je veux venir à votre bureau",
    "vous êtes où exactement à lomé",
    "je peux vous joindre comment rapidement",
    "c’est où votre agence là",
    "je veux parler directement à quelqu’un",

    # fautes / bruit
    "votre numero c koi",
    "coment vous contacter",
    "ou se trouve votre agence",
    "je veu apel un agent",
    "doner moi un contact",
    "je veu vous joindre coment",

    # phrases longues réalistes
    "bonjour j’ai un problème et je voudrais savoir comment contacter un agent de la tde pour avoir de l’aide",
    "bonsoir je veux passer dans une agence tde pouvez-vous me dire où elle se trouve exactement",
    "svp j’ai besoin de parler à quelqu’un du service client pouvez-vous me donner un numéro",
    "je voudrais me déplacer dans votre agence pour un renseignement pouvez-vous me dire l’adresse",
    "franchement j’ai besoin d’aide mais je préfère parler à un agent directement comment vous contacter",

    # cas explicites anti-confusion (très important)
    "je ne veux pas des informations générales je veux un numéro pour vous appeler",
    "ce n’est pas une question sur les tarifs je veux juste vous contacter",
    "je veux joindre un agent pas avoir des explications",
    "je veux un contact direct avec la tde",
],

"horaire_agence": [

    # 🔹 basique
    "horaires d’ouverture",
    "heures de travail agence",
    "quand ouvrir bureau tde",
    "heures d’ouverture tde",
    "horaires agence tde",

    # 🔹 variantes naturelles
    "vous ouvrez à quelle heure",
    "vous travaillez jusqu’à quelle heure",
    "quels sont vos horaires",
    "à quelle heure je peux passer",
    "quand est-ce que vous êtes ouverts",

    # 🔹 formulation administrative (TRÈS IMPORTANT)
    "je souhaite connaître les horaires d’ouverture des agences",
    "information sur les heures de fonctionnement des bureaux",
    "horaires de service de la société togolaise des eaux",
    "jours et heures d’ouverture des agences",
    "plages horaires du service client",

    # 🔹 phrases longues réalistes
    "bonjour je voudrais connaître les horaires d’ouverture de votre agence",
    "svp à quelle heure est-ce que vous ouvrez et fermez",
    "je souhaite passer à l’agence pouvez-vous me donner vos horaires",
    "franchement je veux savoir quand je peux venir à vos bureaux",
    "je voudrais savoir les jours et heures d’ouverture de la tde",

    # 🔹 avec contexte
    "horaires agence à lomé",
    "heures d’ouverture adidogomé",
    "quand ouvrir dans mon quartier",
    "horaires agence proche de moi",
    "heures bureau tde",

    # 🔹 ambiguïtés utiles
    "vous ouvrez quand",
    "je peux venir quand",
    "c’est ouvert aujourd’hui",
    "vous êtes ouverts",
    "je passe à quelle heure",

    # 🔹 langage local / naturel
    "vous ouvrez à quelle heure là",
    "je peux venir quand chez vous",
    "vous fermez à quelle heure",
    "c’est ouvert aujourd’hui ou pas",
    "je peux passer quand",

    # 🔹 fautes humaines
    "horaire agence tde",
    "heure ouverture bureau",
    "kan ouvrir tde",
    "vous ouvrez kel heure",
    "horaire travail tde",

    # 🔹 mix complet (ultra réaliste)
    "bonjour svp je voudrais connaître les horaires d’ouverture de la tde merci",
    "bonsoir à quelle heure est-ce que vous ouvrez vos bureaux",
    "salut je veux savoir quand je peux passer à votre agence",
    "franchement je veux connaître vos horaires de travail",
    "svp aidez moi à savoir quand vous êtes ouverts",

    # 🔹 avec TDE explicite
    "horaires société togolaise des eaux",
    "heures d’ouverture de la tde",
    "jours de travail de la société togolaise des eaux",
    "horaires bureau tde",

    "", ""
],

"fallback": [

    # 🔹 basique
    "je comprends pas",
    "explique encore",
    "c’est pas clair",
    "je veux autre chose",
    "hein quoi",

    # 🔹 variantes naturelles
    "je n’ai pas compris",
    "vous pouvez expliquer mieux",
    "je comprends rien",
    "c’est pas ce que je demande",
    "ça ne répond pas à ma question",

    # 🔹 confusion / incompréhension
    "je suis perdu",
    "je ne vois pas",
    "je comprends toujours pas",
    "vous pouvez reformuler",
    "je ne saisis pas votre réponse",

    # 🔹 frustration (TRÈS IMPORTANT)
    "franchement je comprends rien",
    "ça m’aide pas du tout",
    "vous ne comprenez pas ma question",
    "c’est inutile comme réponse",
    "je veux une vraie réponse",

    # 🔹 reformulation vague
    "non je voulais dire autre chose",
    "c’est pas ça que je cherche",
    "je veux autre chose",
    "pas ça",
    "reprenons",

    # 🔹 ambiguïtés utiles
    "hein",
    "quoi",
    "comment ça",
    "je ne vois pas",
    "???",

    # 🔹 langage local / naturel
    "j’ai pas compris hein",
    "c’est comment ça",
    "tu peux expliquer encore",
    "je capte pas",
    "c’est pas clair là",

    # 🔹 fautes humaines
    "je compren pa",
    "c pa clair",
    "explike encor",
    "je veu autre chose",
    "hein koi",

    # 🔹 hors sujet / inattendu (TRÈS STRATÉGIQUE)
    "tu fais quoi",
    "ça n’a rien à voir",
    "je veux parler d’autre chose",
    "tu peux m’aider sur autre chose",
    "change de sujet",

    # 🔹 mix complet (ultra réaliste)
    "bonjour je comprends pas votre réponse pouvez-vous expliquer encore",
    "svp ce n’est pas clair je veux une meilleure explication",
    "franchement je suis perdu pouvez-vous m’aider autrement",
    "salut je n’ai pas compris ce que vous avez dit",
    "svp aidez moi je comprends rien",

    "", ""
]

}
import random
import csv

# =========================
# ⚙️ CONFIG
# =========================
NB_SAMPLES_PER_INTENT = 300



# intents = {...}  # déjà défini par toi

# =========================
# ❌ BRUIT HUMAIN (AMÉLIORÉ)
# =========================
def add_noise(text):
    replacements = {
        "vous": "vs",
        "pour": "pr",
        "bonjour": "bjr",
        "eau": "o",
        "quoi": "kwa",
        "est-ce": "eske"
    }

    words = text.split()
    new_words = []

    for w in words:
        # remplacement léger
        if random.random() < 0.15:
            w = replacements.get(w.lower(), w)

        # petite faute réaliste (PAS destructive)
        if random.random() < 0.05 and len(w) > 4:
            i = random.randint(0, len(w)-2)
            w = w[:i] + w[i+1] + w[i] + w[i+2:]  # swap lettres

        new_words.append(w)

    return " ".join(new_words)

# =========================
# 🤯 AMBIGUITE CONTRÔLÉE
# =========================
def add_ambiguity(sentence, intent):
    if random.random() < 0.25:
        # éviter fallback et même intent
        other_intents = [i for i in intents.keys() if i != intent and i != "fallback"]
        intent2 = random.choice(other_intents)

        sentence += " et aussi " + random.choice(intents[intent2])

    return sentence

# =========================
# 🧠 CLEAN STRUCTURE
# =========================
def safe_choice(lst):
    return random.choice(lst) if lst else ""

# =========================
# 🏗️ GENERATION
# =========================
def generate_sentence(intent):
    style = random.choice(sentence_styles)

    intro = safe_choice(introductions)
    context = safe_choice(contexts)
    main = random.choice(intents[intent])
    polite = safe_choice(politeness)

    # fallback sécurité
    sentence = main

    if style == "simple":
        sentence = main

    elif style == "long":
        sentence = f"{intro} je voulais savoir {main} parce que {context} et ça devient compliqué pour moi {polite}"

    elif style == "emotion":
        sentence = f"{intro} franchement {main} {context} ça me fatigue un peu {polite}"

    elif style == "indirect":
        sentence = f"{intro} est-ce que vous pouvez m'expliquer {main} {context} {polite}"

    elif style == "broken":
        sentence = f"{main} {context} pourquoi ? {polite}"

    # nettoyage espaces
    sentence = " ".join(sentence.split())

    # ambiguïté contrôlée
    sentence = add_ambiguity(sentence, intent)

    # bruit léger
    sentence = add_noise(sentence)

    return sentence.strip()

# =========================
# 🚀 DATASET
# =========================
def generate_dataset():
    data = []

    for intent in intents:
        for _ in range(NB_SAMPLES_PER_INTENT):
            sentence = generate_sentence(intent)
            data.append((sentence, intent))

    random.shuffle(data)
    return data

# =========================
# 💾 CSV
# =========================
def save_csv(data):
    with open("dataset_last.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "intent"])
        writer.writerows(data)

# =========================
# ▶️ EXECUTION
# =========================
dataset = generate_dataset()
save_csv(dataset)

print(f"Dataset généré : {len(dataset)} phrases 🚀")