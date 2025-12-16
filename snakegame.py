import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

font = pygame.font.SysFont(None, 36)
eat_sound = pygame.mixer.Sound("eatingapple.wav.wav")
gameover_sound = pygame.mixer.Sound("gameover.mp3")
menu_sound = pygame.mixer.Sound("menu.mp3")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # màu táo lớn

//Hàm này mục đích tạo ra đối tượng táo ngẫu nhiên 
def random_apple(snake, other_apple=None):
    //sử dụng while để liên tục tạo ra các tọa độ ngẫu nhiên  
    while True: 
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        //kiểm tra hợp lệ của tọa độ nếu tọa độ (x, y) của quả táo trùng với tọa độ của snake 
         và quả táo khác
        if (x, y) not in snake and (other_apple is None or (x, y) != other_apple):
            return (x, y)

def draw(snake, apple, score, game_state, big_apple):
    screen.fill(BLACK)
    
    if game_state == "menu":
        text = font.render("Press any key to start", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    elif game_state == "gameover":
        text = font.render(f"Game Over! Score: {score}", True, RED)
        retry = font.render("Press any key to return to menu", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(retry, (WIDTH // 2 - retry.get_width() // 2, HEIGHT // 2 + 10))
    elif game_state == "playing":
        for segment in snake:
            //draw.rect là hàm vẽ hcn 
            //tạo ra con rắn. Định nghĩa hình chữ nhật tại vị trí (x, y) với chiều rộng và cao là CELL_SIZE 
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, RED, pygame.Rect(apple[0], apple[1], CELL_SIZE, CELL_SIZE))
        if big_apple:
            pygame.draw.rect(screen, YELLOW, pygame.Rect(big_apple[0], big_apple[1], CELL_SIZE, CELL_SIZE))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# Biến game
clock = pygame.time.Clock()
game_state = "menu"
snake = [(100, 100)]
direction = (CELL_SIZE, 0)
apple = random_apple(snake)
big_apple = None
score = 0
speed = 10
small_apples_eaten = 0

running = True
while running:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                menu_sound.play()
                snake = [(100, 100)]
                direction = (CELL_SIZE, 0)
                apple = random_apple(snake)
                big_apple = None
                score = 0
                speed = 10
                small_apples_eaten = 0
                game_state = "playing"

        elif game_state == "gameover":
            if event.type == pygame.KEYDOWN:
                game_state = "menu"

        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_s and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_a and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_d and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

    if game_state == "playing":
        
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        if head == apple:
            eat_sound.play()
            score += 1
            small_apples_eaten += 1
            speed += 0.3
            apple = random_apple(snake, big_apple)
            
            if small_apples_eaten >= 3:
                big_apple = random_apple(snake, apple)
                small_apples_eaten = 0
        elif big_apple and head == big_apple:
            eat_sound.play()
            score += 3
            speed += 0.3
            big_apple = None
        else:
            snake.pop()
        
        if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake[1:]):
            gameover_sound.play()
            game_state = "gameover"

    draw(snake, apple, score, game_state, big_apple)

pygame.quit()
sys.exit()
