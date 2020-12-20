import game

g = game.Game()

while g.RUNNING:
    g.PLAYING = True
    g.game_loop()
