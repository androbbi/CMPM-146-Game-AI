#p4_brains.py
# James Kuch, Antony Robbins
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message is 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message is 'collide' and details['what'] is 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state is 'curious':

      if message is 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message is 'collide' and details['what'] is 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.have_resource = False

  def handle_event(self, message, details):
    if self.body.amount < 0.5:
      self.state = 'flee'
      self.body.set_alarm(0)
    if message is 'order':
      if details is 'i':
        self.state = 'idle'
        self.body.stop()
      elif isinstance(details, tuple):
        self.body.go_to(details)
      elif details is 'a':
        self.state = 'attack'
        self.body.set_alarm(0)
      elif details is 'b':
        self.state = 'build'
        self.target = self.body.find_nearest('Nest')
        if not self.target:
          self.state = 'idle'
        else:
          self.body.follow(self.target)
      elif details is 'h':
        self.state = 'harvest'
        if not self.have_resource:
          self.target = self.body.find_nearest('Resource') 
        else:
          self.target = self.body.find_nearest('Nest')
        self.body.set_alarm(0)

    if self.state is 'attack':
      if message is 'timer':
        mantis = self.body.find_nearest('Mantis')
        if not mantis:
          self.state = 'idle'
          self.body.stop()
        else:
          self.target = mantis
          self.body.follow(self.target)
          self.body.set_alarm(random.random()+1)
      elif message is 'collide' and details['what'] is 'Mantis':
        mantis = details['who']
        mantis.amount -= 0.05
    elif self.state is 'build':
      if message is 'collide' and details['what'] is 'Nest':
        nest = details['who']
        nest.amount += 0.01
    elif self.state is 'harvest':
      if message is 'timer':
        if not self.target:
          self.state = 'idle'
        else:
          self.body.follow(self.target)
      if message is 'collide' and details['what'] is 'Nest' and self.have_resource:
        self.have_resource = False
        close_res = self.body.find_nearest('Resource') 
        self.target = close_res
        self.body.set_alarm(0)
      elif message is 'collide' and details['what'] is 'Resource' and not self.have_resource:
        self.have_resource = True
        resource = details['who']
        resource.amount -= 0.25
        close_nest = self.body.find_nearest('Nest') 
        self.target = close_nest
        self.body.set_alarm(0)
    elif self.state is 'flee':
      if message is 'timer':
        close_nest = self.body.find_nearest('Nest')
        self.body.follow(close_nest)
        self.body.set_alarm(2)
      elif message is 'collide' and details['what'] is 'Nest':
        if self.body.amount < 1:
          self.body.amount += 0.02
          nest = details['who']
          nest.amount -= 0.01
    pass

world_specification = {
 # 'worldgen_seed': 13, # comment-out to randomize
  'nests': 3,
  'obstacles': 15,
  'resources': 5,
  'slugs': 3,
  'mantises': 2,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
