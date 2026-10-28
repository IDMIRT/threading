import time
import asyncio
import threading


async def api_call_1(time_lock):
    print('Начинаем вывод')
    for i in range(5):

        if i == 3:
            await asyncio.sleep(time_lock)

        print(i)
    
    print('Вывод закончен')

async def api_call_2(time_lock):
    print('Некое действие начато')
    await asyncio.sleep(time_lock)
    print('Некое действие закончено')


def long_task(time_lock):
    print(f'Начало потока c задержкой {time_lock}')
    time.sleep(time_lock)
    print(f'Конец потока c задержкой {time_lock}')




async def main1(): #первое задание
   
    await asyncio.gather(api_call_1(3),api_call_2(1))

async def main2(): #второе задание
    task1 = asyncio.create_task(api_call_1(3))
    task2 = asyncio.create_task(api_call_2(1))

    # состояние задач False через .done()
    for task_work in [task1,task2]:
        print(task_work.done())
        
    tasks = [task1,task2]
    for task_work in asyncio.as_completed(tasks):    
        await task_work
   

    # состояние задач True через .done()
    for task_work in [task1,task2]:
        print(task_work.done())


def main3(): #третье задание потоки

    thread1 = threading.Thread(target=long_task, args=(3,)) 
    thread2 = threading.Thread(target=long_task, args=(1,))

    print('Потоки в работе')
    thread1.start()
    thread2.start()    

    thread1.join()
    thread2.join()

    print('Потоки завершены')


def work_process(name_task, limit):

    limit.acquire() #берем один слот в семафоре

    print(f'Задание {name_task} пошло в работу')
    time.sleep(2)
    print(f'Задание {name_task} звершило работу')

    limit.release() #освобождаем слот в семафоре


def main4(quantity):
    print('Старт потоков')
    limit = threading.Semaphore(quantity)

    threads = []

    for i in range(5):
        thr = threading.Thread(target=work_process, args=(f"Задача-{i+1}", limit))
        threads.append(thr)

    for work in threads:
        work.start()

    for work in threads:
        work.join()

    print('Потоки отработали')

    
print('======Первое задание======')    
asyncio.run(main1())

print('======Второе задание======')
asyncio.run(main2())

print('======Третье задание======')
main3()

print('======Четвертое задание======')
main4(2)