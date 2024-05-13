Step1:-create venv in python. 
   
   python3 -m venv venv
  
   source ./venv/bin/activate

   
step2: import some package.

  pip3 install opentelemetry-api
  
  pip3 install opentelemetry-sdk
  
  pip3 install opentelemetry-instrumentation-starlette
  
  pip3 install opentelemetry-distro opentelemetry-exporter-otlp
  
  opentelemetry-bootstrap -a install
  
  pip3 install starlette
  
  pip3 install uvicorn

step3:
  run the container of otel-collector

step3: Run the app

  opentelemetry-instrument --traces-exporter console --metrics-exporter console --logs-exporter console --service-name str-server  uvicorn example:app --host=0.0.0.0 --port=8000

step4: see the log


  
