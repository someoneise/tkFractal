Hey!
**tkfractal** est une application construite avec Tkinter, en Python, qui vous permet de générer vos propres fractales.

## Caractéristiques :
- **Création** de fractales IFS
- **Utilisation** de palettes de couleurs pour personnaliser votre fractale comme vous le souhaitez
- **Navigation** dans la fenêtre de la fractale, pour ne cadrer que ce que vous voulez cadrer
- **Exportation et importation** de nuages de points, afin que vous puissiez partager vos fractales avec d'autres personnes et qu'elles puissent les modifier.
- **Exportation en tant qu'image** PNG, pour que vous puissiez télécharger votre fractale sur un site web ou l'imprimer.

**tkfractal** est **OpenSource** et ne contient pas de publicité.

## Utilisation :
1. Cloner le dépôt, ou le télécharger sous forme de zip (et le décompresser).
2. Exécutez le fichier principal, appelé "vue.py".
3. Après quelques secondes, vous devriez voir l'interface graphique.
4. Sur la gauche, sélectionnez d'abord la forme fractale que vous voulez voir, puis la palette de couleurs que vous voulez utiliser.
5. Cliquez sur generate, et voilà !
6. Si vous voulez modifier un aspect de la fractale, comme la couleur, cliquez simplement sur la couleur, et cliquez à nouveau sur régénérer.
7. Pour naviguer et ajuster votre fractale à votre convenance, cliquez sur le bouton "navigation".
8. Pour exporter votre fractale en png, cliquez sur "exporter en tant qu'image".

## Une brève description du fonctionnement des IFS :
**IFS** est l'abréviation de **iterated function system** (système de fonctions itérées).

Il s'agit d'un moyen d'obtenir des motifs qui ressemblent à certaines structures mathématiques appelées "fractales", dont la définition est une figure qui contient des motifs qui s'assimilent à l'intérieur d'elle-même (en d'autres termes, une petite partie de la fractale ressemble visuellement au reste de la fractale).

Si cela vous semble un peu illogique ou bizarre, ce n'est pas grave, c'est naturel ; en utilisant notre programme, vous comprendrez de quoi je parle.

Revenons à l'**IFS** :
Dans notre programme, chaque fractale est définie par un système de fonctions (dans ce cas, des fonctions affines) qui transforment un point initial en un autre point dans le plan à deux dimensions.

Chaque fichier se terminant par *.ifs* dans le dossier *ifs_files* contient un certain nombre de lignes, et chaque ligne représente une de ces fonctions, avec une certaine probabilité associée.

Créons maintenant notre fractale :
Nous allons commencer par prendre un **point initial**, pour commencer à dessiner notre fractale : dans notre code, nous prenons le point (0,0) , mais en théorie, n'importe quel point fonctionne. Maintenant, en utilisant les probabilités de chaque fonction de notre système de fonctions, choisissons-en une au hasard. 
(Il peut sembler un peu bizarre de dire que "nous choisissons quelque chose au hasard, selon les probabilités", mais vous pouvez imaginer cela comme si vous aviez 100 fonctions dans un sac, et vous prenez une par hasard. Par exemple, si nous avons des probabilités **f1**=.2, **f2**=.3 et **f3**=.5, il y a 20 **f1**, 30 **f2** et **50** f3 dans le sac, et maintenant, prenez l'un d'entre eux au hasard).
En utilisant cette fonction, nous générons un nouveau point **(x1,y1) = f(0,0)**. Nous plaçons ce point sur le canevas, et répétons la fonction dessiner. Maintenant, nous avons une autre fonction, et nous allons générer un nouveau point. mais attendez, la magie est la suivante : nous allons utiliser comme argument de la fonction, le point précédent que nous venons de générer; **(x2,y2) = f(x1,y1)** . C'est pourquoi on parle de systèmes de fonctions ***itérées*.** Nous plaçons ce nouveau point sur la toile, et nous répétons cette opération environ 50 000 fois, jusqu'à ce que nous obtenions une image visible.

Plus d'info : [Système de fonctions itérées - Wikipedia](https://www.wikiwand.com/fr/Syst%C3%A8me_de_fonctions_it%C3%A9r%C3%A9es)

## Notes sur le programme :
- Le programme utilise un algorithme appelé IFS pour générer des points aléatoires, qui sont ensuite affichés à l'écran.
- Si vous souhaitez ajouter une nouvelle forme fractale, vous devez créer un nouveau fichier _.ifs_ dans le dossier _ifs_files_, qui a les caractéristiques suivantes:
```
Cxx Cxy Cyx Cyy Bx By P
... 
```
Les fonctions affines sont de la forme **f(x)= Cx+B**, avec x un vecteur, C une matrice, B un vecteur.

Les entrées commençant par **C** décrivent la matrice suivante,
Les entrées **B** décrivent le vecteur,
Enfin, **P** est un nombre compris entre 0 et 1 qui décrit la probabilité de choisir cette matrice.

> | Cxx Cxy | +  | Bx |
> 
> | Cyx Cyy |    | By |
