# Map builder

Map builder is a Python module that allows building a map with films locations that were parsed from the given file.

## Running

Call the Python to run main.py with parameters.

```console
$ python3 main.py 2016 43.422037 -80.525161 locations_simple.list
```

Parameters:
1. The year of filming
2. The latitude and longitude of yours location
3. The path to file with data

## Result

The result of running the module is an HTML file - map.html, which can be opened in any browser.
You can see the markers of the nearest film locations and read its name by click. A blue circle shows from which range locations were found.

![Alt text](map_example.png?raw=true "The map opened in a browser")
