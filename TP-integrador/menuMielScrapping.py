import pygame
import pygame_menu
import pygame_menu.events
import threading
from menuScrollBar import on_button_click

import time

from typing import Tuple,Any

FPS = 60
WINDOW_WIDTH_PYGAME = 800
WINDOW_HEIGHT_PYGAME = 600
WINDOW_SIZE = (WINDOW_WIDTH_PYGAME, WINDOW_HEIGHT_PYGAME)

thislist = ["A", "B", "C","D"]
scraping_done = False

def simulate_scraping():
    global scraping_done, scraped_data
    time.sleep(15)  
    scraping_done = True

def change_difficulty(value: Tuple[Any, int], difficulty: str) -> None:
    selected, index = value
    print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')

def make_subject_menu() -> 'pygame_menu.Menu':
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
                           onchange=change_difficulty)
                           #selector_id='select_difficulty')

    menu_subject.add.button('Exit', pygame_menu.events.EXIT)
    return menu_subject



def make_main_menu() -> 'pygame_menu.Menu':
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
    for i in thislist:
        menu.add.button(i,on_button_click,f'Button n°{i}')
    menu.add.button('Exit', pygame_menu.events.EXIT)
    return menu

# Función para la pantalla de carga
def loading_screen(screen):
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
    threading.Thread(target=simulate_scraping, daemon=True).start()

    # Mantener la pantalla de carga visible hasta que scraping_done sea True
    while not scraping_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

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
    progress = 100
    pygame.draw.rect(screen, (200, 200, 200), progress_rect)  # Fondo de la barra
    pygame.draw.rect(screen, (0, 255, 0), (progress_rect.x, progress_rect.y, progress * 4, progress_bar_height))  # Progreso

    # Mostrar el porcentaje de carga al 100%
    percentage_text = font.render(f"{progress}%", True, (0, 0, 0))
    screen.blit(percentage_text, (WINDOW_WIDTH_PYGAME // 2 - percentage_text.get_width() // 2, progress_rect.y + progress_bar_height + 10))

    pygame.display.flip()

    time.sleep(0.5)  # Pausa breve antes de cambiar al menú

    return make_subject_menu()

def main() -> None:

    #screen = create_example_window('Example - Scrolling Menu', WINDOW_SIZE)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)  
    pygame.display.set_caption("MielScrapping")

    clock = pygame.time.Clock()
    menu = loading_screen(screen)

    while True:
        clock.tick(FPS)

        menu.mainloop(
            surface=screen,
            #bgfun=make_main_menu,
            disable_loop=False,
            fps_limit=FPS
        )
        pygame.display.flip()

if __name__ == '__main__':
    main()