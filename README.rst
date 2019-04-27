crowdpong-api README
==================

Getting Started
---------------

Use conventional python initialization steps::

  git clone https://github.com/bostrick/crowdpong-api.git
  cd crowdpong-api

  python3 -m venv venv_cp
  source venv_cp/bin/activate

  pip install -U pip setuptools
  pip install -r requirements.txt

  ./app.sh

Note that to run "out of the box", a passwordless redis server must be 
bound to localhost using the standard redis port.



