import cv2
import mediapipe as mp
import pygame
import sys

pygame.init()

# =========================
# WINDOW
# =========================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AirPuzzle")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
RED = (220, 50, 50)
BLUE = (60, 120, 220)
GREEN = (60, 180, 100)
GRAY = (200, 200, 200)
YELLOW = (255, 200, 50)

# =========================
# BOARD
# =========================

BOARD_X = 150
BOARD_Y = 80

CELL = 80
ROWS = 5
COLS = 6

board_rect = pygame.Rect(
    BOARD_X,
    BOARD_Y,
    COLS * CELL,
    ROWS * CELL
)

# =========================
# FONTS
# =========================

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)
small_font = pygame.font.Font(None, 28)

# =========================
# LEVEL DATA
# =========================

levels = [

    # LEVEL 1
    {
        "player": (0, 0),
        "exit": (5, 2),
        "blocks": [
            (2, 0),
            (3, 1),
            (1, 2),
            (4, 2)
        ]
    },

    # LEVEL 2
    {
        "player": (0, 4),
        "exit": (5, 0),
        "blocks": [
            (1, 3),
            (2, 3),
            (3, 1),
            (4, 1),
            (3, 3)
        ]
    },

    # LEVEL 3
    {
        "player": (0, 2),
        "exit": (5, 2),
        "blocks": [
            (1, 1),
            (1, 3),
            (2, 1),
            (2, 3),
            (3, 1),
            (3, 3),
            (4, 0),
            (4, 4)
        ]
    }
]

# =========================
# GAME VARIABLES
# =========================

current_level = 0

moves = 0
score = 0

won = False
game_complete = False

dragging = False
pinching = False

offset_x = 0
offset_y = 0

missing_hand_frames = 0
MAX_MISSING_HAND_FRAMES = 5

cursor_x = WIDTH // 2
cursor_y = HEIGHT // 2

smooth_x = cursor_x
smooth_y = cursor_y

SMOOTHING = 0.22

# Pinch hysteresis: prevents accidental grab/release
PINCH_ON_THRESHOLD = 50
PINCH_OFF_THRESHOLD = 62

# Small movement steps prevent the player from jumping through blocks
MAX_MOVE_STEP = 6

# =========================
# LEVEL OBJECTS
# =========================

player = None
blocks = []
exit_rect = None


def load_level():

    global player
    global blocks
    global exit_rect
    global won
    global dragging
    global pinching
    global moves

    level = levels[current_level]

    # Player
    px, py = level["player"]

    player = pygame.Rect(
        BOARD_X + px * CELL,
        BOARD_Y + py * CELL,
        CELL,
        CELL
    )

    # Exit
    ex, ey = level["exit"]

    exit_rect = pygame.Rect(
        BOARD_X + ex * CELL,
        BOARD_Y + ey * CELL,
        CELL,
        CELL
    )

    # Blocks
    blocks = []

    for bx, by in level["blocks"]:

        block = pygame.Rect(
            BOARD_X + bx * CELL,
            BOARD_Y + by * CELL,
            CELL,
            CELL
        )

        blocks.append(block)

    won = False
    dragging = False
    pinching = False
    missing_hand_frames = 0

    moves = 0


def is_valid_position(rect):

    if not board_rect.contains(rect):
        return False

    for block in blocks:

        if rect.colliderect(block):
            return False

    return True


def move_player_safely(target_x, target_y):
    """Move in small steps so the player cannot tunnel through blocks."""
    global player

    dx = target_x - player.x
    dy = target_y - player.y
    distance = max(abs(dx), abs(dy))

    if distance == 0:
        return

    steps = max(1, int(distance / MAX_MOVE_STEP))

    for i in range(1, steps + 1):
        nx = round(player.x + dx * i / steps)
        ny = round(player.y + dy * i / steps)
        test_rect = pygame.Rect(nx, ny, CELL, CELL)

        if is_valid_position(test_rect):
            player.x = nx
            player.y = ny
        else:
            # Try moving on each axis separately, but never through a block.
            test_x = pygame.Rect(nx, player.y, CELL, CELL)
            if is_valid_position(test_x):
                player.x = nx

            test_y = pygame.Rect(player.x, ny, CELL, CELL)
            if is_valid_position(test_y):
                player.y = ny


def snap_to_grid(rect):

    col = round(
        (rect.x - BOARD_X) / CELL
    )

    row = round(
        (rect.y - BOARD_Y) / CELL
    )

    col = max(
        0,
        min(COLS - 1, col)
    )

    row = max(
        0,
        min(ROWS - 1, row)
    )

    return pygame.Rect(
        BOARD_X + col * CELL,
        BOARD_Y + row * CELL,
        CELL,
        CELL
    )


def next_level():

    global current_level
    global game_complete
    global score

    if current_level < len(levels) - 1:

        current_level += 1

        score += 100

        load_level()

    else:

        score += 100

        game_complete = True


def restart_game():

    global current_level
    global score
    global game_complete

    current_level = 0
    score = 0
    game_complete = False

    load_level()


# =========================
# LOAD FIRST LEVEL
# =========================

load_level()

