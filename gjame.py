import pgzrun
import pygame

image = pygame.transform.scale(images.jopa, (75, 110))
villain = pygame.transform.scale(images.villain, (75, 120))
villain_walk = pygame.transform.scale(images.villain_walk, (75, 120))
background_decorations = pygame.transform.scale(images.background_decoratios, (1280, 720))
background = pygame.transform.scale(images.background, (1280, 720))
dialogue_bar = pygame.transform.scale(images.dialogue_bar, (1000, 255))
villain_full_icon = pygame.transform.scale(images.villain_full_icon, (385, 394))

#Ширина, Высота окна
WIDTH = 1280
HEIGHT = 720

#Скорость и положение Главного Персонажа
hero_can_move = True
speedx = 0
speedy = 0
x = 1080
y = 640

#Положение Злодея, проверка на погоню, встречу, проверка на смену текстурки
villainx = 50
villainy = 40
villain_chase = False
encounter = False
movement_check_scheduled = False

#Хитбоксы героя и злодея
collision_villain = None
collision_main = None

#Проверка на самое первоее нажатие кнопки
button_was_pressed_once = False
button_first_pressed = (0, 0)   

#Появляение диалогового окна
dialogue_bar_appears = False

#Текст в диалоговом окне
phrase_appeared = False
phrases_list = ("Hey", "Hey, you", "What are you doing in a place like this", "I never forget a face when I see it", "You smell simillar", "To a terryifying guy I know")
current_phrase = 0
text_first_state = False

peasful_mode_music = False
music_in_game = "music_game"

music.set_volume(0.3)
music.play(music_in_game)

def villain_chase_texture_manager(): #меняет состояние анимации злодея
    global villain_chase_texture
    global villain_starts_chase_texture
    villain_starts_chase_texture = True
    villain_chase_texture = True

def villain_chase_texture_manager_while_running(): #меняет состояние анимации обратно
    global villain_chase_texture
    villain_chase_texture = False

def adjusting_mode(): #определяет нажатие мыши + рисует рамку
    global button_was_pressed_once
    global button_first_pressed

    pressed_button = pygame.mouse.get_pressed()
    mousepos = pygame.mouse.get_pos()

    if pressed_button[0] == True and button_was_pressed_once == False:
        button_first_pressed = pygame.mouse.get_pos()
        button_was_pressed_once = True
        print(button_first_pressed)
    if button_was_pressed_once == True and pressed_button[0] == True:
        button_still_pressed = pygame.mouse.get_pos()
        rectx = button_still_pressed[0] - button_first_pressed[0]
        recty = button_still_pressed[1] - button_first_pressed[1]
        print(button_first_pressed)
        #print(button_still_pressed)
        if button_first_pressed[0] < button_still_pressed[0] and button_first_pressed[1] < button_still_pressed[1]:
            rect = pygame.Rect(button_first_pressed, (abs(rectx), abs(recty))) #Сделать размер в зависимости от положения мыши.
            box_x = button_first_pressed[0] + rectx
            box_y = button_first_pressed[1] + recty
            box_coord = button_first_pressed, box_x, box_y
            #print(box_coord)
            screen.draw.rect(rect, (200, 0, 0))
        elif button_first_pressed[0] > button_still_pressed[0] and button_first_pressed[1] > button_still_pressed[1]:
            rect = pygame.Rect(button_still_pressed, (abs(rectx), abs(recty)))
            screen.draw.rect(rect, (200, 0, 0))
        elif button_first_pressed[0] < button_still_pressed[0]:
            rect_object1 = button_first_pressed[0], button_still_pressed[1]
            rect = pygame.Rect(rect_object1, (abs(rectx), abs(recty)))
            screen.draw.rect(rect, (200, 0, 0))
        elif button_still_pressed[1] > button_first_pressed[1]:
            rect_object2 = button_still_pressed[0], button_first_pressed[1]
            rect = pygame.Rect(rect_object2, (abs(rectx), abs(recty)))
            screen.draw.rect(rect, (200, 0, 0))
    if pressed_button[0] == False:
        button_was_pressed_once = False
    
def hero_controls(): #Управление через клаву
    global x
    global y
    global speedx
    global speedy

    x += speedx
    y += speedy

    if hero_can_move == True:
        if keyboard.a == True:
            speedx = -5
        elif keyboard.d == True:
            speedx = 5
        else:
            speedx = 0

        if keyboard.w == True:
            speedy = -5
        elif keyboard.s == True:
            speedy = 5
        else:
            speedy = 0
    elif hero_can_move == False:
        speedx = 0
        speedy = 0
    
    #Ограничение по экрану в широте
    if x > WIDTH - image.get_width(): #Здесь что бы понимать, 1280 - 100 = 1180, это предел для картинки, т.к. отсчет начинается с левого верхнего угла, а не с центра картинки
        x =  WIDTH - image.get_width()
    if x < 0:
        x = 0

    #Ограничение по экрану в высоте
    if y > HEIGHT - image.get_height():
        y = HEIGHT - image.get_height()
    if y < 0:
        y = 0

