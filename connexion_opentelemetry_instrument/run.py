from opentelemetry.instrumentation.logging import LoggingInstrumentor




#collector code
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())  # Log to stdout
logger.setLevel(logging.DEBUG)  # Set log level to DEBUG



from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "con-server"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="0.0.0.0:4317"))

traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="0.0.0.0:4317")
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)






# run.py
from app import app
from opentelemetry.instrumentation.connexion import ConnexionInstrumentor


#def post_greeting(name: str):
#    return f"Hello {name}", 200
def post_greeting(name: str):
    try:
        # Your API logic here
        greeting_message = f"Hello {name}"
        # Log a debug message
        logger.debug(f"Greeting sent to {name}")
        return greeting_message, 200
    except Exception as e:
        # Log an error if an exception occurs
        logger.error(f"Error processing greeting for {name}: {e}")
        return "Internal Server Error", 500

app.add_api("openapi.yaml")

ConnexionInstrumentor().instrument_app(app)

LoggingInstrumentor().instrument(set_logging_format=True)
