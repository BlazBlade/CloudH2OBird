#Flappy_Bird retro By CloudH2O
import pygame
import random, os


# Setup 设置

pygame.init() #初始化
SCREEN = pygame.display.set_mode((288,512)) # 设置游戏边框为宽288，高512
pygame.display.set_caption('CloudH2O Bird --- By CloudH2O') # 窗口名字
CLOCK = pygame.time.Clock() # 引入pygame时钟模块

# Materials

IMAGES = {} #图片
for image in os.listdir('assets/sprites'):
    name, extension = os.path.splitext(image) #拆分文件名+后缀
    path = os.path.join('assets/sprites', image)
    IMAGES[name] = pygame.image.load(path) #名字作为键，路径为值

AUDIO = {} #音频
for audio in os.listdir('assets/audio'):
    name, extension = os.path.splitext(audio)
    path = os.path.join('assets/audio', audio)
    AUDIO[name] = pygame.mixer.Sound(path)

# Constants 常量
W , H = 288 , 512  # 设置长宽固定为288 * 512 同背景图片相同
FPS = 30  #设置锁帧为30
FLOOR_Y = H - IMAGES['floor'].get_height()


#主程序
def main():
    while True:
        AUDIO['1'].play()
        AUDIO['start'].play()
        IMAGES['bgpic'] = IMAGES[random.choice(['day', 'night'])]
        color = random.choice(['red', 'yellow', 'blue'])
        #使用遍历达到素材读取
        IMAGES['birds'] = [IMAGES[color+'-up'], IMAGES[color+'-mid'], IMAGES[color+'-down']]
        pipe = IMAGES[random.choice(['green-pipe', 'red-pipe'])]
        IMAGES['pipes'] = [pipe, pygame.transform.flip(pipe, False, True)] #水管，第二个是左右互换
        menu_window()#菜单
        result = game_window()#游戏界面
        end_window(result)#结果


def menu_window():

    floor_gap = IMAGES['floor'].get_width() - W  #获取地板贴图和屏幕宽的差值
    floor_x = 0

    #计算图片素材所需位置
    guide_x = (W - IMAGES['guide'].get_width())/2
    guide_y = (FLOOR_Y - IMAGES['guide'].get_height())/2

    bird_x = W * 0.2
    bird_y = (H - IMAGES['birds'][0].get_height())/2
    bird_y_vel = 1 #小鸟运动速度
    bird_y_range = [bird_y - 8, bird_y + 8] #运动范围
    idx = 0
    # frames = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
    repeat = 5  # 控制小鸟飞行画面流畅度
    frames = [0] * repeat + [1] * repeat + [2] * repeat + [1] * repeat

    start_image = pygame.transform.scale(IMAGES['kai'], (300, 100))  # 开始按钮
    start_rect = start_image.get_rect()
    start_rect.center = (guide_x + 40, guide_y + 270)

    exit_image = pygame.transform.scale(IMAGES['tuichu'], (100, 67))  # 退出按钮，调整图片尺寸
    exit_rect = exit_image.get_rect()
    exit_rect.center = (W - 60, H - 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit() #退出
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:#检查是否为空格
                return

        #地板移动模块(实现运动)
        floor_x -= 4
        if floor_x <=- floor_gap:
            floor_x = 0

        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1

        idx += 1
        idx %= len(frames) #利用取余得长度
        SCREEN.blit(IMAGES['bgpic'],(0,0))
        SCREEN.blit(IMAGES['floor'],(floor_x,FLOOR_Y))
        SCREEN.blit(IMAGES['guide'],(guide_x,guide_y))
        SCREEN.blit(IMAGES['birds'][frames[idx]],(bird_x,bird_y))
        pygame.display.update()
        CLOCK.tick(FPS) # 30帧

def game_window():
    AUDIO['flap'].play()
    floor_gap = IMAGES['floor'].get_width() - W  # 获取地板贴图和屏幕宽的差值
    floor_x = 0

    bird = Bird(W * 0.2, H * 0.4)

    score = 0
    n_pairs = 4
    pipe_gap = 100
    # distance = random.uniform(100,200)
    # pipe_gap = random.uniform(100,130)
    pipe_group = pygame.sprite.Group() #打包完成方法

    for i in range(n_pairs):
        distance = random.uniform(155, 180)  # 水管之间的距离
        pipe_gap = random.uniform(100, 120)  # 表示上下水管间距
        pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
        pipe_up = Pipe(W+ i * distance, pipe_y, True)
        pipe_down = Pipe(W + i * distance, pipe_y-pipe_gap, False)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)
    while True:
        flap = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # 退出
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 检查是否为空格
                    flap = True
                    AUDIO['flap'].play()


        # 地板移动模块(实现运动)
        floor_x -= 4
        if floor_x <= - floor_gap:
            floor_x = 0

        bird.update(flap)

        #实现水管的循环，利用检验第一根水管是否超出窗口来进行更换
        first_pipe_up = pipe_group.sprites()[0]
        first_pipe_down = pipe_group.sprites()[1]

        if first_pipe_up.rect.right < 0:

            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_pairs * distance, pipe_y, True)
            new_pipe_down = Pipe(first_pipe_up.rect.x + n_pairs * distance, pipe_y - pipe_gap, False)
            pipe_group.add(new_pipe_up)
            pipe_group.add(new_pipe_down)
            first_pipe_up.kill()
            first_pipe_down.kill()

        pipe_group.update()#更新

        # 检查碰撞上下
        if bird.rect.y > FLOOR_Y or bird.rect.y < 0 or pygame.sprite.spritecollideany(bird, pipe_group):
            bird.dying = True
            AUDIO['hit'].play()
            AUDIO['die'].play()
            result = {'bird': bird, 'pipe_group': pipe_group, 'score': score}
            return result

        # 利用计算是否有重合常宽来计算碰撞(不利用pygame特性)
        # for pipe in pipe_group.sprites():
        #     right_to_left = max(bird.rect.right, pipe.rect.right) - min(bird.rect.left, pipe.rect.left)
        #     bottom_to_top = max(bird.rect.bottom, pipe.rect.bottom) - min(bird.rect.top, pipe.rect.top)
        #     if right_to_left < bird.rect.width + pipe.rect.width and bottom_to_top < bird.rect.height + pipe.rect.height:
        #         AUDIO['hit'].play()
        #         AUDIO['die'].play()
        #         result = {'bird': bird, 'pipe_group': pipe_group}
        #         return result

        # 通过水管后+1分，利用辅助线检验目标是否过线来检验得分(前后帧位置)。
        #分别为：前 中心线 后
        if bird.rect.left + first_pipe_up.x_vel < first_pipe_up.rect.centerx < bird.rect.left:
            AUDIO['score'].play()
            score += 1

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        pipe_group.draw(SCREEN)

        show_score(score)
        SCREEN.blit(bird.image, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)  # 30帧

