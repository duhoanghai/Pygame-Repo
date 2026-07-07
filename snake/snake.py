import pygame
from time import sleep
from random import randint

pygame.init()
WIDTH, HEIGHT = 601, 601
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
running = True

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
clock = pygame.time.Clock()

# x, y cua moi con ran
# tail - head
snakes = [[5,10]]
direction = "right" 

apple = [randint(0,19), randint(0,19)]

font_small = pygame.font.SysFont("sans", 20)
font_big = pygame.font.SysFont("sans", 50)

score = 0
point_sound = pygame.mixer.Sound('point.wav')
gameover_sound = pygame.mixer.Sound('gameover.wav')
sound = True
pausing = False
while running:		
	clock.tick(60)
	screen.fill(BLACK)

	tail_x = snakes[0][0]
	tail_y = snakes[0][1]

	# draw grid
	# for i in range(21):
	# 	pygame.draw.line(screen, WHITE,(0,i*30),(WIDTH,i*30)) # chieu ngang
	# 	pygame.draw.line(screen, WHITE,(i*30,1),(i*30,HEIGHT)) # chieu doc

	# create snake
	for snake in snakes:
		pygame.draw.rect(screen, GREEN, (snake[0]*30, snake[1]*30, 30, 30))

	# draw apple
	pygame.draw.rect(screen, RED, (apple[0]*30, apple[1]*30, 30, 30))

	# point
	if snakes[-1][0] == apple[0] and snakes[-1][1] == apple[1]:
		snakes.insert(0,[tail_x, tail_y])
		apple = [randint(0,19), randint(0,19)]
		score += 1
		pygame.mixer.Sound.play(point_sound)

	# create score
	score_txt = font_small.render("Score: " + str(score), True,WHITE)
	screen.blit(score_txt, (5,5))

	# check crash with edge
	if snakes[-1][0] < 0 or snakes[-1][0] > 19 or snakes[-1][1] < 0 or snakes[-1][1] > 19:
		pausing = True

	# sanke moves
	if pausing == False:
		if direction == "right":
			snakes.append([snakes[-1][0]+1, snakes[-1][1]]) 
			snakes.pop(0)
		if direction == "left":
			snakes.append([snakes[-1][0]-1, snakes[-1][1]]) 
			snakes.pop(0)
		if direction == "up":
			snakes.append([snakes[-1][0], snakes[-1][1]-1])
			snakes.pop(0)
		if direction == "down":
			snakes.append([snakes[-1][0], snakes[-1][1]+1]) 
			snakes.pop(0)

	sleep(0.1)

	# check crash with body
	for i in range(len(snakes)-1):
		if snakes[-1][0] == snakes[i][0] and snakes[-1][1] == snakes[i][1]:
			pausing = True	

	# gameover
	if pausing:
		if sound:
			pygame.mixer.Sound.play(gameover_sound)
			sound = False
		game_over_txt = font_big.render("Game Over, score: " + str(score), True, WHITE)
		press_space_txt = font_big.render("Press space to continue", True, WHITE)
		screen.blit(game_over_txt, (50,100))
		screen.blit(press_space_txt, (50,300))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and direction != "down":
				direction = "up"
			if event.key == pygame.K_DOWN and direction != "up":
				direction = "down"
			if event.key == pygame.K_LEFT and direction != "right":
				direction = "left"
			if event.key == pygame.K_RIGHT and direction != "left":
				direction = "right"
			if event.key == pygame.K_SPACE and pausing == True:
				pausing = False
				snakes = [[5,10]]
				apple = [randint(0,19), randint(0,19)]
				score = 0
				sound = True
	pygame.display.flip()

pygame.quit()

