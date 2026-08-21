import pygame
import math
import threading
import time
import os
import random
import json
from datetime import datetime

pygame.init()
pygame.mixer.init()

clock_font = pygame.font.SysFont("Courier New", 27)

WIDTH, HEIGHT = 1500, 1000 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DJ The AI")
clock = pygame.time.Clock()

# Directory Paths. (Default=kadok) Switch with the path of your computer or custom file location.
sounds_dir = r'C:\Users\kadok\3D Objects\DJ the AI 2.0\files\sounds\speech'
music_dir = r'C:\Users\kadok\3D Objects\DJ the AI 2.0\files\sounds\music'
jokes_dir = r'C:\Users\kadok\3D Objects\DJ the AI 2.0\files\sounds\jokes'
memory_file = r'C:\Users\kadok\3D Objects\DJ the AI 2.0\files\v3.5\memory.json'
memoryalternate_file = r'C:\Users\kadok\3D Objects\DJ the AI 2.0\files\v3.5\memoryalternate.json'
memoryalternate2_file = r'C:\Users\kadok\3D Objects\DJ the AI 2.0\files\v3.5\memoryalternate2.json'

# Replace kadok with your pc name. Switch "3D Objects" to where you would like to keep the file.
def load_memory():
    global memory, memoryalternate, memoryalternate2
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            memory = json.load(f)
    else:
        memory = {}
    if os.path.exists(memoryalternate_file):
        with open(memoryalternate_file, 'r') as f:
            memoryalternate = json.load(f)
    else:
        memoryalternate = {}
    if os.path.exists(memoryalternate2_file):
        with open(memoryalternate2_file, 'r') as f:
            memoryalternate2 = json.load(f)
    else:
        memoryalternate2 = {}

load_memory()

current_bg_color = (40, 40, 40)
target_bg_color = (100, 150, 200)
last_input_time = time.time()
audio_playing = threading.Event()
is_powered_on = True

idle_phrases = [
    ['did_female.wav','you_female.wav','leave_female.wav'],
    ['where_female.wav','did_female.wav','you_female.wav','go_female.wav'],
    ['talk_female.wav','to_female.wav','me_female.wav'],
    ['i_female.wav','think_female.wav','it_female.wav','is_female.wav','just_female.wav','me_female.wav','/then_female.wav'],
    ['is_female.wav','that_female.wav','you_female.wav','.like_female.wav','there_female.wav'],
    ['why_female.wav','are_female.wav','you_female.wav','not_female.wav','talk_female.wav','in_female.wav'],
    ['what_female.wav','are_female.wav','you_female.wav','do_female.wav','in_female.wav'],
    ['how_female.wav','was_female.wav','your_female.wav','day_female.wav'],
    ['how_female.wav','are_female.wav','you_female.wav','to_female.wav','day_female.wav'],
    ['i_female.wav','well_female.wav','just_female.wav','wait_female.wav','/here_female.wav','then_female.wav'],
    ['what_female.wav','would_female.wav','you_female.wav','like_female.wav','to_female.wav','do_female.wav'],
    ['are_female.wav','you_female.wav','there_female.wav'],
    ['what_female.wav','now_female.wav'],
    ['want_female.wav','music_female.wav'],
    ['do_female.wav','you_female.wav','want_female.wav','music_female.wav'],
    ['yo_female.wav'],
    ['yo_female.wav','are_female.wav','you_female.wav','there_female.wav'],
    ['yo_female.wav','are_female.wav','you_female.wav','here_female.wav'],
    ['are_female.wav','you_female.wav','here_female.wav'],
    ['what_female.wav','do_female.wav','we_female.wav','do_female.wav','now_female.wav'],
    ['what_female.wav','do_female.wav','we_female.wav','do_female.wav'],
    ['can_female.wav','you_female.wav','here_female.wav','me_female.wav'],
    ['can_female.wav','we_female.wav','play_female.wav','music_female.wav']
]

