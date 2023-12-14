*******************
How to use NoLoadj ?
*******************

NoLoadj stands for Non-Linear Optimization using Automatic
Differentiation with Jax package. It aims to be a light non-linear optimization
tool for energy components and systems. It is an Open Source project located on
GitLab : https://gricad-gitlab.univ-grenoble-alpes.fr/design_optimization/NoLoad_v2.

.. contents:: Table of Contents

Model computation
=================

Writing the model
-----------------

The first thing to do is to write the equations of your physical model
in a Python function. See the example below with the Rosenbrock
function.

.. figure:: images/bar2.png
.. figure:: images/Rosenbrock.PNG

.. code-block:: python


    def rosenbrock(x,y):
        fobj=(1-x)*(1-x)+100*(y-x*x)**2
        ctr1=(x-1)**3-y+1
        ctr2=x+y-2
        return locals().items()

"locals().items()" returns all the variables defined in the function.
NoLoadj will select those you will write in specifications.
If you use mathematical functions, you must call the
jax.numpy library at the beginning of the code :

.. code-block:: python


    import jax.numpy as np

The mathematical functions are "np.exp(x),np.log(x),np.cos(x),... ".
Examples in the following parts will illustre this point.

You also have rules to respect when you create your function because of Jax :

- For assignment to arrays, use JAX pure functional operators instead of A[0] = x : https://jax.readthedocs.io/en/latest/jax.ops.html.
- Do not put a JAX array in a numpy method, and do not put a numpy array in a JAX method.
- Assignments on dataframe (from pandas library) do not work with JAX array.
- "if" structure does not work with JIT functionality, use cond function from jax.lax package : https://jax.readthedocs.io/en/latest/jax.lax.html#control-flow-operators
- Implicit casting of lists to arrays A = np.sum([x, y]), use A = np.sum(np.array([x, y])) instead.

ComputeOnce
-----------

To see how the outputs of your model react to the inputs, you may use
ComputeOnce function. In the example below, we use Rosenbrock function
defined above. The "inputs" attribute is a dictionary with the names and
the values of your inputs, the "outputs" attribute is a list with the
outputs names you want to compute. Then, the "model" attribute is the
name of your function, and it returns a list of the outputs values.

.. code-block:: python

    from noloadj.analyse.simulation import computeOnce

    inputs={'x':1.0, 'y':2.0}
    outputs=['fobj','ctr1','ctr2']
    results = computeOnce(model=rosenbrock, inputs=inputs, outputs=outputs)
    print(outputs, '=', results)


.. parsed-literal::

    ['fobj', 'ctr1', 'ctr2'] = [100.0, -1.0, 1.0]


If there are fixed parameters in your model, they must be put in the
inputs attribute.

ComputeParametric
-----------------

ComputeParametric is a useful function to compute outputs values
according to an input varying in a range of values. In the example below
with the Rosenbrock function, the "inputs" attribute is a dictionary
with the names and the values of the non-varying inputs. The "outputs"
attribute is a list with outputs names you want to compute. The
"variable" attribute is the name of the varying input, and the "values"
attribute is the range of values the input can take. Then, the "model"
attribute is the name of your model function.

.. code-block:: python

    from noloadj.analyse.simulation import computeParametric
    inputs={'y':2.0}
    outputs=['fobj','ctr1','ctr2']

    variable = 'x'
    values = np.arange(-1.5, 1.5, 0.1) #[-1.5, -1.4, ..., 1.5]
    iter = computeParametric(rosenbrock, variable, values, inputs, outputs)

It returns an "Iteration class" with all outputs values. To print all
the values numerically, you may use print function.

.. code-block:: python

    df=iter.print()
    print(df)
.. parsed-literal::

    |    |            x |   fobj |    ctr1 |         ctr2 |
    |---:|-------------:|-------:|--------:|-------------:|
    |  0 | -1.5         |  12.5  | -16.625 | -1.5         |
    |  1 | -1.4         |   5.92 | -14.824 | -1.4         |
    |  2 | -1.3         |  14.9  | -13.167 | -1.3         |
    |  3 | -1.2         |  36.2  | -11.648 | -1.2         |
    |  4 | -1.1         |  66.82 | -10.261 | -1.1         |
    |  5 | -1           | 104    |  -9     | -1           |
    |  6 | -0.9         | 145.22 |  -7.859 | -0.9         |
    |  7 | -0.8         | 188.2  |  -6.832 | -0.8         |
    |  8 | -0.7         | 230.9  |  -5.913 | -0.7         |
    |  9 | -0.6         | 271.52 |  -5.096 | -0.6         |
    | 10 | -0.5         | 308.5  |  -4.375 | -0.5         |
    | 11 | -0.4         | 340.52 |  -3.744 | -0.4         |
    | 12 | -0.3         | 366.5  |  -3.197 | -0.3         |
    | 13 | -0.2         | 385.6  |  -2.728 | -0.2         |
    | 14 | -0.1         | 397.22 |  -2.331 | -0.1         |
    | 15 |  1.33227e-15 | 401    |  -2     |  1.33227e-15 |
    | 16 |  0.1         | 396.82 |  -1.729 |  0.1         |
    | 17 |  0.2         | 384.8  |  -1.512 |  0.2         |
    | 18 |  0.3         | 365.3  |  -1.343 |  0.3         |
    | 19 |  0.4         | 338.92 |  -1.216 |  0.4         |
    | 20 |  0.5         | 306.5  |  -1.125 |  0.5         |
    | 21 |  0.6         | 269.12 |  -1.064 |  0.6         |
    | 22 |  0.7         | 228.1  |  -1.027 |  0.7         |
    | 23 |  0.8         | 185    |  -1.008 |  0.8         |
    | 24 |  0.9         | 141.62 |  -1.001 |  0.9         |
    | 25 |  1           | 100    |  -1     |  1           |
    | 26 |  1.1         |  62.42 |  -0.999 |  1.1         |
    | 27 |  1.2         |  31.4  |  -0.992 |  1.2         |
    | 28 |  1.3         |   9.7  |  -0.973 |  1.3         |
    | 29 |  1.4         |   0.32 |  -0.936 |  1.4         |


