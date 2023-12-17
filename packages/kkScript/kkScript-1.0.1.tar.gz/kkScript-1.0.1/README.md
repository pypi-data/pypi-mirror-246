# kkScript
> ```database```
 
***

###### Установка

> Команда pip
>> ```
>> pip install kkscript
>> 
>> ```

***

###### Применение

> Работа с NoSQL базами данных kkdb через .kks файл.
>> ***.py файл***
>> ```
>> from kkScript import script
>>
>> script("code")
>> ```
>> ***.kks файл***
>> ```
>> $kkdb=create.DB."db"."db1".db1
>>
>> $kkdb.setData."age".89.db1
>> $kkdb.updateData.db1
>>
>> printLn=db1.getData("age", "int")
>> ```
>> ***Вывод***
>>
>> ```
>> 89
>> 
>> ```
>> ***Файл базы данных .kkdb***
>> ```
>> age=\data/=89
>> 
>> ```
> Работа с NoSQL базами данных kkdb через .py файл
>> ***.py файл***
>> ```
>> from kkScript import kkdb
>>
>>db1 = kkdb.DB("db", "db1")
>>
>>db1.setData("age",89)
>>db1.updateData()
>>
>>print(db1.getData("age", "int"))
>> ```
>> ***Вывод***
>>
>> ```
>> 89
>> 
>> ```
>> ***Файл базы данных .kkdb***
>> ```
>> age=\data/=89
>> 
>> ```

***

###### Автор

>Никнейм
>> ***Никнейм 1***
>> ```
>> Omny
>> 
>> ```
>> ***Никнейм 2***
>> ```
>> xDrey
>> 
>> ```
>Контакты
>>***Эл. почта***
>>```
>>omenplay325@gmail.com
>>
>>```
>Соц сети
>>***Telegram***
>>>[EasyOmny](https://t.me/EasyOmny)
>>
>>***YouTube***
>>>[Omny](https://youtube.com/@omnycus?si=SoT0Cady7HjVtZ_S)
>>>
>>>[xDrey](https://youtube.com/@xDrey-gnp?si=dt1ryQAAAcEuFC-g)

***

###### Документация

>Ссылка
>>[Пока нет!]()