sounds = {
    'swear': [os.path.join(sounds_dir, 'that_female.wav'), os.path.join(sounds_dir, 'was_female.wav'), os.path.join(sounds_dir, 'mean_female.wav')],
    'swear_alternate': [os.path.join(sounds_dir, 'dont_female.wav'), os.path.join(sounds_dir, 'say_female.wav'), os.path.join(sounds_dir, 'that_female.wav')],
    'unknown': [os.path.join(sounds_dir, 'what_female.wav'), os.path.join(sounds_dir, 'now_female.wav')],
    'unknown_alternates': [
        [
            os.path.join(sounds_dir, 'what_female.wav'),
            os.path.join(sounds_dir, 'do_female.wav'),
            os.path.join(sounds_dir, 'you_female.wav'),
            os.path.join(sounds_dir, 'mean_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'i_female.wav'),
            os.path.join(sounds_dir, 'dont_female.wav'),
            os.path.join(sounds_dir, 'think_female.wav'),
            os.path.join(sounds_dir, 'i_female.wav'),
            os.path.join(sounds_dir, 'understand_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'okay_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'what_female.wav'),
            os.path.join(sounds_dir, 'now_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'is_female.wav'),
            os.path.join(sounds_dir, 'that_female.wav'),
            os.path.join(sounds_dir, 'good2_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'is_female.wav'),
            os.path.join(sounds_dir, 'that_female.wav'),
            os.path.join(sounds_dir, 'and_female.wav'),
            os.path.join(sounds_dir, 'good2_female.wav'),
            os.path.join(sounds_dir, 'thing_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'letskeepitsimple_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'letskeeptheconversationsimple_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'wow_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'okay_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'i_female.wav'),
            os.path.join(sounds_dir, 'dont_female.wav'),
            os.path.join(sounds_dir, 'understand_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'sorry_female.wav'),
            os.path.join(sounds_dir, 'but_female.wav'),
            os.path.join(sounds_dir, 'i_female.wav'),
            os.path.join(sounds_dir, 'dont_female.wav'),
            os.path.join(sounds_dir, 'understand_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'what_female.wav'),
            os.path.join(sounds_dir, 'now_female.wav'),
        ],
        [
            os.path.join(sounds_dir, 'sorry_female.wav'),
            os.path.join(sounds_dir, 'but_female.wav'),
            os.path.join(sounds_dir, 'i_female.wav'),
            os.path.join(sounds_dir, 'do_female.wav'),
            os.path.join(sounds_dir, 'not_female.wav'),
            os.path.join(sounds_dir, 'understand_female.wav')
        ],
        [
            os.path.join(sounds_dir, 'what_female.wav'),
            os.path.join(sounds_dir, 'is_female.wav'),
            os.path.join(sounds_dir, 'that_female.wav')
        ]
    ]
}

def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def play_sound(file):
    global last_input_time
    try:
        stop_music()
        sound = pygame.mixer.Sound(file)
        audio_playing.set()
        channel = sound.play()
        while channel.get_busy():
            time.sleep(0.1)
        audio_playing.clear()
        last_input_time = time.time()
    except:
        pass

def play_music():
    def music_thread():
        if not pygame.mixer.music.get_busy():
            files = os.listdir(music_dir)
            if files:
                filename = random.choice(files)
                pygame.mixer.music.load(os.path.join(music_dir, filename))
                pygame.mixer.music.play()
                print("Playing music:", filename)
    threading.Thread(target=music_thread, daemon=True).start()

def draw_animation(time_elapsed, pause=False):
    global current_bg_color, target_bg_color, last_robot_pos
    fade_speed = 0.2
    r = int(current_bg_color[0] + (target_bg_color[0] - current_bg_color[0]) * fade_speed)
    g = int(current_bg_color[1] + (target_bg_color[1] - current_bg_color[1]) * fade_speed)
    b = int(current_bg_color[2] + (target_bg_color[2] - current_bg_color[2]) * fade_speed)
    current_bg_color = (r, g, b)

    screen.fill(current_bg_color)

    def get_color_cycle(t):
        r = int(127 * (math.sin(t) + 1))
        g = int(127 * (math.sin(t + 2 * math.pi / 3) + 1))
        b = int(127 * (math.sin(t + 4 * math.pi / 3) + 1))
        return (r, g, b)

    def draw_visualizer(time_elapsed, amplitude=1.0):
        ring_radius = 150 + amplitude * 50
        color = get_color_cycle(time_elapsed)
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, 50), (WIDTH//2, HEIGHT//2), int(ring_radius), 8)
        screen.blit(surface, (0, 0))

    if pygame.mixer.music.get_busy():
        amplitude = abs(math.sin(time.time() * 2))
    else:
        amplitude = 0
    draw_visualizer(time_elapsed, amplitude)

    if pause:
        # dj paused
        x_center, y_center = WIDTH // 2, HEIGHT // 2
    else:
        # dj unpaused
        bob = math.sin(time_elapsed * 3) * 8
        x_center = WIDTH // 2
        y_center = HEIGHT // 2 + bob

    last_robot_pos = (x_center, y_center + 45)

    body_rect = pygame.Rect(0, 0, 90, 100)
    body_rect.center = (x_center, y_center + 45)
    pygame.draw.rect(screen, (170, 180, 195), body_rect, border_radius=12)
    pygame.draw.rect(screen, (20, 20, 20), body_rect, 3, border_radius=12)

    head_rect = pygame.Rect(0, 0, 80, 70)
    head_rect.center = (x_center, y_center - 35)
    pygame.draw.rect(screen, (190, 200, 215), head_rect, border_radius=10)
    pygame.draw.rect(screen, (30, 30, 30), head_rect, 3, border_radius=10)

    pygame.draw.circle(screen, (255, 172, 200), (x_center - 18, int(y_center - 40)), 6)
    pygame.draw.circle(screen, (255, 172, 200), (x_center + 18, int(y_center - 40)), 6)
    pygame.draw.circle(screen, (0, 5, 6), (x_center - 18, int(y_center - 40)), 4)
    pygame.draw.circle(screen, (0, 5, 6), (x_center + 18, int(y_center - 40)), 4)

    mouth_speed = 25
    mouth_amount = 8
    if audio_playing.is_set():
        mouth_open = abs(math.sin(time_elapsed * mouth_speed)) * mouth_amount
    else:
        mouth_open = 2
    mouth_x = x_center
    mouth_y = int(y_center - 15)
    if mouth_open < 1.5:
        pygame.draw.line(screen, (90, 70, 70),
                         (mouth_x - 15, mouth_y),
                         (mouth_x + 15, mouth_y), 3)
    else:
        mouth_rect = pygame.Rect(
            mouth_x - 15,
            mouth_y - int(mouth_open / 2),
            30,
            int(mouth_open)
        )
        pygame.draw.ellipse(screen, (40, 20, 20), mouth_rect)
        pygame.draw.ellipse(screen, (90, 70, 70), mouth_rect, 2)

    pygame.draw.line(screen, (255, 0, 0),
                     (x_center, int(y_center - 70)),
                     (x_center, int(y_center - 90)), 3)
    pygame.draw.circle(screen, (255, 70, 70),
                       (x_center, int(y_center - 95)), 5)

    pygame.draw.line(screen, (120, 120, 120),
                     (body_rect.left, body_rect.top + 25),
                     (body_rect.left - 25, body_rect.top + 45), 5)
    pygame.draw.line(screen, (120, 120, 120),
                     (body_rect.right, body_rect.top + 25),
                     (body_rect.right + 25, body_rect.top + 45), 5)
    pygame.draw.circle(screen, (90, 90, 90),
                       (body_rect.left - 25, body_rect.top + 45), 6)
    pygame.draw.circle(screen, (90, 90, 90),
                       (body_rect.right + 25, body_rect.top + 45), 6)

    pygame.draw.line(screen, (120, 120, 120),
                     (x_center - 18, body_rect.bottom),
                     (x_center - 18, body_rect.bottom + 35), 5)
    pygame.draw.line(screen, (120, 120, 120),
                     (x_center + 18, body_rect.bottom),
                     (x_center + 18, body_rect.bottom + 35), 5)
    pygame.draw.line(screen, (80, 80, 80),
                     (x_center - 30, body_rect.bottom + 35),
                     (x_center - 5, body_rect.bottom + 35), 5)
    pygame.draw.line(screen, (80, 80, 80),
                     (x_center + 5, body_rect.bottom + 35),
                     (x_center + 30, body_rect.bottom + 35), 5)

    return last_robot_pos
    bob = math.sin(time_elapsed * 3) * 8
    x_center = WIDTH // 2
    y_center = HEIGHT // 2 + bob

    last_robot_pos = (x_center, y_center + 45)  
    body_rect = pygame.Rect(0, 0, 90, 100)
    body_rect.center = (x_center, y_center + 45)
    pygame.draw.rect(screen, (170, 180, 195), body_rect, border_radius=12)
    pygame.draw.rect(screen, (20, 20, 20), body_rect, 3, border_radius=12)

    head_rect = pygame.Rect(0, 0, 80, 70)
    head_rect.center = (x_center, y_center - 35)
    pygame.draw.rect(screen, (190, 200, 215), head_rect, border_radius=10)
    pygame.draw.rect(screen, (30, 30, 30), head_rect, 3, border_radius=10)

    pygame.draw.circle(screen, (255, 172, 200), (x_center - 18, int(y_center - 40)), 6)
    pygame.draw.circle(screen, (255, 172, 200), (x_center + 18, int(y_center - 40)), 6)
    pygame.draw.circle(screen, (0, 5, 6), (x_center - 18, int(y_center - 40)), 4)
    pygame.draw.circle(screen, (0, 5, 6), (x_center + 18, int(y_center - 40)), 4)

    mouth_speed = 25
    mouth_amount = 8
    if audio_playing.is_set():
        mouth_open = abs(math.sin(time_elapsed * mouth_speed)) * mouth_amount
    else:
        mouth_open = 2
    mouth_x = x_center
    mouth_y = int(y_center - 15)
    if mouth_open < 1.5:
        pygame.draw.line(screen, (90, 70, 70),
                         (mouth_x - 15, mouth_y),
                         (mouth_x + 15, mouth_y), 3)
    else:
        mouth_rect = pygame.Rect(
            mouth_x - 15,
            mouth_y - int(mouth_open / 2),
            30,
            int(mouth_open)
        )
        pygame.draw.ellipse(screen, (40, 20, 20), mouth_rect)
        pygame.draw.ellipse(screen, (90, 70, 70), mouth_rect, 2)

    pygame.draw.line(screen, (255, 0, 0),
                     (x_center, int(y_center - 70)),
                     (x_center, int(y_center - 90)), 3)
    pygame.draw.circle(screen, (255, 70, 70),
                       (x_center, int(y_center - 95)), 5)

    pygame.draw.line(screen, (120, 120, 120),
                     (body_rect.left, body_rect.top + 25),
                     (body_rect.left - 25, body_rect.top + 45), 5)
    pygame.draw.line(screen, (120, 120, 120),
                     (body_rect.right, body_rect.top + 25),
                     (body_rect.right + 25, body_rect.top + 45), 5)
    pygame.draw.circle(screen, (90, 90, 90),
                       (body_rect.left - 25, body_rect.top + 45), 6)
    pygame.draw.circle(screen, (90, 90, 90),
                       (body_rect.right + 25, body_rect.top + 45), 6)

    pygame.draw.line(screen, (120, 120, 120),
                     (x_center - 18, body_rect.bottom),
                     (x_center - 18, body_rect.bottom + 35), 5)
    pygame.draw.line(screen, (120, 120, 120),
                     (x_center + 18, body_rect.bottom),
                     (x_center + 18, body_rect.bottom + 35), 5)
    pygame.draw.line(screen, (80, 80, 80),
                     (x_center - 30, body_rect.bottom + 35),
                     (x_center - 5, body_rect.bottom + 35), 5)
    pygame.draw.line(screen, (80, 80, 80),
                     (x_center + 5, body_rect.bottom + 35),
                     (x_center + 30, body_rect.bottom + 35), 5)

    return last_robot_pos

strokes = []

def add_stroke(points, color):
    strokes.append({'points': points.copy(), 'color': color})

def clear_strokes():
    strokes.clear()

def handle_command(user_input):
    global memory, memoryalternate, memoryalternate2, is_powered_on, current_music, last_input_time
    user_input=user_input.lower()

    if user_input == 'power on':
        for f in [os.path.join(sounds_dir, 'poweringon_female.wav'), os.path.join(sounds_dir, 'hello.wav')]:
            if os.path.exists(f):
                play_sound(f)
        is_powered_on=True
        print("Powered ON")
        return
    if user_input == 'power off':
        f=os.path.join(sounds_dir, 'poweringoff_female.wav')
        if os.path.exists(f):
            play_sound(f)
        is_powered_on=False
        print("Powered OFF")
        return

    if not is_powered_on:
        return

    if 'joke' in user_input:
        jokes = [
            os.path.join(jokes_dir, 'WhyDoYouNeverGiveBoomerangsAsGif_Female.wav'),
            os.path.join(jokes_dir, 'WhyWas10ScaredOfNineBecauseItWas_Female.wav'),
            os.path.join(jokes_dir, 'WhyDoAntsNeverGetSickBecauseThey_Female.wav'),
            os.path.join(jokes_dir, 'WhyDidThePancakeTakeADayOffWorkB_Female.wav'),
            os.path.join(jokes_dir, 'WhyCantDinosaursClapTheirHandsBe_Female.wav')
        ]
        play_sound(random.choice(jokes))
        return

    if 'music' in user_input:
        play_music()
        return

    files = os.listdir(music_dir)
    max_match_length = 0
    matched_files = []

    def normalize(text):
        return ''.join(c for c in text.lower() if c.isalnum() or c.isspace())

    clean_input = normalize(user_input)

    for f in files:
        name, ext = os.path.splitext(f)
        name_clean = normalize(name)

        if clean_input in name_clean:
            match_length = len(clean_input)
            filename_length = len(name_clean)
            if match_length >= 0.5 * filename_length:
                if filename_length > max_match_length:
                    max_match_length = filename_length
                    matched_files = [f]
                elif filename_length == max_match_length:
                    matched_files.append(f)

    if matched_files:
        chosen = random.choice(matched_files)
        pygame.mixer.music.load(os.path.join(music_dir, chosen))
        pygame.mixer.music.play()
        print("Playing:", chosen)
        return

    selected_memory=random.choice([memory,memoryalternate,memoryalternate2])
    detected=False
    for trigger,actions in selected_memory.items():
        if trigger in user_input:
            detected=True
            for action in actions:
                if action=='pause':
                    time.sleep(1)
                elif action.startswith('pause,'):
                    try:
                        pause_duration=int(action.split(',')[1])
                        time.sleep(pause_duration)
                    except:
                        pass
                elif '/' in action:
                    filename=os.path.join(sounds_dir, action.replace('/', ''))
                    if os.path.exists(filename):
                        play_sound(filename)
                else:
                    filename=os.path.join(sounds_dir, action)
                    if os.path.exists(filename):
                        play_sound(filename)
            break
    if not detected:
        if random.choice([True, False]):
            alt_list=random.choice(sounds['unknown_alternates'])
            for f in alt_list:
                if os.path.exists(f):
                    play_sound(f)
            return
        play_sound(sounds['unknown'][0])

def play_startup_sounds():
    for f in [os.path.join(sounds_dir, 'welcome.wav'), os.path.join(sounds_dir, 'hello.wav')]:
        if os.path.exists(f):
            play_sound(f)

def idle_monitor():
    global last_input_time
    while True:
        wait_time = random.uniform(15, 189)
        time.sleep(wait_time)
        if (
            not audio_playing.is_set()
            and not pygame.mixer.music.get_busy()
            and (time.time() - last_input_time) >= wait_time
            and is_powered_on
        ):
            phrase = random.choice(idle_phrases)
            for word in phrase:
                sound_file = os.path.join(sounds_dir, word)
                if os.path.exists(sound_file):
                    play_sound(sound_file)

def main():
    global current_bg_color, target_bg_color, last_robot_pos
    play_startup_sounds()
    time.sleep(2)

    if is_powered_on:
        target_bg_color = (100, 150, 200)
    else:
        target_bg_color = (10, 10, 10)
    current_bg_color = target_bg_color

    timestamp_path = "last_launch.txt"
    if os.path.exists(timestamp_path):
        with open(timestamp_path, 'r') as f:
            try:
                last_launch = datetime.fromisoformat(f.read().strip())
            except:
                last_launch = None
    else:
        last_launch = None
    with open(timestamp_path, 'w') as f:
        f.write(datetime.now().isoformat())

    threading.Thread(target=idle_monitor, daemon=True).start()

    animation_start = time.time()
    input_text = ""

    global clock_rect
    clock_rect = pygame.Rect(WIDTH - 170, 8, 160, 40)

    color_list = [
        (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
        (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 192, 203),
        (0, 255, 255)
    ]
    color_rects = []
    for idx, col in enumerate(color_list):
        rect = pygame.Rect(20 + idx*60, 10, 50, 40)
        color_rects.append(rect)

    pencil_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50)
    eraser_rect = pygame.Rect(WIDTH - 120, HEIGHT - 60, 50, 50)

    PAUSE_KEY = pygame.K_HOME

    drawing_points = []
    current_color = (0, 0, 0)
    drawing_mode = False
    pause_animation = False

    def draw_pause_indicator():
        if pause_animation:
            font = pygame.font.SysFont(None, 36)
            text_surf = font.render("Paused", True, (255, 0, 0))
            screen.blit(text_surf, (WIDTH//2 - text_surf.get_width()//2, HEIGHT//2 - text_surf.get_height()//2))

    while True:
        if is_powered_on:
            target_bg_color = (100, 150, 200)
        else:
            target_bg_color = (41, 35, 23)
        fade_speed = 0.2
        r = int(current_bg_color[0] + (target_bg_color[0] - current_bg_color[0]) * fade_speed)
        g = int(current_bg_color[1] + (target_bg_color[1] - current_bg_color[1]) * fade_speed)
        b = int(current_bg_color[2] + (target_bg_color[2] - current_bg_color[2]) * fade_speed)
        current_bg_color = (r, g, b)

        screen.fill(current_bg_color)

        if not pause_animation:
            robot_pos = draw_animation(time.time() - animation_start)
        else:
            robot_pos = draw_animation(time.time() - animation_start, pause=True)

        for stroke in strokes:
            pts = stroke['points']
            col = stroke['color']
            if len(pts) > 1:
                for i in range(len(pts) - 1):
                    start = (robot_pos[0] + pts[i][0], robot_pos[1] + pts[i][1])
                    end = (robot_pos[0] + pts[i+1][0], robot_pos[1] + pts[i+1][1])
                    pygame.draw.line(screen, col, start, end, 4)
            elif len(pts)==1:
                start = (robot_pos[0] + pts[0][0], robot_pos[1] + pts[0][1])
                pygame.draw.circle(screen, col, start, 4)

        for idx, rect in enumerate(color_rects):
            pygame.draw.rect(screen, (255,255,255), rect, 2)
            pygame.draw.rect(screen, color_list[idx], rect.inflate(-4,-4))
            if current_color == color_list[idx]:
                pygame.draw.rect(screen, (255,255,255), rect, 3)

        pygame.draw.rect(screen, (180,180,180), eraser_rect)
        pygame.draw.rect(screen, (50,50,50), eraser_rect.inflate(-10,-10))
        pygame.draw.line(screen, (0,0,0), (eraser_rect.left+10, eraser_rect.top+15),
                         (eraser_rect.right-10, eraser_rect.top+15), 2)

        pygame.draw.rect(screen, (200,180,50), pencil_rect)
        pygame.draw.polygon(
            screen,
            (150,75,0),
            [
                (pencil_rect.left+10, pencil_rect.top+10),
                (pencil_rect.left+30, pencil_rect.top+5),
                (pencil_rect.left+35, pencil_rect.top+15),
                (pencil_rect.left+15, pencil_rect.top+30)
            ]
        )

        pygame.draw.rect(screen, (35,35,45), clock_rect, border_radius=10)
        pygame.draw.rect(screen, (120,160,255), clock_rect, 2, border_radius=10)
        current_time = datetime.now().strftime("%I:%M %p")
        time_surface = clock_font.render(current_time, True, (255,255,255))
        screen.blit(time_surface, (WIDTH - 155, 16))

        font = pygame.font.SysFont(None, 24)
        prompt_surf = font.render("Type command:", True, (255,255,0))
        input_surf = font.render(f"{input_text}_", True, (255,255,255))
        screen.blit(prompt_surf, (10, HEIGHT - 60))
        screen.blit(input_surf, (10, HEIGHT - 30))

        draw_pause_indicator()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                with open("last_launch.txt", 'w') as f:
                    f.write(datetime.now().isoformat())
                pygame.quit()
                return
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    if input_text.strip() != '':
                        handle_command(input_text.strip())
                    input_text=''
                elif event.key==pygame.K_BACKSPACE:
                    input_text=input_text[:-1]
                elif event.key==PAUSE_KEY:
                    pause_animation = not pause_animation
                    print("Paused" if pause_animation else "Resumed")
                elif event.unicode != '':
                    input_text+=event.unicode
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=event.pos
                for idx, rect in enumerate(color_rects):
                    if rect.collidepoint(mouse_pos):
                        current_color = color_list[idx]
                if eraser_rect.collidepoint(mouse_pos):
                    strokes.clear()
                if pencil_rect.collidepoint(mouse_pos):
                    drawing_mode = not drawing_mode
                    if drawing_mode:
                        pause_animation=True
                    else:
                        pause_animation=False

        if 'drawing_mode' in locals() and drawing_mode:
            mouse_buttons=pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                mouse_pos=pygame.mouse.get_pos()
                rel_x=mouse_pos[0]-robot_pos[0]
                rel_y=mouse_pos[1]-robot_pos[1]
                add_stroke([(rel_x, rel_y)], current_color)

        pygame.display.flip()
        clock.tick(30)

if __name__=='__main__':
    main()
