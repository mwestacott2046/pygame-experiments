import pygame

CLOCK_RATE = 200

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
LINE_THICKNESS = 5
PADDLE_SIZE = 70
PADDLE_WIDTH = 12
PADDLE_OFFSET = 30
PLAYER_SPEED = 3
AI_SPEED = 2
BALL_SIZE = 20
SERVE_SPEED = 2


class PlayerControls:
    player1_up_pressed = False
    player1_down_pressed = False
    player2_up_pressed = False
    player2_down_pressed = False
    serve_pressed = False
    quit_pressed = False


def draw_arena(game_screen):
    game_screen.fill(BLACK)
    pygame.draw.line(game_screen, WHITE, (0, 0), (SCREEN_WIDTH, 0), LINE_THICKNESS)
    pygame.draw.line(game_screen, WHITE, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), LINE_THICKNESS)
    pygame.draw.line(game_screen, WHITE, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT), 2)


def draw_paddle(game_screen, paddle):
    pygame.draw.rect(game_screen, WHITE, paddle)


def draw_ball(game_screen, ball_position):
    pygame.draw.rect(game_screen, WHITE, ball_position)


def move_ball(ball, ball_direction_x, ball_direction_y):
    ball.x += ball_direction_x
    ball.y += ball_direction_y
    return ball


def side_collision(ball, ball_direction_x, ball_direction_y):
    if ball.top <= LINE_THICKNESS or ball.bottom >= (SCREEN_HEIGHT - LINE_THICKNESS):
        ball_direction_y = ball_direction_y * -1

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_direction_x = ball_direction_x * -1

    return ball_direction_x, ball_direction_y


def score_collision(ball, ball_direction_x, ball_direction_y):
    if ball.left <= 0:
        return 2    # player 2 scored
    elif ball.right >= SCREEN_WIDTH:
        return 1    # player 1 scored

    return 0


def move_paddle(player_position, up_pressed, down_pressed):
    if up_pressed and player_position > 0:
        player_position -= PLAYER_SPEED

    if down_pressed and player_position < SCREEN_HEIGHT:
        player_position += PLAYER_SPEED

    return player_position


def check_ball_paddle_collision(ball, player1_paddle, player2_paddle, ball_direction_x):
    if ball_direction_x < 0 and player1_paddle.right >= ball.left and player1_paddle.left > ball.left and ball.top < player1_paddle.bottom and ball.bottom > player1_paddle.top:
        return -1
    elif ball_direction_x > 0 and ball.right >= player2_paddle.left and player2_paddle.right <= ball.right and ball.top < player2_paddle.bottom and ball.bottom > player2_paddle.top:
        return -1
    else:
        return 1


def ai_player(ball, ball_direction_x, paddle, flip):
    if flip:
        ball_direction_x = ball_direction_x * -1

    if ball_direction_x < 0:
        if paddle.centery < (SCREEN_HEIGHT / 2):
            paddle.y += AI_SPEED
        elif paddle.centery > (SCREEN_HEIGHT / 2):
            paddle.y -= AI_SPEED

    elif ball_direction_x > 0:
        if paddle.centery < ball.centery:
            paddle.y += AI_SPEED
        else:
            paddle.y -= AI_SPEED

    return paddle


def process_game_events(player_controls):
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            player_controls.quit_pressed = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            # print("User pressed a key.", event.key)
            if event.key == 113:
                player_controls.player1_up_pressed = True
            elif event.key == 97:
                player_controls.player1_down_pressed = True
            elif event.key == 112:
                player_controls.player2_up_pressed = True
            elif event.key == 108:
                player_controls.player2_down_pressed = True
            elif event.key == 32:
                player_controls.serve_pressed = True
        elif event.type == pygame.KEYUP:
            # print("User let go of a key.", event.key)
            if event.key == 113:
                player_controls.player1_up_pressed = False
            elif event.key == 97:
                player_controls.player1_down_pressed = False
            elif event.key == 112:
                player_controls.player2_up_pressed = False
            elif event.key == 108:
                player_controls.player2_down_pressed = False
            elif event.key == 32:
                player_controls.serve_pressed = False
    return player_controls


