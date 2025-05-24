import pygame
import time
import random

pygame.font.init()

# Window settings
WIDTH, HEIGHT = 800, 533
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Load and scale background image
BG = pygame.image.load("dd.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_VEL = 5
PLAYER_IMG = pygame.image.load("playerShip3_green.png")
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Star (meteor) settings
STAR_WIDTH = 20
STAR_HEIGHT = 30
STAR_VEL = 3
STAR_IMG = pygame.image.load("meteorBrown_small1.png")  # ✅ Fix: added ".png"
STAR_IMG = pygame.transform.scale(STAR_IMG, (STAR_WIDTH, STAR_HEIGHT))

# Font
FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars):
    """Draw everything on the screen."""
    WIN.blit(BG, (0, 0))  # Draw background
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", True, "white")
    WIN.blit(time_text, (10, 10))  # Draw timer
    WIN.blit(PLAYER_IMG, (player.x, player.y))  # Draw player

    for star in stars:
        WIN.blit(STAR_IMG, (star.x, star.y))  # Draw meteor stars

    pygame.display.update()


def main():
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    run = True
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Add random stars
        if star_count > star_add_increment:
            for _ in range(random.randint(1, 5)):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        # Move stars
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                hit = True
                break

        draw(player, elapsed_time, stars)

        if hit:
            lost_text = FONT.render("You Lost!", True, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2,
                                 HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

    pygame.quit()


if __name__ == "__main__":
    main()
