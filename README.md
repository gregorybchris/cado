<div align="center">
  <img src="assets/cado-banner.png">
  <h1>cado</h1>

  <p>
    <strong>Python notebook IDE with a focus on reactivity</strong>
  </p>

  <br>
  <div>
    <a href="https://badge.fury.io/py/cado"><img src="https://badge.fury.io/py/cado.svg" alt="PyPI"></a>
    <a href="https://pepy.tech/project/cado"><img src="https://pepy.tech/badge/cado" alt="Downloads"></a>
    <a href="https://github.com/gregorybchris/cado/actions/workflows/ci.yaml"><img src="https://github.com/gregorybchris/cado/actions/workflows/ci.yaml/badge.svg" alt="CI"></a>
  </div>
  <br>
</div>

## About

`cado` is a notebook IDE for Python, like [Jupyter](https://jupyter.org/), but with a reactive cell model, taking inspiration from [Observable](https://observablehq.com/). Each cell defines its own outputs that other cells can listen to. When the output of a parent cell updates, the change propagates to all child cells. When a child runs, it uses cached outputs from parent cells, reducing the amount of computation per cell.

## Installation

```bash
pip install cado
```

## Usage

```bash
# Start up a cado server
cado up
```
