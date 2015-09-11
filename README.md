### Where's the Bus Stop?

Visualizing the proposed metro cuts in Seattle.

[thatplaybyplay.com/wheres_the_bus_stop/](http://thatplaybyplay.com/wheres_the_bus_stop/ "Where's the Bus Stop?")

#### Setting Up

Create and activate a virtual environemnt (recommended):
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Begin a local webserver:
```
python -m SimpleHTTPServer
```

Navigate your browser to the following:
```
localhost:8000/
```

#### Rebuilding datasets (optional)

One command will rebuild to the two `.json` files needed to render the map overlay:
```
PYTHONPATH=. python data_gen/build_dataset.py
```
