# Keep babbling and everyone survives - Embedded core

Ensemble du système de jeu et de communication embarqué pour KBAES sur raspberry PI 3+. Codé pour Python 2.7

## Dépendances

- tornado
  - Gestion de l'event loop principale, utilitaires de communication avec Redis, et client HTTP.
- tornadis
  - Client redis tiers pour tornado
- RPi.GPIO

## Architecture générale

Le script écoute l'api (via redis), requête l'api pour avancer dans le jeu, implémente les séquences de jeu indépendemment (display des séquences, écoute inputs). 

l'écoute de l'api est implémentée sur la main IOLoop de Tornado, syncronisée avec le client REDIS grâce à `IOLoop.current().run_sync()`. Le client redis boucle indéfiniment et réagit à la réaction des messages. Les messages possibles sont pour l'instant: `RequestNewGame` et `RequesGameHalt`. Le premier initie la séquence de jeu.

Le Thread principal synchronisé à l'écoute de redis a aussi en charge les appels HTTP vers l'API ainsi que la diffusiond es réponses.

Le script a deux postures: une posture d'attente de redis pour lancer un jeu (standby), une posture de jeu (boucle de gameplay)

### La boucle de gameplay

- __init__: Création d'un thread pour le timer, lancement du timer dans le thread
- __début boucle__: Création d'un thread pour le module de gameplay (Affichage de la séquence de LEDs, écoute des boutons sur la board)
- Création d'un thread d'attente des messages des threads de gameplay.
- Réception des inputs des threads (Input utilisateur, fin du timer)
- En cas de fin du timer: coupure du thread d'écoute de gameplay, affichage des messages de fin de jeu, remise en posture d'écoute de Redis. __sortie de boucle__
- En cas de réponse utilisateur: Envoi de la réponse utilisateur à l'API.
- La _response_ de l'api définit la suite:
  - Le jeu est perdu (Trop d'erreurs), affichage d'un message d'échec sur le petit écran. __sortie de boucle__
  - Le jeu est gagné (tous les modules ont été répondu dans le temps donné sans dépasser la limite d'erreurs). Affichage du message de victoire __sortie de boucle__
  - Le jeu continue: La réponse de l'api contient le résultat de l'envoi (Bonne/mauvaise réponse), ainsi que la séquence de jeu suivante. __Itération suivante__
  
### Les modules électroniques

Le script gère deux modules externes pour l'affichage et l'écoute des inputs: Un timer codé sur l'afficheur 2 lignes (mini LCD), un système d'alumage de LEDs et d'écoute des boutons.

## API

Le script joint l'api sur ces routes:

- POST /api/game/{id}/confirm => Confirme que la board a bien reçu la demande de nouveau et est capable de jouer le jeu demandé
- POST /api/game/{gameid}/answer/{rulesetId} => Envoi d'un tableau de réponses en body
- POST /api/game/{id}/timesup => Envoie une notification de fin de compte à rebours à l'API. (inconsistance d'archi)

## Utilisation

Lancer src/kbaes.py (python 2.7)
