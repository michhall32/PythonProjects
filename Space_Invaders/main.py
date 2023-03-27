import pygame
import setUp
import images 
import random
pygame.font.init()


WIN = pygame.display.set_mode((setUp.WIDTH, setUp.HEIGHT))
pygame.display.set_caption("Space Invaders")


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 30)
    lost_font = pygame.font.SysFont('comicsans', 80)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    laser_vel = 5
    player_vel = 5
    player = setUp.Player(300, 630)
    
    clock = pygame.time.Clock()
    
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(setUp.BG, (0,0))
        # draw text
        lives_label = main_font.render(f'Lives: {lives}', 1, (255,255,255))
        level_label = main_font.render(f'Level: {level}', 1, (255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (setUp.WIDTH - level_label.get_width()- 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render('YOU LOST!!!', 1, (255,0,0))
            WIN.blit(lost_label,(setUp.WIDTH/2 - lost_label.get_width()/2, 400))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <=0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for _ in range(wave_length):
                enemy = setUp.Enemy(random.randrange(50, setUp.WIDTH-100), random.randrange(-1500, -100), random.choice(['red','blue','green']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:    #left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < setUp.WIDTH:    #right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:    #up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < setUp.HEIGHT:    #down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*FPS) == 1:
                enemy.shoot()
            
            if setUp.collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > setUp.HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            
        player.move_lasers(-laser_vel, enemies)



def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True
    while run:
        WIN.blit(setUp.BG, (0,0))
        title_label = title_font.render("Press mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (setUp.WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

if __name__ == '__main__':
    main_menu()  
