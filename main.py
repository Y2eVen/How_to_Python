import game

gamez = game.Game()


while gamez.RUNNING:

    gamez.menu.display_menu()

    gamez.loop()
