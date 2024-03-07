import pygame
import time
import sys
import os
import datetime


class LifeGame():
    def __init__(self,size:tuple = (50,50), matrix = [], update_interval = 300, cellsize = 30, monitor = True, result_save = (False,10)):
        # 类型检查(对于matrix的检测相对没那么严格)
        # update_interval
        if isinstance(update_interval, int) and update_interval > 0:
            pass
        else:
            raise TypeError("update_interval应该是一个大于0的整数")
        # size
        if isinstance(size, list) or isinstance(size, tuple):
            pass
        else:
            raise TypeError("size应该是一个二元元组或数组")
        if len(size) != 2:
            raise TypeError("size应该是一个二元元组或数组")
        for i in [0,1]:
            if not isinstance(size[i], int) or size[i] <= 0:
                raise TypeError("size中应该是两个正整数") 
        # cellsize
        if isinstance(cellsize, int):
            if cellsize > 0:
                self.__cellsize = cellsize
        else:
            raise TypeError("cellsize应该是一个正整数")
        # monitor
        if isinstance(monitor, bool):
            # 记录细胞位置是否改变的变量
            self.__monitor = monitor
            self.__cell_change = True
            self.__age = 0
        else:
            raise TypeError("monitor应该是True或False")
        # result_save
        if isinstance(result_save, bool):
            self.__result_save = result_save
            self.__maxage = 10
        elif isinstance(result_save, tuple) and len(result_save) == 2:
            self.__result_save = result_save[0]
            self.__maxage = result_save[1]
        else:
            raise TypeError("result_save应该是应该bool变量或是一个二元元组")

        # 初始化位置矩阵
        self.__rows, self.__cols = size
        if matrix == []:
            print("系统自动初始化位置矩阵")
            self.__matrix = [[0 for _ in range(self.__rows)] for _ in range(self.__cols)]
        elif len(matrix) == self.__cols and len(matrix[0]) == self.__rows:
            print("手动初始化位置矩阵")
            self.__matrix = matrix
        else:
            self.__matrix = [[0 for _ in range(self.__rows)] for _ in range(self.__cols)]
            raise TypeError(f"\n传入矩阵与矩阵大小不匹配:\n正确大小应该为{self.__rows}*{self.__cols}\n实际大小为{len(matrix)}*{len(matrix[0])}")

        # 测试用修改矩阵处

        # 与时间相关的初始化
        pygame.init()
        self.__clock = pygame.time.Clock()  # 创建一个时钟对象
        self.__update_interval = update_interval  # 更新间隔，以毫秒为单位
        self.__last_time = 0
        self.__current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def info(self):
        # 以字典的形式返回类中部分参数的信息
        information = {}
        information['cellsize'] = self.__cellsize
        information['monitor'] = self.__monitor
        information['cell_change'] = self.__cell_change
        information['age'] = self.__age
        information['result_save'] = self.__result_save
        information['maxage'] = self.__maxage
        information['cols'] = self.__cols
        information['rows'] = self.__rows
        information['update_interval'] = self.__update_interval
        information['current_time'] = self.__current_time
        return information
        

    def __cell_show(self,matrix):
        # 显示位置矩阵中细胞的位置
        for x in range(self.__cols):
            for y in range(self.__rows):
                if matrix[x][y]:
                    left = y * self.__cellsize
                    top = x * self.__cellsize
                    #print(x,y)
                    pygame.draw.rect(self.__screen, (0,0,0), (left, top, self.__cellsize, self.__cellsize), 0)
    
    def __status(self, position:tuple)->bool:
        # 判断一个细胞下一回合是活着还是死去
        matrix = self.__matrix
        x, y = position
        surronding_cell = 0

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if x + i < 0 or x + i > self.__cols-1 or y + j < 0 or y + j > self.__rows-1:
                    pass
                else:
                    if matrix[x+i][y+j]:
                        surronding_cell += 1

        if matrix[x][y]:
            surronding_cell -= 1
            if surronding_cell < 2:
                return False
            elif surronding_cell == 2 or surronding_cell == 3:
                return True
            elif surronding_cell > 3:
                return False
        else:
            if surronding_cell == 3:
                return True
            else:
                return False

    def __update(self):
        # 计算下一代的细胞
        new_matrix = [[0 for _ in range(self.__rows)] for _ in range(self.__cols)]
        for x in range(self.__cols):
            for y in range(self.__rows):
                if self.__status((x,y)):
                    new_matrix[x][y] = 1
        return new_matrix

    def monitor_func(self):
        # 监测是否还有剩余细胞,细胞是否还在移动
        # 剩余细胞
        cell_number = 0
        for x in range(self.__cols):
            for y in range(self.__rows):
                if self.__matrix[x][y]:
                    cell_number += 1
        # 细胞是否在变化
        if self.__cell_change:
            if self.__matrix == self.__update():
                self.__cell_change = False
        return cell_number,self.__cell_change, self.__age


    def __save_result(self, max_age):
        # 获取当前脚本所在的目录
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # 将各代的形状保存为图片
        if self.__cell_change or self.__age == 1:
            folder_path = os.path.join(script_directory, f"Results_{self.__current_time}")
            if self.__age <= self.__maxage:
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        image_path = os.path.join(folder_path, f"age {self.__age}.png")
                        pygame.image.save(self.__screen, image_path)
                
        return 

    def create_matrix(self):
        # 初始化矩阵
        my_matrix = [[0 for _ in range(self.__rows)] for _ in range(self.__cols)]
        # 设置窗口大小
        width, height = self.__rows*self.__cellsize+200 , self.__cols*self.__cellsize # 相比于run中的窗口大了3倍
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Create Your Matrix")
        # 颜色定义
        white = (255,255,255)
        black = (0,0,0)
        grid_color = (100,100,100)
        # 方格信息
        num_rows, num_cols = self.__rows, self.__cols
        #cell_size = 30
        # 绘制图像
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #print(my_matrix)
                    self.__matrix = my_matrix
                    return my_matrix
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  #左键点击
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        x = mouse_x // self.__cellsize
                        y = mouse_y // self.__cellsize
                        my_matrix[y][x] = 1
                        #print("Mouse clicked at:", x, y)
                    elif event.button == 3: # 右键点击
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        x = mouse_x // self.__cellsize
                        y = mouse_y // self.__cellsize
                        my_matrix[y][x] = 0
                        #print("Mouse clicked at:", x, y)
                    #print(my_matrix)

                screen.fill(white)
                
                #绘制方格图
                for row in range(num_cols):
                    for col in range(num_rows):
                        left = col * self.__cellsize
                        top = row * self.__cellsize
                        if my_matrix[row][col]:
                            pygame.draw.rect(screen, black, (left, top, self.__cellsize, self.__cellsize), 0)
                        else:
                            pygame.draw.rect(screen, white, (left, top, self.__cellsize, self.__cellsize), 0)
                        pygame.draw.rect(screen, grid_color, (left, top, self.__cellsize, self.__cellsize), 1) # 绘制边框
                pygame.display.flip()


    def run(self):
        # 初始化Pygame
        window_size = (self.__rows*self.__cellsize, self.__cols*self.__cellsize) # 定义窗口大小
        self.__screen = pygame.display.set_mode(window_size) # 创建窗口
        self.__screen.fill((255, 255, 255))
        pygame.display.set_caption("Conway's Game of Life") # 设置窗口标题
        self.__last_update_time = pygame.time.get_ticks()  # 上一次更新的时间
        

        # 游戏循环
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            current_time = pygame.time.get_ticks()

            if current_time - self.__last_update_time >= self.__update_interval:
                self.__last_update_time = current_time

                # 填充窗口背景色
                self.__screen.fill((255, 255, 255))  # 使用RGB颜色，这里是白色

                # 绘制图片
                self.__cell_show(self.__matrix)
                self.__matrix = self.__update()

                self.__age += 1
        
                if self.__monitor:
                    print(self.monitor_func())
                if self.__result_save:
                    self.__save_result(self.__maxage)
                # 更新屏幕显示
                pygame.display.flip()

            self.__clock.tick(60)

        # 退出Pygame
        #pygame.quit()

if __name__ == "__main__":
    game = LifeGame(size=(80,50), update_interval= 300, cellsize= 10, monitor = True, result_save = (False, 40))
    game.create_matrix()
    game.run()
    sys.exit()