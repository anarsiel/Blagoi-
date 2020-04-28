# Запуск

`$ python3 runRPAF.py main.rpaf`

# Пример кода на языке RPAF
Эта [программа](https://github.com/anarsiel/RPA-Language/blob/master/main.rpaf) создает коллекцию в MS WORD
из изображений дня за 2019 год с разбивкой по месяцам. Итоговый файл для всех 12 месяцев весит очень много, поэтому я выложил
демо вариант для Января и Февраля.

# Основы языка

### Этапы обработки исходного кода
  * Препроцессинг/Компиляция
    
    На вход поступает программа на языке RPAF: `file.rpaf`
    На этом этапе расставляются goto и метки, необходимые для корректной работы циклов
    (и функций, если бы они у меня были), а так же проводится статическая валидация (подробнее в разделе команд).
    На выходе получаем `file.o.rpaf`
    
  * Интерпретация
  
    На этом этапе производится построчное выполнение скомпилированного кода.
    

### Переменные

  ```
  var x := const 3                  # создание новой переменной со значением "3"
  x := const Saint-P                # создание переменной со значением "Saint-P"
  print %x                          # взятие значения переменной (оператор %)
  ```
  
  * Имя переменной должно быть в формате: `[a-zA-Z][a-zA-Z0-9_]*`  
  ```
  var 234sdsdf := const 3
  ```
  > ERROR:root:Compilation error: Line: 1. Command: `var`. Wrong variable name: 234sdsdf.
  ```
  import IO
  
  var x := const 3
  print %y
  ```
  > ERROR:root:Compilation error: Line: 4. Command: `print`. Variable do not exist: `y`.
  
  Тип значения переменной, если ее захаркодить - str. Если же переменная это результат, который возвращает функция, то
  ее тип может быть любым. Это позволяет обмениваться легко данными между модулями и функциями, без написания специальных
  прослоек.
  
### Использование модулей
  Стоит сразу сказать, что модули это не библиотеки в питоне, которые я просто подключаю. Каждый модуль это специальным образом
  хранящиеся и подгружаемые функции, информация об их аргументах и их логика (вот она уже написана на питоне).
  Подробнее про создание модулей читайте ниже в отдельном разделе.

  Изначально доступны команды, лежащие в основном модуле `CORE`. Они подгружаются по умолчанию. 
  Команда `import` позволяет загрузить кастомные модули и использовать их функции.
    
  ```
  concat qwerty ytrewq             
  ```
  > ERROR:root:Compilation error: Line: 1. Command: `concat`. Wrong command name: `concat`

  ```
  import ALGO
  concat qwerty ytrewq             # OK
  ```

### Команды
  * У всех пременных глобальная область видимости

  * Все команды кроме `var` могут принимать в качестве аргументов либо константы, либо значения переменных. Команда `var`
    первым аргументом всегда принимает функцию.
  
  ```
  var x := concat str ing             # создание новой переменной со значением "string"
  print_to_file %filename texXxXxt    # запись строки в файл с именем `%filepath`
  ```

  * Некоторые команды являются парными:
  
  ```
  var x := const 0
  loop 239                            # повторить 239
      print %x                        
      x := inc %x                     # инкрементирование значения переменной
  endloop                             # конец цикла
  ```
  
  При компиляции осуществляется проверка на корректность парных комманд
    
  ```
  loop 239
      loop 932
      endloop
  endloop
  endloop
  ```
  > ERROR:root:Compilation error: Line: 5. Command: `endloop`. Wrong command pair: [`None`, `endloop`].
  
  * Значения аргументов передаваемых в команду обязательно валидируются. Дважды. 
  Первый раз на этапе препроцессинга и компиляции. Второй уже перед непосредственным исполнением команды. Это
  позволяет определить часть ошибок до запуска программы. 
  
  Заметим, что во всех случаях программа некоректна: мы не можем увеличить значения типа str на 1, однако ошибка и
  момент в который она будет показана пользователю - отличается.
  
  ```
  # I                                       # II                    # III
  import ALGO                               import ALGO             import ALGO
                                                                    
  var x := const SoMeTeXt                   inc SoMeTeXt            inc %some_var
  inc %x                                               
  ```
  ---------------------------------------------------------------------------
  > ERROR:root:Runtime error. Line: 5. Command: `inc`. Wrong param type.   
  > Param #1: `SoMeTeXt` cannot be casted to <class 'int'>.
  ---------------------------------------------------------------------------
  > ERROR:root:Compilation error. Line: 4. Command: `inc`. Wrong param type.
  > Param #1: `SoMeTeXt` cannot be casted to <class 'int'>. 
  ---------------------------------------------------------------------------
  > ERROR:root:Compilation error: Line: 4. Command: `inc`.
  > Variable do not exist: `some_var`.
  ---------------------------------------------------------------------------
  В последнем случае мы получаем такую ошибку т.к. аргумент похож на переменную, поэтому скорее всего
  программист просто ошибочно написал имя переменной.
  
  # Модули
  
  RPAF - это предметно-ориентированный язык, поэтому огромное значение имеет удобство написания модулей и работы с ними.
  Я специально вынес в отдельные модули некоторые команды, чтобы Вы могли лучше понять устройство модулей, хотя там почти
  все функции можно было положить в 'CORE'. Рассмотрим на примере.
  
  Давайте создадим модуль, который будет содержать одну функцию, складывающую два четных числа.
  Назовем модуль TEST, а функцию sum_even_even. Нам нужно будет создать три класса:
  
  * сlass Test (содержащий информацию о модуле)
      ``` python
      __info = [
          ['sum_even_even', TestLogic.sum22, [int, int], None, TestValidator.validate_sum22]
      ]
      
      @staticmethod
      def get_info():
          return Test.__info
      ```
      Мы задали [имя фукнции], [функцию логики, которую опишем ниже], [колличество параметров и их типы],
      [парную фукнцию], [функцию валидации аргументов]
  
  * class TestLogic (содержащий логику)
      ``` python
      @staticmethod
      def sum22(a, b):
          DataProvider.return_value(a + b) # класс, реализующий интерфейс взаимодействия с данными
      ```
  * class TestValidator (будет валидировать аргументы)
      ``` python
      @staticmethod
      def validate_sum22(args):
         for idx, arg in enumerate(args):
            if arg % 2 == 1:
                raise CommonValidator.ValidationError(f'Argument #{idx + 1} must be even')
      ```
  Теперь нам осталось только зарегистрировать этот модуль, добавив в словарик в ModuleManager пару `{'TEST', Test}`.
  
  Всё это я сейчас написал прямо в браузере, и не тестил, но я верю, что оно сработает, можете попробовать.
  Таким образом я хочу вам продемостировать, что добавить новый модуль очень просто, не говоря уже о
  добавлении одной функции в уже существующий модуль.
  
  Хочу отметить, что во время содания нового модуля мы работали только с папкой `modules`. Т.е. чтобы разрабатывать модули 
  не нужно знать как все устроено под капотом. Я мог бы написать скрипт добавляющий новый модуль, получая на вход массив
  `info` и все необходимые функции логики и валидации. Сложность была бы в валидации этих данных, поэтому я не стал
  этого делать.
