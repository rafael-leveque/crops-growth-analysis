# Crops Growth Analysis

## Performance Review

To process results, we can either use an external library (stackstac) or use xarrays. The first option is easier to use, but the second option is more flexible (and has some serious memory benefits when loading a lot of data).

Here is a quick benchmark comparing the two methods:

| Method    | Parcels | Assets | Time (s) | Memory (GB) | Result (MB) |
| --------- | ------- | ------ | -------- | ----------- | ----------- |
| stackstac | 1       | 1      | 20s      | 2.8         | 950         |
| xarrays   | 1       | 1      | 30s      | 1.6         | 428         |
| stackstac | 1       | 2      | N/A      | > 4         | N/A         |
| xarrays   | 1       | 2      | 46s      | 2.8         | 428         |

Now with bounds, Memory is not an issue at all :

| Method    | Parcels | Assets | Time (s) | Memory (GB) | Result (KB) |
| --------- | ------- | ------ | -------- | ----------- | ----------- |
| stackstac | 1       | 1      | 1.20     | -           | 5.6         |
| xarrays   | 1       | 1      | 1.60     | -           | 2.4         |
| stackstac | 1       | all    | 2.16     | -           | 27.9        |
| xarrays   | 1       | all    | 6.56     | -           | 11.9        |
| stackstac | all     | 1      | 40.77    | -           | 1.1         |
| xarrays   | all     | 1      | 67.22    | -           | 538.6       |
| stackstac | all     | all    | 199      | -           | 11Mb        |
| xarrays   | all     | all    | 677      | -           | 6.5Mb       |

Next step may be to use dask to parallelize the process (stackstac is already using it, maybe that explains the time difference).

## Database choice

Three kind of storage are possible:

- PostgreSQL : popular sql database. Useful for complex queries and sql requests.
- MongoDB : popular nosql database. Useful for storing json data and scaling.
- Minio + Backend : popular object storage. Useful for storing large files and keep light data in a database.

## Visualization

We can use the following libraries to visualize the data:

- Matplotlib : popular library for static plots. A bit basic but reliable for testing.
- Plotly : popular library for interactive plots. A bit less basic and more interactive.

Going outside of python, we can use the following libraries:

- Kepler.gl : popular library for geospatial data. Useful for visualizing large datasets.
- Carto : popular library for geospatial data. Useful for visualizing large datasets. But expensive.
