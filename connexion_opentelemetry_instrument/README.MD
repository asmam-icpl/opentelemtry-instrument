step 1



pip install connexion

pip install connexion[flask,swagger-ui,uvicorn]


connexion  copy the package into below path

 /home/ubuntu/connection_example/connvenv/lib/python3.12/site-packages/opentelemetry/instrumentation


-------------------env var--------------------

export OTEL_PYTHON_LOGGING_CONNEXION__INSTRUMENTATION_ENABLED=true

export OTEL_PYTHON_LOGGING_INSTRUMENTATION_ENABLED=true

step 2 Run using this command

uvicorn run:app --host=0.0.0.0 --port=8000

step 3

put the connexion package into below directory

/home/ubuntu/connection_example/connvenv/lib/python3.12/site-packages


step 4

then run below command




opentelemetry-instrument --traces_exporter console, otlp  --metrics_exporter console, otlp  --logs_exporter console, otlp  --service_name con-server uvicorn run:app --host=0.0.0.0 --port=8000


using this commad oyu can shoew the telemetry data into console

step 5

run otel collector

step 6


opentelemetry-instrument --traces_exporter=otlp --metrics_exporter=otlp --logs_exporter=otlp --service_name=con-server  uvicorn run:app --host=0.0.0.0 --port=8000


using this command show log into otel collector
