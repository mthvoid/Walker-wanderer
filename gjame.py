import pgzrun
import pygame
from datetime import datetime

background_decorations = pygame.transform.scale(images.background_decoratios, (1920, 1080))
background = pygame.transform.scale(images.background, (1920, 1080))
npc_layer = pygame.transform.scale(images.npc_layer, (1920, 1080))

#Ширина, Высота окна
WIDTH = 1920
HEIGHT = 1080

class Villain():

    def __init__(self, hero, game):
        self.villainx_position = 50
        self.villainy_position = 240
        self.villain_walk_texture = pygame.transform.scale(images.villain_walk, (75, 120))
        self.villain_icon = pygame.transform.scale(images.villain, (75, 120))
        self.villain_chase = False
        self.hero = hero
        self.game = game

    def villain_stays_draw(self): #отрисовка злодея
            screen.blit(self.villain_icon, (self.villainx_position, self.villainy_position))

    def villain_runs_update(self): #Бег злодея

        if self.villainx_position < self.hero.herox_position:
            self.villainx_position += 2
        elif self.villainx_position > self.hero.herox_position:
            self.villainx_position -= 2

        if self.villainy_position < self.hero.heroy_position:
            self.villainy_position += 2
        elif self.villainy_position > self.hero.heroy_position:
            self.villainy_position -= 2
    
    #def start_chase(self): #Включает погоню за героем
    #    self.villain_chase = True

    #def villain_chase_texture_manager(self): #меняет состояние анимации злодея
        #global villain_chase_texture
        #global villain_starts_chase_texture
        #villain_starts_chase_texture = True
        #villain_chase_texture = True

    #def villain_chase_texture_manager_while_running(self): #меняет состояние анимации обратно
        #global villain_chase_texture
        #villain_chase_texture = False

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
        self.speedx = 0
        self.speedy = 0
        self.old_herox_position = None
        self.old_heroy_position = None
        self.herox_position = 991
        self.heroy_position = 963
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
                self.speedx = -5
            elif keyboard.d == True:
                self.speedx = 5
            else:
                self.speedx = 0

            if keyboard.w == True:
                self.speedy = -5
            elif keyboard.s == True:
                self.speedy = 5
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
                self.hero_is_running = True
                self.idle_start = None
                self.long_idle = False
                self.anim_timer += 1
                dt = datetime.now()
                tc = dt.microsecond%(500000/1)/(100000/1)

                if tc < 1.25 and self.distancex > 0:
                    screen.blit(self.heroxpos1, (self.herox_position, self.heroy_position))
                    self.vector = "x"
                    self.hero_walk_stage = 1

                elif tc < 1.25 and self.distancex < 0:
                    screen.blit(self.heroxpos1reversed, (self.herox_position, self.heroy_position))
                    self.vector = "-x"
                    self.hero_walk_stage = 1

                elif tc > 2.5 and self.vector == "x":
                    screen.blit(self.heroxpos2, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1
                elif tc < 2.5 and self.vector == "x":
                    screen.blit(self.heroxpos3, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1

                elif tc > 3.75 and self.vector == "-x":
                    screen.blit(self.heroxpos2reversed, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1
                elif tc < 3.75 and self.vector == "-x":
                    screen.blit(self.heroxpos3reversed, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1


                if tc < 1.25 and self.distancey < 0:
                    screen.blit(self.heroypos1, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1
                    self.vector = "y"
                elif tc < 1.25 and self.distancey > 0:
                    screen.blit(self.heroypos1reversed, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1    
                    self.vector = "-y"

                elif tc < 4 and self.vector == "y":
                    screen.blit(self.heroypos2, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1
                elif tc < 4 and self.vector == "-y":
                    screen.blit(self.heroypos2reversed, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1

                elif self.vector == "y":
                    screen.blit(self.heroypos3, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1
                elif self.vector == "-y":
                    screen.blit(self.heroypos1reversed, (self.herox_position, self.heroy_position))
                    self.hero_walk_stage = 1

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
        self.text_first_state = False
        self.dialogue_bar_appears = None
        self.dialogue_bar = pygame.transform.scale(images.dialogue_bar, (1000, 255))
        self.villain_full_icon = pygame.transform.scale(images.villain_full_icon, (385, 394))

    def dialogue_bar_appears_off(self): #Выключает диалоговое окно
        self.dialogue_bar_appears = False

    def dialogue_bar_icon_draw(self): #Рисует диалоговое окно
        if self.dialogue_bar_appears == True:
            screen.blit(self.dialogue_bar, (540, 827))
            screen.blit(self.villain_full_icon, (390, 750))
            #screen.draw.text("Vasiliy Axe Guy", (265, 520), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black")

    def villain_talking_draw(self):
        if self.dialogue_bar_appears == True:
            if self.current_phrase == 0:
                screen.draw.text(self.phrases_list[self.current_phrase], (680, 951), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black", shadow=(1,1), scolor="#202020")
            elif self.current_phrase > 0 and self.current_phrase < 6:
                screen.draw.text(self.phrases_list[self.current_phrase], (680, 951), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black", shadow=(1,1), scolor="#202020")

    def next_phrase(self):

        if self.current_phrase == 0 and self.text_first_state == False:
            self.text_first_state = True
            clock.schedule(self.next_phrase, 1.5)

        elif self.current_phrase == 0 and self.text_first_state == True:
            self.current_phrase += 1
            clock.schedule(self.next_phrase, 1.4)

        elif self.current_phrase == 1:
            self.current_phrase += 1
            clock.schedule(self.next_phrase, 3.6)

        elif self.current_phrase == 2:
            self.current_phrase += 1
            clock.schedule(self.next_phrase, 2.5)

        elif self.current_phrase == 3:
            self.current_phrase += 1
            clock.schedule(self.next_phrase, 1.5)

        elif self.current_phrase == 4:
            self.current_phrase += 1
            clock.schedule(self.next_phrase, 2.3)

class Music():

    def __init__(self, game):
        self.first_scene = False
        self.game = game

    def main_music(self):
        music_game = "music_game"
        music.set_volume(0.3)
        music.play(music_game)

    def villain_first_reply(self):
        if self.first_scene == True:
            music.play_once("rezero - todd fang hey you")
            pygame.mixer.music.set_pos(8)
            self.first_scene = False
            clock.schedule(self.game.start_chase, 17)

class Obstacle():

    def __init__(self):
        self.obstacles = [
        None
        ]

    def show_obstacles(self):
        for obs in self.obstacles:
            screen.draw.rect(obs, (200, 0, 0))

class Game():

    def __init__(self):
        self.obstacle = Obstacle()
        self.hero = Hero(self)
        self.villain = Villain(self.hero, self)
        self.dialogue = Dialogue()
        self.music = Music(self)
        self.adjust = Adjusting_mode()
        self.music.main_music()
        self.first_encounter = False

        self.fullscreen_set = False
        self.fullscreen_was_settled_first_time = False

        self.spectator_mode = False
        self.game_states = ("exploratioin", "dialogue", "chase")
        self.game_state = "exploration"
        self.collision_villain = None #сюда ниже присваиваются хитбоксы
        self.collision_hero = None

        clock.schedule(self.set_window_title, 0.0)

    def set_window_title(self):
        pygame.display.set_caption("Ходилка бродилка хуйилка")

    def hero_return_by_death(self): #Повторные смерти от злодея

        if self.collision_hero.collidelist([self.collision_villain]) != -1 and self.hero.return_by_death_effect == True: #ПОТОМ СДЕЛАТЬ УСЛОВНИИЕ В GAME НЕ ЗАБЫТЬ
            self.hero.herox_position = 991
            self.hero.heroy_position = 963
            self.villain.villainx_position = 50
            self.villain.villainy_position = 240
            music.play_once("rezero return by death sound effect")
            pygame.mixer.music.set_pos(1)

    def first_meet_villain(self): #Первая встреча со злодеем, включение погони через 17 сек

        self.collision_villain = self.villain.villain_icon.get_rect(topleft = (self.villain.villainx_position, self.villain.villainy_position))
        self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))

        if self.first_encounter == False:
            if self.collision_hero.collidelist([self.collision_villain]) != -1: #Буквально, если игрок сталкивается со злодеем, то...
                self.start_dialogue()
                self.first_encounter = True
                self.dialogue.dialogue_bar_appears = True
                self.music.first_scene = True
                self.hero.hero_can_move = False
                clock.schedule(self.dialogue.next_phrase, 0.7)

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

    def set_screen_mode(self):
        if self.fullscreen_was_settled_first_time == False:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            self.fullscreen_was_settled_first_time = True
        if keyboard.f11 == True and self.fullscreen_set == False:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            self.fullscreen_set = True
        elif keyboard.f11 == True and self.fullscreen_set == True:
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT))
            self.fullscreen_set = False

    def update(self):
        
        self.adjust.adjusting_mode()

        if self.game_state == "exploration":
            prev_hero_x = self.hero.herox_position
            prev_hero_y = self.hero.heroy_position

            self.hero.make_hero_old_position_update()

            self.hero.hero_controls()

            self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))
            self.collision_hero.inflate_ip(-60, -150)
            self.collision_hero.y += 40

            #if self.collision_hero.collidelist(self.obstacle.obstacles) != -1: #ТУТ ГЕРОЙ СПОТЫКАЕТСЯ ОБ obstacles
            #    self.hero.herox_position = prev_hero_x 
            #    self.hero.heroy_position = prev_hero_y 

        self.first_meet_villain() # ТУТ Я ВЫНЕС ПРОВЕРКУ НА СТОЛКНОВЕНИЕ, КОТОРОЕ ДОЛЖНО ЗАПУСКАТЬ ДИАЛОГ, ДАЛЬШЕ НАДО СДЕЛАТЬ ПЕРЕКЛЮЧЕНИЕ С ДИАЛОГА НА CHASE

        if self.game_state == "dialogue":
            self.music.villain_first_reply()

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

            #prev_villain_x = self.villain.villainx_position
            #prev_villain_y = self.villain.villainy_position

            #self.collision_villain = self.villain.villain_icon.get_rect(topleft = (self.villain.villainx_position, self.villain.villainy_position))
            #self.collision_hero.inflate_ip(-60, -150)
            #self.collision_hero.y += 40

            self.villain.villain_runs_update()

            #if self.collision_villain.collidelist(self.obstacle.obstacles) != -1:
           #     self.villain.villainx_position = prev_villain_x
            #    self.villain.villainy_position = prev_villain_y

            self.hero_return_by_death()
            self.hero.enable_return_by_death_effect()
            self.dialogue.dialogue_bar_appears_off()
            self.hero.allow_hero_move()

    def draw(self):

        screen.clear()
        screen.blit(background, (0, 0))

        self.set_screen_mode()

        self.hero.hero_draw()
        self.hero.hero_walk_draw()
        if self.spectator_mode == True:
            self.obstacle.show_obstacles()
            
            if self.collision_hero:
                self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))
                self.collision_hero.inflate_ip(-60, -100)
                self.collision_hero.y += 55
                screen.draw.rect(self.collision_hero, (200, 0, 0))

        self.villain.villain_stays_draw()

        screen.blit(background_decorations, (0, 0))
        screen.blit(npc_layer, (0, 0))

        self.adjust.adjusting_mode()

        self.dialogue.dialogue_bar_icon_draw()
        self.dialogue.villain_talking_draw()

        screen.draw.text("P - включить режим отладки", (5, 5), color=(200, 0, 0))
        screen.draw.text("Esc - Насувать васлию пенисов в рот", (5, 20), color=(200, 0, 0))
game = Game()

def update():
    game.update()

def draw():
    game.draw()

def on_key_down(key):
    if key == keys.P:
        game.spectator_mode = not game.spectator_mode

pgzrun.go()