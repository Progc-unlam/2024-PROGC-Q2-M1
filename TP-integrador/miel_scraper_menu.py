import threading
import time

import pygame
import pygame_menu
import pygame_menu.events
from miel_scraper import MielScraper

FPS = 60
WINDOW_WIDTH_PYGAME = 800
WINDOW_HEIGHT_PYGAME = 600
WINDOW_SIZE = (WINDOW_WIDTH_PYGAME, WINDOW_HEIGHT_PYGAME)


scraping_done = False
text_input_user = ""
text_input_pass = ""


class MenuScraping:
    def __init__(self):
        self.ms = MielScraper()
        self.label_error = None

    def main(self) -> None:
        pygame.init()
        pygame.display.set_caption("MielScrapping")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.menu = self.make_login_menu()
        clock = pygame.time.Clock()
        clock.tick(FPS)
        self.menu.mainloop(
            surface=self.screen,
            disable_loop=False,
            fps_limit=FPS,
        )

    def make_login_menu(self) -> 'pygame_menu.Menu':
        theme_menu = pygame_menu.themes.THEME_BLUE.copy()
        theme_menu.scrollbar_cursor = pygame_menu.locals.CURSOR_HAND
        self.menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT_PYGAME,
            width=WINDOW_WIDTH_PYGAME,
            theme=theme_menu,
            title='Iniciar sesión'
        )
        self.text_input_user = self.menu.add.text_input(
            'Usuario: ', default='', maxchar=30)
        self.text_input_pass = self.menu.add.text_input(
            'Contraseña: ', default='', maxchar=30, password=True)
        self.menu.add.button('Iniciar sesión', self.on_login)
        self.menu.add.button('Salir', pygame_menu.events.EXIT)

        return self.menu

    def on_login(self):
        username = self.text_input_user.get_value()
        password = self.text_input_pass.get_value()
        if self.ms.login(username, password):
            self.loading_screen(pygame.display.set_mode(WINDOW_SIZE))
        else:
            if self.label_error:
                self.menu.remove_widget(self.label_error)

            self.label_error = self.menu.add.label(
                "Credenciales incorrectas, intenta nuevamente.")
            self.label_error.set_background_color(color=(255, 0, 0))

    def loading_screen(self, screen):
        theme_menu = pygame_menu.themes.THEME_BLUE.copy()
        font_name = theme_menu.title_font
        font_size = 50
        font = pygame.font.SysFont(font_name, font_size)
        loading_text = font.render("Cargando...", True, (0, 0, 0))
        loading_rect = loading_text.get_rect(
            center=(WINDOW_WIDTH_PYGAME // 2, WINDOW_HEIGHT_PYGAME // 3))
        imageBackgroundCharge = pygame.image.load("./OutOfRangePresenta.png")
        window_width, window_height = WINDOW_SIZE
        image = pygame.transform.scale(
            imageBackgroundCharge, (window_width, window_height))
        image_rect = image.get_rect()
        progress_bar_width = 400
        progress_bar_height = 30
        progress_rect = pygame.Rect((WINDOW_WIDTH_PYGAME // 2 - progress_bar_width // 2, WINDOW_HEIGHT_PYGAME // 2),
                                    (progress_bar_width, progress_bar_height))
        progress = 0
        increment = 1
        self.ms.get_files_to_download()
        downLoadThread = threading.Thread(
            target=self.ms.download_files, daemon=True)
        downLoadThread.start()
        while not progress == 99:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    return

            screen.fill((0, 0, 0))
            screen.blit(image, image_rect)
            screen.blit(loading_text, loading_rect)
            pygame.draw.rect(screen, (200, 200, 200), progress_rect)
            pygame.draw.rect(screen, (0, 255, 0), (progress_rect.x,
                             progress_rect.y, progress * 4, progress_bar_height))
            percentage_text = font.render(f"{progress}%", True, (0, 0, 0))
            screen.blit(percentage_text, (WINDOW_WIDTH_PYGAME // 2 -
                        percentage_text.get_width() // 2, progress_rect.y + progress_bar_height + 10))
            pygame.display.flip()
            progress = min(progress + increment, 99)
            time.sleep(0.15)

        while downLoadThread.is_alive():
            print("Descargando")

        downLoadThread.join()
        progress = 100
        pygame.draw.rect(screen, (200, 200, 200), progress_rect)
        pygame.draw.rect(screen, (0, 255, 0), (progress_rect.x,
                         progress_rect.y, progress * 4, progress_bar_height))
        percentage_text = font.render(f"{progress}%", True, (0, 0, 0))
        screen.blit(percentage_text, (WINDOW_WIDTH_PYGAME // 2 -
                    percentage_text.get_width() // 2, progress_rect.y + progress_bar_height + 10))
        pygame.display.flip()
        imageBackgroundCharge = pygame.image.load("./OutOfRangeSaluda.png")
        image = pygame.transform.scale(
            imageBackgroundCharge, (window_width, window_height))
        image_rect = image.get_rect()
        screen.blit(image, image_rect)
        pygame.display.flip()
        time.sleep(2)
        exit()


if __name__ == '__main__':
    menuScraping = MenuScraping()
    menuScraping.main()