You can also use the plotXY function to print it graphically.

.. code-block:: python

    iter.plotXY()

.. figure:: images/output_20_0.png

.. figure:: images/output_20_2.png


ComputeJacobian
---------------

To compute the gradient of the objective and constraints of your model,
you may use computeJacobian function. It has the same structure as the
ComputeOnce function.

.. code-block:: python

    from noloadj.analyse.simulation import computeJacobian

    inputs={'x':1.0, 'y':2.0}
    outputs = ['fobj', 'ctr1', 'ctr2']
    dfobj,dctr1,dctr2 = computeJacobian(model=rosenbrock, inputs=inputs,
                                    outputs=outputs)
    print('dfobj =', dfobj)
    print('dctr1 =', dctr1)
    print('dctr2 =', dctr2)

.. parsed-literal::

    dfobj = [-400.0, 200.0]
    dctr1 = [0.0, -1.0]
    dctr2 = [1.0, 1.0]


Unconstrained Optimization
==========================

To solve an unconstrained optimization problem, see the example below
with the Ackley function.

Ackley function
---------------
.. figure:: images/bar.png
.. figure:: images/Ackley.png

The objective is written in the Python function below. Note the use of
jax.numpy mathematical functions such as np.square, np.exp, …

.. code-block:: python

    import jax.numpy as np
    import math

    def ackley(x,y):
        fobj = -20 * np.exp(-0.2 * np.sqrt(0.5 * (np.square(x) + np.square(y)))) \
               - np.exp(0.5 * (np.cos(2 * math.pi * x) + np.cos(2 * math.pi * y))) \
               + math.exp(1) + 20
        return locals().items()

The specifications of the optimization problem are written in the Spec
class. The "variables" attribute is a dictionary with the names and the
initial values of the variables to optimize. The "bounds" attribute is
also a dictionary which represents the search domain for the variables.
The "objective" attribute is a dictionary with the name of the objective
function and a gap of values that can take this function.

.. code-block:: python

    from noloadj.optimization.optimProblem import Spec, OptimProblem

    spec = Spec(variables={'x':2, 'y':2}, bounds={'x':[-5, 5], 'y':[-5, 5]},
                objectives={'fobj':[0.,15.]})

We define the optimization problem with the OptimProblem class. The
"model" attribute is the name of your model function, and the
"specifications" attribute corresponds to the class defined before.

.. code-block:: python

    optim = OptimProblem(model=ackley, specifications=spec)

We start the optimization with the "run" function of the OptimProblem
class. It returns a "result" class.

.. code-block:: python

    result = optim.run()


.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: [6.64437582e-05]
                Iterations: 9
                Function evaluations: 20
                Gradient evaluations: 9


The optimization was successfully done. The "Current objective function"
is the objective function evaluated at the optimal point (here
f(opt)=0). We print the optimized variable with the "printResults"
function.

.. code-block:: python

    result.printResults()


.. parsed-literal::

    {'x': 1.5781116638803522e-05, 'y': 1.739422385733534e-05}
    {'fobj': 6.644375817899117e-05}


We find the global minimum expected : f(0,0)=0.

Actually, there are attributes for the "run" function such as the
tolerance wanted for the objective function (ftol) and the name of the
optimization algorithm (method). By default, ftol=1e-5 and the method is
'SLSQP' ( for Sequential Least Square Quadratic Programming algorithm).
Other algorithms are :

- 'LeastSquare' for Least Square algorithm (only for unconstrainted optimization).
- 'IPOPT' for Interior Point method.
- 'stochastic' for a genetic algorithm (without gradients). With this algorithm,
you should add an input parameter called 'popsize' which is the length of the
initial population sample.
We can rerun the previous optimization with an other method.

.. code-block:: python

    result = optim.run(ftol=1e-7,method='LeastSquare')


.. parsed-literal::

    `gtol` termination condition is satisfied.
    Solution found:  [-4.4408921e-16  8.8817842e-16]
    Value of the cost function at the solution:  6.310887241768095e-30
    Vector of residuals at the solution:  [3.55271368e-15]
    Gradient of the cost function at the solution:  [-4.49386684e-15  8.98773368e-15]


We find the same results as before.

Display results
---------------

There are several functions to print or return the results of the
optimization. Note that all these functions are methods of the result
class.

At first, the "printResults" method to print optimized variables and
outputs (objective function + constraints) as dictionaries.

.. code-block:: python

    result.printResults()


.. parsed-literal::

    {'x': -4.440892098500626e-16, 'y': 8.881784197001252e-16}
    {'fobj': 3.552713678800501e-15}


"plotResults" shows graphically values of inputs and outputs for each iteration
 of the optimization. Outputs are choosen by the user with a list.

.. code-block:: python

    result.plotResults(['fobj'])

.. figure:: images/output_48_0.png

.. figure:: images/output_48_2.png

solution returns a list with the values of optimized variables.

.. code-block:: python

    sol=result.solution()
    print('sol=',sol)

.. parsed-literal::

    sol= [-4.440892098500626e-16, 8.881784197001252e-16]


getLastInputs returns a dictionary of the optimized variables.

.. code-block:: python

    inp=result.getLastInputs()
    print('inp=',inp)

