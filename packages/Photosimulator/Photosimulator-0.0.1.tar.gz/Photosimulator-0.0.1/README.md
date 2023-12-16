# Photosimulator

## photokineticanalysis.py

```

PhotokineticAnalysis()
  
```

#### Functions:

```

PhotokineticAnalysis.check()
  
```
  
  Checks that the inputs for the calculate_theoretical function are correct
  
  
 
```

PhotokineticAnalysis.calculate_theoretical()
  
```
  
  This section allows for calculating theoretical photouncaging values using the following first order kinetic equation for photouncaging: 
  
  $Y = {Y_o} + (plateau-{Y_o})(1-exp(-K*x))$
  
  ${Y_o} = 0$
  
  Plateau = 1
  
  **Input:** 
  
  *   Array of x values (Dosage)
  *   Photokinetic constant, k 
  
  **Output:** 
  
  *   Table of x and corresponding y values (normalized to 1)
  *   Graph of theoretical data


```

PhotokineticAnalysis.calculate_experimental()
  
```

  This section allows for calculating the photouncaging constant k using the first order kinetic equation:
  
  $Y = {Y_o} + (plateau-{Y_o})(1-exp(-K*x))$
  
  ${Y_o} = 0$
  
  Plateau = 1
  
  **Input:** 
  
  
  *   Excel file formatted such that the first column is labelled with the time unitstime and has all the time values and the corresponding y values labelled.  
  
  **Output:** 
  
  *   Kinetic rate constand with standard deviation
  *   Table of x and corresponding y values (normalized to 1)
  *   Graph of theoretical data

# photokineticanalysis.py


 
```

ChemotaxisSimulation()
  
```

### Functions:

```

ChemotaxisSimulation.cell_movement()
  
```

  This section allows for modeling cell migration in 2D. It is based off of a stochastic compartment model developed by Fadai et al. 2019. 
  
  **Input:** 
  
  * n:matrix size 
  * m:matrix size
  * CC:location of initial cells
  * V:compartment size 
  * rm: motility rate between 0-1, where 1 equates to faster cells
  * rp: proliferation rate between 0-1, where 1 equates to max proliferation
  * rd: death rate between 0-1, where 1 equates to max death rate
  * tf: final dimensionless time
  * C_start: if there is a chemotactic variable applied, when is it applied.
  * C_end: if there is a chemotactic variable applied, when does it end.
  * rhox: how the chemotactic variable is applied over space (i.e gradient,etc)
  
  **Output:** 
  
  * n * m matrix with final cell positions

 
```

ChemotaxisSimulation.simulate()
  
```

  This function plots cell position over time and saves a movie file. 
  
  **Input:** 
  
  * Title of movie file to be saved
  
**Output:** 

* Movie file_name.gif
