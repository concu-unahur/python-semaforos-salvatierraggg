import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
comnsalesAtendibles=threading.Lock()
despierto=threading.Semaphore(0)
PlatosDisponibles = 3
platosDisponibles=threading.Semaphore(3)

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global despierto
    global PlatosDisponibles
    global comnsalesAtendibles
    while (True):
      
      despierto.acquire()
      logging.info('Reponiendo los comnsalesAtendibles...')
      for i in range (3):
        PlatosDisponibles +=1 
        platosDisponibles.release()
      
      logging.info(f"hay {PlatosDisponibles} comnsalesAtendibles disponibles")
      
      

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'


  def run(self):
    global PlatosDisponibles
    global despierto
    global comnsalesAtendibles

    
    try:
      
      comnsalesAtendibles.acquire()
      platosDisponibles.acquire()
      PlatosDisponibles -= 1
     
      logging.info(f'¡Qué rico! Quedan {PlatosDisponibles} comnsalesAtendibles') 
      comnsalesAtendibles.release() 
    finally:
      if PlatosDisponibles==0:
        despierto.release()
        #no queria usar un if pero me gano el programa

Cocinero().start()

for i in range(10):
  Comensal(i).start()

