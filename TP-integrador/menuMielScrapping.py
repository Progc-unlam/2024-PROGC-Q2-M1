from pickle import TRUE
import pygame
import pygame_menu
import pygame_menu.events
import threading
#from menuScrollBar import on_button_click
from miel_scraper import MielScraper

import time

from typing import Tuple,Any

from miel_scraper import MielScraper

FPS = 60
WINDOW_WIDTH_PYGAME = 800
WINDOW_HEIGHT_PYGAME = 600
WINDOW_SIZE = (WINDOW_WIDTH_PYGAME, WINDOW_HEIGHT_PYGAME)


scraping_done = False
text_input_user = ""
text_input_pass = ""
thislist = ["A", "B", "C","D"]




def simulate_scraping():
    global scraping_done, scraped_data
    time.sleep(5)  
    scraping_done = True



class MenuScraping:
    def __init__(self):
        self.ms = MielScraper()
        
    
    def main(self) -> None:
        #screen = create_example_window('Example - Scrolling Menu', WINDOW_SIZE)
        pygame.init()
        #screen = pygame.display.set_mode(WINDOW_SIZE)  
        pygame.display.set_caption("MielScrapping")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.menu = self.make_login_menu()
        clock = pygame.time.Clock()
        #self.menu = make_login_menu()

        while True:
            clock.tick(FPS)

            self.menu.mainloop(
                surface=self.screen,
                #bgfun=make_main_menu,
                disable_loop=False,
                fps_limit=FPS
            )
            pygame.display.flip()
        
    def make_login_menu(self) -> 'pygame_menu.Menu':
        theme_menu = pygame_menu.themes.THEME_BLUE.copy()
        theme_menu.scrollbar_cursor = pygame_menu.locals.CURSOR_HAND

        # Función que será llamada cuando se intente iniciar sesión
        def on_login():
            # Obtener los valores de los campos de texto
            username = text_input_user.get_value()
            password = text_input_pass.get_value()

            if self.ms.login(username,password):
            #if self.ms.login(username,password):
                # Si las credenciales son correctas, pasa a la pantalla de carga
                self.menu = self.loading_screen(pygame.display.set_mode(WINDOW_SIZE))
                #return loading_screen(pygame.display.set_mode(WINDOW_SIZE))
            else:
                # Si las credenciales son incorrectas, mostrar un mensaje de error
                #TODO si no esta agregar el label, sino nada XD
                self.menu.add.label("Credenciales incorrectas, intenta nuevamente.")
        
        # Crear el menú de login
        self.menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT_PYGAME,
            width=WINDOW_WIDTH_PYGAME,
            theme=theme_menu,
            title='Iniciar sesión'
        )
    
        # Usar 'text_input' con password=True para el campo de la contraseña
        text_input_user = self.menu.add.text_input('Usuario: ', default='', maxchar=30)  # Campo para el nombre de usuario
        text_input_pass = self.menu.add.text_input('Contraseña: ', default='', maxchar=30, password=True)  # Campo para la contraseña con 'password=True'
        self.menu.add.button('Iniciar sesión', on_login)  # Botón de login
        self.menu.add.button('Salir', pygame_menu.events.EXIT)  # Botón de salida
        
        return self.menu

    def change_difficulty(self, value: Tuple[Any, int], difficulty: str) -> None:
        selected, index = value
        print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')

    def make_subject_menu(self) -> 'pygame_menu.Menu':
        theme_menu = pygame_menu.themes.THEME_BLUE.copy()
        theme_menu.scrollbar_cursor = pygame_menu.locals.CURSOR_HAND

        menu_subject = pygame_menu.Menu(
            height=WINDOW_HEIGHT_PYGAME,
            width=WINDOW_WIDTH_PYGAME,
            onclose=pygame_menu.events.EXIT,
            theme=theme_menu,
            title='Subject Menu'
        )
        #crear lista de examples
        
        if (len(thislist) < 1):
            menu_subject.add.label("No hay materias XD")
        

        for i in thislist:
            menu_subject.add.label(i)
            menu_subject.add.selector('Select difficulty ',
                            [('1 - Easy', 'EASY'),
                                ('2 - Medium', 'MEDIUM'),
                                ('3 - Hard', 'HARD')],
                            onchange=self.change_difficulty)
                            #selector_id='select_difficulty')

        menu_subject.add.button('Exit', pygame_menu.events.EXIT)
        return menu_subject



    def make_main_menu(self) -> 'pygame_menu.Menu':
        theme_menu = pygame_menu.themes.THEME_BLUE.copy()
        theme_menu.scrollbar_cursor = pygame_menu.locals.CURSOR_HAND

        menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT_PYGAME,
            width=WINDOW_WIDTH_PYGAME,
            onclose=pygame_menu.events.EXIT,
            theme=theme_menu,
            title='Select Menu'
        )
        #crear lista de examples
        thislist = ["apple", "banana", "cherry"]
        #for i in thislist:
            ##menu.add.button(i,on_button_click,f'Button n°{i}')
        menu.add.button('Exit', pygame_menu.events.EXIT)
        return menu

    # Función para la pantalla de carga
    def loading_screen(self,screen):
        #font = pygame.font.SysFont('Arial', 30)
        theme_menu = pygame_menu.themes.THEME_BLUE.copy()
        font_name = theme_menu.title_font 
        font_size = 50  
        font = pygame.font.SysFont(font_name, font_size) 


        loading_text = font.render("Cargando...", True, (0, 0, 0))
        loading_rect = loading_text.get_rect(center=(WINDOW_WIDTH_PYGAME // 2, WINDOW_HEIGHT_PYGAME // 3))

        image = pygame.image.load("./OutOfRangePresenta.png")
        #image_rect = image.get_rect(center=(WINDOW_WIDTH_PYGAME // 2, WINDOW_HEIGHT_PYGAME // 4))

        window_width, window_height = WINDOW_SIZE

        # Escalar la imagen para que cubra toda la ventana, puede distorsionarla
        image = pygame.transform.scale(image, (window_width, window_height))

        # Obtener el rectángulo de la imagen escalada
        image_rect = image.get_rect()

        # Barra de progreso
        progress_bar_width = 400
        progress_bar_height = 30
        progress_rect = pygame.Rect((WINDOW_WIDTH_PYGAME // 2 - progress_bar_width // 2, WINDOW_HEIGHT_PYGAME // 2),
                                    (progress_bar_width, progress_bar_height))

        progress = 0  # Empieza en 0%
        increment = 1  # Aumentamos un 1% por ciclo de actualización

        # Llamamos al hilo de scraping
        self.ms.get_files_to_download()
        hilito1 = threading.Thread(target=self.ms.download_files, daemon=True)
        #hilito1 = threading.Thread(target=simulate_scraping, daemon=True)
        hilito1.start()

        # Mantener la pantalla de carga visible hasta que scraping_done sea True
        while not progress==99:
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         return

            # Limpiar pantalla
            screen.fill((0, 0, 0))
            
            screen.blit(image, image_rect)

            # Dibujar texto de carga
            screen.blit(loading_text, loading_rect)

            # Dibujar la barra de progreso
            pygame.draw.rect(screen, (200, 200, 200), progress_rect)  # Fondo de la barra
            pygame.draw.rect(screen, (0, 255, 0), (progress_rect.x, progress_rect.y, progress * 4, progress_bar_height))  # Progreso

            # Mostrar el porcentaje de carga
            percentage_text = font.render(f"{progress}%", True, (0, 0, 0))
            screen.blit(percentage_text, (WINDOW_WIDTH_PYGAME // 2 - percentage_text.get_width() // 2, progress_rect.y + progress_bar_height + 10))

            # Actualizar pantalla
            pygame.display.flip()

            # Incrementamos el progreso
            progress = min(progress + increment, 99)  # Limitar al 99%

            # Simulamos la carga
            time.sleep(0.05)  # Controlamos la velocidad de incremento

        # Una vez que el scraping haya terminado, mostrar el menú con los datos obtenidos
        # Cuando scraping_done sea True, ponemos el progreso al 100%
        
        hilito1.join()
        progress = 100
        pygame.draw.rect(screen, (200, 200, 200), progress_rect)  # Fondo de la barra
        pygame.draw.rect(screen, (0, 255, 0), (progress_rect.x, progress_rect.y, progress * 4, progress_bar_height))  # Progreso

        # Mostrar el porcentaje de carga al 100%
        percentage_text = font.render(f"{progress}%", True, (0, 0, 0))
        screen.blit(percentage_text, (WINDOW_WIDTH_PYGAME // 2 - percentage_text.get_width() // 2, progress_rect.y + progress_bar_height + 10))

        #pygame.display.flip()
        self.menu= self.make_subject_menu()
        pygame.display.flip()

if __name__ == '__main__':
    menuScraping = MenuScraping()
    menuScraping.main()