.. parsed-literal::

    inp= {'x': -4.440892098500626e-16, 'y': 8.881784197001252e-16}


getLastOutputs returns a dictionary of the optimized outputs.

.. code-block:: python

    out=result.getLastOutputs()
    print('out=',out)

.. parsed-literal::

    out= {'fobj': 3.552713678800501e-15}


printAllResults prints the different variables of inputs during each
iteration of the optimization.

.. code-block:: python

    result.printAllResults()

.. parsed-literal::

    {'x': 2.0, 'y': 2.0}
    {'x': 0.6593599079287253, 'y': 0.6593599079287253}
    {'x': 0.4104981710953608, 'y': 0.41049817109536085}
    {'x': -5.0, 'y': -5.0}
    {'x': -1.6440850614698304, 'y': -1.6440850614698304}
    {'x': -0.33810682730902497, 'y': -0.3381068273090249}
    {'x': 0.09148338273764894, 'y': 0.09148338273764844}
    {'x': -0.1799196026243623, 'y': -0.17991960262435064}
    {'x': -0.00895860673980714, 'y': -0.008958606739803143}
    {'x': 0.02067226145979892, 'y': 0.020672261459031463}
    {'x': 0.0012982860687560573, 'y': 0.0012982860684930125}
    {'x': -0.00337098703976194, 'y': -0.003370986812025232}
    {'x': -0.0003054604929685332, 'y': -0.0003054604149209264}
    {'x': 0.0004861656298466346, 'y': 0.0004859049562408854}
    {'x': 1.6682393036306098e-05, 'y': 1.657636128318536e-05}
    {'x': -0.0033402599064650375, 'y': 0.0030628310706608134}
    {'x': -0.0003190118369138283, 'y': 0.0003212018322209482}
    {'x': -1.6887029958707345e-05, 'y': 4.703890837696164e-05}
    {'x': 1.3325450736804753e-05, 'y': 1.9622615992562988e-05}
    {'x': 1.5781116638803522e-05, 'y': 1.739422385733534e-05}
    {'x': 2.0, 'y': 2.0}
    {'x': -4.440892098500626e-16, 'y': 8.881784197001252e-16}


getIteration returns the variables and outputs values at an Iteration
given in parameter (the 3rd one in the code below).

.. code-block:: python

    inp,out=result.getIteration(3)
    print('inp=',inp)
    print('out=',out)

.. parsed-literal::

    inp= {'x': 0.4104981710953608, 'y': 0.41049817109536085}
    out= {'fobj': 3.865550771773872}

Graphical User Interface (GUI)
------------------------------

There is also a graphical user interface (GUI) than can be called with openGUI
method of wrapper class.
.. code-block:: python

    result.openGUI()
To display one variable, right-click on it then select "Plot" option.

Ackley function with fixed parameters
-------------------------------------

We add fixed parameters, for which values are given before the optimization,
to the Ackley function :'a','b','c' are added to Ackley function inputs with x,y
variables.

We fix the parameters values in the 'p' dictionnary.

.. code-block:: python

    def ackley(x,y,a,b,c):
        fobj = -a * np.exp(-b * np.sqrt(0.5 * (np.square(x) + np.square(y)))) \
               - np.exp(0.5 * (np.cos(c * x) + np.cos(c* y))) \
               + math.exp(1) + 20
        return locals().items()

    p={'a':20.0,'b':0.2,'c':2*math.pi}

We do the same procedure as in the previous chapter, to define the
optimization problem, except that we add the parameters dictionary to
the OptimProblem class.

.. code-block:: python

    spec = Spec(variables={'x':2, 'y':2}, bounds={'x':[-5, 5], 'y':[-5, 5]},
                objectives={'fobj':[0.,15.]})
    optim = OptimProblem(model=ackley, specifications=spec,parameters=p)
    result = optim.run()
    result.printResults()


.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: [6.64437582e-05]
                Iterations: 9
                Function evaluations: 20
                Gradient evaluations: 9
    {'x': 1.5781116638803522e-05, 'y': 1.739422385733534e-05}
    {'fobj': 6.644375817899117e-05}


Optimization with input vector
------------------------------

Instead of using scalar variables, we can rewrite the model function
with vector variables. In the example below,a 2-dimensions vector X is used
instead of the 2 scalar variables x,y.

.. code-block:: python

    def ackley(X,a,b,c):
        x=X[0]
        y=X[1]
        fobj = -a * np.exp(-b * np.sqrt(0.5 * (np.square(x) + np.square(y)))) \
               - np.exp(0.5 * (np.cos(c * x) + np.cos(c* y))) \
               + math.exp(1) + 20
        return locals().items()

    p={'a':20.0,'b':0.2,'c':2*math.pi}

Therefore, there are changes in the Spec class : the initial values of
variables are defined in a list, and their bounds with the following
form : [ [min coordinate1, max coordinate1], [min coordinate2, max
coordinate2] ].

.. code-block:: python

    spec = Spec(variables={'X':[2,2]}, bounds={'X':[[-5, 5],[-5, 5]]},
                objectives={'fobj':[0.,15.]})
    optim = OptimProblem(model=ackley, specifications=spec,parameters=p)
    result = optim.run()
    result.printResults()


.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: [6.64437582e-05]
                Iterations: 9
                Function evaluations: 20
                Gradient evaluations: 9
    {'X': [[1.5781116638803522e-05, 1.739422385733534e-05]]}
    {'fobj': 6.644375817899117e-05}


You can mix scalar and vector variables in the same optimization
problem.

Constrained Optimization
========================

Optimization problems with constraints (equality or inequality ones) are
treated in the following chapter. See the example below with the
Rosenbrock function.

