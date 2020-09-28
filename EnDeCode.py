import os
import sys

def createMask(level):
    # Создаем шаблоны маски
    imgMask = 0b11111111
    secretMask = 0b11111111

    # Сдвигаем их под нашу степень шифрования
    secretMask <<= (8 - level)
    secretMask %= 256
    imgMask >>= level
    imgMask <<= level

    # Возвращаем результат
    return secretMask, imgMask



def encode():
    # getSize secret and img
    secret_size = os.stat('secret.txt').st_size
    img_size = os.stat('img.bmp').st_size
    print(F'Размер секрета: {secret_size} бит')
    print(F'Размер изображения: {img_size} бит\n')

    # Select level encode
    print("### WARNING ### \nЧем выше уровень шифрования, тем хуже будет качество изображения\n### WARNING ###\n\n")
    # Если l(Low) - то работаем по 1 биту, если m(Medium) - то по 2, если h(High) - то по 4
    levels = {'l':1, 'm':2, 'h':4}
    level = input('Введите уровень шифрования (l/m/h): ')
    showOFF = input("Покзать процесс? (y): ")

    #FUCNTIONS#

    # Check max size


    # Open all files
    secret = open('secret.txt', 'r')
    origin_img = open('img.bmp', 'rb')
    encode_img = open('img_encoded.bmp', 'wb')

    # Читаем первые 54 байта, где хранятся мета-данные и заголовки
    first54byte = origin_img.read(54)
    # Записываем в новую картинку
    encode_img.write(first54byte)



    def decor():
        print("Выполняется проверка...")

    #########################
    # Pre Main BODY [PROGRAM]
    if level == 'l':
        decor()
    elif level == 'm':
        decor()
    elif level == 'h':
        decor()
    else:
        print("Откат изменений, выбрано неправильное значение")
        return

    # Use fucn
    checkMaxSize(level)
    # Get MASKs
    secretMask, imgMask = createMask(levels.get(level))

    while True:
        # Читаем по одному байту секрета
        symbol = secret.read(1)
        # Если секрет закончен, то выходим из цикла
        if not symbol:
            break

        # Прячем процесс
        if showOFF == 'y':
            print(F'\nСимвол: {symbol} > {bin(ord(symbol))}')
            print(F'Сдвиг на {levels.get(level)} бита')

        # Преобразование символов в цифры
        symbol = ord(symbol)

        # Для каждой пары битов (если уровень СРЕДНИЙ)
        # В каждом байте размерности от 0 до 8
        # с промежутком выбранного уровня шифрования
        for bytes in range(0,8,levels.get(level)):
            # use MASK
            imgByte = int.from_bytes(origin_img.read(1), sys.byteorder) & imgMask

            # Получаем количество бит из символа
            # Пример [10][11][01[00] -> [10]110100
            bits = symbol & secretMask
            # Сдвигаем их в конец
            # Пример [10][11][01[00] -> [00][00][00][10] (то есть получаем итоговую маску)
            bits >>= (8 - levels.get(level))

            if showOFF == 'y':
                print('{0} Сдвиг на {1:d}'.format(imgByte, bits))

            # С помощью маски записываем биты в байты изображения
            # Пример:
            # байт изображения - [10][01][11][11]
            # полученая маска секрета [00][00][00][10]
            # Получаем: [10][01][11].[10]
            imgByte |= bits

            if showOFF == 'y':
                print(F'Получено: {imgByte}')

            # Записываем полученный байт в новую картинку (В байтовом виде)
            encode_img.write(imgByte.to_bytes(1, sys.byteorder))
            # Сдвигаем символ на уровень сжатия, чтобы цеплять оставшиеся биты.
            # Пример: [01][11][10][00] -> [-][11][10][00] -> [11][10][00][00]
            symbol <<= levels.get(level)


    print(F'Шифрование закончено на : {origin_img.tell()} бите')
    print('Готово, секрет спрятан')

    # Записываем оставшиеся байты в новую картинку
    encode_img.write(origin_img.read())

    ########################
    # Close all files
    secret.close()
    origin_img.close()
    encode_img.close()

    return True

def decode():
    # FUNCTIONS >>>>>
    def checkMaxSize(level):
        if to_read > img_size * levels.get(level) / 8 - 54:
            print('Невозможно прочитать файл меньшего размера, чем секрет')
            os.exit(1)
        else:
            print("Расшифровка разрешена\nПолучаем секрет")

    def decor():
        print("Выполняется проверка...")


    #########################
    # INIT all VAR
    img_size = os.stat('img_encoded.bmp').st_size
    print(F'Размер изображения: {img_size} бит\n')
    levels = {'l': 1, 'm': 2, 'h': 4}
    level = input('Введите уровень шифрования (l/m/h): ')
    to_read = input('Сколько символов считать?: ([количество]/all) ')

    # Обработка запроса
    if to_read == 'all':
        try:
            size = os.stat('secret.txt').st_size
            to_read = int(size)
        except:
            print('Файл не найден, попробуйте прописать количество')
            return
    elif type(to_read) is str:
        try:
            to_read = int(to_read)
        except:
            print('Ожидается число')
            return
    else:
        print('Что то пошло не так, попробуйте снова')
        return

    showOFF = input("Показать процесс? (y): ")

    # Счетчик просчитанных символов
    countRead = 0


    # Pre Main BODY [PROGRAM]
    if level == 'l':
        decor()
    elif level == 'm':
        decor()
    elif level == 'h':
        decor()
    else:
        print("Откат изменений, выбрано неправильное значение")
        return

    checkMaxSize(level)

    # Open all Files
    secret = open('secret_decode.txt', 'w')
    img_encoded = open('img_encoded.bmp', 'rb')

    # Пропускаем первые 54 бита
    img_encoded.seek(54)

    # Get MASK for img bytes
    maskList = createMask(levels.get(level))
    # Делаем обратную маску, чтобы считывать последние биты
    # Пример: [11][11][11][11] -> [00][00][00][11]
    imgMask = ~maskList[1]

    while countRead < to_read:
        # Начинаем с первого символа
        symbol = 0
        for bits in range(0, 8, levels.get(level)):
            # Также берем последние (нужные) биты
            imgByte = int.from_bytes(img_encoded.read(1), sys.byteorder) & imgMask
            # Сдвигаем влево
            symbol <<= levels.get(level)
            # Помещаем биты на нужную позицию
            symbol |= imgByte

        if showOFF == 'y':
            print(F'Символ {countRead + 1} >> {symbol:c}')
        # Следующий символ
        countRead += 1
        # Записываем символ
        secret.write(chr(symbol))

    # Close all Files
    secret.close()
    img_encoded.close()

    return True
