Программа шифрует либо дешифрует текстовое сообщение на латинице шифром Цезаря/Виженера. А также пытается взломать сообщение, закодированное шифром Цезаря.

ЗАПУСК:

python encryptor.py encode/decode --cipher {caesar,vigenere}
--key {number|word} [--input-file input.txt]
[--output-file output.txt]

ПАРАМЕТРЫ ЗАПУСКА:
1) encode/decode - зашифровать/расшифровать сообщение
2) --cipher - тип шифра: Цезарь/Виженер
3) --key - ключ шифра. Для Цезаря - число, для Виженера - слово на латинице
4) --input-file - путь ко входному файлу. Если не указан, текст вводится с клавиатуры
5) --output-file - путь к выходному файлу. Если не указан, текст выводится в консоль

ВЗЛОМ:

Команда для сбора информации по тексту для дальнейшего взлома:
  python encryptor.py train --text-file {input.txt} --model-file {model}

Команда для взлома после сбора информации:
  python encryptor.py hack [--input-file input.txt] [--output-file output.txt] --model-file
  
ПАРАМЕТРЫ:
1) --text-file - путь к файлу с зашифрованным сообщением. Если не указан, сообщение вводится с клавиатуры
2) --model-file - путь к файлу, в котором будет сохранена информация о тексте
3) --input-file - путь к файлу с зашифрованным сообщением. Если не указан, сообщение вводится с клавиатуры
4) --output-file - путь к выходному файлу. Если не указан, сообщение выводится в консоль