Constrained Rosenbrock function
-------------------------------

We want to minimize the Rosenbrock function subjected to 2 inequality
constraints with upper bound equals to 0 and no lower bound.

.. figure:: images/bar2.png
.. figure:: images/Rosenbrock.PNG

We define the model function below :

.. code-block:: python

    def rosenbrock(x,y):
        fobj=(1-x)*(1-x)+100*(y-x*x)**2
        ctr1=(x-1)**3-y+1
        ctr2=x+y-2
        return locals().items()

We add the inequality constraints to the problem by using the
"ineq_cstr" attribute in the Spec class. It's a dictionary with the
names and the gap of the inequality constraints ("None" indicates that
there is no lower (or upper) bound as in this example).

.. code-block:: python

    spec = Spec(variables={'x':2.0, 'y':2.0},
                bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
                objectives={'fobj':[0.,15.]},
                ineq_cstr={'ctr1':[None, 0],'ctr2':[None, 0]})

    optim = OptimProblem(model=rosenbrock, specifications=spec)
    result = optim.run()
    result.printResults()


.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: [2.88481749e-24]
                Iterations: 7
                Function evaluations: 14
                Gradient evaluations: 7
    {'x': 1.0000000000000566, 'y': 0.9999999999999435}
    {'fobj': 2.8848174917769927e-24, 'ctr1': 5.651035195342047e-14, 'ctr2': 0.0}


We can also define ctr1 as an equality constraint that must be equal to
0. We do this by using the "eq_cstr" of the Spec class :

.. code-block:: python

    spec = Spec(variables={'x':2.0, 'y':2.0},
                bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
                objectives={'fobj':[0.,15.]}, eq_cstr={'ctr1':0},
                ineq_cstr={'ctr2':[None, 0]})

    optim = OptimProblem(model=rosenbrock, specifications=spec)
    result = optim.run()
    result.printResults()


.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: [5.42085619e-09]
                Iterations: 7
                Function evaluations: 8
                Gradient evaluations: 7
    {'x': 0.9999975471448505, 'y': 1.0000024528551497}
    {'fobj': 5.420856190159052e-09, 'ctr1': -2.4528551496594275e-06, 'ctr2': 0.0}


Optimization with constrained vector
------------------------------------

Instead of using scalar constraints, we can rewrite the model function
with a constraint vector.

.. code-block:: python

    def rosenbrock(x,y):
        fobj=(1-x)*(1-x)+100*(y-x*x)**2
        ctr=[(x-1)**3-y+1 , x+y-2]
        return locals().items()

We define the gap admissible for the inequality constraints in the
"ineq_cstr" attribute of the Spec class. The syntax is the following : [
[min coordinate1, max coordinate1], [min coordinate2, max coordinate2]
].

.. code-block:: python

    spec = Spec(variables={'x':2.0, 'y':2.0},
                bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
                objectives={'fobj':[0.,15.]},
                ineq_cstr={'ctr':[[None, 0],[None, 0]]})

    optim = OptimProblem(model=rosenbrock, specifications=spec)
    result = optim.run()
    result.printResults()


.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: [2.88481749e-24]
                Iterations: 7
                Function evaluations: 14
                Gradient evaluations: 7
    {'x': 1.0000000000000566, 'y': 0.9999999999999435}
    {'fobj': 2.8848174917769927e-24, 'ctr': [5.651035195342047e-14, 0.0]}


OptimizeParam
-------------

OptimizeParam is a function that solves all optimization problems
according to an input varying in a range of values, while the others
remain constants.

The model function is defined below.

.. code-block:: python

    def rosenbrock(x,y):
        fobj=(1-x)*(1-x)+100*(y-x*x)**2
        ctr1=(x-1)**3-y+1
        ctr2=x+y-2
        return locals().items()

We define the Spec class with only constant variables (not the varying
one) in the "variables" and "bounds" attributes, and only the objective
(not the constraints). The attributes for the optimizeParam function are
: the "model" function, the "specifications" defined by the Spec class,
the fixed parameters (optional) in "parameters", the name of the varying
variable in "variable", a vector with all the values that the "variable"
can take in "range", and the names of the objective function and
constraints in "outputs".

.. code-block:: python

    from noloadj.optimization.optimProblem import optimizeParam

    spec = Spec(variables={'y':2.0}, bounds={'y':[-0.5, 2.5]}, objectives={'fobj':[0.,15.]})

    iter = optimizeParam(model=rosenbrock, specifications=spec,
                         parameters={}, variable='x',
                         range=np.arange(-1.5, 2.0, 0.5), #[-1.5,-1,...,1.5]
                         outputs=['fobj', 'ctr1', 'ctr2'])


We display the results with the "print" function.

.. code-block:: python

    df=iter.print()
    print(df)
.. parsed-literal::

    |    |    x |   fobj |    ctr1 |   ctr2 |
    |---:|-----:|-------:|--------:|-------:|
    |  0 | -1.5 |   6.25 | -16.875 |  -1.25 |
    |  1 | -1   |   4    |  -8     |  -2    |
    |  2 | -0.5 |   2.25 |  -2.625 |  -2.25 |
    |  3 |  0   |   1    |   0     |  -2    |
    |  4 |  0.5 |   0.25 |   0.625 |  -1.25 |
    |  5 |  1   |   0    |   0     |   0    |
    |  6 |  1.5 |   0.25 |  -1.125 |   1.75 |

We display the results graphically with the "plotXY" function.

.. code-block:: python

    iter.plotXY()

.. figure:: images/output_96_0.png

.. figure:: images/output_96_2.png


FreeOutputs(XML)
----------------

Suppose that in your problem, there are outputs you want to see the values
accross iterations but you don't want to constraint them.
These are called "freeOutputs".

