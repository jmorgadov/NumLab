# Numlab

## Objetivos

El objetivo de este proyecto es crear una herramienta de aprendizaje
desarrollada para ayudar a los estudiantes de Ciencias de la Computación que
están cursando la asignatura Matemática Numérica. Se quiere crear un lenguaje
basado en Python en el cual los estudiantes implementen soluciones de problemas
numéricos como: hallar cero de funciones, resolver sistemas de ecuación, entre
otros; y a la vez, realizar un análisis de la ejecución de estas soluciones.

Una de las características que tendrá este lenguaje es la capacidad de simular
regiones de código bajo ciertas condiciones o limitantes, como por ejemplo:
limitar el tiempo de ejecución, limitar la cantidad de variables que se pueden
crear, lmitar el tiempo que toma realizar una operación determinada, entre
otro. Esto fomenta en los estudiantes la implementación de soluciones más
eficientes. Además, el lenguaje también constará con la posibilidad, mediante
un algoritmo genético, de optimizar códigos ya escritos.

## Lenguaje

**Numlab** es el lenguaje que se ha implementado para dar solución a los
objetivos mencionados anteriormente. En las siquientes seciones, se muestran
las principales características del mismo.

### Características básicas

**Numlab** está basado en Python, aunque no implementa todas las
funcionalidades del mismo, la sintaxis básica si es la misma. Ejemplos:

```python
# Declaración de variables
a = 5
pi = 3.14
name = "John"
val = True 

# Funciones built-in
print("my name is", name)

# Operaciones aritméticas
print(a + pi)
print(a - pi)
print(a ** 2)

# Control de flujo
if val:
    print("val is true")
else:
    print("val is false")

for i in range(10):
    if i % 2 == 0:
         print(i)


# Declaración de funciones
def foo(a, b):
    return a + b

bar = lambda a, b: a + b

# Declaración de tipos
class Foo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "Foo(%s, %s)" % (self.a, self.b)
```

### Estadísticas en tiempo de ejecución

En cada ejecución existe una variable llamada `stats`, la cual contiene un
diccionario con las estadísticas de la ejecución. Entre las estadísticas que se
pueden obtener se encuentran:

 - `stats["time"]`: tiempo de ejecución en segundos
 - `stats["assign_count"]`: cantidad de asignaciones realizadas
 - `stats["var_count"]`: cantidad de variables creadas
 - `stats["call_count"]`: cantidad de llamados a funciones realizados
 - `stats["add_count"]`: cantidad de veces que se realizó la operación suma
 - `stats["sub_count"]`: cantidad de veces que se realizó la operación resta
 - `stats["mul_count"]`: cantidad de veces que se realizó la operación multiplicación
 - `stats["truediv_count"]`: cantidad de veces que se realizó la operación división
 - `stats["pow_count"]`: cantidad de veces que se realizó la operación potencia
 - `stats["mod_count"]`: cantidad de veces que se realizó la operación módulo
 - `stats["floordiv_count"]`: cantidad de veces que se realizó la operación división entera
 - `stats["lshift_count"]`: cantidad de veces que se realizó la operación **left shift**
 - `stats["rshift_count"]`: cantidad de veces que se realizó la operación **right shift**
 - `stats["matmul_count"]`: cantidad de veces que se realizó la operación multiplicación de matrices
 - `stats["bit_xor_count"]`: cantidad de veces que se realizó la operación **bitwise xor**
 - `stats["bit_and_count"]`: cantidad de veces que se realizó la operación **bitwise and**
 - `stats["bit_or_count"]`: cantidad de veces que se realizó la operación **bitwise or**
 - `stats["in_count"]`: cantidad de veces que se comprobó si un elemento está contenido en otro
 - `stats["eq_count"]`: cantidad de veces que se comprobó si dos elementos son iguales
 - `stats["ne_count"]`: cantidad de veces que se comprobó si dos elementos son distintos
 - `stats["lt_count"]`: cantidad de veces que se comprobó si un elemento es menor que otro
 - `stats["gt_count"]`: cantidad de veces que se comprobó si un elemento es mayor que otro
 - `stats["le_count"]`: cantidad de veces que se comprobó si un elemento es menor o igual que otro
 - `stats["ge_count"]`: cantidad de veces que se comprobó si un elemento es mayor o igual que otro
 - `stats["and_count"]`: cantidad de veces que se realizó la operación lógica **and**
 - `stats["or_count"]`: cantidad de veces que se realizó la operación lógica **or**

