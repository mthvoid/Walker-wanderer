import pgzrun
import pygame

background_decorations = pygame.transform.scale(images.background_decoratios, (1280, 720))
background = pygame.transform.scale(images.background, (1280, 720))

#Ширина, Высота окна
WIDTH = 1280
HEIGHT = 720

class Villain():

    def __init__(self, hero, game):
        self.villainx_position = 50
        self.villainy_position = 40
        self.villain_walk_texture = pygame.transform.scale(images.villain_walk, (75, 120))
        self.villain_icon = pygame.transform.scale(images.villain, (75, 120))
        self.villain_chase = False
        self.hero = hero
        self.game = game

    def villain_stays_draw(self): #отрисовка злодея
            screen.blit(self.villain_icon, (self.villainx_position, self.villainy_position))

    def villain_runs_update(self): #Бег злодея

        if self.villain_chase == True:
            if self.villainx_position < self.hero.herox_position:
                self.villainx_position += 2
            elif self.villainx_position > self.hero.herox_position:
                self.villainx_position -= 2

            if self.villainy_position < self.hero.heroy_position:
                self.villainy_position += 2
            elif self.villainy_position > self.hero.heroy_position:
                self.villainy_position -= 2
    
    def start_chase(self): #Включает погоню за героем
        self.villain_chase = True

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
    def __init__(self):
        self.image = pygame.transform.scale(images.jopa, (75, 110))
        self.hero_can_move = True
        self.speedx = 0
        self.speedy = 0
        self.herox_position = 1080
        self.heroy_position = 640
        self.return_by_death_effect = False

    def hero_draw(self):
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
            screen.blit(self.dialogue_bar, (150, 500))
            screen.blit(self.villain_full_icon, (0, 400))
            #screen.draw.text("Vasiliy Axe Guy", (265, 520), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black")

    def villain_talking_draw(self):
        if self.dialogue_bar_appears == True:
            if self.current_phrase == 0:
                screen.draw.text(self.phrases_list[self.current_phrase], (300, 600), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black", shadow=(1,1), scolor="#202020")
            elif self.current_phrase > 0 and self.current_phrase < 6:
                screen.draw.text(self.phrases_list[self.current_phrase], (300, 600), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black", shadow=(1,1), scolor="#202020")

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

    def __init__(self):
        self.first_scene = False

    def main_music(self):
        music_game = "music_game"
        music.set_volume(0.3)
        music.play(music_game)

    def villain_first_reply(self):
        if self.first_scene == True:
            music.play_once("rezero - todd fang hey you")
            pygame.mixer.music.set_pos(8)
            self.first_scene = False

class Obstacle():

    def __init__(self):
        self.obstacles = [
        pygame.Rect((1167, 690), (65, 31)),
        pygame.Rect((1040, 518), (36, 35)),
        pygame.Rect((935, 621), (143, 73)),
        pygame.Rect((926, 360), (150, 97)),
        pygame.Rect((1123, 365), (39, 43)),
        pygame.Rect((1135, 204), (118, 83)),
        pygame.Rect((906, 177), (143, 100)),
        pygame.Rect((704, 212), (158, 114)),
        pygame.Rect((1230, 452), (31, 34)),
        pygame.Rect((1041, 520), (35, 33)),
        pygame.Rect((890, 550), (21, 21)),
        pygame.Rect((750, 346), (99, 36)),
        pygame.Rect((832, 362), (64, 60)),
        pygame.Rect((575, 621), (349, 96)),
        pygame.Rect((1124, 67), (29, 32)),
        pygame.Rect((321, 622), (237, 98)),
        pygame.Rect((404, 405), (86, 56)),
        pygame.Rect((240, 550), (81, 49)),
        pygame.Rect((156, 610), (138, 106)),
        pygame.Rect((49, 585), (35, 33)),
        pygame.Rect((192, 325), (78, 65)),
        pygame.Rect((9, 429), (61, 59)),
        pygame.Rect((125, 409), (62, 44)),
        pygame.Rect((32, 229), (124, 121)),
        pygame.Rect((198, 202), (55, 55)),
        pygame.Rect((353, 210), (57, 51)),
        pygame.Rect((17, 178), (49, 50)),
        pygame.Rect((249, 7), (161, 97)),
        pygame.Rect((65, 35), (61, 61)),
        pygame.Rect((568, 582), (23, 23)),
        pygame.Rect((667, 153), (18, 25)),
        pygame.Rect((408, 158), (24, 27)),
        pygame.Rect((447, 1), (96, 66)),
        pygame.Rect((542, 32), (42, 35)),
        pygame.Rect((479, 164), (128, 66)),
        pygame.Rect((447, 230), (193, 99)),
        pygame.Rect((479, 295), (193, 34)),
        pygame.Rect((512, 328), (189, 65)),
        pygame.Rect((544, 394), (223, 33)),
        pygame.Rect((582, 425), (186, 39)),
        pygame.Rect((700, 357), (36, 38)),
        pygame.Rect((448, 64), (194, 27)),
        pygame.Rect((447, 152), (192, 40)),
        pygame.Rect((573, 447), (302, 38)),
        pygame.Rect((572, 559), (332, 25))
        ]


    def show_obstacles(self):
        for obs in self.obstacles:
            screen.draw.rect(obs, (200, 0, 0))

class Game():

    def __init__(self):
        self.obstacle = Obstacle()
        self.hero = Hero()
        self.villain = Villain(self.hero, self)
        self.dialogue = Dialogue()
        self.music = Music()
        self.adjust = Adjusting_mode()
        self.music.main_music()
        self.first_encounter = False

    #Хитбоксы героя и злодея
        self.game_state = None
        self.collision_villain = None #сюда ниже присваиваются хитбоксы
        self.collision_hero = None

        clock.schedule(self.set_window_title, 0.0)

    def set_window_title(self):
        pygame.display.set_caption("Ходилка бродилка хуйилка")

    def hero_return_by_death(self): #Повторные смерти от злодея

        if self.collision_hero.collidelist([self.collision_villain]) != -1 and self.hero.return_by_death_effect == True: #ПОТОМ СДЕЛАТЬ УСЛОВНИИЕ В GAME НЕ ЗАБЫТЬ
            self.hero.herox_position = 1080
            self.hero.heroy_position = 640
            self.villain.villainx_position = 50
            self.villain.villainy_position = 40
            music.play_once("rezero return by death sound effect")
            pygame.mixer.music.set_pos(1)

    def first_meet_villain(self): #Первая встреча со злодеем, включение погони через 17 сек

        self.collision_villain = self.villain.villain_icon.get_rect(topleft = (self.villain.villainx_position, self.villain.villainy_position))
        self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))

        if self.first_encounter == False:
            if self.collision_hero.collidelist([self.collision_villain]) != -1: #Буквально, если игрок сталкивается со злодеем, то...
                self.first_encounter = True
                self.dialogue.dialogue_bar_appears = True
                self.music.first_scene = True
                self.hero.hero_can_move = False
                clock.schedule(self.dialogue.next_phrase, 0.7)
                clock.schedule(self.hero.enable_return_by_death_effect,17)
                clock.schedule(self.dialogue.dialogue_bar_appears_off, 17)
                clock.schedule(self.villain.start_chase, 17)
                clock.schedule(self.hero.allow_hero_move, 17)

    def update(self):
        
        self.adjust.adjusting_mode()

        prev_hero_x = self.hero.herox_position
        prev_hero_y = self.hero.heroy_position

        self.hero.hero_controls()

        self.collision_villain = self.villain.villain_icon.get_rect(topleft = (self.villain.villainx_position, self.villain.villainy_position))
        self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))
        self.collision_hero.inflate_ip(-37, -100)
        self.collision_hero.y += 55

        if self.collision_hero.collidelist(self.obstacle.obstacles) != -1:
            self.hero.herox_position = prev_hero_x 
            self.hero.heroy_position = prev_hero_y 

        self.villain.villain_runs_update()

        self.first_meet_villain()
        self.music.villain_first_reply()
        self.hero_return_by_death()

    def draw(self):
        
        screen.clear()
        screen.blit(background, (0, 0))

        self.hero.hero_draw()

        screen.blit(background_decorations, (0, 0))

        if self.collision_hero:
            self.collision_hero = self.hero.image.get_rect(topleft = (self.hero.herox_position, self.hero.heroy_position))
            self.collision_hero.inflate_ip(-37, -100)
            self.collision_hero.y += 55
            screen.draw.rect(self.collision_hero, (200, 0, 0))

        self.adjust.adjusting_mode()

        self.villain.villain_stays_draw()

        self.dialogue.dialogue_bar_icon_draw()
        self.dialogue.villain_talking_draw()

        self.obstacle.show_obstacles()

game = Game()

def update():
    game.update()

def draw():
    game.draw()

pgzrun.go()