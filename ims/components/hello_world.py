from django_unicorn.components import UnicornView


class HelloWorldView(UnicornView):
    name = "World"

    def mount(self):
        arg = self.component_args[0]
        kwarg = self.component_kwargs["name"]

        assert f"{arg} {kwarg}" == "Hello World"