.. code-block:: python

    def rosenbrock(x,y):
        fobj=(1-x)*(1-x)+100*(y-x*x)**2
        ctr1=(x-1)**3-y+1
        ctr2=x+y-2
        return locals().items()

Back to the Rosenbrock optimization problem, we define ctr1 as an
equality constraint and ctr2 as a freeOutput. It is done by using the
"freeOutputs" attribute in the Spec class.

.. code-block:: python

    spec = Spec(variables={'x':2.0, 'y':2.0},
                bounds={'x':[-1.5, 1.5],'y':[-0.5, 2.5]},
                objectives={'fobj':[0.,15.]},
                eq_cstr={'ctr1': 0},freeOutputs=['ctr2'])

.. code-block:: python

    optim = OptimProblem(model=rosenbrock, specifications=spec)
    result = optim.run()
    result.printResults()

.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: [5.19862556e-09]
                Iterations: 10
                Function evaluations: 11
                Gradient evaluations: 10
    {'x': 0.9999963993636343, 'y': 0.9999999998935956}
    {'fobj': 5.198625557105132e-09, 'ctr1': 1.0640444081388978e-10, 'ctr2': -3.6007427701711947e-06}


The getIteration function is very useful to print the value of the
freeOutput at a certain iteration (for instance, the 4th one in the code
below).

.. code-block:: python

    inp,out,fp=result.getIteration(4)
    print('inp=',inp)
    print('out=',out)
    print('fp=',fp)

.. parsed-literal::

    inp= {'x': 0.7239575043144895, 'y': 0.9974823725823181}
    out= {'fobj': 22.483916763247052, 'ctr1': -0.01851666153168452}
    fp= {'ctr2': -0.27856012310319245}


You can export the results in the XML format by using the
"exportToXML" function.

.. code-block:: python

    result.exportToXML("rosenbrock.result")

In your work folder, a XML file named 'rosenbrock.result' will appear.
You can open it and see that all inputs and outputs values are printed for each
iteration of the optimization.

Multi-Objective Optimization
============================

NoLoad can also solve multi-objective optimization problems. See the
example below with the Binh and Korn function.

Binh and Korn function
----------------------

.. figure:: images/BinhAndKorn.png

We define the Binh and Korn function with 2 objective functions and 2
inequality constraints.

.. code-block:: python

    def BinhAndKorn(x, y):
        f1 = 4*x**2+4*y**2
        f2 = (x-5)**2+(y-5)**2
        g1 = (x-5)**2+y
        g2 = (x-8)**2+(y+3)**2
        return locals().items()

We do the procedure described in the previous parts, except that the
"objectives" attribute is a list of 2 elements, each one is the name of
an objective function.

.. code-block:: python

    spec = Spec(variables={'x':0, 'y':0}, bounds={'x':[0, 5], 'y':[0, 3]},
                objectives={'f1':[0.,140.],'f2':[0.,50.]},
                ineq_cstr={'g1':[None, 25],'g2':[7.7, None]})

    optim = OptimProblem(model=BinhAndKorn, specifications=spec)
    result = optim.run()


.. parsed-literal::

    Optimization terminated successfully    (Exit mode 0)
                Current function value: 0.0
                Iterations: 1
                Function evaluations: 1
                Gradient evaluations: 1
    Optimization terminated successfully    (Exit mode 0)
                Current function value: [4.]
                Iterations: 2
                Function evaluations: 2
                Gradient evaluations: 2
    Singular matrix C in LSQ subproblem    (Exit mode 6)
                Current function value: 50.0
                Iterations: 1
                Function evaluations: 1
                Gradient evaluations: 1
    WARNING : Optimization doesn't converge... Trying random inital guess
    Optimization terminated successfully    (Exit mode 0)
                Current function value: [13.72381047]
                Iterations: 8
                Function evaluations: 10
                Gradient evaluations: 8
    Optimization terminated successfully    (Exit mode 0)
                Current function value: [5.69821164]
                Iterations: 5
                Function evaluations: 6
                Gradient evaluations: 5
    Optimization terminated successfully    (Exit mode 0)
                Current function value: [8.13884001]
                Iterations: 7
                Function evaluations: 7
                Gradient evaluations: 7


| To print the Pareto front, we use the "plotPareto" function of the result class.
| ['Pareto'] is the legend of the graph and 'Pareto Front' its title.

.. code-block:: python

    result.plotPareto(['BinhAndKorn'],'Pareto Front')

.. figure:: images/output_117_0.png


To get the inputs and outputs at a point, "getIteration" function is
useful. For instance, the 2nd point from the left corresponds to the 2nd
iteration of the multi-objective optimization, as shown below.

.. code-block:: python

    inp,out=result.getIteration(2)
    print('inp=',inp)
    print('out=',out)

.. parsed-literal::

    inp= {'x': 1.0086280321907704, 'y': 1.0086523159535503}
    out= {'f1': 8.138840007197945, 'f2': 31.861906520356282, 'g1': 16.939702501366874, 'g2': 64.94857538246845}


You can select the number of Pareto points to print in the graph with
the "nbParetoPoints" attribute of the optim.run function (by default,
nbParetoPts=5). With the "disp" attribute set to False, the message
"Optimization terminated successfully" is not printed. You can also change solving
method ('epsconstr' by default, or 'ponderation').

.. code-block:: python

    optim = OptimProblem(model=BinhAndKorn, specifications=spec)

    result = optim.run(disp=False,nbParetoPts=6,method2d='ponderation')

    result.plotPareto(['6points'],'Pareto Front',nb_annotation=6)

.. parsed-literal::

    WARNING : Optimization doesn't converge... Trying random inital guess