Ejemplo:

```python
for i in range(10):
    a = i * 2

print(stats["mul_count"])  # Output: 10
```

En cualquier momento de la ejecución, se puede restablecer todas las estadísticas
a 0 usando la palabra clave `resetstats`.

Ejemplo:
```python
for i in range(10):
    a = i * 2
    if i == 4:
        resetstats

print(stats["mul_count"])  # Output: 5
```

### Simulación de código

En **Numlab** es posble simular regiones de código bajo diferentes
restricciones, como lo son: limitar la cantidad de variables que se pueden
crear (`max_var_count`) y limitar el tiempo de ejecución (`max_time`), limitar
la cantidad de veces que se realiza una operación determinada y establecer el
tiempo que toma en realizarse una operación.

El nombre de las restrcciones relacionadas con operadores se nombran:
`max_<operator>_count` y `<operator>_time` para establecer la catidad máxima de
veces que se puede realizar una operación y el tiempo que toma en realizarse
respectivamente. Por ejemplo, si se desea limitar la cantidad de veces que se
realiza la operación suma: `max_add_count`.

#### Configuración de la simulación

Para establecer estas restricciones en **Numlab** se utiliza un bloque de
configuración:

```python
conf general_conf:
    max_time 0.5
    max_var_count 10
    max_add_count 100
    max_sub_count 100
    sub_time 0.1
```

Es posible también crear jerarquías de restricciones, por ejemplo:

```python
conf add_config1(general_conf):
    add_time 0.3

conf add_config2(general_conf):
    add_time 0.5
```

Estas configuraciones heredan las restricciones de la configuración base. De
esta forma se pueden declarar configuraciones diferentes pero que tengan
restricciones en común sin tener que repetir las mismas. Si se establece
una restricción que ya estaba en la configuración base, se sobreescribe.

Los valores de una configuración pueden ser resultados de una operación, por
ejemplo:

```python
a = 2

conf c1:
    max_time a ** 3 + 8
```

Si la restricción es sobre el tiempo de ejecución de un operador, es posible
también especificar en vez de un valor, una función que devuelva el tiempo de
ejecución de la operación. Esta función se ejecuta cada vez que se realiza la
operación determinada y debe devolver el tiempo que debe durar la operación.
Por ejemplo:

```python
conf c1:
    add_time lambda : rand() * 2 
```

> `rand` es una función built-in que devuelve un número aleatorio entre 0 y 1.

En el ejemplo anterior, cada vez que se simule la operación suma, la misma
demorará un tiempo aleatorio entre 0 y 2 (diferente para cada vez que se
realice).

#### Regiones de código simuladas

Para establecer una región de código donde se simulen las restricciones
establescidas en una configuración, se utilizan las palabras claves `begsim
<config>` y `endsim`, donde `<config>` es el nombre de la configuración que se
decea usar. Estas palabras indican donde comienza y termina la simulación
respectivamente. Por ejemplo:

```python
conf c1:
    max_time 0.5

begsim c1
a = 1
b = 1
print(a)
print(b)
for _ in range(98):
    c = a + b
    a = b
    b = c
    print(c)
endsim
```

Es posible utilizar `begsim` y `endsim` más de una vez en una misma ejecución
(en tal caso se recomienta usar `resetstats` antes de cada empezar de
simulación). Se pueden relizar simulaciónes dentro de simulaciones, en tal caso
se pasa a utilizar la configuración de la ultima simulación. Cada `endsim`
termina un nivel de simulación (la última que se haya hecho). Estas palabras
claves pueden estar en cualquier parte del código, la única restricción es que
no se pueden realizar más `endsim` que `begsim`.
