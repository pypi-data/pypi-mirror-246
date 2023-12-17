# nbtof
This module is used to transfer .ipynb file to .py function.
**Table of contents**
- [nbtof](#nbtof)
  - [Intoroduction](#intoroduction)
  - [Documantation](#documantation)
    - [Tags](#tags)
  - [Examples and Recomended Usage](#examples-and-recomended-usage)
    - [Setting Parameters](#setting-parameters)
    - [Batch processing](#batch-processing)
  - [Installation](#installation)



## Intoroduction

Jupyter notebookに`#@`タグをつけることで, notebookの一連の処理を関数に変換することができます.  
たとえば, 下記`short_sample.ipynb`の処理を関数化する場合, 
  
**short_sample.ipynb**

```python
#@param
a = 1
b = 1
```
```python
c = a + b
```
```python
#@return
c
```
  

以下を実行すると, 関数化された`output.py`が出力されます.

```python
import nbtof

nbtof.nbtof_generate(
    output_py_file='output.py',
    notebook_file='short_sample.ipynb',
    )
```

**output.py**
```python
def short_sample(a, b):
    c = a + b
    return c
```
## Documantation
### Tags
| Tag | Description |
| ---- | ---- |
| `#@param` | 関数の引数になります. 代入した数値は無視されます. |
| `#@default` | 関数の引数になります. 代入した数値が既定値として設定されます. |
| `#@args` | 関数の可変長引数 ***args** になります. 代入した数値は無視されます. |
| `#@kwargs` | 関数の可変長引数 ****kwargs** になります. 代入した数値は無視されます. |
| `#@return` | 関数の戻り値になります. |
| `#@ignore` | セル内の内容は無視されます. |
| `#@help` | 関数内の docstring になります. |



## Examples and Recomended Usage

### Setting Parameters
### Batch processing
複数のnotebook, 関数をまとめて1つの py fileに出力する場合は引数の`notebook_file`にnotebookのfilenameもしくはfilepathをリストにして渡す.

## Installation

