# npm-deps-viz
Dot generator for npm dependencies

## Usage
```
./main.py {package name}
```

## How to generate png
You need to install graphviz first

```
./main.py {package name} | dot -Tpng -o output.png
```

## Example with react
![Image of Example](https://github.com/lbaillehaiche/npm-deps-viz/blob/master/assest/react.png)

