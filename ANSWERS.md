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

## 3. Authenticated Symetric Encryption

1. Fernet est moins risqué que le précédent chapitre parce qu'il est plus facile à implémenter. Étant donné qu'il est plus facile à implémenter, il y a donc moins de risques qu'une mauvaise utilisation de l'algorithme fragilise le système.

2. Cette attaque est appelée "replay attack" ou "attaque par rejeu".

3. Une méthode permet de s'affranchir de l'attaque par rejeu : il s'agit de l'horodatage des messages. Le message envoyé possède un horodatage (ou timestamp) qui doit être calculé lors de sa réception. Si l'horodatage est identique, alors le message n'a pas été détourné.

## 4. TTL

1. La différence avec le chapitre précédent vient de l'ajout d'un horodatage, qui permet d'empêcher la récupération et la restitution du message, puisqu'un message trop vieux générera une erreur.

2. Lorsqu'on soustrait 45 au temps lors de l'émission, on remarque que cela déclenche une erreur, que l'on peut capturer en ajoutant une exception dans la fonction ```decrypt()```. Cette erreur se déclenche car le token (l'horodatage évoqué plus haut) est invalide : ainsi, le message envoyé n'ayant pas le même token que le message reçu, il est donc rejeté.

3. Ce système permet de prévenir ou d'être au courant en cas de compromission du serveur ; cependant, il ne protège pas contre l'attaque en soi.

4. Dans la pratique, ce système ne peut pas être utilisé si le chiffrement et le déchiffrement du message n'ont pas lieu au même moment, voire dans le contexte d'un échange de messages asynchrone.


## Regard critique
