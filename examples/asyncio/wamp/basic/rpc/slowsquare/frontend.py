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

import time

try:
   import asyncio
except ImportError:
   ## Trollius >= 0.3 was renamed
   import trollius as asyncio

from functools import partial

from autobahn.asyncio.wamp import ApplicationSession



class Component(ApplicationSession):
   """
   An application component using the time service.
   """

   @asyncio.coroutine
   def onJoin(self, details):

      def got(started, msg, f):
         res = f.result()
         duration = 1000. * (time.clock() - started)
         print("{}: {} in {}".format(msg, res, duration))

      t1 = time.clock()
      d1 = self.call('com.math.slowsquare', 3, 2)
      d1.add_done_callback(partial(got, t1, "Slow Square"))

      t2 = time.clock()
      d2 = self.call('com.math.square', 3)
      d2.add_done_callback(partial(got, t2, "Quick Square"))

      yield from asyncio.gather(d1, d2)
      print("All finished.")
      self.leave()


   def onDisconnect(self):
      asyncio.get_event_loop().stop()
