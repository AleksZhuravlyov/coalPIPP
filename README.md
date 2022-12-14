# coalPIPP

## Build

```
git clone https://github.com/AleksZhuravlyov/coalPIPP
cd coalPIPP
mkdir build
cd build
cmake ..
cmake --build .
```

## Preprocess dataset
```
python3 parameters.py ../config/config.ini
```

## Process steady state dataset
```
python3 optimization/steady/analytical_analytical.py config/config.ini
```
or
```
python3 optimization/steady/analytical_scipy.py config/config.ini
```

## Process steady state dataset
```
python3 optimization/transient/numerical_scipy.py config/config.ini
```

### Prerequisites

The libraries you need to install and how to install them

#### macOS:
```
brew install eigen
brew install cmake
brew install pybind11
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
```
#### Ubuntu:
```
apt-get install eigen
apt-get install cmake
apt-get install pybind11
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
```

## Authors

* [**Aleksandr Zhuravlyov**](https://github.com/AleksZhuravlyov/) and [**Zakhar Lanets**](https://github.com/lanetszb/)


## License

This project is licensed under the MIT License wich is a permissive free software license originating at the Massachusetts Institute of Technology (MIT) - see the [LICENSE](LICENSE) file for details