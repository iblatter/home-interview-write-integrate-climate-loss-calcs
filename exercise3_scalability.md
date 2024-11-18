## Exercise 3

### Scalability Analysis
As part of exercise 2, the runtimes for each calculation is included in the output.  Each individual calculation took ~10^-7 seconds, but when we get into the hundreds of thousands of buildings that can quickly become slow.  The data loading, even for such a small dataset, is also non-trivial when we are talking about hundreds of thousands of buildings.

### Optimization Strategies
There are two optimizations strategies that could be used here.  The first is parallelizing the processing.  Because python in not technically multithreaded, it may help, or could actually be counter productive, but there are two basic strategies for running the computations in parallel.  The first is threading and the second is sub processes.  The python standard library comes with a `concurrent.futures` that allows running code in parallel (where possible) using either the `ProcessPoolExecutor` or the `ThreadPoolExecutor`.  These classes have similar signatures, which allows us to experiment easily with both and swap them out with little refactoring.  They both allow queueing a set of tasks on a 'pool' that has a max size, etc.  The `ProcessPoolExecutor` executes each task on a pool of sub processes, and the `ThreadPoolExecutor` executes each taks on a pool of sub threads.  Because python is not multi-threaded, the `ThreadPoolExecutor` is generally preferable when the code is IO bound, whereas the `ProcessPoolExecutor` is generally more useful for CPU bound code.  The `ProcessPoolExecutor` comes with more overhead, due to the fact that it has to marshal data across process boundaries.

The other important piece that could be optimized is the input.  Obviously when we get past a small number of buildings, using a file becomes much more cumbersome than it is worth and using a DB or other source of data becomes more important.  If we are still stuck using a file, then we could use a streaming approach to load the data, reading one `building` object at a time and then sending that to a `PoolExecutor` as described above. The more efficient route would be to use a DB or API or some other source for the data, allowing us to have more fine grained control over the queries.

### Resource Management
As we scale up the amount of data processed we will have to keep an eye on system resources.  Setting the max pool sizes, for exampe, if using a `ProcessPoolExecutor` to match the computing power available on the machine.  The other, perhaps simpler way to manage this would be to distribute the computations across multiple machines or serverless functions.  Setting up a queue that would have multiple 'workers' processing the requests would be a generic and highly scalable way to handle this.

### Example Code
In the case where we are not concerned about creating an entire job processing system, but simply running this on one machine, the following code gives a good sense of how to implement a system that parallelizes computation using the `ProcessPoolExecutor`
```
import concurrent.futures

def run_in_parallel(buildings: list[BuildingData]):
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=number_of_requests)
    tasks = {}
    for building in buildings:
        building_id = building["buildingId"]
        args = [building, years_out, standard_discount_rate]
        task = executor.submit(_complex_loss, *args)
        tasks[building_id] = task

    concurrent.futures.wait(tasks)
    results = {}
    for building_id, task in tasks.items():
        result = task.result()
        results[building_id] = result
```
