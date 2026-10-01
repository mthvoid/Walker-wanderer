import pgzrun
import pygame
import av
import sys
from datetime import datetime

background_decorations = pygame.transform.scale(images.background_decoratios, (1920, 1080))
background = pygame.transform.scale(images.background, (1920, 1080))
map_shadows = pygame.transform.scale(images.map_shadows, (1920, 1080))
npc_layer = pygame.transform.scale(images.npc_layer, (1920, 1080))

#Ширина, Высота окна
WIDTH = 1920
HEIGHT = 1080

HERO_START = (991, 963)
VILLAIN_START = (50,240)

HERO_SPEED = 5
VILLAIN_SPEED = 2

VILLAIN_ROUTE_RIGHT = 1370
VILLAIN_ROUTE_DOWN = 750
VILLAIN_ROUTE_LEFT = 1000
VILLAIN_ROUTE_UP = 200

PHRASES_LIST = [
                    ("Hey",(2.5)), 
                    ("Hey, you",(1.5)), 
                    ("What are you doing in a place like this",(3.2)), 
                    ("I never forget a face when I see it",(2.3)), 
                    ("You smell simillar",(1.8)), 
                    ("To a terryifying guy I know",(3.3))
]

class Villain():

    def __init__(self, hero, game):
        self.villainx_position, self.villainy_position = VILLAIN_START
        self.villain_icon = pygame.transform.scale(images.villain, (75, 120))
        self.villainxpos1 = pygame.transform.scale(images.villainxpos1, (75, 110))
        self.villainxpos1reversed = pygame.transform.scale(images.villainxpos1reversed, (75, 110))
        self.villainxpos2 = pygame.transform.scale(images.villainxpos2, (75, 110))
        self.villainxpos2reversed = pygame.transform.scale(images.villainxpos2reversed, (75, 110))
        self.villainxpos3 = pygame.transform.scale(images.villainxpos3, (75, 110))
        self.villainxpos3reversed = pygame.transform.scale(images.villainxpos3reversed, (75, 110))
        self.villainypos1 = pygame.transform.scale(images.villainypos1, (75, 110))
        self.villainypos1reversed = pygame.transform.scale(images.villainypos1reversed, (75, 110))
        self.villainypos2 = pygame.transform.scale(images.villainypos2, (75, 110))
        self.villainypos2reversed = pygame.transform.scale(images.villainypos2reversed, (75, 110))
        self.villainypos3 = pygame.transform.scale(images.villainypos3, (75, 110))
        self.villain_chase = False
        self.villain_phase = None
        self.hero = hero
        self.game = game

        self.speed = VILLAIN_SPEED
        self.vector = None # Это флаг для направления ходьбы героя
        self.distancex = None # SAME
        self.distancey = None
        self.anim_timer = 0
        self.anim_texture = 1
        self.villain_is_running = False

        self.villain_walk_stage = 0
        self.old_villainx_position = None
        self.old_villainy_position = None

    def villain_stays_draw(self): #отрисовка злодея
        if self.villain_walk_stage == 0:
            screen.blit(self.villain_icon, (self.villainx_position, self.villainy_position))

    def villain_runs_update(self): #Бег злодея
        if self.villain_chase == "Right": 
            self.villainx_position += self.speed
            if self.villainx_position >= VILLAIN_ROUTE_RIGHT:
                self.villainx_position = VILLAIN_ROUTE_RIGHT
                self.villain_chase = "Down"
        if self.villain_chase == "Down":
            self.villainy_position += self.speed
            if self.villainy_position >= VILLAIN_ROUTE_DOWN:
                self.villainy_position = VILLAIN_ROUTE_DOWN
                self.villain_chase = "Left"
        if self.villain_chase == "Left":
            self.villainx_position -= self.speed
            if self.villainx_position <= VILLAIN_ROUTE_LEFT:
                self.villainx_position = VILLAIN_ROUTE_LEFT
                self.villain_chase = "Up"
        if self.villain_chase == "Up":
            self.villainy_position -= self.speed
            if self.villainy_position <= VILLAIN_ROUTE_UP:
                self.villainy_position = VILLAIN_ROUTE_UP
                self.villain_chase = "Right"

    def make_villain_old_position_update(self):
        self.old_villainx_position = self.villainx_position
        self.old_villainy_position = self.villainy_position

    def villain_walk_draw(self):
        if self.game.game_state == "chase":
            self.distancex = self.old_villainx_position - self.villainx_position
            self.distancey = self.old_villainy_position - self.villainy_position

            if self.distancex == 0 and self.distancey == 0:
                self.villain_is_running = False
                self.anim_timer = 0
                self.anim_texture = 1
                self.villain_walk_stage = 0

                if self.idle_start is None:
                    self.idle_start = datetime.now()
                elif (datetime.now() - self.idle_start).total_seconds() >= 6:
                    self.long_idle = True
                
            else:
                self.villain_is_running = True
                self.idle_start = None
                self.long_idle = False
                self.anim_timer += 1
                dt = datetime.now()
                tc = dt.microsecond%(500000/1)/(100000/1)

                if tc < 1.25 and self.distancex > 0:
                    screen.blit(self.villainxpos1, (self.villainx_position, self.villainy_position))
                    self.vector = "x"
                    self.villain_walk_stage = 1

                elif tc < 1.25 and self.distancex < 0:
                    screen.blit(self.villainxpos1reversed, (self.villainx_position, self.villainy_position))
                    self.vector = "-x"
                    self.villain_walk_stage = 1

                elif tc > 2.5 and self.vector == "x":
                    screen.blit(self.villainxpos2, (self.villainx_position, self.villainy_position))
                    self.villain_walk_stage = 1
                elif tc < 2.5 and self.vector == "x":
                    screen.blit(self.villainxpos3, (self.villainx_position, self.villainy_position))
                    self.villain_walk_stage = 1

                elif tc > 3.75 and self.vector == "-x":
                    screen.blit(self.villainxpos2reversed, (self.villainx_position, self.villainy_position))
                    self.villain_walk_stage = 1
                elif tc < 3.75 and self.vector == "-x":
                    screen.blit(self.villainxpos3reversed, (self.villainx_position, self.villainy_position))
                    self.villain_walk_stage = 1


                if tc < 1.25 and self.distancey < 0:
                    screen.blit(self.villainypos1, (self.villainx_position, self.villainy_position))
                    self.hero_walk_stage = 1
                    self.vector = "y"
                elif tc < 1.25 and self.distancey > 0:
                    screen.blit(self.villainypos1reversed, (self.villainx_position, self.villainy_position))
                    self.hero_walk_stage = 1    
                    self.vector = "-y"

                elif tc < 4 and self.vector == "y":
                    screen.blit(self.villainypos2, (self.villainx_position, self.villainy_position))
                    self.hero_walk_stage = 1
                elif tc < 4 and self.vector == "-y":
                    screen.blit(self.villainypos2reversed, (self.villainx_position, self.villainy_position))
                    self.hero_walk_stage = 1

                elif self.vector == "y":
                    screen.blit(self.villainypos3, (self.villainx_position, self.villainy_position))
                    self.hero_walk_stage = 1
                elif self.vector == "-y":
                    screen.blit(self.villainypos1reversed, (self.villainx_position, self.villainy_position))
                    self.hero_walk_stage = 1

    def villain_shadow_draw(self):
        shadow = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 60), (50, 50), 20)
        screen.surface.blit(shadow, (self.villainx_position - 15, self.villainy_position + 50))

