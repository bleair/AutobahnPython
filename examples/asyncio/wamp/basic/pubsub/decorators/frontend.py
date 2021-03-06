###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

try:
   import asyncio
except ImportError:
   ## Trollius >= 0.3 was renamed
   import trollius as asyncio

from autobahn import wamp
from autobahn.asyncio.wamp import ApplicationSession



class Component(ApplicationSession):
   """
   An application component that subscribes and receives events,
   and stop after having received 5 events.
   """

   @asyncio.coroutine
   def onJoin(self, details):

      self.received = 0

      ## subscribe all methods on this object decorated with "@wamp.subscribe"
      ## as PubSub event handlers
      ##
      results = yield from self.subscribe(self)
      for res in results:
         if isinstance(res, wamp.protocol.Subscription):
            ## res is an Subscription instance
            print("Ok, subscribed handler with subscription ID {}".format(res.id))
         else:
            ## res is an Failure instance
            print("Failed to subscribe handler: {}".format(res))


   @wamp.subscribe('com.myapp.topic1')
   def onEvent1(self, i):
      print("Got event on topic1: {}".format(i))
      self.received += 1
      if self.received > 5:
         self.leave()


   @wamp.subscribe('com.myapp.topic2')
   def onEvent2(self, msg):
      print("Got event on topic2: {}".format(msg))


   def onDisconnect(self):
      asyncio.get_event_loop().stop()