# =========================
# MEDIAPIPE
# =========================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.50,
    min_tracking_confidence=0.60
)

# =========================
# CAMERA
# =========================

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():

    print("Camera open nahi ho raha.")
    sys.exit()

print("================================")
print("       AIRPUZZLE")
print("================================")
print("☝️ Move index finger")
print("🤏 Pinch to grab")
print("🖐️ Move hand")
print("R = Restart")
print("Q = Quit")
print("================================")

# =========================
# MAIN LOOP
# =========================

running = True

while running:

    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                restart_game()

            if event.key == pygame.K_q:

                running = False

    # =========================
    # CAMERA
    # =========================

    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    camera_h, camera_w, _ = frame.shape

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    # =========================
    # HAND DETECTION
    # =========================

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        index = hand.landmark[8]
        thumb = hand.landmark[4]

        # -------------------------
        # SMOOTH CURSOR
        # -------------------------

        # -------------------------
        # HAND -> BOARD MAPPING
        # -------------------------
        # Use only the board area for hand control.
        # This makes the red block easier to control.
        hand_x = max(0.08, min(0.92, index.x))
        hand_y = max(0.08, min(0.92, index.y))

        hand_x = (hand_x - 0.08) / 0.84
        hand_y = (hand_y - 0.08) / 0.84

        raw_x = int(
            BOARD_X + hand_x * (COLS * CELL)
        )

        raw_y = int(
            BOARD_Y + hand_y * (ROWS * CELL)
        )

        smooth_x = (
            smooth_x * (1 - SMOOTHING)
            + raw_x * SMOOTHING
        )

        smooth_y = (
            smooth_y * (1 - SMOOTHING)
            + raw_y * SMOOTHING
        )

        cursor_x = int(smooth_x)
        cursor_y = int(smooth_y)

        cursor_x = max(
            0,
            min(WIDTH - 1, cursor_x)
        )

        cursor_y = max(
            0,
            min(HEIGHT - 1, cursor_y)
        )

        # -------------------------
        # PINCH
        # -------------------------

        index_x = int(
            index.x * camera_w
        )

        index_y = int(
            index.y * camera_h
        )

        thumb_x = int(
            thumb.x * camera_w
        )

        thumb_y = int(
            thumb.y * camera_h
        )

        distance = (
            (index_x - thumb_x) ** 2
            +
            (index_y - thumb_y) ** 2
        ) ** 0.5

        if pinching:
            new_pinching = distance < PINCH_OFF_THRESHOLD
        else:
            new_pinching = distance < PINCH_ON_THRESHOLD

        # =========================
        # GRAB
        # =========================

        if not won and not game_complete:

            if new_pinching and not dragging:

                if player.collidepoint(
                    cursor_x,
                    cursor_y
                ):

                    dragging = True

                    offset_x = (
                        player.centerx - cursor_x
                    )

                    offset_y = (
                        player.centery - cursor_y
                    )

            # =========================
            # MOVE
            # =========================

            if dragging and new_pinching:

                new_x = int(
                    cursor_x
                    + offset_x
                    - CELL / 2
                )

                new_y = int(
                    cursor_y
                    + offset_y
                    - CELL / 2
                )

                new_player = pygame.Rect(
                    new_x,
                    new_y,
                    CELL,
                    CELL
                )

                move_player_safely(
                    new_player.x,
                    new_player.y
                )

            # =========================
            # RELEASE
            # =========================

            if dragging and not new_pinching:

                dragging = False

                snapped = snap_to_grid(player)

                # Snap to the nearest valid grid cell.
                if is_valid_position(snapped):
                    if snapped.x != player.x or snapped.y != player.y:
                        moves += 1
                    player = snapped
                else:
                    best = None
                    best_dist = float("inf")

                    for row in range(ROWS):
                        for col in range(COLS):
                            candidate = pygame.Rect(
                                BOARD_X + col * CELL,
                                BOARD_Y + row * CELL,
                                CELL,
                                CELL
                            )
                            if is_valid_position(candidate):
                                d = abs(candidate.x - player.x) + abs(candidate.y - player.y)
                                if d < best_dist:
                                    best = candidate
                                    best_dist = d

                    if best is not None:
                        if best.x != player.x or best.y != player.y:
                            moves += 1
                        player = best

        pinching = new_pinching
        missing_hand_frames = 0

    else:

        missing_hand_frames += 1

        if missing_hand_frames <= MAX_MISSING_HAND_FRAMES:
            pass
        else:
            pinching = False

        if dragging and missing_hand_frames > MAX_MISSING_HAND_FRAMES:

            dragging = False

            snapped = snap_to_grid(player)

            if is_valid_position(snapped):
                player = snapped
            else:
                # Return to the nearest valid grid cell.
                best = None
                best_dist = float("inf")
                for row in range(ROWS):
                    for col in range(COLS):
                        candidate = pygame.Rect(
                            BOARD_X + col * CELL,
                            BOARD_Y + row * CELL,
                            CELL,
                            CELL
                        )
                        if is_valid_position(candidate):
                            d = abs(candidate.x - player.x) + abs(candidate.y - player.y)
                            if d < best_dist:
                                best = candidate
                                best_dist = d
                if best is not None:
                    player = best

    # =========================
    # WIN DETECTION
    # =========================

    if not won and not game_complete:

        if player.colliderect(exit_rect):

            won = True

            score += max(
                10,
                100 - moves * 5
            )

            dragging = False

    # =========================
    # DRAW
    # =========================

    screen.fill(WHITE)

    # =========================
    # TITLE
    # =========================

    title = font.render(
        "AIRPUZZLE",
        True,
        BLACK
    )

    screen.blit(
        title,
        (BOARD_X, 20)
    )

    # =========================
    # LEVEL / SCORE / MOVES
    # =========================

    level_text = small_font.render(
        f"Level: {current_level + 1}",
        True,
        BLACK
    )

    screen.blit(
        level_text,
        (500, 25)
    )

    score_text = small_font.render(
        f"Score: {score}",
        True,
        BLACK
    )

    screen.blit(
        score_text,
        (600, 25)
    )

    moves_text = small_font.render(
        f"Moves: {moves}",
        True,
        BLACK
    )

    screen.blit(
        moves_text,
        (20, 55)
    )

    # =========================
    # GRID
    # =========================

    for row in range(ROWS):

        for col in range(COLS):

            x = BOARD_X + col * CELL
            y = BOARD_Y + row * CELL

            pygame.draw.rect(
                screen,
                GRAY,
                (x, y, CELL, CELL),
                2
            )

    # =========================
    # EXIT
    # =========================

    pygame.draw.rect(
        screen,
        GREEN,
        exit_rect
    )

    exit_text = font.render(
        "EXIT",
        True,
        WHITE
    )

    screen.blit(
        exit_text,
        (
            exit_rect.x + 8,
            exit_rect.y + 22
        )
    )

    # =========================
    # BLUE BLOCKS
    # =========================

    for block in blocks:

        pygame.draw.rect(
            screen,
            BLUE,
            block
        )

    # =========================
    # RED BLOCK
    # =========================

    pygame.draw.rect(
        screen,
        RED,
        player
    )

    # =========================
    # CURSOR
    # =========================

    cursor_color = (
        YELLOW if pinching else RED
    )

    pygame.draw.circle(
        screen,
        cursor_color,
        (
            cursor_x,
            cursor_y
        ),
        10
    )

    # =========================
    # STATUS
    # =========================

    if game_complete:

        status = "GAME COMPLETE!"

    elif won:

        status = "LEVEL COMPLETE!"

    elif dragging:

        status = "GRABBING"

    elif pinching:

        status = "PINCH"

    else:

        status = "MOVE FINGER"

    status_text = font.render(
        status,
        True,
        BLACK
    )

    screen.blit(
        status_text,
        (20, HEIGHT - 75)
    )

    # =========================
    # LEVEL COMPLETE
    # =========================

    if won and not game_complete:

        overlay = pygame.Surface(
            (WIDTH, 150),
            pygame.SRCALPHA
        )

        overlay.fill(
            (255, 255, 255, 235)
        )

        screen.blit(
            overlay,
            (0, HEIGHT // 2 - 75)
        )

        complete_text = big_font.render(
            "LEVEL COMPLETE!",
            True,
            GREEN
        )

        screen.blit(
            complete_text,
            (
                WIDTH // 2
                - complete_text.get_width() // 2,
                HEIGHT // 2 - 50
            )
        )

        next_text = small_font.render(
            "Press SPACE for next level",
            True,
            BLACK
        )

        screen.blit(
            next_text,
            (
                WIDTH // 2
                - next_text.get_width() // 2,
                HEIGHT // 2 + 25
            )
        )

    # =========================
    # GAME COMPLETE
    # =========================

    if game_complete:

        overlay = pygame.Surface(
            (WIDTH, 200),
            pygame.SRCALPHA
        )

        overlay.fill(
            (255, 255, 255, 240)
        )

        screen.blit(
            overlay,
            (0, HEIGHT // 2 - 100)
        )

        complete_text = big_font.render(
            "YOU FINISHED!",
            True,
            GREEN
        )

        screen.blit(
            complete_text,
            (
                WIDTH // 2
                - complete_text.get_width() // 2,
                HEIGHT // 2 - 65
            )
        )

        final_score = font.render(
            f"Final Score: {score}",
            True,
            BLACK
        )

        screen.blit(
            final_score,
            (
                WIDTH // 2
                - final_score.get_width() // 2,
                HEIGHT // 2 + 5
            )
        )

        restart_text = small_font.render(
            "Press R to play again",
            True,
            BLACK
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2
                - restart_text.get_width() // 2,
                HEIGHT // 2 + 45
            )
        )

    # =========================
    # NEXT LEVEL
    # =========================

    keys = pygame.key.get_pressed()

    if won and not game_complete:

        if keys[pygame.K_SPACE]:

            next_level()

            pygame.time.wait(250)

    # =========================
    # DISPLAY
    # =========================

    pygame.display.flip()

    clock.tick(60)

# =========================
# CLEANUP
# =========================

cap.release()
hands.close()

pygame.quit()
cv2.destroyAllWindows()

sys.exit()