.. figure:: images/output_121_1.png


Display several curves in the same graph
----------------------------------------

You can print several Pareto fronts in the same graph. For example,
suppose we add a parameter "a" to the Binh and Korn function and we want
to do 3 Pareto fronts with differents values of a.

.. code-block:: python

    def BinhAndKorn(x, y, a):
        f1 = a*x**2+a*y**2
        f2 = (x-5)**2+(y-5)**2
        g1 = (x-5)**2+y
        g2 = (x-8)**2+(y+3)**2
        return locals().items()

.. code-block:: python

    p = {'a':4}
    optim = OptimProblem(BinhAndKorn, spec, p)
    result1 = optim.run(disp=False)

    p = {'a':6}
    optim = OptimProblem(BinhAndKorn, spec, p)
    result2 = optim.run(disp=False)

    p = {'a':8}
    optim = OptimProblem(BinhAndKorn, spec, p)
    result3 = optim.run(disp=False)

.. parsed-literal::

    WARNING : Optimization doesn't converge... Trying random inital guess
    WARNING : Optimization doesn't converge... Trying random inital guess
    WARNING : Optimization doesn't converge... Trying random inital guess


We plot the final results after adding the previous result classes in the
addParetoList method.

.. code-block:: python

   result3.addParetoList(result1,result2)
   result3.plotPareto(['a=4','a=6','a=8'],'Comparaison')

.. figure:: images/output_128_0.png


To avoid annotations on the graph, you can hide them by
putting with the "nb_annotation" attribute of the plotPareto.function
equal to 0. The "joinDots" attribute put to False do not connect dots on the graph.

.. code-block:: python

    result3.plotPareto(['a=4','a=6','a=8'],'Comparaison',nb_annotation = 0)

.. figure:: images/output_130_0.png

Dynamic systems optimization
============================

NoLoad can also be used to solve optimization problems with dynamic systems.
Several functions are available in the ODE folder to run dymamic simulation :

- odeint44 (file : ode44) solves an ODE system with a Runge-Kutta 44 algorithm. It stores values across time. It is used for optimal control problems.
- odeint45 (file : ode45) solves an ODE system with a Runge-Kutta 45 algorithm. It stores values across time.
- odeint45_extract (file : ode45_extract) solves an ODE system with a Runge-Kutta 45 algorithm, without storage of values across time. Features can be calculated from the simulation.
- odeint45_fft (file : ode45_fft) solves an ODE system with a Runge-Kutta 45 algorithm, and computes its Fast-Fourier Transform (FFT). It stores values across time.
- odeint45_extract_fft (file : ode45_extract_fft) solves an ODE system with a Runge-Kutta 45 algorithm, and computes its Fast-Fourier Transform (FFT) without storage of values across time. Features can be calculated from the simulation and the FFT.

Optimal control example
-----------------------

Let's solve the optimization problem defined below with NoLoad :

min J(u,p)= p

s.t x1_dot=p*x3*cos(u)

    x2_dot=p*x3*sin(u)

    x3_dot=p*sin(u)

    -(0.4*x1-x2+0.2)>=0 (constraint)

    x1(1)=0 (constraint)

    x(0)=(0,0,0) (initial point)

    -4<u<4 (bounds)

    1<p<100 (bounds)

First, we need to define our ODE system in a python class :

.. code-block:: python

    import jax. numpy as np
    from noloadj.ODE.ode_tools import get_indice

    class Brachistochrone():

        def __init__(self):
            self.xnames=['x1','x2','x3']
            self.ynames=['x1']

        def derivative(self,x,t,u,p):
            x3=get_indice(self.xnames,x,['x3'])
            x1_dot=p*x3*np.cos(u[indice_t(t,pas)])
            x2_dot=p*x3*np.sin(u[indice_t(t,pas)])
            x3_dot=p*np.sin(u[indice_t(t,pas)])
            return np.array([x1_dot,x2_dot,x3_dot])

        def output(self,x,t,u,p):
            return x[0]

The 2 attributes of the class are:

- xnames : a list with the names of state variables.
- ynames : a list with the names of output variables.

2 methods must be defined :

- derivative : it describes the ODE system (with as input parameters: x the state variable, t the time, then the optimization inputs).
- output : it describes the expression of the output variables (with the same inputs parameters as the derivative method).

get_indice is a function from ode_tools file, that returns the coordinate of an array corresponding to the variable name given as input parameter.

We can then define the optimization problem with NoLoad :

.. code-block:: python

    from noloadj.optimization.optimProblem import OptimProblem,Spec
    from noloadj.ODE.ode44 import odeint44
    from noloadj.ODE.ode_tools import vect_temporel

    def model(u,p,x10,x20,x30,tf,pas):
        t_eval=vect_temporel(0,tf,pas)
        brachistochrone=Brachistochrone()
        x,y = odeint44(brachistochrone,np.array([x10,x20,x30]), t_eval,u,p)
        x1,x2,x3=get_indice(brachistochrone.xnames,x,['x1','x2','x3'])
        cstr=-(0.4*x1-x2+0.2*np.ones(len(x1))) # inequality constraint
        x1f=x1[-1] # equality constraint
        J=p  # objective function
        return locals().items()

    pas=0.01 # stepsize
    tf=1. # final time of the simulation
    N=int(tf/pas)-1 # number of points during the simulation
    ulim,cstr=[],[]
    for i in range(N):
        ulim.append([-4,4])
        cstr.append([None,0.])

    spec=Spec(variables={'u':[0.5]*N,'p':2.0},bounds={'u':ulim,'p':[1,100]},objectives={'J':[0.,5.]},
          eq_cstr={'x1f':1.},ineq_cstr={'cstr':cstr},
          freeOutputs=['x1','x2','x3'])

    parameters={'x10':0.,'x20':0.,'x30':0.,'tf':tf,'pas':pas} # constant inputs during the simulation
    optim=OptimProblem(model=model,specifications=spec,parameters=parameters)
    result=optim.run()

