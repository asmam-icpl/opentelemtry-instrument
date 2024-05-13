from opentelemetry.instrumentation.starlette import StarletteInstrumentor
from starlette import applications
from starlette.responses import PlainTextResponse
from starlette.routing import Route

def home(request):
    return PlainTextResponse("hi")

app = applications.Starlette(
    routes=[Route("/foobar", home)]
)
StarletteInstrumentor.instrument_app(app)