def death_by_villain(): #Смерть от злодея, Первая встреча со злодеем
    global x
    global y
    global villainx
    global villainy
    global villain_chase
    global encounter
    global movement_check_scheduled
    global collision_main
    global collision_villain
    global hero_can_move
    global dialogue_bar_appears
    global peasful_mode_music

    collision_villain = villain.get_rect(topleft = (villainx, villainy))
    collision_main = image.get_rect(topleft = (x, y))

    if encounter == False:
        if collision_main.collidelist([collision_villain]) != -1: #Буквально, если игрок сталкивается со злодеем, то...
            x = villainx + 100
            music.play_once("rezero - todd fang hey you")
            pygame.mixer.music.set_pos(8)
            encounter = True
            movement_check_scheduled = True

    elif movement_check_scheduled == True: # Рестрикты к соприкосновению
        hero_can_move = False
        movement_check_scheduled = False
        dialogue_bar_appears = True
        clock.schedule(next_phrase, 0.7)
        clock.schedule(dialogue_bar_appears_off, 17)
        clock.schedule(villain_movement_check, 17)
        clock.schedule(allow_hero_move, 17)
        if peasful_mode_music == False:
            clock.schedule(music_is_playing, 17)

def villain_stays(): #Злодей стоит, если погони нет
    if villain_chase == False:
        screen.blit(villain, (villainx, villainy))

def villain_runs(): #Бег злодея, если есть погоня
    global villainx
    global villainy

    if villain_chase == True:
        screen.blit(villain_walk, (villainx, villainy))

        if villainx < x:
            villainx += 2
        elif villainx > x:
            villainx -= 2

        if villainy < y:
            villainy += 2
        elif villainy > y:
            villainy -= 2

def allow_hero_move(): #Разрешает ходить герою
    global hero_can_move
    hero_can_move = True

def villain_movement_check(): #Включает погоню за героем
    global villain_chase
    villain_chase = True

def hero_return_by_death(): #Повторные смерти от злодея
    global x
    global y
    global villainx
    global villainy

    if collision_main.collidelist([collision_villain]) != -1 and movement_check_scheduled == False:
        x = 1080
        y = 640
        villainx = 50
        villainy = 40
        music.play_once("rezero return by death sound effect")
        pygame.mixer.music.set_pos(1)

def dialogue_bar_appears_off(): #Выключает диалоговое окно
    global dialogue_bar_appears
    dialogue_bar_appears = False

def dialogue_bar_icon_draw(): #Рисует диалоговое окно
    if dialogue_bar_appears == True:
        screen.blit(dialogue_bar, (150, 500))
        screen.blit(villain_full_icon, (0, 400))
        #screen.draw.text("Vasiliy Axe Guy", (265, 520), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black")

def villain_talking():
    global phrase_appeared
    global current_phrase
    global text_first_state

    if dialogue_bar_appears == True and text_first_state == True:
        if current_phrase == 0:
            screen.draw.text(phrases_list[current_phrase], (300, 600), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black", shadow=(1,1), scolor="#202020")
        elif current_phrase > 0 and current_phrase < 6:
            screen.draw.text(phrases_list[current_phrase], (300, 600), color = (211, 100, 100), fontsize = 45, owidth=1, ocolor="black", shadow=(1,1), scolor="#202020")

def next_phrase():
    global current_phrase
    global text_first_state

    if current_phrase == 0 and text_first_state == False:
        text_first_state = True
        clock.schedule(next_phrase, 1.5)

    elif current_phrase == 0 and text_first_state == True:
        current_phrase += 1
        clock.schedule(next_phrase, 1.4)

    elif current_phrase == 1:
        current_phrase += 1
        clock.schedule(next_phrase, 3.6)

    elif current_phrase == 2:
        current_phrase += 1
        clock.schedule(next_phrase, 2.5)

    elif current_phrase == 3:
        current_phrase += 1
        clock.schedule(next_phrase, 1.5)

    elif current_phrase == 4:
        current_phrase += 1
        clock.schedule(next_phrase, 2.3)

def music_is_playing():
    global peasful_mode_music
    music.set_volume(1)
    music.play(music_in_game)
    peasful_mode_music = True

def update():
    hero_controls()
    death_by_villain()
    hero_return_by_death()
    adjusting_mode()

def draw():
    screen.clear()
    screen.blit(background, (0, 0))
    screen.blit(background_decorations, (0, 0))
    adjusting_mode()
    screen.blit(image, (x, y))
    villain_stays()
    villain_runs()
    dialogue_bar_icon_draw()
    villain_talking()
    if villain_chase == True:
        screen.draw.text("БЕГИ", (WIDTH / 2 - 100, HEIGHT / 2 - 100), color = "red", fontsize = 100)

pgzrun.go()