class Hero():

        #Скорость и положение Главного Персонажа
    def __init__(self, game):

        self.image = pygame.transform.scale(images.jopa, (60, 110))
        self.hero_stays2 = pygame.transform.scale(images.hero_stay_02, (75, 110))
        self.heroxpos1 = pygame.transform.scale(images.heroxpos1, (75, 110))
        self.heroxpos1reversed = pygame.transform.scale(images.heroxpos1reversed, (75, 110))
        self.heroxpos2 = pygame.transform.scale(images.heroxpos2, (75, 110))
        self.heroxpos2reversed = pygame.transform.scale(images.heroxpos2reversed, (75, 110))
        self.heroxpos3 = pygame.transform.scale(images.heroxpos3, (75, 110))
        self.heroxpos3reversed = pygame.transform.scale(images.heroxpos3reversed, (75, 110))
        self.heroypos1 = pygame.transform.scale(images.heroypos1, (75, 110))
        self.heroypos1reversed = pygame.transform.scale(images.heroypos1yreversed, (75, 110))
        self.heroypos2 = pygame.transform.scale(images.heroypos2, (75, 110))
        self.heroypos2reversed = pygame.transform.scale(images.heroypos2yreversed, (75, 110))
        self.heroypos3 = pygame.transform.scale(images.heroypos3, (75, 110))

        self.vector = None # Это флаг для направления ходьбы героя
        self.distancex = None # SAME
        self.distancey = None
        self.anim_timer = 0
        self.anim_texture = 1
        self.idle_start = None          # когда герой остановился
        self.long_idle = False          # стоит ли он уже 6+ секунд
        self.hero_is_running = False

        self.hero_can_move = True
        self.hero_walk_stage = 0
        self.speed = HERO_SPEED
        self.speedx = 0
        self.speedy = 0
        self.old_herox_position = None
        self.old_heroy_position = None
        self.herox_position, self.heroy_position = HERO_START
        self.return_by_death_effect = False
        self.game = game

    def hero_draw(self):
        if self.hero_walk_stage == 0:
            if self.long_idle:
                screen.blit(self.hero_stays2, (self.herox_position, self.heroy_position))
            else:
                screen.blit(self.image, (self.herox_position, self.heroy_position))

    def hero_controls(self): #Управление через клаву

        self.herox_position += self.speedx
        self.heroy_position += self.speedy

        if self.hero_can_move == True:
            if keyboard.a == True:
                self.speedx = -self.speed
            elif keyboard.d == True:
                self.speedx = self.speed
            else:
                self.speedx = 0

            if keyboard.w == True:
                self.speedy = -self.speed
            elif keyboard.s == True:
                self.speedy = self.speed
            else:
                self.speedy = 0

        elif self.hero_can_move == False:
            self.speedx = 0
            self.speedy = 0
        
        #Ограничение по экрану в широте
        if self.herox_position > WIDTH - self.image.get_width(): #Здесь что бы понимать, 1280 - 100 = 1180, это предел для картинки, т.к. отсчет начинается с левого верхнего угла, а не с центра картинки
            self.herox_position =  WIDTH - self.image.get_width()
        if self.herox_position < 0:
            self.herox_position = 0

        #Ограничение по экрану в высоте
        if self.heroy_position > HEIGHT - self.image.get_height():
            self.heroy_position = HEIGHT - self.image.get_height()
        if self.heroy_position < 0:
            self.heroy_position = 0

    def make_hero_old_position_update(self):
        self.old_herox_position = self.herox_position
        self.old_heroy_position = self.heroy_position

    def hero_walk_draw(self):
        if self.game.game_state in ("exploration", "chase"):
            self.distancex = self.old_herox_position - self.herox_position
            self.distancey = self.old_heroy_position - self.heroy_position

            if self.distancex == 0 and self.distancey == 0:
                self.hero_is_running = False
                self.anim_timer = 0
                self.anim_texture = 1
                self.hero_walk_stage = 0

                if self.idle_start is None:
                    self.idle_start = datetime.now()
                elif (datetime.now() - self.idle_start).total_seconds() >= 6:
                    self.long_idle = True
                
            else:

                #навайбкожено, но с моей основы
                self.hero_is_running = True
                self.idle_start = None
                self.long_idle = False

                self.anim_timer += 1

                # ──────────────── X ────────────────

                if self.distancex > 0:

                    if self.vector != "x":
                        self.vector = "x"
                        self.anim_timer = 0

                    if self.anim_timer < 3:
                        screen.blit(
                            self.heroxpos1,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 1

                    elif self.anim_timer < 6:
                        screen.blit(
                            self.heroxpos2,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 2

                    else:
                        screen.blit(
                            self.heroxpos3,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 3


                elif self.distancex < 0:

                    if self.vector != "-x":
                        self.vector = "-x"
                        self.anim_timer = 0

                    if self.anim_timer < 3:
                        screen.blit(
                            self.heroxpos1reversed,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 1

                    elif self.anim_timer < 6:
                        screen.blit(
                            self.heroxpos2reversed,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 2

                    else:
                        screen.blit(
                            self.heroxpos3reversed,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 3


                # ──────────────── Y ────────────────

                elif self.distancey < 0:

                    if self.vector != "y":
                        self.vector = "y"
                        self.anim_timer = 0

                    if self.anim_timer < 3:
                        screen.blit(
                            self.heroypos1,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 1

                    elif self.anim_timer < 6:
                        screen.blit(
                            self.heroypos2,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 2

                    else:
                        screen.blit(
                            self.heroypos3,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 3


                elif self.distancey > 0:

                    if self.vector != "-y":
                        self.vector = "-y"
                        self.anim_timer = 0

                    if self.anim_timer < 3:
                        screen.blit(
                            self.heroypos1reversed,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 1

                    elif self.anim_timer < 6:
                        screen.blit(
                            self.heroypos2reversed,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 2

                    else:
                        screen.blit(
                            self.heroypos1reversed,
                            (self.herox_position, self.heroy_position)
                        )
                        self.hero_walk_stage = 3


                if self.anim_timer >= 8:
                    self.anim_timer = 0

    def hero_shadow_draw(self):
        shadow = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 60), (50, 50), 20)
        screen.surface.blit(
            shadow,
            (self.herox_position - 15, self.heroy_position + 50)
        )

    def allow_hero_move(self): #Разрешает ходить герою
        self.hero_can_move = True

    def enable_return_by_death_effect(self):
        self.return_by_death_effect = True
    
class Adjusting_mode():

        #Проверка на самое первоее нажатие кнопки
    def __init__(self):
        self.button_was_pressed_once = False
        self.button_first_pressed = (0, 0) 

    def adjusting_mode(self): #определяет нажатие мыши + рисует рамку

        pressed_button = pygame.mouse.get_pressed()
        mousepos = pygame.mouse.get_pos()

        if pressed_button[0] == True and self.button_was_pressed_once == False:
            self.button_first_pressed = pygame.mouse.get_pos()
            self.button_was_pressed_once = True
            print(self.button_first_pressed)
        if self.button_was_pressed_once == True and pressed_button[0] == True:
            button_still_pressed = pygame.mouse.get_pos()
            rectx = button_still_pressed[0] - self.button_first_pressed[0]
            recty = button_still_pressed[1] - self.button_first_pressed[1]
            print(self.button_first_pressed)
            if self.button_first_pressed[0] < button_still_pressed[0] and self.button_first_pressed[1] < button_still_pressed[1]:
                rect = pygame.Rect(self.button_first_pressed, (abs(rectx), abs(recty))) #Сделать размер в зависимости от положения мыши.
                box_x = self.button_first_pressed[0] + rectx
                box_y = self.button_first_pressed[1] + recty
                box_coord = self.button_first_pressed, box_x, box_y
                screen.draw.rect(rect, (200, 0, 0))
                print(abs(rectx), abs(recty))
            elif self.button_first_pressed[0] > button_still_pressed[0] and self.button_first_pressed[1] > button_still_pressed[1]:
                rect = pygame.Rect(button_still_pressed, (abs(rectx), abs(recty)))
                screen.draw.rect(rect, (200, 0, 0))
                print(abs(rectx), abs(recty))
            elif self.button_first_pressed[0] < button_still_pressed[0]:
                rect_object1 = self.button_first_pressed[0], button_still_pressed[1]
                rect = pygame.Rect(rect_object1, (abs(rectx), abs(recty)))
                screen.draw.rect(rect, (200, 0, 0))
                print(abs(rectx), abs(recty))
            elif button_still_pressed[1] > self.button_first_pressed[1]:
                rect_object2 = button_still_pressed[0], self.button_first_pressed[1]
                rect = pygame.Rect(rect_object2, (abs(rectx), abs(recty)))
                screen.draw.rect(rect, (200, 0, 0))
                print(abs(rectx), abs(recty))
        if pressed_button[0] == False:
            self.button_was_pressed_once = False

class Dialogue():

    def __init__(self):
        self.phrase_appeared = False
        self.phrases_list = ("Hey", "Hey, you", "What are you doing in a place like this", "I never forget a face when I see it", "You smell simillar", "To a terryifying guy I know")
        self.current_phrase = 0
        self.time = 0
        self.text_first_state = False
        self.dialogue_bar_appears = None
        self.first_phrase_ready = False
        self.dialogue_bar = pygame.transform.scale(images.dialogue_bar, (1000, 255))
        self.villain_full_icon = pygame.transform.scale(images.villain_full_icon, (385, 394))

    def dialogue_bar_appears_off(self): #Выключает диалоговое окно
        self.dialogue_bar_appears = False

    def dialogue_bar_icon_draw(self): #Рисует диалоговое окно
        if self.dialogue_bar_appears == True:
            screen.blit(self.dialogue_bar, (540, 827))
            screen.blit(self.villain_full_icon, (390, 750))
            screen.draw.text("VASILIY AXE GUY", (688, 837), color = (211, 100, 100), fontsize = 45, owidth=2, ocolor="black", shadow=(1,1), scolor="#202020")

    def show_first_phrase(self):
        self.first_phrase_ready = True

    def villain_talking_draw(self):
        if self.dialogue_bar_appears == True and self.first_phrase_ready:
            text, duration = PHRASES_LIST[self.current_phrase]
            screen.draw.text(text, (680, 920), color = (211, 100, 100), fontsize = 45, owidth=2, ocolor="black", shadow=(1,1), scolor="#202020")

    def next_phrase(self, dt):
        if self.current_phrase < len(PHRASES_LIST) - 1:
            self.time += dt
            text, duration = PHRASES_LIST[self.current_phrase]
            if self.time >= duration:
                self.current_phrase += 1
                self.time = 0
                self.text_first_state = True
                self.next_phrase

class Music():

    def __init__(self, game):
        self.first_scene = True
        self.before_dialogue = True
        self.music_started = False
        self.game = game

    def main_music(self):
        if self.before_dialogue:
            pygame.mixer.music.load("music/music_game.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
        elif self.game.game_state == "chase" and self.music_started == False:
            pygame.mixer.music.load("music/shapeshift.mp3")
            print("AFTER LOAD:", pygame.mixer.music.get_busy())
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
            print("AFTER PLAY:", pygame.mixer.music.get_busy())
            self.music_started = True

    def villain_first_reply(self):
        if self.first_scene == True:
            
            sound = pygame.mixer.Sound("music/rezero - todd fang hey you.mp3")
            sound.play()

            self.first_scene = False

    def hero_dies_sound(self):
        sound = pygame.mixer.Sound("music/rezero return by death sound effect.wav")
        sound.play()
        stabbing_sound = pygame.mixer.Sound("music/stabbing_sound.wav")
        stabbing_sound.play()

class Obstacle():

    def __init__(self):
        self.obstacles = [
        None
        ]

    def show_obstacles(self):
        for obs in self.obstacles:
            try:
                screen.draw.rect(obs, (200, 0, 0))
            except:
                screen.draw.text("Препятствий нет!", (900, 540), color=(200, 0, 0), fontsize = 30, owidth=4, ocolor="black", shadow=(1,2), scolor="#202020")
                

class Pause():

    def __init__(self, game):
        self.pause_image = pygame.transform.scale(images.pause_image, (1920, 1080))
        self.rectangle_19 = pygame.transform.scale(images.rectangle_19, (694, 132))
        self.polygon1 = pygame.transform.scale(images.polygon31, (104, 100))
        self.polygon2 = pygame.transform.scale(images.polygon32, (104, 100))
        self.pause_icon = pygame.transform.scale(images.pause_icon, (450, 300))
        self.last_game_state = None
        self.game = game

        self.mouse_x = 0
        self.mouse_y = 0

        self.alpha = 0
        self.opening = False

    def update(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def pause_toggle(self):
        if self.game.game_state != "Pause":
            self.last_game_state = self.game.game_state
            self.game.game_state = "Pause"
            pygame.mixer.pause()

        else: 
            self.game.game_state = "Pause"
            pygame.mixer.unpause()
            self.game.game_state = self.last_game_state

    def opening_menu(self):
        self.alpha = 0
        self.opening = True

    def alpha_update(self):
        if self.opening:
            self.alpha += 5

            if self.alpha == 250:
                self.opening = False

    def pause_draw(self):
        self.pause_image.set_alpha(self.alpha)
        self.pause_icon.set_alpha(self.alpha)
        screen.blit(self.pause_image, (0, 0))
        screen.blit(self.pause_icon, (250, 125))

        if 132 <= self.mouse_x <= 826 and 353 <= self.mouse_y <= 485:
            screen.blit(self.rectangle_19, (132, 353))

        elif 132 <= self.mouse_x <= 826 and 453 <= self.mouse_y <= 585:
            screen.blit(self.rectangle_19, (132, 453))

        elif 132 <= self.mouse_x <= 826 and 453 <= self.mouse_y <= 677:
            screen.blit(self.rectangle_19, (132, 550))

        elif 132 <= self.mouse_x <= 826 and 453 <= self.mouse_y <= 777:
            screen.blit(self.rectangle_19, (132, 650))

        elif 132 <= self.mouse_x <= 826 and 453 <= self.mouse_y <= 877:
            screen.blit(self.rectangle_19, (132, 745))

        elif 132 <= self.mouse_x <= 826 and 453 <= self.mouse_y <= 977:
            screen.blit(self.rectangle_19, (132, 845))

        elif 1000 <= self.mouse_x <= 1130 and 973 <= self.mouse_y <= 1105:
            screen.blit(self.polygon2, (1000, 973))

        elif 1143 <= self.mouse_x <= 1380 and 973 <= self.mouse_y <= 1105:
            screen.blit(self.polygon1, (1143, 973))

        font = pygame.font.Font(None, 45)
        buttons = [("ПРОДОЛЖИТЬ",479,419), ("НАСТРОЙКИ (in progress)",479,519), ("УПРАВЛЕНИЕ (in progress)",479,616), ("ПОСМОТРЕТЬ ЭДИТ",479,716), ("ГЛАВНОЕ МЕНЮ (in progress)",479,811), ("ВЫЙТИ",479,911)]

        for text, x, y in buttons:
            text_surface = font.render(text, True, (210, 180, 100))
            text_surface.set_alpha(self.alpha)
            text_rect = text_surface.get_rect(center=(x, y))

            screen.blit(text_surface, text_rect)

class Video(): # СДЕЛАЛ НЕ Я ЭТО ВАЙБ КОД

    def __init__(self):
        self.container = None
        self.frames = None
        self.frame = None

        self.playing = False

        self.fps = 30
        self.frame_duration = 1000 / 30
        self.next_frame_time = 0


    def play(self, filename):
        self.container = av.open(filename)

        self.fps = float(
            self.container.streams.video[0].average_rate
        )

        self.frame_duration = 1000 / self.fps

        self.frames = self.container.decode(video=0)

        self.playing = True

        self.next_frame_time = pygame.time.get_ticks()


    def update(self):

        if not self.playing:
            return

        current_time = pygame.time.get_ticks()

        if current_time < self.next_frame_time:
            return

        self.next_frame_time += self.frame_duration

        try:
            frame = next(self.frames)

            image = frame.to_image()

            self.frame = pygame.image.fromstring(
                image.tobytes(),
                image.size,
                image.mode
            )

        except StopIteration:
            self.stop()


    def draw(self):

        if self.frame:

            rect = self.frame.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )

            screen.surface.blit(
                self.frame,
                rect
            )


    def stop(self):

        self.playing = False

        if self.container:
            self.container.close()

        self.container = None
        self.frames = None
        self.frame = None

class Game():

    def __init__(self):
        self.obstacle = Obstacle()
        self.hero = Hero(self)
        self.villain = Villain(self.hero, self)
        self.dialogue = Dialogue()
        self.music = Music(self)
        self.adjust = Adjusting_mode()
        self.pause = Pause(self)
        self.video = Video()

        self.first_encounter = False
        self.dialogue_started = False

        self.fullscreen_set = False
        self.fullscreen_was_settled_first_time = False

        self.spectator_mode = False
        self.game_states = ("exploratioin", "dialogue", "chase", "Pause")
        self.game_state = "exploration"
        self.collision_villain = None #сюда ниже присваиваются хитбоксы
        self.collision_hero = None

        self.music.main_music()

        clock.schedule(self.set_window_title, 0.0)

    def set_window_title(self):
        pygame.display.set_caption("Ходилка бродилка хуйилка")

    def hero_return_by_death(self): #Повторные смерти от злодея

        if self.collision_hero.collidelist([self.collision_villain]) != -1 and self.hero.return_by_death_effect == True: #ПОТОМ СДЕЛАТЬ УСЛОВНИИЕ В GAME НЕ ЗАБЫТЬ
            self.hero.herox_position = 991
            self.hero.heroy_position = 963
            self.villain.villainx_position = 50
            self.villain.villainy_position = 240
            self.villain.villain_chase = "Right"
            self.music.hero_dies_sound()

    def first_meet_villain(self): #Первая встреча со злодеем, включение погони через 17 сек

        self.collision_villain = self.villain.villain_icon.get_rect(topleft = (self.villain.villainx_position, self.villain.villainy_position))
        self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))

        if self.first_encounter == False:
            if self.collision_hero.collidelist([self.collision_villain]) != -1: #Буквально, если игрок сталкивается со злодеем, то...
                self.start_dialogue()
                self.villain.villain_chase = "Right"
                self.first_encounter = True

                self.music.first_scene = True
                self.music.before_dialogue = False
                pygame.mixer.music.stop()


    def start_exploration(self):
        self.game_state = "exploration"

    def start_dialogue(self):
        self.game_state = "dialogue"
        self.hero.hero_walk_stage = 0
        self.hero.distancex = 0
        self.hero.distancey = 0
        self.hero.idle_start = None
        self.hero.long_idle = False

    def start_chase(self):
        self.game_state = "chase"
        self.music.main_music()

    def set_screen_mode(self):
        if self.fullscreen_was_settled_first_time == False:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            self.fullscreen_was_settled_first_time = True

    def draw_debug_menu(self):
        #отладка
        x = 5
        y = 620
        debug_list = [
            (f"state={self.game_state}"),
            (f"last_game_state={self.pause.last_game_state}"),
            (f"chase={self.villain.villain_chase}"),
            (f"hero_x={self.hero.herox_position}"),
            (f"hero_y={self.hero.heroy_position}"),
            (f"hero_can_move={self.hero.hero_can_move}"),
            (f"hero_is_running={self.hero.hero_is_running}"),
            (f"villain_x={self.villain.villainx_position}"),
            (f"villain_y={self.villain.villainy_position}"),
            (f"mouse_pos={pygame.mouse.get_pos()}"),
            (f"first_encounter={self.first_encounter}"),
            (f"return_by_death={self.hero.return_by_death_effect}"),
            (f"current_phrase={self.dialogue.current_phrase}"),
            (f"dialogue_bar_appears={self.dialogue.dialogue_bar_appears}")
        ]

        for debug in debug_list:
            y += 30
            screen.draw.text(debug, (x, y), color=(200, 0, 0), fontsize = 30, owidth=4, ocolor="black", shadow=(1,2), scolor="#202020")

    def update(self, dt):

        self.video.update()
        
        self.adjust.adjusting_mode()

        self.pause.alpha_update()

        self.pause.update()

        if self.game_state == "exploration":

            self.hero.make_hero_old_position_update()

            self.hero.hero_controls()

            self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))
            self.collision_hero.inflate_ip(-60, -150)
            self.collision_hero.y += 40

        self.first_meet_villain()

        if self.game_state == "dialogue":

            self.dialogue.next_phrase(dt)
             
            if self.dialogue_started == False:

                self.hero.hero_can_move = False
                self.music.villain_first_reply()
                self.dialogue.dialogue_bar_appears = True
                clock.schedule(self.dialogue.show_first_phrase, 0.7)
                self.dialogue_started = True

            if self.dialogue.current_phrase == len(PHRASES_LIST) - 1:
                self.dialogue.time += dt
                text, duration = PHRASES_LIST[self.dialogue.current_phrase]
                if self.dialogue.time >= duration:
                    self.start_chase()
                    self.dialogue.time = 0
        
        
        if self.game_state == "chase":

            prev_hero_x = self.hero.herox_position
            prev_hero_y = self.hero.heroy_position

            self.hero.make_hero_old_position_update()

            self.hero.hero_controls()

            #self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position)) #ТУТ ГЕРОЙ СПОТЫКАЕТСЯ ОБ obstacles
            #self.collision_hero.inflate_ip(-60, -150)
            #self.collision_hero.y += 40

            #if self.collision_hero.collidelist(self.obstacle.obstacles) != -1:
            #    self.hero.herox_position = prev_hero_x 
            #    self.hero.heroy_position = prev_hero_y 

            self.villain.make_villain_old_position_update()

            self.villain.villain_runs_update()

            self.hero_return_by_death()
            self.hero.enable_return_by_death_effect()
            self.dialogue.dialogue_bar_appears_off()
            self.hero.allow_hero_move()

    def draw(self):

        screen.clear()

        screen.blit(background, (0, 0))

        self.set_screen_mode()

        #screen.blit(map_shadows, (0, 0))

        self.hero.hero_shadow_draw()
        self.hero.hero_draw()
        self.hero.hero_walk_draw()
        if self.spectator_mode == True:
            self.obstacle.show_obstacles()
            
            if self.collision_hero:
                self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))
                self.collision_hero.inflate_ip(-60, -100)
                self.collision_hero.y += 55
                screen.draw.rect(self.collision_hero, (200, 0, 0))

        self.villain.villain_shadow_draw()
        self.villain.villain_walk_draw()

        self.villain.villain_stays_draw()

        #screen.blit(background_decorations, (0, 0))
        #screen.blit(npc_layer, (0, 0))

        self.adjust.adjusting_mode()

        self.dialogue.dialogue_bar_icon_draw()
        self.dialogue.villain_talking_draw()

        if self.game_state == "Pause":
            self.pause.pause_draw()

        screen.draw.text("P - включить режим отладки", (5, 5), color=(200, 0, 0))
        screen.draw.text("Esc - выйти в меню", (5, 20), color=(200, 0, 0))
        screen.draw.text("Когда в меню, O - посмотреть эдит", (5, 35), color=(200, 0, 0))

        if game.video.playing:
            game.video.draw()

        self.draw_debug_menu()

game = Game()

def update(dt):
    game.update(dt)

def draw():
    game.draw()

def on_key_down(key):
    if key == keys.F11:
        if game.fullscreen_set == False:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            game.fullscreen_set = True
        elif game.fullscreen_set == True:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT))
            game.fullscreen_set = False

    if key == keys.P:
        game.spectator_mode = not game.spectator_mode
    if key == keys.ESCAPE:
        game.pause.pause_toggle()
        game.pause.opening_menu()

    if key == keys.ESCAPE and game.video.playing:
        game.video.stop()
        game.pause.pause_toggle()
        game.pause.opening_menu()
        game.pause.alpha = 250

def on_mouse_down(pos, button):
    if game.game_state == "Pause":
        if 132 <= pos[0] <= 826 and 845 <= pos[1] <= 977:
            pygame.quit()
            sys.exit()
        if 132 <= pos[0] <= 826 and 650 <= pos[1] <= 782:
            game.video.play("video/edit1.mp4")
        if 132 <= pos[0] <= 826 and 353 <= pos[1] <= 485:
            game.pause.pause_toggle()
            game.pause.opening_menu()

pgzrun.go()