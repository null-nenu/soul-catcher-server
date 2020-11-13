from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

class textTopng:
  font = ImageFont.truetype("src/api/font/MSYH.TTF", 40)
  def __init__(self, text,pngWidth = 8, pngHeight = 20, result = "result.png"):
    self.pngWidth = pngWidth
    self.pngHeight = pngHeight
    self.result = result
    # 预设宽度 可以修改成你需要的图片宽度 1500最优
    self.width = 1500
    # 文本
    self.text = text
    # 段落 , 行数, 行高
    self.duanluo, self.note_height, self.line_height = self.split_text()

  def get_duanluo(self, text):
    txt = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    # 所有文字的段落
    duanluo = ""
    # 宽度总和
    sum_width = 0
    # 几行
    line_count = 1
    # 行高
    line_height = 0
    for char in text:
      width, height = draw.textsize(char, self.font)
      sum_width += width
      if sum_width > self.width: # 超过预设宽度就修改段落 以及当前行数
        line_count += 1
        sum_width = 0
        duanluo += '\n'
      duanluo += char
      line_height = max(height, line_height)
    if not duanluo.endswith('\n'):
      duanluo += '\n'
    return duanluo, line_height, line_count

  def split_text(self):
    # 按规定宽度分组
    max_line_height, total_lines = 0, 0
    allText = []
    for text in self.text.split('\n'):
      duanluo, line_height, line_count = self.get_duanluo(text)
      max_line_height = max(line_height, max_line_height)
      total_lines += line_count
      allText.append((duanluo, line_count))
    line_height = max_line_height
    total_height = total_lines * line_height
    return allText, total_height, line_height


  def draw_text(self):
    """
    绘图以及文字
    :return:
    """
    fig = plt.gcf()
    name = r"src/api/data/" + self.result
    fig.set_size_inches(self.pngWidth, self.pngHeight)
    fig.savefig(name, dpi=180)

    png = name
    note_img = Image.open(png).convert("RGBA")
    draw = ImageDraw.Draw(note_img)
    # 左上角开始
    x, y = 50, 50
    for duanluo, line_count in self.duanluo:
      draw.text((x, y), duanluo, fill=(0, 0, 0), font=self.font)
      y += self.line_height * line_count
    note_img.save(name)
