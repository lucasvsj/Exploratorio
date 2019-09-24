<strong>Nombre:</strong> Lucas Van Sint Jan
<strong>Número de alumno:</strong> 17640040
<h2 id="titulo">Sacarse un 7 está de moda</h2>
<p>Mi algoritmo se divide en 5 partes:</p>

<ul>

<li>```pre_loop```: donde se mueve la iteracion actual al registo A, para así despues comprobar si se debe seguir ejecutando el programa o no (cuando éste sea 0, se dejará de ejecutar, ya que quiere decir que se recorrió todo el array).</li>
<li>```loop```: donde se comparan el elemento <em>n</em> con el <em>n+1</em> y se comprueba si son iguales o no. En caso de que lo sean, se ejecuta ```iguales``` y en lo contrario, se ejecuta ```reset_array_loop```.</li>
<li>```iguales:``` se aumenta la moda actual y se chequea si ésta es mayor que ```max_moda```, la cual es la máxima moda que hay hasta ese momento. Si ésta es mayor, se ejecuta ```set_max_moda```, de lo contrario se ejecuta ```reset_array_loop```.</li>
<li>```set_max_moda:``` se reescribe ```max_moda```, pasandole la la moda actual, luego se ejecuta ```reset_array_loop```.</li>
<li>```reset_array_loop:``` con este loop, se vuelve a la posicion del último elemento analizado en ```loop```. Finalmente se ejecuta ```pre_loop```.</li>