.. parsed-literal::
    Optimization terminated successfully 	(Exit mode 0)
                Current function value: 1.795235462608259
                Iterations: 10
                Function evaluations: 12
                Gradient evaluations: 10



vect_temporel is a function from ode_tools that create a time vector with an initial time, a final time and stepsize.
odeint44 has for input parameters :

- the class that describes the ODE system defined above.
- the initial state vector.
- the time vector.
- optimization inputs (here u and p).

It returns two matrices : one with the values of state variables across time simulation (x),
and the other with the values of output variables across time simulation (y).

Sizing of a ball
----------------

Let's do an optimization problem of sizing. We want to size a ball so that its throw respects some constraints.
In this case, we will use ODE function with Runge-Kutta 45 algorithms without storage of values across time simulation.

We define the ODE system below.

.. code-block:: python

    import jax. numpy as np
    from noloadj.ODE.ode_tools import *

    class Ball():

        def __init__(self):
            self.g=9.81
            self.xnames=['x','y','vx','vy']
            self.ynames = ['x', 'y']
            self.constraints={'max_y':Max('y')}
            self.stop=threshold('y',0.)

        def derivative(self,X,t,k,m):
            vx,vy=get_indice(self.xnames,X,['vx','vy'])
            vx_dot=-k*vx*(vx*vx+vy*vy)**0.5/m
            vy_dot=-k*vy*(vx*vx+vy*vy)**0.5/m-self.g
            return np.array([vx,vy,vx_dot,vy_dot])

        def output(self, X, t, k, m):
            return X[0:2]

Other attributes appear :

- g is a constant parameter that defines the gravitational constant.
- stop is the way the simulation will stop. Here, threshold means the simulation stops when y reach the 0 value. We could have defined a simulation with a constant final time, by writting self.stop=final_time(value_of_the_final_time).
- constraints represents the features we want to extract from the time simulation. Here we want to extract the maximum value of y during the simulation.

Other methods of features are :

- Min(variable) : to extract the minimum value of a variable during the simulation.
- moy(variable) : to extract the mean value of a variable during the simulation.
- eff(variable) : to extract the Root Mean Square value of a variable during the simulation.

The optimization problem is defined below :

.. code-block:: python

    from noloadj.optimization.optimProblem import OptimProblem,Spec
    from noloadj.ODE.ode45_extract import *
    from noloadj.ODE.ode45 import *

    def lancer(m,R,v0,a, x0, y0):
        k=0.5*1.292*0.5*np.pi*R*R
        vx0,vy0= v0*np.cos(a),v0*np.sin(a)
        ball=Ball()
        tf,Xf,Yf,cstr = odeint45_extract(ball,np.array([x0,y0,vx0,vy0]),k,m,h0=1e-3)
        hauteur=cstr['max_y']
        xf=get_indice(ball.xnames,Xf,['x'])
        yf=get_indice(ball.xnames,Xf,['y'])
        return locals().items()

    spec=Spec(variables={'m':1.0,'R':0.2,'v0':10,'a':np.pi/4}, bounds={'m':[0.5,10.],'R':[0.001,1.0],'v0':[10.,100.],'a':[np.pi/6,np.pi/2]},
          objectives={'hauteur':[0.,15.]}, eq_cstr={'xf':22.0},freeOutputs=['tf','yf'])

    parameters={'x0':0.,'y0':2.}

    optim=OptimProblem(model=lancer,specifications=spec,parameters=parameters)
    result=optim.run()
    result.printResults()

.. parsed-literal::
    Optimization terminated successfully 	(Exit mode 0)
                Current function value: 4.665652029082664
                Iterations: 28
                Function evaluations: 53
                Gradient evaluations: 28
    {'m': 3.8622372277782335, 'R': 0.0010000000000000059, 'v0': 14.673244119484888, 'a': 0.5235987755982988}
    {'hauteur': 4.665652029082664, 'xf': 21.999782988719115, 'tchoc': 1.731262599305921, 'yf': 3.625396093720089e-15}

odeint45_extract has for input parameters :

- the class that describes the ODE system defined above.
- the initial state vector.
- optimization inputs (here u and p).
- h0 as the initial stepsize.

It returns the final time of the simulation (tf), the final state vector (Xf), the final output vector (Yf), and the constraints (cstr) defined in ODE class as a dictionary.

After the simulation, we can visualize the simulation of the optimal point.

.. code-block:: python

    import matplotlib.pyplot as plt

    mopt=result.solution()[0]
    Ropt=result.solution()[1]
    vopt=result.solution()[2]
    aopt=result.solution()[3]
    print(aopt*180./np.pi)
    tf=result.getLastOutputs()['tf']
    xf=result.getLastOutputs()['xf']
    k=0.5*1.292*0.5*np.pi*Ropt*Ropt
    vx0,vy0=vopt*np.cos(aopt),vopt*np.sin(aopt)

    ball=Ball()
    X,Y= odeint45(ball,np.array([0.,2.,vx0,vy0]),
                vect_temporel(0.,tchoc,1e-2), k, mopt, h0=1e-4)

    x,y=get_indice(ball.xnames,X,['x','y'])
    plt.figure(figsize = (10, 8))
    plt.plot(x, y)
    plt.plot(xf, 0.0, 'ro') # the final point
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')

.. figure:: images/throw_ball_simulation.png

