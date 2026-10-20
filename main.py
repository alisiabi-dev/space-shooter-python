from functools import lru_cache
from pathlib import Path
import random
import sys

import pygame

from data import list_of_images, list_of_sounds


BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
FPS = 60
WINDOW_SIZE = (1312, 738)


@lru_cache(maxsize=None)
def load_image(relative_path):
    """Load an image from the project assets and reuse it across frames."""
    asset_path = BASE_DIR / relative_path
    if not asset_path.is_file():
        raise FileNotFoundError(f"Image asset not found: {asset_path}")

    image = pygame.image.load(str(asset_path))
    if pygame.display.get_surface() is not None:
        image = image.convert_alpha()
    return image


@lru_cache(maxsize=None)
def load_sound(relative_path):
    """Load a sound from the project assets and reuse the sound object."""
    asset_path = BASE_DIR / relative_path
    if not asset_path.is_file():
        raise FileNotFoundError(f"Sound asset not found: {asset_path}")
    return pygame.mixer.Sound(str(asset_path))


class Game:

    def __init__(self):
        self.stones_pos3 = None
        self.stones_pos2 = None
        self.stones_pos1 = None
        self.boss_rect = None
        pygame.init()
        pygame.display.set_caption("Space Shooter")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.start_btn_rect = None
        self.mouse_rect = None
        self.stone_pos1 = None
        self.stone_pos2 = None
        self.stone_pos3 = None
        self.skin = 1
        self.reset_stone_pos = False
        self.keys = [False, False, False, False]
        self.main_menu_active = True
        self.level_select_active = False
        self.game_active = False
        self.info_screen_active = True
        self.player_pos = None
        self.screen_photo = load_image(list_of_images[0]['Image'])
        self.bg_sound = load_sound(list_of_sounds[1]['address'])
        self.shot_sound = load_sound(list_of_sounds[3]['address'])
        self.stone = None
        self.stone1 = None
        self.stone2 = None
        self.random_num = random.randrange(5, 10)
        self.random_num1 = random.randrange(5, 10)
        self.random_num2 = random.randrange(5, 10)
        self.score = 0
        self.player_rect = None
        self.stones_rect = None
        self.stones_rect1 = None
        self.stones_rect2 = None
        self.loss = 1
        self.reset_key = False
        self.reset_key1 = False
        self.reset_key2 = False
        self.font_size = 70
        self.best_score = 0
        self.font = pygame.font.Font(None, self.font_size)
        self.shot = False
        self.start_shot = False
        self.level_rect1 = None
        self.level_rect2 = None
        self.level_rect3 = None
        self.level_rect4 = None
        self.level_rect5 = None
        self.choose_skin_rect = None
        self.player1 = None
        self.player2 = None
        self.player3 = None
        self.player1_rect = None
        self.player2_rect = None
        self.player3_rect = None
        self.back_button_rect = None
        # for shot
        self.arrow = load_image(list_of_images[12]['Image'])
        self.arrow_rect = self.arrow.get_rect()
        self.arrow_rect[0] = 1312
        self.win_level = 0
        self.information_rect = None
        self.choose_skin_key = False
        self.boss_arrow = None
        self.boss_arrow_rect = None
        self.boss_arrow_speed = 15
        self.boss_start_shot = True
        self.boss_shot = True

    def run(self):
        """Run the game loop."""
        try:
            while True:
                self.show_main_menu()
                self.show_level_selection()
        finally:
            pygame.quit()

    def handle_quit_event(self, event_name):
        if event_name.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def draw_main_menu(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        self.screen_photo = load_image(list_of_images[0]['Image'])
        self.screen.blit(self.screen_photo, (0, 0))

        information = load_image(list_of_images[25]['Image'])
        self.screen.blit(information, (5, 8))
        self.information_rect = pygame.Rect(information.get_rect())
        self.information_rect[0], self.information_rect[1] = 5, 8

        choose_skin = load_image(list_of_images[26]['Image'])
        self.screen.blit(choose_skin, (1090, 15))
        self.choose_skin_rect = pygame.Rect(choose_skin.get_rect())
        self.choose_skin_rect[0], self.choose_skin_rect[1] = 1090, 15

        start_btn = load_image(list_of_images[14]['Image'])
        self.screen.blit(start_btn, (530, 350))
        # draw start button rect
        start_btn_coordinates = []
        start_btn_coordinates += start_btn.get_rect()
        start_btn_coordinates[0] = 530
        start_btn_coordinates[1] = 350
        self.start_btn_rect = pygame.Rect(start_btn_coordinates)

    def draw_skin_selection(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        self.screen_photo = load_image(list_of_images[0]['Image'])
        self.screen.blit(self.screen_photo, (0, 0))

        self.player1 = load_image(list_of_images[1]['Image'])
        self.screen.blit(self.player1, (350, 500))
        self.player1_rect = pygame.Rect(self.player1.get_rect())
        self.player1_rect[0], self.player1_rect[1] = 350, 500

        self.player2 = load_image(list_of_images[2]['Image'])
        self.screen.blit(self.player2, (550, 500))
        self.player2_rect = pygame.Rect(self.player2.get_rect())
        self.player2_rect[0], self.player2_rect[1] = 550, 500

        self.player3 = load_image(list_of_images[3]['Image'])
        self.screen.blit(self.player3, (750, 500))
        self.player3_rect = pygame.Rect(self.player3.get_rect())
        self.player3_rect[0], self.player3_rect[1] = 750, 500

        back_button = load_image(list_of_images[23]['Image'])
        self.screen.blit(back_button, (10, 20))
        self.back_button_rect = pygame.Rect(back_button.get_rect())
        self.back_button_rect[0], self.back_button_rect[1] = 10, 10

        showing = True

        return showing

    def show_main_menu(self):
        skin_num = 0
        while self.main_menu_active:
            if not self.choose_skin_key:
                self.draw_main_menu()
                while self.main_menu_active and not self.choose_skin_key:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.update_mouse_rect()
                            if self.start_btn_rect.colliderect(self.mouse_rect):
                                # close
                                self.main_menu_active = False
                                self.level_select_active = True
                            if self.information_rect.colliderect(self.mouse_rect):
                                self.main_menu_active = False
                                self.info_screen_active = True
                                self.show_info_screen()
                            if self.choose_skin_rect.colliderect(self.mouse_rect):
                                self.choose_skin_key = True

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()
                    self.clock.tick(FPS)

            if self.choose_skin_key:

                showing = self.draw_skin_selection()
                enter_btn = load_image(list_of_images[27]['Image'])
                enter_rect = pygame.Rect(enter_btn.get_rect())
                enter_rect[0], enter_rect[1] = 900, 300

                while self.main_menu_active and self.choose_skin_key:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.update_mouse_rect()

                            if enter_rect.colliderect(self.mouse_rect):
                                if skin_num > 0:
                                    self.skin = skin_num

                            if self.back_button_rect.colliderect(self.mouse_rect):
                                self.choose_skin_key = False

                            if self.player1_rect.colliderect(self.mouse_rect):
                                if showing:
                                    skin_num = 1
                                    self.screen.blit(enter_btn, (900, 300))
                                    self.screen.blit(pygame.transform.scale2x(self.player1), (470, 200))
                                    showing = False
                                else:
                                    skin_num = 0
                                    showing = self.draw_skin_selection()
                            if self.player2_rect.colliderect(self.mouse_rect):
                                if showing:
                                    skin_num = 2
                                    self.screen.blit(enter_btn, (900, 300))
                                    self.screen.blit(pygame.transform.scale2x(self.player2), (470, 200))
                                    showing = False
                                else:
                                    skin_num = 0
                                    showing = self.draw_skin_selection()
                            if self.player3_rect.colliderect(self.mouse_rect):
                                if showing:
                                    skin_num = 3
                                    self.screen.blit(enter_btn, (900, 300))
                                    self.screen.blit(pygame.transform.scale2x(self.player3), (470, 200))
                                    showing = False
                                else:
                                    skin_num = 0
                                    showing = self.draw_skin_selection()

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()
                    self.clock.tick(FPS)

    def update_mouse_rect(self):
        mouse_pos = []
        mouse_pos += pygame.mouse.get_pos()
        mouse_pos += 1, 1
        self.mouse_rect = pygame.Rect(mouse_pos)

    def draw_level_selection(self, bg_num, level1_num, level2_num, level3_num, level4_num, level5_num):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        self.screen_photo = load_image(list_of_images[0]['Image'])
        self.screen.blit(self.screen_photo, (0, 0))

        levels_bg = load_image(list_of_images[22][bg_num])
        self.screen.blit(levels_bg, (0, 0))

        level1 = load_image(list_of_images[17][level1_num])
        self.screen.blit(level1, (140, 510))
        self.level_rect1 = level1.get_rect()
        self.level_rect1[0], self.level_rect1[1] = 140, 510

        level2 = load_image(list_of_images[18][level2_num])
        self.screen.blit(level2, (140, 39))
        self.level_rect2 = level2.get_rect()
        self.level_rect2[0], self.level_rect2[1] = 140, 39

        level3 = load_image(list_of_images[19][level3_num])
        self.screen.blit(level3, (720, 35))
        self.level_rect3 = level3.get_rect()
        self.level_rect3[0], self.level_rect3[1] = 720, 35

        level4 = load_image(list_of_images[20][level4_num])
        self.screen.blit(level4, (750, 510))
        self.level_rect4 = level4.get_rect()
        self.level_rect4[0], self.level_rect4[1] = 750, 510

        level5 = load_image(list_of_images[21][level5_num])
        self.screen.blit(level5, (1130, 510))
        self.level_rect5 = level5.get_rect()
        self.level_rect5[0], self.level_rect5[1] = 1130, 510

    def show_level_selection(self):
        if self.win_level == 0:
            self.draw_level_selection('Image', 'Image', 'Image', 'Image', 'Image', 'Image')
        if self.win_level == 1:
            self.draw_level_selection('Image1', 'Image1', 'Image', 'Image', 'Image', 'Image')
        if self.win_level == 2:
            self.draw_level_selection('Image2', 'Image1', 'Image1', 'Image', 'Image', 'Image')
        if self.win_level == 3:
            self.draw_level_selection('Image3', 'Image1', 'Image1', 'Image1', 'Image', 'Image')
        if self.win_level == 4:
            self.draw_level_selection('Image4', 'Image1', 'Image1', 'Image1', 'Image1', 'Image')
        if self.win_level == 5:
            self.draw_level_selection('Image4', 'Image1', 'Image1', 'Image1', 'Image1', 'Image1')
        while self.level_select_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.update_mouse_rect()
                    if self.level_rect1.colliderect(self.mouse_rect):
                        self.level_select_active = False
                        self.game_active = True
                        self.play_level(7, 1)

                    if self.win_level >= 1:
                        if self.level_rect2.colliderect(self.mouse_rect):
                            self.level_select_active = False
                            self.game_active = True
                            self.play_level(14, 2)

                    if self.win_level >= 2:
                        if self.level_rect3.colliderect(self.mouse_rect):
                            self.level_select_active = False
                            self.game_active = True
                            self.play_level(20, 3)

                    if self.win_level >= 3:
                        if self.level_rect4.colliderect(self.mouse_rect):
                            self.level_select_active = False
                            self.game_active = True
                            self.play_level(27, 4)

                    if self.win_level >= 4:
                        if self.level_rect5.colliderect(self.mouse_rect):
                            self.level_select_active = False
                            self.game_active = True
                            self.play_level(35, 5)

            # update and set fps
            pygame.display.update()
            self.clock.tick(FPS)

    def draw_stone(self, stone_pos, random_num):
        stone_img = load_image(list_of_images[random_num]['Image'])
        self.screen.blit(stone_img, stone_pos)
        rect_name = pygame.Rect(stone_img.get_rect())
        rect_name[0], rect_name[1] = stone_pos[0], stone_pos[1]
        stone_pos[0] -= 15

        if stone_pos[0] < -150:
            self.reset_stone_pos = True
        else:
            self.reset_stone_pos = False

        return rect_name

    def update_player(self):
        player = load_image(list_of_images[self.skin]['Image'])
        self.screen.blit(player, self.player_pos)
        self.player_rect = pygame.Rect(player.get_rect())
        self.player_rect[0], self.player_rect[1] = self.player_pos[0], self.player_pos[1]

        for events in pygame.event.get():
            self.handle_quit_event(events)
            # ifs for movement
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_UP:
                    self.keys[0] = True
                elif events.key == pygame.K_LEFT:
                    self.keys[1] = True
                elif events.key == pygame.K_DOWN:
                    self.keys[2] = True
                elif events.key == pygame.K_RIGHT:
                    self.keys[3] = True

            if events.type == pygame.KEYUP:
                if events.key == pygame.K_UP:
                    self.keys[0] = False
                elif events.key == pygame.K_LEFT:
                    self.keys[1] = False
                elif events.key == pygame.K_DOWN:
                    self.keys[2] = False
                elif events.key == pygame.K_RIGHT:
                    self.keys[3] = False

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_SPACE:
                    self.shot = True
                    if self.arrow_rect.x >= 1312:
                        self.start_shot = True

        # Complete ifs for movement
        if self.keys[0] and self.player_rect[1] >= 0:
            self.player_pos[1] -= 15
        if self.keys[2] and self.player_rect[1] <= 632:
            self.player_pos[1] += 15
        if self.keys[1] and self.player_rect[0] >= 0:
            self.player_pos[0] -= 15
        if self.keys[3] and self.player_rect[0] <= 1162:
            self.player_pos[0] += 15

    def reset_after_hit(self, key, key2):
        if key:
            game_over_sound = load_sound(list_of_sounds[0]['address'])
            game_over_sound.play()
            if key2:
                self.loss = 2
        self.keys[0], self.keys[1], self.keys[2], self.keys[3] = False, False, False, False
        self.arrow_rect = self.arrow.get_rect()
        self.arrow_rect[0] = 1312

    def spawn_stone(self):
        self.score += 1
        pos = [1310, random.randrange(0, 588)]
        random_num = random.randrange(5, 10)

        return pos, random_num

    def shoot_player_projectile(self):

        if self.shot:
            if self.start_shot:
                self.shot_sound.play()
                self.arrow_rect.midright = self.player_rect.midright
            self.start_shot = False
            self.arrow_rect.x += 15
            self.screen.blit(self.arrow, self.arrow_rect)

    def shoot_boss_projectile(self):

        if self.boss_shot:
            if self.boss_start_shot:
                self.boss_arrow_rect.midleft = self.boss_rect.midleft
            self.boss_start_shot = False
            self.boss_arrow_rect.x -= self.boss_arrow_speed
            self.screen.blit(self.boss_arrow, self.boss_arrow_rect)

    def play_level(self, number, win_status):

        self.stones_pos1 = [1310, random.randrange(0, 588)]
        self.stones_pos2 = [1480, random.randrange(0, 588)]
        self.stones_pos3 = [1520, random.randrange(0, 588)]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.player_pos = [100, 100]
        self.bg_sound.play()
        break_sound = load_sound(list_of_sounds[2]['address'])
        boss_pos = [1050, 450]
        boss_mov = False
        self.boss_arrow = load_image(list_of_images[29]['Image'])
        self.boss_arrow_rect = pygame.Rect(self.boss_arrow.get_rect())
        self.boss_arrow_rect.x = 1312
        boss_health = 10

        while self.game_active:
            if self.loss == 1:
                self.screen.blit(self.screen_photo, (0, 0))
                self.update_player()

                score_img = self.font.render(str(self.score), True, 'yellow')
                self.screen.blit(score_img, (1250, 20))
                target_img = self.font.render(str(number), True, 'red')
                self.screen.blit(target_img, (1250, 70))

                self.shoot_player_projectile()

                # stones
                if self.reset_key:
                    self.stones_pos1, self.random_num = self.spawn_stone()
                if self.reset_key1:
                    self.stones_pos2, self.random_num1 = self.spawn_stone()
                if self.reset_key2:
                    self.stones_pos3, self.random_num2 = self.spawn_stone()

                self.stones_rect = self.draw_stone(self.stones_pos1, self.random_num)
                if self.arrow_rect.colliderect(self.stones_rect):
                    break_sound.play()
                    self.stones_pos1, self.random_num = self.spawn_stone()
                    self.arrow_rect = self.arrow.get_rect()
                    self.arrow_rect[0] = 1312
                if self.player_rect.colliderect(self.stones_rect):
                    self.reset_after_hit(True, True)
                if self.reset_stone_pos:
                    self.stones_pos1, self.random_num = self.spawn_stone()

                if self.score >= 2:
                    self.stones_rect1 = self.draw_stone(self.stones_pos2, self.random_num1)
                    if self.arrow_rect.colliderect(self.stones_rect1):
                        break_sound.play()
                        self.stones_pos2, self.random_num1 = self.spawn_stone()
                        self.arrow_rect = self.arrow.get_rect()
                        self.arrow_rect[0] = 1312
                    if self.player_rect.colliderect(self.stones_rect1):
                        self.reset_after_hit(True, True)
                    if self.reset_stone_pos:
                        self.stones_pos2, self.random_num1 = self.spawn_stone()

                if self.score >= 5:
                    self.stones_rect2 = self.draw_stone(self.stones_pos3, self.random_num2)
                    if self.arrow_rect.colliderect(self.stones_rect2):
                        break_sound.play()
                        self.stones_pos3, self.random_num2 = self.spawn_stone()
                        self.arrow_rect = self.arrow.get_rect()
                        self.arrow_rect[0] = 1312
                    if self.player_rect.colliderect(self.stones_rect2):
                        self.reset_after_hit(True, True)
                    if self.reset_stone_pos:
                        self.stones_pos3, self.random_num2 = self.spawn_stone()

                if self.score >= number and self.score != 35:
                    self.loss = 3
                    if self.win_level <= win_status:
                        self.win_level = win_status

                if self.score >= 35:
                    self.loss = 4

            if self.loss == 2:
                self.screen.blit(self.screen_photo, (0, 0))

                score_img = self.font.render(f"score:{str(self.score)}", True, 'orange')
                self.screen.blit(score_img, (850, 250))
                if self.score > self.best_score:
                    self.best_score = self.score
                best_score_img = self.font.render(f"best_score:{str(self.best_score)}", True, 'green')
                self.screen.blit(best_score_img, (800, 350))

                game_over_img = load_image(list_of_images[15]['Image'])
                self.screen.blit(game_over_img, (300, 80))

                try_again_button = load_image(list_of_images[16]['Image'])
                self.screen.blit(try_again_button, (500, 400))
                try_again_button_rect = pygame.Rect(try_again_button.get_rect())
                try_again_button_rect[0], try_again_button_rect[1] = 500, 400

                back_button = load_image(list_of_images[23]['Image'])
                self.screen.blit(back_button, (10, 20))
                back_button_rect = pygame.Rect(back_button.get_rect())
                back_button_rect[0], back_button_rect[1] = 10, 20

                for events in pygame.event.get():
                    self.handle_quit_event(events)
                    if events.type == pygame.MOUSEBUTTONDOWN:
                        self.update_mouse_rect()
                        if try_again_button_rect.colliderect(self.mouse_rect):
                            self.stones_pos1 = [1310, random.randrange(0, 588)]
                            self.stones_pos2 = [1480, random.randrange(0, 588)]
                            self.stones_pos3 = [1520, random.randrange(0, 588)]
                            self.screen = pygame.display.set_mode(WINDOW_SIZE)
                            self.player_pos = [100, 100]
                            self.score = 0
                            self.loss = 1

                        if back_button_rect.colliderect(self.mouse_rect):
                            self.score = 0
                            self.best_score = 0
                            self.bg_sound.stop()
                            self.loss = 1
                            self.game_active = False
                            self.main_menu_active = True

            if self.loss == 3:

                self.screen.blit(self.screen_photo, (0, 0))
                win_img = load_image(list_of_images[24]['Image'])
                self.screen.blit(win_img, (450, 200))

                back_button = load_image(list_of_images[23]['Image'])
                self.screen.blit(back_button, (10, 20))
                back_button_rect = pygame.Rect(back_button.get_rect())
                back_button_rect[0], back_button_rect[1] = 10, 10

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.update_mouse_rect()
                        if back_button_rect.colliderect(self.mouse_rect):
                            self.score = 0
                            self.best_score = 0
                            self.bg_sound.stop()
                            self.loss = 1
                            self.game_active = False
                            self.main_menu_active = True
                            self.reset_after_hit(False, False)

            if self.loss == 4:
                self.screen.blit(self.screen_photo, (0, 0))
                self.update_player()
                self.shoot_player_projectile()

                boss = load_image(list_of_images[28]['Image'])
                self.screen.blit(boss, boss_pos)

                score_img = self.font.render(str(boss_health), True, 'red')
                self.screen.blit(score_img, (1250, 20))

                self.boss_rect = pygame.Rect(boss.get_rect())
                self.boss_rect[0], self.boss_rect[1] = boss_pos[0], boss_pos[1]

                if boss_pos[1] <= 0:
                    boss_mov = True

                if boss_pos[1] >= 488:
                    boss_mov = False

                if boss_mov:
                    boss_pos[1] += 10
                if not boss_mov:
                    boss_pos[1] -= 10

                self.shoot_boss_projectile()

                if self.boss_arrow_rect.x <= -250:
                    self.boss_start_shot = True

                if self.arrow_rect.colliderect(self.boss_rect):
                    boss_health -= 1
                    break_sound.play()
                    self.arrow_rect = self.arrow.get_rect()
                    self.arrow_rect[0] = 1312

                if self.boss_arrow_rect.colliderect(self.player_rect):
                    self.reset_after_hit(True, True)
                    boss_pos = [1050, 450]
                    boss_mov = False
                    self.boss_arrow = load_image(list_of_images[29]['Image'])
                    self.boss_arrow_rect = pygame.Rect(self.boss_arrow.get_rect())
                    self.boss_arrow_rect.x = 1312
                    boss_health = 10
                    self.boss_start_shot = True
                    self.boss_arrow_speed = 15

                if boss_health == 8:
                    self.boss_arrow_speed = 20

                if boss_health == 6:
                    self.boss_arrow_speed = 27

                if boss_health == 4:
                    self.boss_arrow_speed = 36

                if boss_health == 2:
                    self.boss_arrow_speed = 48

                if boss_health == 0:
                    self.reset_after_hit(False, False)
                    self.loss = 3
                    boss_pos = [1050, 450]
                    boss_mov = False
                    self.boss_arrow = load_image(list_of_images[29]['Image'])
                    self.boss_arrow_rect = pygame.Rect(self.boss_arrow.get_rect())
                    self.boss_arrow_rect.x = 1312
                    boss_health = 10
                    self.boss_start_shot = True
                    self.boss_arrow_speed = 15
                    self.win_level = 5

            # update and set fps
            pygame.display.update()
            self.clock.tick(FPS)

    def show_info_screen(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        screen_photo = load_image(list_of_images[30]['Image'])
        self.screen.blit(screen_photo, (0, 0))

        back_button = pygame.transform.scale2x(load_image(list_of_images[23]['Image']))
        self.screen.blit(back_button, (30, 350))
        back_button_rect = pygame.Rect(back_button.get_rect())
        back_button_rect[0], back_button_rect[1] = 30, 350

        while self.info_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.update_mouse_rect()
                    if back_button_rect.colliderect(self.mouse_rect):
                        self.info_screen_active = False
                        self.main_menu_active = True

            # update and set fps
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
