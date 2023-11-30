from PIL import Image, ImageDraw, ImageFont
import yaml
from typing import Union

INCHES_TO_S = 2.54
class Scheme:
    def __init__(self, width: int, height: int, track_width: int, line_count: int = 0, lines: list[list[int]] = None):
        self.get_configs()
        self.width = self.inches_to_pixels(width)
        self.height = self.inches_to_pixels(height)
        self.track_width = self.inches_to_pixels(track_width*0.4)
        self.img = Image.new('RGB', (self.width, self.height), self.background_color)
        self.img.save(self.pic_name)
        self.grid_width = width
        self.grid_height = height
        self.line_count = line_count
        self.lines = lines

    def get_configs(self):
        with open('configs.yaml', 'r') as f:
            configs = yaml.load(f, Loader=yaml.FullLoader)
            self.dpi = configs['dpi'] 
            self.background_color = configs['background_color']
            self.pic_name = configs['pic_name']
            self.grid_color = configs['grid_color']
            self.reference_file = configs['reference_file']
            self.line_color = configs['line_color']
            self.circle_radius = configs['circle_radius']
            
    def inches_to_pixels(self, num: float) -> int:
        return int(num*self.dpi*2.5/INCHES_TO_S/10)
    
    def make_grid(self):
        draw = ImageDraw.Draw(self.img)
        for i in range(1, self.grid_width):
            draw.line((self.inches_to_pixels(i), 0, self.inches_to_pixels(i), self.height), fill = self.grid_color, width = 1)
        for i in range(1, self.grid_height):
            draw.line((0, self.inches_to_pixels(i), self.width, self.inches_to_pixels(i)), fill = self.grid_color, width = 1)
        self.img.save(self.pic_name)
        
    def _draw(self, coords: list):
        draw = ImageDraw.Draw(self.img)
        draw.line(coords, fill = self.line_color, width = self.track_width, joint = 'curve')
        self.img.save(self.pic_name)
    
    def _draw_line(self, x: int, y: int, dir: str):
        if dir=='v':
            x = self.inches_to_pixels(x)+1
            y1 = self.inches_to_pixels(y)
            x+=self.inches_to_pixels(0.5)
            y2 = y1+self.inches_to_pixels(1)+1
            self._draw((x, y1, x, y2))
        elif dir=='h':
            x1 = self.inches_to_pixels(x)
            y = self.inches_to_pixels(y)
            y+= self.inches_to_pixels(0.5)
            x2 = x1+self.inches_to_pixels(1)+1
            self._draw((x1, y, x2, y))
            
    def _draw_angle(self, x: int, y: int, dir: int):
        if dir==1:
            y1 = self.inches_to_pixels(y)
            x1 = self.inches_to_pixels(x)+self.inches_to_pixels(0.5)+1
            y2 = y1+self.inches_to_pixels(0.5)
            x2 = x1
            y3 = y2
            x3 = x2+self.inches_to_pixels(0.5)+1
            self._draw((x1, y1, x2, y2, x3, y3))
        elif dir==2:
            y1 = self.inches_to_pixels(y)
            x1 = self.inches_to_pixels(x)+self.inches_to_pixels(0.5)+1
            y2 = y1+self.inches_to_pixels(0.5)
            x2 = x1
            y3 = y2
            x3 = x2-self.inches_to_pixels(0.5)-1
            self._draw((x1, y1, x2, y2, x3, y3))
        elif dir==3:
            y1 = self.inches_to_pixels(y)+self.inches_to_pixels(0.5)
            x1 = self.inches_to_pixels(x)
            y2 = y1
            x2 = x1+self.inches_to_pixels(0.5)+1
            y3 = y2+self.inches_to_pixels(0.5)+1
            x3 = x2
            self._draw((x1, y1, x2, y2, x3, y3))
        elif dir==4:
            y1 = self.inches_to_pixels(y)+self.inches_to_pixels(0.5)
            x1 = self.inches_to_pixels(x+1)
            y2 = y1
            x2 = x1-self.inches_to_pixels(0.5)-1
            y3 = y2+self.inches_to_pixels(0.5)+1
            x3 = x2
            self._draw((x1, y1, x2, y2, x3, y3))
            
    def _draw_circle(self, xy: list[int], dir:int):
        x = xy[0]
        y = xy[1]
        rad = self.circle_radius*0.4
        indent = self.inches_to_pixels((1-rad)/2)
        x1 = self.inches_to_pixels(x)+indent+1
        y1 = self.inches_to_pixels(y)+indent+1
        x2 = x1+self.inches_to_pixels(rad)+1
        y2 = y1+self.inches_to_pixels(rad)
        draw = ImageDraw.Draw(self.img)
        draw.chord((x1, y1, x2, y2), 0, 360, fill = "black")
        self._draw_circle_dir(xy, dir)
        self.img.save(self.pic_name)
    
    def _draw_circle_dir(self, xy:list[int], dir: int):
        x = xy[0]
        y = xy[1]
        if dir == 1:
            x1 = self.inches_to_pixels(x+0.5)
            y = self.inches_to_pixels(y)
            y+= self.inches_to_pixels(0.5)
            x2 = x1+self.inches_to_pixels(0.5)+1
            self._draw((x1, y, x2, y))
        elif dir == 2:
            x = self.inches_to_pixels(x+0.5)
            y1 = self.inches_to_pixels(y)
            y2=y1+ self.inches_to_pixels(0.5)
            self._draw((x, y1, x, y2))
        elif dir == 3:
            x1 = self.inches_to_pixels(x)
            y = self.inches_to_pixels(y+0.5)
            x2=x1+ self.inches_to_pixels(0.5)
            self._draw((x1, y, x2, y))
        elif dir == 4:
            x = self.inches_to_pixels(x+0.5)+1
            y1 = self.inches_to_pixels(y+0.5)
            y2=y1+ self.inches_to_pixels(0.5)
            self._draw((x, y1, x, y2))
        
        
        
    def fill_cell(self, xy: list[int], type: str, direction: Union[str, int]):
        x = xy[0]
        y=xy[1]
        if type=='line':
            self._draw_line(x, y, direction)
        elif type=='angle':
            self._draw_angle(x, y, direction)
        elif type=='circle':
            self._draw_circle(x, y, direction)
            
    def _get_type_and_dir(self, xy1: list[int], xy2: list[int], xy3: list[int])-> tuple[str, Union[str, int]]:
        if xy1[0]==xy2[0]:
            if xy2[0]==xy3[0]:
                return 'line', 'v'
            if xy1[1]<xy2[1]:
                if xy3[0]>xy2[0]:
                    return 'angle', 1
                else:
                    return 'angle', 2
            else:
                if xy3[0]>xy2[0]:
                    return 'angle', 4
                else:
                    return 'angle', 3
        else:
            if xy2[1]==xy3[1]:
                return 'line', 'h'
            if xy1[0]<xy2[0]:
                if xy3[1]>xy2[1]:
                    return 'angle', 3
                else:
                    return 'angle', 2
            else:
                if xy3[1]>xy2[1]:
                    return 'angle', 4
                else:
                    return 'angle', 1
            
        
            
    def draw_lines(self):
        for line in self.lines:
            head = line[0]
            next = line[1]
            if next[0]>head[0]:
                self._draw_circle(head, 1)
            elif next[0]<head[0]:
                self._draw_circle(head, 3)
            elif next[1]>head[1]:
                self._draw_circle(head, 4)
            else:
                self._draw_circle(head, 2)
            for i in range(1, len(line)-1):
                type_, dir = self._get_type_and_dir(line[i-1], line[i], line[i+1])
                self.fill_cell(line[i], type_, dir)
            end = line[-1]
            prev = line[-2]
            if end[0]>prev[0]:
                self._draw_circle(end, 3)
            elif end[0]<prev[0]:
                self._draw_circle(end, 1)
            elif end[1]>prev[1]:
                self._draw_circle(end, 2)
            else:
                self._draw_circle(end, 4)

        
        
        
              
        
    
def get_data() -> Scheme:
    with open('test.txt', 'r') as f:
        data = f.read()
        data = data.split('\n')
        size = data[0].split(' ')
        width = int(size[0])
        height = int(size[0])
        line_width = int(data[1])
        line_count = int(data[2])
        lines = data[3:]
    for i in range(0, len(lines)):
        if len(lines[i])!=0:
            lines[i] = lines[i].split(' ')
            for j in range(0, len(lines[i])):
                lines[i][j] = lines[i][j].split(';')
                for k in range(0, len(lines[i][j])):
                    lines[i][j][k] = int(lines[i][j][k])
        else:
            lines.pop(i)
    result = Scheme(width, height, line_width, line_count, lines)
    return result

a = get_data()
# строку ниже раскомментишь, если нужна будет сетка
# a.make_grid()
a.draw_lines()
# строку ниже раскомментишь, если нужно чтоб по итогу выполнения картинка сама открылась
# a.img.show() 