from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep
from twisted.internet.defer import inlineCallbacks


class MyComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("session ready")

        counter = 0
        while True:
            self.publish(u'com.myapp.onbreak', counter)
            counter += 1
            self.publish(u'com.myapp.oncmd', 'CHS ' + str(counter))
            self.publish(u'some-topic', 'foobar ' + str(counter))
            yield sleep(1)

if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)

    runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1")
    runner.run(MyComponent)