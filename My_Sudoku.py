import pygame
from grid import Grid

pygame.init()

pygame.font.init()
fontgame = pygame.font.SysFont('Comic Sans MS', 30)
fontgame2 = pygame.font.SysFont('Comic Sans MS', 18)

grid = Grid(fontgame, pygame)

screen = pygame.display.set_mode((830, 605))
pygame.display.set_caption("My Sudoku")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
            if pygame.mouse.get_pressed()[0]:  
                pos = pygame.mouse.get_pos()
                grid.getclick(pos[0], pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if grid.win:
                    grid.restart()  
                else:
                    grid.toggle_help()  
            if event.key == pygame.K_h:
                grid.toggle_help()  

    screen.fill((0, 0, 0))

    grid.draw_lines(pygame, screen)
    grid.draw_numbers(screen)
    grid.show_select(pygame, screen)

    grid.draw_timer(screen)
    grid.draw_mistakes(screen)  

    if grid.show_help:
        grid.draw_help(screen)
    else:
   
        if grid.win:
            won_surface = fontgame.render("Congrats!", False, (100, 240, 0))
            screen.blit(won_surface, (650, 430))
            return_message = fontgame2.render("Press space to play again", False, (100, 240, 0))
            screen.blit(return_message, (610, 480))

    pygame.display.flip()

pygame.quit()
