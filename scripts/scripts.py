from asyncio import sleep, ensure_future
from pyodide.ffi import create_proxy
from random import randrange
from js.console import log
from js import document, location, window

# Affectation de toutes les variables nécessaires
switchAudioButton = document.getElementById('switchAudioButton')
imgSwitchButton = document.getElementById('imgSwitchButton')
explosionSound = document.getElementById('explosionSound')
rulesButton = document.getElementById('rulesButton')
bombsSlider = document.getElementById('bombsSlider')
playButton = document.getElementById('playButton')
slidersDiv = document.getElementById('slidersDiv')
backButton = document.getElementById('backButton')
flagCount = document.getElementById('flagCount')
gameSpace = document.getElementById('gameSpace')
retryDiv = document.getElementById('retryDiv')
rulesDiv = document.getElementById('rulesDiv')
xSlider = document.getElementById('xSlider')
ySlider = document.getElementById('ySlider')
quitDiv = document.getElementById('quitDiv')
timer = document.getElementById('timer')
music = document.getElementById('music')
title = document.getElementById('title')
grid = document.getElementById('grid')
rulesActive = False
firstTime = True
bombsValue = 40
lose = False
win = False

# Fonction pour changer la valeurs des sliders à chaque changement
def updateSliders(event):
    if event.target.id == 'xSlider':
        xSlider.value = event.target.value
        Element('xValue').write(f'NOMBRES DE LIGNES : {xSlider.value}')
    elif event.target.id == 'ySlider':
        Element('yValue').write(f'NOMBRES DE COLONNES : {ySlider.value}')
        ySlider.value = event.target.value
    else:
        global bombsValue
        Element('bombsValue').write(f'NOMBRES DE BOMBES : {bombsSlider.value}')
        bombsValue = int(bombsSlider.value)

# 3 "écouteurs" pour détécter quand un slider est bougé
xSlider.addEventListener('input', create_proxy(updateSliders))
ySlider.addEventListener('input', create_proxy(updateSliders))
bombsSlider.addEventListener('input', create_proxy(updateSliders))

# Fonction asynchrone pour afficher les règles et les afficher tant que l'utilisateur n'appuie pas sur le bouton retour
async def printRules():
    global rulesActive
    while rulesActive:
        await sleep(1)

# Fonction asynchrone pour lancer le timeur quand le bouton play est appuyé et pour geler le timer quand les règles sont affichées
async def launchTimer():
    seconds, minutes, hours = 0, 0, 0
    global rulesActive, lose, win
    while 1:
        flagCount.style.color = 'black'
        if rulesActive:
            await printRules()
        if lose or win:
            return 0
        Element('timer').write(f'⏱️ | {hours} : {minutes} : {seconds} |')
        seconds += 1
        if seconds >= 60:
            minutes += 1
            seconds = 0
        if minutes >= 60:
            hours += 1
            minutes = 0
        await sleep(1)

# 2 fonctions pour changer la couleur du bouton de l'audio quand on le survole
def hoverInSwitchAudio(event):
    if imgSwitchButton.src[-6:] == 'Up.svg':
        imgSwitchButton.src = '../assets/volumeUpHover.svg'
    else:
        imgSwitchButton.src = '../assets/volumeMuteHover.svg'
imgSwitchButton.addEventListener('mouseenter', create_proxy(hoverInSwitchAudio))

def hoverOutSwitchAudio(event):
    if imgSwitchButton.src[-11:] == 'UpHover.svg':
        imgSwitchButton.src = '../assets/volumeUp.svg'
    elif imgSwitchButton.src[-13:] == 'MuteHover.svg':
        imgSwitchButton.src = '../assets/volumeMute.svg'
imgSwitchButton.addEventListener('mouseleave', create_proxy(hoverOutSwitchAudio))

# Fonction pour changer l'image du bouton volume et couper/reprendre la musique
def switchAudio(*ags, **kws):
    if firstTime:
        imgSwitchButton.src = '../assets/volumeMuteHover.svg'
    elif music.paused:
        music.play()
        imgSwitchButton.src = '../assets/volumeUpHover.svg'
    else:
        music.pause()
        imgSwitchButton.src = '../assets/volumeMuteHover.svg'

# Fonction de débug pour obtenir l'id d'un élément
def getId(event):
    log(event.target.id)

async def loseAnimation():
    music.pause()
    explosionSound.volume = 0.1
    explosionSound.play()
    global bombLocations
    await sleep(1)
    for ordonne, absc in bombLocations.items():
        for abscisse in absc:
            document.getElementById(f'{ordonne} {abscisse}').innerText = '💣'
            document.getElementById(f'{ordonne} {abscisse}').style.backgroundColor = 'crimson'
            await sleep(0.1)
    await sleep(1)
    printWidgets(2)

