import enum
import random
import time

import pygame, sys
import pygame.locals


class Ball:

	def __init__(self, x, y):
		self.x = x
		self.y = y

		self.dir_x = 0
		self.dir_y = 0

	def set_pos(self, x, y):
		self.x = x
		self.y = y

	def set_direction(self, dir_x=None, dir_y=None):
		print(f"zmiana kierunku: {dir_x} {dir_y}")

		if dir_x is not None:
			self.dir_x = dir_x

		if dir_y is not None:
			self.dir_y = dir_y

	@property
	def next_x(self):
		return self.x + self.dir_x

	@property
	def next_y(self):
		return self.y + self.dir_y

	def move(self):
		self.x = self.next_x
		self.y = self.next_y


class Board:

	def __init__(self, width, height):
		self.width = width
		self.height = height

	def is_left_wall_collision(self, ball):
		return ball.next_x < 0

	def is_right_wall_collision(self, ball):
		return ball.next_x > (self.width - 1)

	def is_top_wall_collision(self, ball):
		return ball.next_y < 0

	def is_bottom_wall_collision(self, ball):
		return ball.next_y > (self.height - 1)

	@property
	def center_x(self):
		return int(self.width / 2)
		

class Paddle:

	def __init__(self, x, y, width):
		self.x = x
		self.y = y
		self.width = width

	def is_collision(self, ball):
		if ball.next_y != self.y:
			return False
	
		if self.width == 0:
			return False

		return self.x <= ball.next_x <= (self.x + self.width - 1)

	def move(self, dir_x, width=None):
		if (dir_x == -1) and (self.x == 0):
			return

		if (width is not None) and (dir_x == 1) and ((width - self.x - 1) < self.width):
			return

		self.x += dir_x


class PongGame:

	def __init__(self, width, height):
		self.board = Board(width, height)

		self.ball = Ball(self.board.center_x, 1)
		
		self.top_paddle = Paddle(0, 0, width=2)
		self.bottom_paddle = Paddle(0, (self.board.height - 1), width=2)

		self.game_started = False	

	def process(self):
		if not self.game_started:
			return

		random_dir_x = False
		ball = self.ball

		print(f"ball: x:{ball.x} y:{ball.y}")

		if self.board.is_right_wall_collision(ball):
			ball.set_direction(-1, None)

		if self.board.is_left_wall_collision(ball):
			ball.set_direction(1, None)

		if self.bottom_paddle.is_collision(ball):
			ball.set_direction(0, -1)
			random_dir_x = True

		if self.top_paddle.is_collision(ball):
			ball.set_direction(0, 1)
			random_dir_x = True

		if self.board.is_bottom_wall_collision(ball):
			print("punkt dla gracz1")
			self.new_game(1)
			return

		if self.board.is_top_wall_collision(ball):
			print("punkt dla gracz2")
			self.new_game(2)
			return

		if random_dir_x:
			if self.board.is_right_wall_collision(ball):
				ball.set_direction(random.choice([-1, 0]), None)

			elif self.board.is_left_wall_collision(ball):
				ball.set_direction(random.choice([0, 1]), None)

			else:
				ball.set_direction(random.choice([-1, 0, 1]), None)

		self.ball.move()

	def top_paddle_move(self, dir_x):
		self.top_paddle.move(dir_x, self.board.width)

	def bottom_paddle_move(self, dir_x):
		self.bottom_paddle.move(dir_x, self.board.width)

	def new_game(self, starting_player_id: int = 1):
		assert starting_player_id in (1, 2), f"Invalid starting player id: {starting_player}"

		self.game_started = False

		if starting_player_id == 1:
			self.ball.set_pos(self.board.center_x, self.top_paddle.y + 1)
			self.ball.set_direction(0, 1)

		elif starting_player_id == 2:
			self.ball.set_pos(self.board.center_x, self.bottom_paddle.y - 1)
			self.ball.set_direction(0, -1)

	def start_game(self):
		self.game_started = True


class PongDisplay:

	def __init__(self, pong_game: PongGame):
		self.pong_game = pong_game

	def draw(self):
		pong_game = self.pong_game

		for i in range(pong_game.board.height):
			line = []
			for j in range(pong_game.board.width):
				if (pong_game.top_paddle.x <= j <= (pong_game.top_paddle.x + pong_game.top_paddle.width - 1) and (i == pong_game.top_paddle.y)):
					line.append("=")
				elif (pong_game.bottom_paddle.x <= j <= (pong_game.bottom_paddle.x + pong_game.bottom_paddle.width - 1) and (i == pong_game.bottom_paddle.y)):
					line.append("=")
				elif (j == pong_game.ball.x and i == pong_game.ball.y):
					line.append("O")
				else:
					line.append(" ")

			print(" | ".join(line))

		print("")


if __name__ == "__main__":
	pygame.init()
	pygame.key.set_repeat(400)

	pong = PongGame(width=5, height=6)
	pong.new_game(2)
	disp = PongDisplay(pong)

	start_time = time.time()

	while True:
		for event in pygame.event.get(2):
			
			if event.key == pygame.K_q:
				pong.top_paddle_move(-1)

			if event.key == pygame.K_w:
				pong.top_paddle_move(1)

			if event.key == pygame.K_o:
				pong.bottom_paddle_move(-1)

			if event.key == pygame.K_p:
				pong.bottom_paddle_move(1)

			if event.key == pygame.K_SPACE:
				pong.start_game()

			if event.key == pygame.K_ESCAPE:
				sys.exit(0)

			disp.draw()

		if time.time() - start_time >= 1.0:
			start_time = time.time()

			pong.process()
			disp.draw()

		time.sleep(0.05)
