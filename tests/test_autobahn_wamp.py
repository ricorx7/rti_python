from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

class MyComponent(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("component created")

    @inlineCallbacks
    def onJoin(self, details):
        print("session joined")

        def on_send_cmd(cmd):
            print("event send command received: {0}", cmd)

        def on_send_break(time):
            print("event break command received: {0}", time)

        try:
            yield self.subscribe(on_send_cmd, u'com.myapp.oncmd')
            print("subscribed to on_send_cmd")
        except Exception as e:
            print("could not subscribe to topic: {0}".format(e))

        try:
            yield self.subscribe(on_send_break, u'com.myapp.onbreak')
            print("subscribed to on_send_break")
        except Exception as e:
            print("could not subscribe to topic: {0}".format(e))


    def onConnect(self):
        print("transport connected")
        self.join(self.config.realm)

    def onChallenge(self, challenge):
        print("authentication challenge received")

    def onLeave(self, details):
        print("session left")

    def onDisconnect(self):
        print("transport disconnected")

if __name__ == '__main__':
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)

    runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1")
    runner.run(MyComponent)