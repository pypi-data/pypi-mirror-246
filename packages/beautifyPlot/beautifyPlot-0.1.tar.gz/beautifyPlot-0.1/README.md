# beautifyPlot
A matplotlib wrapper to make plotting easier. 


## Installation

`pip install beautifyPlot`


## Usage 

Using matplotlib:

```python
import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0,100,1)
y = x**3

plt.plot(x,y,label='y=f(x)')
plt.title("test plot")
plt.xlim([0,10])
plt.ylim([0,1000])
plt.legend(fontsize=15)
plt.tight_layout()



```
Using beautifyPlot

```python
from beautifyPlot.bplt import beautifyPlot
import numpy as np
x = np.arange(0,100,1)
y = x**3

plt.plot(x,y,label='y=f(x)')

beautifyPlot({
    'title':['test plot'], ## Use list to pass a set of arguments to the function
    'xlim':[0,10],
    'ylim':[0,1000],  
    'legend':{'fontsize':15}, ## Use dictionary to specify arguments
    'tight_layout':[] ## Leave list empty if there is nothing to pass 
})


```
