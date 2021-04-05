FROM python:3.9

ADD . .

RUN python3 -m venv /opt/venv 
RUN /opt/venv/bin/python3 -m pip install --upgrade pip
RUN . /opt/venv/bin/activate && pip install --trusted-host pypi.python.org --no-cache -r requirements.txt 
RUN sed -i 's/from imp import reload/from importlib import reload/' /opt/venv/lib/python3.9/site-packages/past/builtins/misc.py

EXPOSE 8050

CMD . /opt/venv/bin/activate && python index.py -p $PORT 