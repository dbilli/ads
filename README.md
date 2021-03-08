# ads - Anomaly Detection Server

A simple HTTP server implementing Anomaly Detection REST APIs with ADTK (Anomaly Detection Toolkit).

The server is based on Flask/uWSGI.

## Documentation

## Install

    git clone https://github.com/dbilli/ads.git
    
    cd ads
    python setup.py build
    python setup.py install


## Run server

Launch:

    adsd-daemon

With params:

    adsd-daemon --listen 127.0.0.1:5555 --datadir /tmp

## Test Server

    python -m ads.server.test_client  nyc_taxi.csv

### REST API

TODO

## Authors

* **Diego Billi**

## License

This project is licensed under the GNUv2 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* ADTK (https://github.com/arundo/adtk)