def end_window(result):
    AUDIO['1'].stop()
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0
    guide_x = (W - IMAGES['guide'].get_width()) / 2
    guide_y = (FLOOR_Y - IMAGES['guide'].get_height()) / 2
    gameover_x = (W -IMAGES['gameover'].get_width())/2
    gameover_y = (FLOOR_Y - IMAGES['gameover'].get_height())/2

    bird = result['bird']
    pipe_group = result['pipe_group']

    start_image = pygame.transform.scale(IMAGES['kai'], (300, 100))  # 开始按钮
    start_rect = start_image.get_rect()
    start_rect.center = (guide_x + 40, guide_y + 270)

    exit_image = pygame.transform.scale(IMAGES['tuichu'], (100, 67))  # 退出按钮，调整图片尺寸
    exit_rect = exit_image.get_rect()
    exit_rect.center = (W - 60, H - 60)

    while True:
        if bird.dying:
            bird.go_die()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()  # 退出
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # 检查是否为空格
                    return

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (0, FLOOR_Y))
        SCREEN.blit(IMAGES['kai'], (guide_x + 40, guide_y + 270))
        SCREEN.blit(IMAGES['tuichu'], (W - 60, H - 60))
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        show_score(result['score'])
        SCREEN.blit(bird.image, bird.rect)
        pygame.display.update()
        CLOCK.tick(FPS)  # 30帧

def show_score(score):    #计分板
    score_str = str(score)
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1
    x = (W - n * w) / 2
    y = H * 0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number], (x, y))
        x += w


class Bird:
    def __init__(self, x, y):
        self.frames = [0] * 5 + [1] * 5 + [2] * 5 + [1] * 5
        self.idx = 0
        self.images = IMAGES['birds']
        self.image = IMAGES['birds'][self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #控制Bird上下飞行
        self.y_vel = -10 #上升速度
        self.max_y_vel = 10 #最大速度
        self.gravity = 1 #模拟重力
        self.y_vel_after_flap = -10
        self.rotate_after_flap = 45
        #Bird角度
        self.rotate = 45
        self.max_rotate = -20
        self.rotate_vel = -3 #旋转角度变化量
        self.dying = False

    #帧之间更新方法
    def update(self, flap = False):

        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap

        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel)#取小，使不超过最大速度
        self.rect.y += self.y_vel
        self.rotate = max(self.rotate+self.rotate_vel,self.max_rotate)

        self.idx += 1
        self.idx %= len(self.frames)
        self.image = self.images[self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image, self.rotate) #执行角度调整

    def go_die(self):
        if self.rect.y < FLOOR_Y:
            self.rect.y += self.max_y_vel
            self.rotate = -90
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image, self.rotate)
        else:
            self.dying = False

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, upwards = True):   #upwards默认水管开口朝上，所以if写的下方水管，else写的上方水管
        pygame.sprite.Sprite.__init__(self)
        if upwards:
           self.image = IMAGES['pipes'][0]
           self.rect = self.image.get_rect()
           self.rect.x = x
           self.rect.top = y
           self.mask = pygame.mask.from_surface(self.image)
        else:
            self.image = IMAGES['pipes'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
            self.mask = pygame.mask.from_surface(self.image)
        self.x_vel = -4    #水管X方向速度

    def update(self):
        self.rect.x += self.x_vel

# 运行游戏
main()