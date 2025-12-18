import pygame
import random
import os
import sys

# =====================================================
#  INICIALIZAÇÃO
# =====================================================
pygame.init()

# ---------- CONFIGURAÇÕES ----------
LARGURA = 800
ALTURA = 480
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("The Game...")

# =====================================================
# FUNÇÃO PARA COMPATIBILIDADE COM PYINSTALLER
# =====================================================
def resource_path(rel_path):
    """Retorna o caminho absoluto para um recurso, compatível com PyInstaller.
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.getcwd()))
    return os.path.join(base_path, rel_path)

# =====================================================
# CARREGAMENTO DE ARQUIVOS
# =====================================================
try:
    pygame.display.set_icon(pygame.image.load(resource_path("data/icone.png")))
except:
    pass

FUNDO = pygame.image.load(resource_path("data/jigsaw.png"))
MUSICA = resource_path("data/jogos.mp3")

try:
    pygame.mixer.music.load(MUSICA)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    pass

# =====================================================
#  FUNÇÕES
# =====================================================
def efeito_ruido(surface):
    """Adiciona ruído vermelho/preto estilo Jigsaw."""
    for _ in range(2500):
        x = random.randint(0, surface.get_width()-1)
        y = random.randint(0, surface.get_height()-1)
        cor = (random.randint(80, 150), 0, 0)
        surface.set_at((x, y), cor)


def desenhar_botao(x, y, w, h, texto, acao=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    mouse_sobre = x < mouse[0] < x+w and y < mouse[1] < y+h

    cor_base = (120, 0, 0)
    cor_hover = (170, 0, 0)
    cor_fonte = (230, 230, 230)

    pygame.draw.rect(screen, cor_hover if mouse_sobre else cor_base, (x, y, w, h))

    for _ in range(15):
        xa = random.randint(x, x+w)
        pygame.draw.line(screen, (30, 0, 0), (xa, y), (xa + random.randint(-6, 6), y + 4))
        pygame.draw.line(screen, (30, 0, 0), (xa, y + h), (xa + random.randint(-6, 6), y + h - 4))

    fonte = pygame.font.Font(None, 40)
    label = fonte.render(texto, True, cor_fonte)
    screen.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))

    if mouse_sobre and click:
        pygame.time.delay(150)
        if acao:
            acao()


def iniciar_jogo():
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    total = 5

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        segundos = (pygame.time.get_ticks() - start_ticks) // 1000
        restante = total - segundos

        if restante <= 0:
            rodando = False
            break

        screen.blit(FUNDO, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 60)
        t = font.render(f"O jogo começa em {restante}", True, (200, 0, 0))
        screen.blit(t, (LARGURA//2 - t.get_width()//2, ALTURA//2 - t.get_height()//2))

        pygame.display.update()
        clock.tick(30)


def opcoes():
    ajustando = True
    volume = pygame.mixer.music.get_volume()

    while ajustando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_ESCAPE:
                    ajustando = False

        screen.blit(FUNDO, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 50)
        texto = font.render("Ajuste o volume da música:", True, (200, 0, 0))
        screen.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 60))

        vol_info = font.render(f"Volume: {int(volume * 100)}%", True, (200, 0, 0))
        screen.blit(vol_info, (LARGURA//2 - vol_info.get_width()//2, ALTURA//2))

        inst = font.render("UP/DOWN para ajustar, ESC para sair", True, (200, 0, 0))
        screen.blit(inst, (LARGURA//2 - inst.get_width()//2, ALTURA//2 + 60))

        pygame.display.update()


# =====================================================
#  TETRIS COM TEMA JIGSAW
# =====================================================
class TetrisPeca:
    """Representação de uma peça de Tetris."""
    PECAS = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1, 0], [0, 1, 1]],  # Z
        [[1, 0, 0], [1, 1, 1]],  # J
        [[0, 0, 1], [1, 1, 1]],  # L
        [[0, 1, 0], [1, 1, 1]],  # T
    ]

    def __init__(self):
        self.forma = random.choice(self.PECAS)
        self.cor = random.choice([(200, 0, 0), (150, 0, 0), (100, 0, 0), (180, 0, 0)])
        self.x = 3
        self.y = 0

    def rotacionar(self):
        """Rotaciona a peça 90 graus."""
        nova_forma = []
        for i in range(len(self.forma[0])):
            linha = []
            for j in range(len(self.forma) - 1, -1, -1):
                linha.append(self.forma[j][i])
            nova_forma.append(linha)
        self.forma = nova_forma

    def get_blocos(self):
        """Retorna as coordenadas absolutas dos blocos da peça."""
        blocos = []
        for i, linha in enumerate(self.forma):
            for j, bloco in enumerate(linha):
                if bloco:
                    blocos.append((self.x + j, self.y + i))
        return blocos


class TetrisGame:
    """Jogo Tetris com tema Jigsaw."""
    LARGURA_GRADE = 10
    ALTURA_GRADE = 20
    TAM_BLOCO = 20

    def __init__(self):
        self.grade = [[0] * self.LARGURA_GRADE for _ in range(self.ALTURA_GRADE)]
        self.peca_atual = TetrisPeca()
        self.pontos = 0
        self.game_over = False
        self.relogio = pygame.time.Clock()

    def pode_mover(self, peca, dx, dy):
        """Verifica se a peça pode se mover."""
        for x, y in peca.get_blocos():
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= self.LARGURA_GRADE or ny >= self.ALTURA_GRADE:
                return False
            if ny >= 0 and self.grade[ny][nx]:
                return False
        return True

    def fixar_peca(self):
        """Fixa a peça na grade."""
        for x, y in self.peca_atual.get_blocos():
            if 0 <= y < self.ALTURA_GRADE:
                self.grade[y][x] = self.peca_atual.cor
        self.peca_atual = TetrisPeca()
        if not self.pode_mover(self.peca_atual, 0, 0):
            self.game_over = True

    def limpar_linhas(self):
        """Remove linhas completas e aumenta pontos."""
        linhas_removidas = 0
        for i in range(self.ALTURA_GRADE - 1, -1, -1):
            if all(self.grade[i]):
                linhas_removidas += 1
                del self.grade[i]
                self.grade.insert(0, [0] * self.LARGURA_GRADE)
        self.pontos += linhas_removidas * 100

    def atualizar(self):
        """Atualiza o estado do jogo."""
        if not self.pode_mover(self.peca_atual, 0, 1):
            self.fixar_peca()
            self.limpar_linhas()
        else:
            self.peca_atual.y += 1

    def desenhar(self, surface):
        """Desenha o jogo Tetris."""
        x_offset = 300
        y_offset = 50

        # Desenha a grade
        for y in range(self.ALTURA_GRADE):
            for x in range(self.LARGURA_GRADE):
                rect = pygame.Rect(
                    x_offset + x * self.TAM_BLOCO,
                    y_offset + y * self.TAM_BLOCO,
                    self.TAM_BLOCO,
                    self.TAM_BLOCO
                )
                if self.grade[y][x]:
                    pygame.draw.rect(surface, self.grade[y][x], rect)
                pygame.draw.rect(surface, (50, 0, 0), rect, 1)

        # Desenha a peça atual
        for x, y in self.peca_atual.get_blocos():
            rect = pygame.Rect(
                x_offset + x * self.TAM_BLOCO,
                y_offset + y * self.TAM_BLOCO,
                self.TAM_BLOCO,
                self.TAM_BLOCO
            )
            pygame.draw.rect(surface, self.peca_atual.cor, rect)
            pygame.draw.rect(surface, (100, 0, 0), rect, 2)

        # Desenha a pontuação
        font = pygame.font.Font(None, 40)
        pontos_texto = font.render(f"Pontos: {self.pontos}", True, (200, 0, 0))
        surface.blit(pontos_texto, (50, 100))

        if self.game_over:
            font_go = pygame.font.Font(None, 60)
            game_over_texto = font_go.render("GAME OVER!", True, (200, 0, 0))
            surface.blit(game_over_texto, (LARGURA // 2 - game_over_texto.get_width() // 2, ALTURA // 2 - 100))


def jogar_tetris():
    """Loop principal do Tetris."""
    jogo = TetrisGame()
    tetris_rodando = True
    velocidade_queda = 500  # ms

    while tetris_rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if jogo.pode_mover(jogo.peca_atual, -1, 0):
                        jogo.peca_atual.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if jogo.pode_mover(jogo.peca_atual, 1, 0):
                        jogo.peca_atual.x += 1
                elif event.key == pygame.K_UP:
                    jogo.peca_atual.rotacionar()
                elif event.key == pygame.K_DOWN:
                    if jogo.pode_mover(jogo.peca_atual, 0, 1):
                        jogo.peca_atual.y += 1
                elif event.key == pygame.K_ESCAPE:
                    tetris_rodando = False

        screen.blit(FUNDO, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(100)
        screen.blit(overlay, (0, 0))

        jogo.atualizar()
        jogo.desenhar(screen)

        font_instrucoes = pygame.font.Font(None, 30)
        instr = font_instrucoes.render("Setas: mover, UP: girar, ESC: voltar", True, (200, 0, 0))
        screen.blit(instr, (50, 400))

        pygame.display.update()
        jogo.relogio.tick(60)


# =====================================================
#  LOOP PRINCIPAL
# =====================================================
ruido = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
efeito_ruido(ruido)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(FUNDO, (0, 0))

    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(100)
    screen.blit(overlay, (0, 0))

    screen.blit(ruido, (0, 0))

    fonte_titulo = pygame.font.Font(None, 80)
    titulo = fonte_titulo.render("Let’s Play a Game", True, (200, 0, 0))
    screen.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 40))

    desenhar_botao(250, 170, 300, 60, "INICIAR JOGO", iniciar_jogo)
    desenhar_botao(250, 250, 300, 60, "TETRIS", jogar_tetris)
    desenhar_botao(250, 330, 300, 60, "OPÇÕES", opcoes)

    pygame.display.update()

pygame.quit()
