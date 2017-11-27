from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, ImageColorGenerator

d = path.dirname(__file__)

stopwords = {}
isCN = 1
back_coloring_path = 'byc2.jpg'
text_path = 'fenci_all.txt'
font_path = 'simkai.ttf'
stopwords_path = r'C:\Users\三川\Desktop\sxcspider\spider\分词\stopword.txt'
imgname1 = "WordCloudDefautColors1.png"
imgname2 = "WordCloudColorsByImg1.png"
my_words_list = ['Python']
back_coloring = imread(path.join(d, back_coloring_path))

wc = WordCloud(font_path=font_path,
               background_color="white",
               max_words=2000,
               mask=back_coloring,
               max_font_size=100,
               random_state=42,
               width=1000, height=860, margin=2,
               )


def add_word(lists):
  for items in lists:
    jieba.add_word(items)


add_word(my_words_list)

text = open(path.join(d, text_path), 'r', encoding='utf-8').read()


def jiebaclearText(text):
  mywordlist = []
  seg_list = jieba.cut(text, cut_all=False)
  liststr = "/ ".join(seg_list)
  f_stop = open(stopwords_path, 'r', encoding='utf-8')
  try:
    f_stop_text = f_stop.read()

  finally:
    f_stop.close()
  f_stop_seg_list = f_stop_text.split('\n')
  for myword in liststr.split('/'):
    if not(myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
      mywordlist.append(myword)
  return ''.join(mywordlist)


if isCN:
  text = jiebaclearText(text)
wc.generate(text)

image_colors = ImageColorGenerator(back_coloring)
plt.figure()
plt.imshow(wc)
plt.axis("off")
plt.show()

wc.to_file(path.join(d, imgname1))

image_colors = ImageColorGenerator(back_coloring)

plt.imshow(wc.recolor(color_func=image_colors))
plt.figure()
plt.imshow(back_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
wc.to_file(path.join(d, imgname2))