def draw_score(game_screen, player1_score, player2_score):
    font = pygame.font.SysFont(None, 64)
    score1 = font.render(str(player1_score), True, WHITE)
    game_screen.blit(score1, (20, 20))
    score2 = font.render(str(player2_score), True, WHITE)
    game_screen.blit(score2, (SCREEN_WIDTH - 80, 20))


def main():
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.init()
    game_screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")
    pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()

    # Game loop init
    player1_is_ai = False
    player2_is_ai = False
    player1_score = 0
    player2_score = 0

    controls = PlayerControls()
    score_counted = False

    serving_player = 1
    player1_position = (SCREEN_HEIGHT - PADDLE_SIZE) / 2
    player2_position = (SCREEN_HEIGHT - PADDLE_SIZE) / 2
    ball = pygame.Rect(PADDLE_OFFSET + LINE_THICKNESS, SCREEN_HEIGHT / 2, BALL_SIZE, BALL_SIZE)
    ball_direction_x = 0
    ball_direction_y = 0

    player1_paddle = pygame.Rect(PADDLE_OFFSET, player1_position, PADDLE_WIDTH, PADDLE_SIZE)
    player2_paddle = pygame.Rect(SCREEN_WIDTH - PADDLE_OFFSET, player2_position, PADDLE_WIDTH, PADDLE_SIZE)

    # -------- Main Program Loop -----------
    while not controls.quit_pressed:

        controls = process_game_events(controls)

        if ball_direction_x == 0:
            if controls.serve_pressed:
                score_counted = False
                if serving_player == 1:
                    ball_direction_x = SERVE_SPEED
                    ball_direction_y = SERVE_SPEED
                else:
                    ball_direction_x = SERVE_SPEED * -1
                    ball_direction_y = SERVE_SPEED * -1
            else:
                if serving_player == 1:
                    ball.y = ((PADDLE_SIZE // 2) - BALL_SIZE / 2) + player1_paddle.top
                else:
                    ball.y = ((PADDLE_SIZE // 2) - BALL_SIZE / 2) + player2_paddle.top

        ball_direction_x, ball_direction_y = side_collision(ball, ball_direction_x, ball_direction_y)
        player_scored = score_collision(ball, ball_direction_x, ball_direction_y)

        if player_scored == 0:
            # do score
            ball = move_ball(ball, ball_direction_x, ball_direction_y)

            if player1_is_ai:
                player1_paddle = ai_player(ball, ball_direction_x, player1_paddle, True)
            else:
                player1_paddle.y = move_paddle(player1_paddle.y, controls.player1_up_pressed, controls.player1_down_pressed)

            if player2_is_ai:
                player2_paddle = ai_player(ball, ball_direction_x, player2_paddle, False)
            else:
                player2_paddle.y = move_paddle(player2_paddle.y, controls.player2_up_pressed, controls.player2_down_pressed)

            direction_modifier = check_ball_paddle_collision(ball, player1_paddle, player2_paddle, ball_direction_x)
            ball_direction_x = ball_direction_x * direction_modifier

        else:
            if not score_counted:
                # print("Scored by player", player_scored)
                ball.y = SCREEN_HEIGHT / 2
                ball_direction_x = 0
                ball_direction_y = 0

                # deal with score
                if player_scored == 1:
                    player1_score += 1
                    ball.x = SCREEN_WIDTH - (PADDLE_OFFSET + ball.width)
                    serving_player = 2
                elif player_scored == 2:
                    player2_score += 1
                    ball.x = PADDLE_OFFSET + PADDLE_WIDTH
                    serving_player = 1

                # print("Player 1:", player1_score, " Player 2:", player2_score)
                score_counted = True

        draw_arena(game_screen)
        draw_paddle(game_screen, player1_paddle)
        draw_paddle(game_screen, player2_paddle)
        draw_ball(game_screen, ball)

        draw_score(game_screen, player1_score, player2_score)

        # flip and wait
        pygame.display.flip()
        clock.tick(CLOCK_RATE)

    pygame.quit()


if __name__ == '__main__':
    main()
