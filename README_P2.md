<strong>Nombre:</strong> Lucas Van Sint Jan
<strong>Número de alumno:</strong> 17640040
<h2 id="titulo">Sacarse un 7 está de moda</h2>
<p>Mi algoritmo se divide en 5 partes:</p>

<ul>

<li><code>pre_loop</code>: donde se mueve la iteracion actual al registo A, para así despues comprobar si se debe seguir ejecutando el programa o no (cuando éste sea 0, se dejará de ejecutar, ya que quiere decir que se recorrió todo el array).</li>
<li><code>loop</code>: donde se comparan el elemento <em>n</em> con el <em>n+1</em> y se comprueba si son iguales o no. En caso de que lo sean, se ejecuta <code>iguales</code> y en lo contrario, se ejecuta <code>reset_array_loop</code>.</li>
<li><code>iguales:</code> se aumenta la moda actual y se chequea si ésta es mayor que <code>max_moda</code>, la cual es la máxima moda que hay hasta ese momento. Si ésta es mayor, se ejecuta <code>set_max_moda</code>, de lo contrario se ejecuta <code>reset_array_loop</code>.</li>
<li><code>set_max_moda:</code> se reescribe <code>max_moda</code>, pasandole la la moda actual, luego se ejecuta <code>reset_array_loop</code>.</li>
<li><code>reset_array_loop:</code> con este loop, se vuelve a la posicion del último elemento analizado en <code>loop</code>. Finalmente se ejecuta <code>pre_loop</code>.</li>

</ul>