# Fonction de débug pour changer le texte des boutons
def addNumber(event):
    global lose, bombsValue, firstTime
    caseDiscover = 0
    if not lose and not win:
        if firstTime:
            firstTime = False
            event.target.style.backgroundColor = 'black'
            event.target.innerText = '0'
            return launchBombs(event.target.id)
        else:
            if gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])] == 'B':
                bombLocations[int(event.target.id.split()[0])].remove(int(event.target.id.split()[1]))
                event.target.innerText = '💥'
                lose = True
                return ensure_future(loseAnimation())

            event.target.style.backgroundColor = 'black'
            if event.target.innerText == '🚩':
                bombsValue += 1
                Element('flagCount').write(f'🚩 : {bombsValue}')
                event.target.innerText = '‍‍‍‍‍‍‍'

            if gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])] == 0:
                event.target.style.color = 'lime'
            elif gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])] == 1:
                event.target.style.color = 'lime'
            elif gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])] == 2:
                event.target.style.color = 'yellow'
            elif gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])] == 3:
                event.target.style.color = 'orange'
            elif gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])] == 4:
                event.target.style.color = 'crimson'
            else:
                for i in range(4, 9):
                    if gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])] == i:
                        event.target.style.color = 'red'

            event.target.innerText = gridResponse[int(event.target.id.split()[0])][int(event.target.id.split()[1])]
            # Vérifier si l'utilisateur à gagner
            for i in range(int(ySlider.value)):
                for r in range(int(xSlider.value)):
                    if document.getElementById(f'{i} {r}').innerText == '‍‍‍‍‍‍‍' or document.getElementById(f'{i} {r}').innerText == '🚩':
                        caseDiscover += 1

            if caseDiscover == int(bombsSlider.value):
                win = True

# Fonction pour ajouter un drapeau dans la case si cela est possible
def addFlag(event):
    event.preventDefault()
    global bombsValue
    if not firstTime:
        if event.target.innerText == '🚩':
            event.target.style.backgroundColor = 'white'
            event.target.innerText = '‍‍‍‍‍‍‍'
            bombsValue += 1
            Element('flagCount').write(f'🚩 : {bombsValue}')
        elif event.target.innerText == '‍‍‍‍‍‍‍':
            if event.target.style.backgroundColor != 'black':
                if bombsValue <= 0:
                    flagCount.style.color = 'red'
                else:
                    event.target.innerText = '🚩'
                    event.target.style.backgroundColor = 'black'
                    bombsValue -= 1
                    Element('flagCount').write(f'🚩 : {bombsValue}')

def verifMouseDown(event):
    if event.which == 1:
        addNumber(event)

# Fonction pour créer la grille avec le nombre de cases (boutons) nécessaires
def createGrid(*ags, **kws):
    grid.style.height = f'{30*int(ySlider.value)}px'
    grid.style.width = f'{30*int(xSlider.value)}px'

    for i in range(int(ySlider.value)):
        for r in range(int(xSlider.value)):
            tempButton = document.createElement('button')
            tempButton.style = 'height:30px; width:30px; bottom:-10px; margin:0; padding:0;'
            tempButton.addEventListener('mouseenter', create_proxy(verifMouseDown))
            tempButton.addEventListener('contextmenu', create_proxy(addFlag))
            tempButton.addEventListener('click', create_proxy(addNumber))
            tempButton.id = f'{i} {r}'
            tempButton.innerText = '‍‍‍‍‍‍‍'
            grid.append(tempButton)

# Fonction qui affiche les éléments au bon moment et les retire quand il faut, en fonction du parmètre qu'on lui donne
def printWidgets(order):
    if order == 1:
        Element('flagCount').write(f'🚩 : {bombsValue}')
        playButton.remove()
        rulesButton.style.display = 'block'
        slidersDiv.style.display = 'none'
        gameSpace.style.display = 'block'
    elif order == 'rulesOn':
        if not lose:
            backButton.style.display = 'block'
        rulesButton.style.display = 'none'
        rulesDiv.style.display = 'block'
        gameSpace.style.display = 'none'
        timer.style.display = 'none'
        global rulesActive
        rulesActive = True
    elif order == 'rulesOff':
        rulesButton.style.display = 'block'
        backButton.style.display = 'none'
        gameSpace.style.display = 'block'
        rulesDiv.style.display = 'none'
        timer.style.display = 'block'
        rulesActive = False
    elif order == 2:
        gameSpace.style.display = 'none'
        retryDiv.style.display = 'block'
    elif order == 3:
        switchAudioButton.style.display = 'none'
        rulesButton.style.display = 'none'
        retryDiv.style.display = 'none'
        quitDiv.style.display = 'block'
        title.style.display = 'none'
        timer.style.display = 'none'
        ensure_future(quitGame())
        
async def quitGame():
    await sleep(1)
    window.close()

