# route-optimizer

This is a "basic" python implementation of routing optimization that use a Tabu Search algorithm

There are Service Points with Items, a Vehicle that collects items and a Team with many Vehicles

We have Job represented as a touple (SP_ID, NO_OF_ITEMS) and the are organized as a sequence of jobs Job_Sequence.
TeamJob has (put together) a Job_Sequence and a Team

Solution, Candidate and Neighbourhood classes are use for the searching algorithm

NOTE: This is a POC


# distance metric standarized mapping
This are the location and the state of each SPs (Service Point) in a map (plane)

## Load locations
map location:
data path: 'spList/items'

e.g.:
```
{'id':''spId', 'x':'lng', 'y':'lat', 'meta':{}}
```
location
- id
- x (longitude)
- y (latitude)
- meta

## Create distance matrix
map distance matrix
data path: 'spDMResult/items'
e.g.: 
distance will have the default map of 'distance'
meta: will include additional data that could be aggregated.

```
{'origin': 'originSpId', 'destination':'destinationSpId', 'meta':{}}
```

simplfy standards and map data
- origin
- destination
- distannce
- meta

### How to test it?

Run the following script
```
python test_optimizer.py
```