import cv2

img = cv2.imread('relize.jpg')
text = ('привет \n privet \n привет')
cv2.putText(img, text, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (85,85,85), 2)
cv2.imwrite('result1.jpg', img)


# from PIL import ImageFont
# from PIL import Image
# from PIL import ImageDraw
#
# # определяете шрифт
# font = ImageFont.truetype('Roboto-MediumItalic.ttf', size=30)
#
# # определяете положение текста на картинке
# text_position = (10, 10)
#
# # цвет текста, RGB
# text_color = (0,0,0)
#
# # собственно, сам текст
# text = 'Бородавка:%\nГрибок:%\nЗдоровый:%'
#
# # загружаете фоновое изображение
# img = Image.open('relize.jpg')
#
# # определяете объект для рисования
# draw = ImageDraw.Draw(img)
#
# # добавляем текст
# draw.text(text_position, text, text_color, font)
#
# # сохраняем новое изображение
# img.save('blank_with_text.jpg')