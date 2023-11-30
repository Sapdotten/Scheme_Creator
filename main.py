from PIL import Image, ImageDraw, ImageFont
import yaml

INCHES_TO_S = 2.54
class Scheme:
    def __init__(self, width: int, height: int, track_width: int):
        self.get_configs()
        self.width = self.inches_to_pixels(width)
        self.height = self.inches_to_pixels(height)
        self.track_width = self.inches_to_pixels(track_width)
        self.img = Image.new('RGB', (self.width, self.height), self.background_color)
        self.img.save(self.pic_name)
        self.grid_width = width
        self.grid_height = height

    def get_configs(self):
        with open('configs.yaml', 'r') as f:
            configs = yaml.load(f, Loader=yaml.FullLoader)
            self.dpi = configs['dpi'] 
            self.background_color = configs['background_color']
            self.pic_name = configs['pic_name']
            self.grid_color = configs['grid_color']
            
    def inches_to_pixels(self, num: int) -> int:
        return int(num*self.dpi*2.5/INCHES_TO_S/10)
    
    def make_grid(self):
        draw = ImageDraw.Draw(self.img)
        for i in range(0, self.grid_width):
            draw.line((self.inches_to_pixels(i), 0, self.inches_to_pixels(i), self.height), fill = self.grid_color, width = 1)
        for i in range(0, self.grid_height):
            draw.line((0, self.inches_to_pixels(i), self.width, self.inches_to_pixels(i)), fill = self.grid_color, width = 1)
        self.img.save(self.pic_name)
            
        
    


# img = Image.new('RGB', (200, 200), 'white')
# draw = ImageDraw.Draw(img)
# draw.line((0, 0) + img.size, fill='black')
# draw.line((0, img.size[1], img.size[0], 0), fill='black', width = 30)
# img.save('test1.jpg')

# img = Image.open('test1.jpg')
# img.show()

a = Scheme(9, 9, 15)
a.make_grid()
a.img.show()