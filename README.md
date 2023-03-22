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

`cado` is a notebook IDE for Python, like [Jupyter](https://jupyter.org/), but with a reactive cell model, taking inspiration from [Observable](https://observablehq.com/). Each cell defines its own outputs that other cells can listen to. When a child cell runs, it uses cached outputs from parent cells. And when the output of a parent cell updates, the change propagates to all child cells automatically.

## Installation

```bash
pip install cado
```

## Usage

```bash
# Start up a cado server
cado up

# Open http://0.0.0.0:8000 in a browser
```

You should now see a screen that lists out all of your notebooks. Click on the example notebook to get started.

<p align="center">
  <img style="inline-block; margin-right: 10px;" src="assets/notebooks-screen.png" height=400>
  <img style="inline-block" src="assets/notebook-screen.png" height=400>
</p>

## Keyboard Shortcuts

| Action                                       | Command        |
| -------------------------------------------- | -------------- |
| Make the cell above the active cell          | `UpArrow`      |
| Make the cell below the active cell          | `DownArrow`    |
| Run the active cell                          | `Shift+Enter`  |
| Clear the active cell                        | `Shift+Delete` |
| Turn on edit mode                            | `Enter`        |
| Turn off edit mode                           | `Escape`       |
| Create a new cell before the active cell     | `Control+a`    |
| Create a new cell after the active cell      | `Control+b`    |
| Create a new cell at the end of the notebook | `Control+n`    |
| Delete the active cell                       | `Control+d`    |

## Features

If you have ideas for new features feel free to create an issue or submit a pull request!

- [x] Reactive cells
- [x] Auto-save to disk
- [x] Keyboard shortcuts
- [x] Drag cells to reorder
- [x] Markdown mode
- [x] Notebook files viewer