odeint45_extract has the same inputs parameters as odeint45, with one more : h0 as the initial stepsize of the simulation.


Power electronics applications
------------------------------

NoLoad can also simulate power electronics applications until detection of their steady-state and extract fratures from it.
Let's see an example with a Buck application. The ODE system is defined below.

.. code-block:: python

    import jax. numpy as np
    from noloadj.ODE.ode_tools import *

    class buck():

        def __init__(self,Ve,R,alpha,T):
            self.Ve=Ve
            self.R=R
            self.aT=alpha*T

            self.state=1
            self.xnames=['vc','il']
            self.ynames=['id']

            self.stop,self.constraints=steady_state(T,10,self.xnames,1e-5)

        def derivative(self,x,t,C,L):
            def state0():
                vc=x[0]
                vc_dot=-vc/(self.R*C)
                return np.array([vc_dot,0.])
            def state1():
                vc,il=x[0],x[1]
                vc_dot=(il-vc/self.R)/C
                il_dot=(self.Ve-vc)/L
                return np.array([vc_dot,il_dot])
            def state2():
                vc,il=x[0],x[1]
                vc_dot=(il-vc/self.R)/C
                il_dot=-vc/L
                return np.array([vc_dot,il_dot])
            return Switch(self.state,[state0,state1,state2])

        def computeotherX(self,x,t,C,L):
            def state0():
                vc=x[0]
                il=0.
                return np.array([vc,il])
            def state1():
                return x
            def state2():
                return x
            return Switch(self.state,[state0,state1,state2])

        def output(self,x,t,C,L):
            il=x[1]
            def state0():
                id=0.
                return np.array([id])
            def state1():
                id=0.
                return np.array([id])
            def state2():
                id=il
                return np.array([id])
            return Switch(self.state,[state0,state1,state2])

        def commande(self,t,T):
            moduloT=(t//T)*T
            c=np.where(t-moduloT<self.aT,1,0)
            tpdi=np.where(t-moduloT<self.aT,self.aT+moduloT,T+moduloT)
            return tpdi+1e-12,c

        def update(self,x,y,t,state,c):
            eps,nstate,nx,ny=1e-10,state,x,y
            id=ny[0]
            def state0():
                def to_state_1(state):
                    nstate,nx,ny=state
                    return 1,nx,ny
                return Condition([c==1],[to_state_1],(nstate,nx,ny))
            def state1():
                def to_state_2(state):
                    nstate,nx,ny=state
                    return 2,nx,ny
                return Condition([c==0],[to_state_2],(nstate,nx,ny))
            def state2():
                def to_state_0(state):
                    nstate,nx,ny=state
                    vc=nx[0]
                    il=0.
                    id=0.
                    return 0,np.array([vc,il]),np.array([id])
                def to_state_1(state):
                    nstate,nx,ny=state
                    return 1,nx,ny
                return Condition([id<eps,c==1],[to_state_0,to_state_1],(nstate,nx,ny))
            return Switch(self.state,[state0,state1,state2])

New attributes appear :

- Ve,R,a,T are constant parameters.
- state defines the configuration of the system for the present iteration.
- stop uses the 'steady-state' method, that means the simulation will stop when the steady-state of the system was detected. The inputs parameters of this method are the operating period, the
number of periods that has to be compared to detect the steady-state, the list of state variables for which the maximum and minimum across the number of periods will be computed, and the tolerance to detect the steady-state.
With the 'steady-state' method, some features are automatically added to the constraints attribute : the maximum and the minimum values for each state variable (here 'vc_min','vc_max','il_min','il_max').

New methods for the class has to be defined :

- computerotherX describes for each configuration the state variables that are not defined by an ODE system but by an equation with other state variables.
- commande defines the value of some commanded devices of the application (such as transistor).
- update defines the tests needed so that the model switches fro one configuration to another.

Methods of features for periodic applications are :

- min_T(T,variable) : to extract the minimum value of a variable during the simulation, with T the operating period of the application.
- max_T(T,variable) : to extract the maximum value of a variable during the simulation, with T the operating period of the application.
- moy_T(variable) : to extract the mean value of a variable during the simulation.
- eff_T(variable) : to extract the Root Mean Square value of a variable during the simulation.

The optimization problem is defined below :

.. code-block:: python

    from noloadj.ODE.ode45_extract import *
    from noloadj.ODE.ode_tools import *

    def model(L,C,Ve,R,a,T,pas):
        Buck=buck(Ve,R,a,T)
        tchoc,X,Y,cstr,states=odeint45_extract(Buck, np.array([0.,0.]), C, L,T=T, h0=pas)
        vc_min=cstr['vc_min']
        fobj=L+C
        return locals().items()

    from noloadj.optimization.optimProblem import Spec,OptimProblem
    spec=Spec(variables={'L':0.002,'C':1e-4},objectives={'fobj':[0.,0.1]},
              bounds={'L':[1e-3,1e-1],'C':[1e-3,1e-1]},ineq_cstr={'vc_min':[2.,4.5]},debug=True)
    parameters={'Ve':12,'R':15,'a':0.2,'T':1/5000,'pas':1e-8}
    optim=OptimProblem(model,spec,parameters)
    res=optim.run()
    res.printResults()

.. parsed-literal::
    Optimization terminated successfully 	(Exit mode 0)
                Current function value: 0.0020000000000000217
                Iterations: 2
                Function evaluations: 2
                Gradient evaluations: 2
    {'L': 0.001, 'C': 0.001000000000000022}
    {'fobj': 0.0020000000000000217, 'vc_min': 2.587396867696324}

When we call the odeint45_extract function with a periodic model, it returns another output parameter called 'states', that gives the configuration of the model for the final time.