# Fonction pour vérifier que le nombre de bombe est compatibles avec le nombre de cases
def verifSetting():
    if bombsValue < int(xSlider.value)*int(ySlider.value) and bombsValue >= int(xSlider.value)*int(ySlider.value)-8:
        Element('bombsError').write('IMPOSSIBLE : IL Y A TROP DE BOMBES POUR LE NOMBRE DE CASES CHOISI (MINIMUM 9 CASES DE PLUS QUE DE BOMBES)')
        document.getElementById('bombsError').style.display = 'block'
        return False
    elif bombsValue > int(xSlider.value)*int(ySlider.value):
        Element('bombsError').write('IMPOSSIBLE : IL Y A BEAUCOUP TROP DE BOMBES')
        document.getElementById('bombsError').style.display = 'block'
        return False
    elif bombsValue == int(xSlider.value)*int(ySlider.value):
        Element('bombsError').write('IMPOSSIBLE : IL Y A AUTANT DE BOMBES QUE DE CASES')
        document.getElementById('bombsError').style.display = 'block'
        return False
    return True

# Fonction pour jouer la musique au début de la partie, si l'utilisateur ne l'a pas couper avant
def playMusic():
    if imgSwitchButton.src[-6:] == 'Up.svg':
        music.volume = 0.1
        music.play()

# Fonction principal éxécutant toutes les autres fonctions dans le bon ordre
async def play(*ags, **kws):
    global firstTime, gridResponse
    # 1) vérifier que la grille est créable et la créer
    if verifSetting():
        # Création de la grille de réponse (comme dans la V1)
        gridResponse = [[0 for i in range(int(xSlider.value))] for d in range(int(ySlider.value))]
        # 2) Lancer la musique ou non
        playMusic()
        # 3) Créer la grille
        createGrid()
        # 4) Afficher les boutons qui doivent être affichés à ce moment la
        printWidgets(1)
        #5) Lancer le timeur
        ensure_future(launchTimer())
        #6) On attend que l'utilisateur clique sur une case (le sleep consomme peut-être beaucoup de puissance processeur vu coment la fonction marche mais personnellement je n'ai eu aucun soucis donc je l'ai laissé comme ça, c'est la solution la plus simple)
        while firstTime:
            await sleep(0.1)
        #6) Placer les bombes sur la grille (La fonction est appelée directement dans la fonction addNumber() pour pouvoir avoir l'id du bouton cliquer)

# Fonction pour mettre les bombes et les numéros dans la grille réponse
def launchBombs(case):
    global bombLocations
    case = case.split()
    bombLocations = {}
    [bombLocations.update({i:[]}) for i in range(int(ySlider.value))]

    for i in range(bombsValue):
        ok = False
        while not ok:
            # La même condition beaucoup trop grande que dans la V1, mais que je ne sais toujours pas comment améliorer, pour vérifier qu'il n'y a pas de bombe autour et dans la première case choisie par l'utilisateur, afin que la première case choisie soit un 0.
            abscisse, ordonnee = randrange(int(xSlider.value)), randrange(int(ySlider.value))
            while (ordonnee == int(case[0]) and abscisse == int(case[1])) or (ordonnee == int(case[0])-1 and abscisse == int(case[1])) or (ordonnee == int(case[0])+1 and abscisse == int(case[1])) or (ordonnee == int(case[0])-1 and abscisse == int(case[1])-1) or (ordonnee == int(case[0])-1 and abscisse == int(case[1])+1) or (ordonnee == int(case[0]) and abscisse == int(case[1])-1) or (ordonnee == int(case[0]) and abscisse == int(case[1])+1) or (ordonnee == int(case[0])+1 and abscisse == int(case[1])-1) or (ordonnee == int(case[0])+1 and abscisse == int(case[1])+1):
                abscisse, ordonnee = randrange(int(xSlider.value)), randrange(int(ySlider.value))

            if abscisse not in bombLocations[ordonnee]:
                bombLocations[ordonnee].append(abscisse)
                ok = True

    # Rajouter les bombes et les numéros de 1 à 8 dans la grille réponse
    for cle, valeur in bombLocations.items():
        for i in valeur:
            gridResponse[cle][i] = 'B'
            # Pour éviter que les cases de gauches changent les cases de droite tab[-1] = dernière case en python et les out of range
            if i-1 > -1 and gridResponse[cle][i-1] != 'B':
                gridResponse[cle][i-1] += 1
            if i+1 < int(xSlider.value) and gridResponse[cle][i+1] != 'B':
                gridResponse[cle][i+1] += 1
            if i+1 < int(xSlider.value) and cle+1 < int(ySlider.value) and gridResponse[cle+1][i+1] != 'B':
                gridResponse[cle+1][i+1] += 1
            if cle+1 < int(ySlider.value) and i-1 > -1 and gridResponse[cle+1][i-1] != 'B':
                gridResponse[cle+1][i-1] += 1
            if cle-1 > -1 and i+1 < int(xSlider.value) and gridResponse[cle-1][i+1] != 'B':
                gridResponse[cle-1][i+1] += 1
            if cle-1 > -1 and i-1 > -1 and gridResponse[cle-1][i-1] != 'B':
                gridResponse[cle-1][i-1] += 1
            if cle-1 > -1 and gridResponse[cle-1][i] != 'B':
                gridResponse[cle-1][i] += 1
            if cle+1 < int(ySlider.value) and gridResponse[cle+1][i] != 'B':
                gridResponse[cle+1][i] += 1
