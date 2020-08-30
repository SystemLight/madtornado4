from tornado.web import UIModule


class HelloModule(UIModule):

    def __init__(self, handler):
        super(HelloModule, self).__init__(handler)

    def render(self, *args, **kwargs):
        return "<h1>Hello uiModule</h1>"


export = {
    "Hello": HelloModule
}
