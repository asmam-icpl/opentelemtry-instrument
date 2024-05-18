import typing
from typing import Collection

from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.connexion.version import __version__
from opentelemetry.metrics import get_meter
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Span
from opentelemetry.util.http import get_excluded_urls

_excluded_urls = get_excluded_urls("CONNEXION")

_ServerRequestHookT = typing.Optional[typing.Callable[[Span, dict], None]]
_ClientRequestHookT = typing.Optional[typing.Callable[[Span, dict], None]]
_ClientResponseHookT = typing.Optional[typing.Callable[[Span, dict], None]]


class ConnexionInstrumentor(BaseInstrumentor):
    """An instrumentor for Connexion

    See `BaseInstrumentor`
    """

    @staticmethod
    def instrument_app(
        app: typing.Any,
        server_request_hook: _ServerRequestHookT = None,
        client_request_hook: _ClientRequestHookT = None,
        client_response_hook: _ClientResponseHookT = None,
        meter_provider=None,
        tracer_provider=None,
    ):
        """Instrument an uninstrumented Connexion application."""
        meter = get_meter(
            __name__,
            __version__,
            meter_provider,
            schema_url="https://opentelemetry.io/schemas/1.11.0",
        )
        if not getattr(app, "is_instrumented_by_opentelemetry", False):
            app.add_middleware(
                OpenTelemetryMiddleware,
                excluded_urls=_excluded_urls,
                default_span_details=_get_default_span_details,
                server_request_hook=server_request_hook,
                client_request_hook=client_request_hook,
                client_response_hook=client_response_hook,
                tracer_provider=tracer_provider,
                meter=meter,
            )
            app.is_instrumented_by_opentelemetry = True

    @staticmethod
    def uninstrument_app(app: typing.Any):
        app.user_middleware = [
            x
            for x in app.user_middleware
            if x.cls is not OpenTelemetryMiddleware
        ]
        app.middleware_stack = app.build_middleware_stack()
        app._is_instrumented_by_opentelemetry = False

    def instrumentation_dependencies(self) -> Collection[str]:
        return ["connexion"]

    def _instrument(self, **kwargs):
        pass

    def _uninstrument(self, **kwargs):
        pass


def _get_default_span_details(scope):
    """
    Callback to retrieve span name and attributes from scope.

    Args:
        scope: A Connexion request scope
    Returns:
        A tuple of span name and attributes
    """
    operation = scope.get("operation", {})
    summary = operation.get("summary", "")
    tags = operation.get("tags", [])
    method = scope.get("method", "")
    path = scope.get("path", "")
    attributes = {
        SpanAttributes.HTTP_METHOD: method,
        SpanAttributes.HTTP_ROUTE: path,
        SpanAttributes.HTTP_URL: f"{method} {path}",
        SpanAttributes.HTTP_STATUS_CODE: 200,  # Default status code
        SpanAttributes.HTTP_FLAVOR: "1.1",  # Default HTTP version
    }
    if summary:
        attributes[SpanAttributes.HTTP_ROUTE] = summary
    if tags:
        attributes[SpanAttributes.HTTP_ROUTE] = tags[0]
    span_name = f"{method} {path}"
    return span_name, attributes

