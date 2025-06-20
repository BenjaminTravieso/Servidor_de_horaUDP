
"""
Cliente UDP 
"""

import socket, pygame, sys, time, argparse

# CLI (parametros de conexion)
ap = argparse.ArgumentParser(description="Cliente gráfico UDP (hora)")
ap.add_argument("--host", default="127.0.0.1")
ap.add_argument("--port", type=int, default=12345)
ap.add_argument("--auto", type=int, metavar="SEG",
                help="Intervalo de consulta automática (s). Sin --auto = sólo clic.")
args = ap.parse_args()

HOST, PORT = args.host, args.port

# Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1.5)

def pedir_hora():
    """Devuelve (hora_str, rtt_ms) o (None, None) en caso de fallo."""
    try:
        t0 = time.perf_counter()
        sock.sendto(b"HORA", (HOST, PORT))
        data, _ = sock.recvfrom(64)
        rtt = (time.perf_counter() - t0) * 1000
        return data.decode(), rtt
    except socket.timeout:
        return None, None
    except OSError as e:
        print(f"[ERROR] {e}")
        return None, None

# Interfaz Pygame 
pygame.init()
FONT  = pygame.font.SysFont("consolas", 42, bold=True)
FONT2 = pygame.font.SysFont("consolas", 22)
screen = pygame.display.set_mode((540, 180))
pygame.display.set_caption("Cliente UDP — reloj")

hora   = "--:--:--"
estado = "clic para solicitar"
color  = (50, 120, 50)

# Temporizador automático
if args.auto:
    CONSULTA_EVT = pygame.USEREVENT + 1
    pygame.time.set_timer(CONSULTA_EVT, args.auto * 1000)

running = True
try:
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                h, r = pedir_hora()
                if h:
                    hora, estado = h, f"RTT: {r:.1f} ms"
                    color = (30, 150, 70)
                else:
                    hora, estado = "--:--:--", "sin respuesta"
                    color = (180, 60, 60)
            elif args.auto and ev.type == CONSULTA_EVT:
                # automático
                h, r = pedir_hora()
                if h:
                    hora, estado = h, f"RTT: {r:.1f} ms"
                    color = (30, 150, 70)
                else:
                    hora, estado = "--:--:--", "timeout"
                    color = (180, 60, 60)

        screen.fill(color)
        screen.blit(FONT.render(hora, True, (255, 255, 255)), (40, 40))
        screen.blit(FONT2.render(estado, True, (240, 240, 240)), (40, 110))
        pygame.display.flip()

finally:
    sock.close()
    pygame.quit()
    sys.exit()