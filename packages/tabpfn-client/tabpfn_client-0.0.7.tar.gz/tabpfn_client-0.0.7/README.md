# Free client to use an updated TabPFN

This is an alpha family and friends service, so please do not expect this to never be down or run into errors.
We did test it though and can say that it seems to work fine in the settings that we tried.

**We release this to get feedback, if you encounter bugs or curiosities please create an issue or email me (samuelgabrielmuller (at) gmail com).**


# How to

### Tutorial

We created a [![colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/liam-sbhoo/a78a0fab40d8940c218cf2dc3b4f2bf8/tabpfndemo.ipynb)
tutorial to get started quickly.

### Installation

```bash
pip install --extra-index-url https://test.pypi.org/simple/ tabpfn-client
```

### Usage

Import and login
```python
from tabpfn_client import init, TabPFNClassifier
init()
```

Now you can use our model just like any other sklearn estimator
```python
tabpfn = TabPFNClassifier()
tabpfn.fit(X_train, y_train)
tabpfn.predict(X_test)
# or you can also use tabpfn.predict_proba(X_test)
```
