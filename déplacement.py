while running :
    
    events = pg.event.get()
    a = sum(event.type == pg.KEYDOWN for event in events)
    while a == 0:
        events = pg.event.get()
        a = sum(event.type == pg.KEYDOWN for event in events)
    

    for event in events:

        a, b = character.x, character.y

        if event.type == pg.QUIT:
            running = False
        
        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
            if event.key == pg.K_q:
                running = False
            
            elif (event.key == pg.K_UP) and (level.map[character.x, character.y -1] != 0):
                character.y -= 1
                character.direction = 'N'
                move_character(screen, character, a, b)

            elif event.key == pg.K_DOWN and (level.map[character.x, character.y +1] != 0):
                character.y += 1
                character.direction = 'S'
                move_character(screen, character, a, b)

            elif event.key == pg.K_LEFT and (level.map[character.x-1, character.y] != 0):
                character.x -= 1
                character.direction = 'O'
                move_character(screen, character, a, b)

            elif (event.key == pg.K_RIGHT) and (level.map[character.x+1, character.y] != 0):
                character.x += 1
                character.direction = 'E'
                move_character(screen, character, a, b)

    pg.display.update()
