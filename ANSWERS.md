# TP secure chat

## 1. Prise en main

1. Cette topologie semble être une topologie en étoile.

2. Dans les logs, on peut voir lorsque les deux clients se connectent au serveur. On peut également lire les messages, qui sont transmis en clair.

3. C'est un problème, car cela viole le principe de confidentialité des données. 

4. La solution la plus simple serait donc de mettre en place un chiffrement de données, de telle sorte à ce que seuls les interlocuteurs aient accès aux messages échangés.

## 2. Chiffrement

1. La fonction ```urandom``` est un bon choix pour la cryptographie, car elle est décrite dans sa documentation comme une librairie se basant sur un générateur de hasard réellement aléatoire (dans le cas où il existe sur l'ordinateur). Ce générateur de hasard est dit réellement aléatoire, car les nombres générés le sont à l'aide de processus physiques aléatoires, donc imprévisibles.

2. Utiliser ses propres primitives cryptographiques peut être dangereux dans le cas où le développeur n'a pas forcément les compétences mathématiques et techniques pour l'écrire de manière robuste, ce qui pourrait laisser des vulnérabilités dans les algorithmes. De plus, les primitives cryptographiques étant récentes, elles n'ont pas forcément été testées par un ou plusieurs chercheurs dans le domaine de la cryptographie.

3. Malgré le chiffrement, un serveur malveillant peut toujours nuire dans le cas où il se ferait passer pour l'un des interlocuteurs et modifierait les messages.

4. Ici, parmi les 3 principes de confidentialité, intégrité et disponibilité, la confidentialité est assurée puisque les messages sont chiffrés et déchiffrés localement par les clients et les messages ne sont pas lisibles par le serveur. L'intégrité, en revanche, n'est pas assurée car il n'y a pas de moyen de vérifier que le message reçu est bien le même que le message émis.