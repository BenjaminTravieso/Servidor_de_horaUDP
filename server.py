
"""
Servidor de hora UDP 
"""

import socket, datetime, pygame, sys, select

# Configuración (inicial)
IP, PORT      = "0.0.0.0", 12345
BUFFER        = 1024
MAX_LINEAS_GUI = 15

# Socket UDP 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
sock.setblocking(False)               
print(f"Servidor UDP escuchando en {IP}:{PORT}")

# Interfaz Pygame 
pygame.init()
FONT = pygame.font.SysFont("consolas", 18)
W, H = 580, 360
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption(f"Servidor UDP — {IP}:{PORT}")

logs = [f"Servidor iniciado {datetime.datetime.now()}"]

def add_log(text: str):
    print(text)
    logs.append(text)
    if len(logs) > MAX_LINEAS_GUI:
        logs.pop(0)

add_log("Esperando datagramas…")

clock = pygame.time.Clock()
running = True
try:
    while running:
        # 1) Eventos ventana
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        # 2) ¿Llegó el datagrama?
        rlist, _, _ = select.select([sock], [], [], 0)   
        if rlist:
            try:
                data, addr = sock.recvfrom(BUFFER)
            except OSError as e:
                add_log(f"[ERROR recv] {e}")
            else:
                ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    sock.sendto(ahora.encode(), addr)
                except OSError as e:
                    add_log(f"[ERROR send] {e}")
                add_log(f"{addr[0]}:{addr[1]}  →  {ahora}")

        # 3) Dibujar GUI
        screen.fill((30, 34, 38))
        for i, linea in enumerate(logs):
            txt = FONT.render(linea, True, (200, 255, 200))
            screen.blit(txt, (10, 10 + 22 * i))
        pygame.display.flip()
        clock.tick(30)               #30 FPS

finally:
    sock.close()
    pygame.quit()
    sys.exit()