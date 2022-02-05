# Numlab

## Contenidos

- [Objetivos](https://github.com/jmorgadov/NumLab#objetivos)
- [Lenguaje](https://github.com/jmorgadov/NumLab#lenguaje)
  - [Cracterísticas básicas](https://github.com/jmorgadov/NumLab#caracter%C3%ADsticas-b%C3%A1sicas)
  - [Estadísticas en tiempo de ejecución](https://github.com/jmorgadov/NumLab#estad%C3%ADsticas-en-tiempo-de-ejecuci%C3%B3n)
  - [Simulación de código](https://github.com/jmorgadov/NumLab#simulaci%C3%B3n-de-c%C3%B3digo)
    - [Configuración de la simulación](https://github.com/jmorgadov/NumLab#configuraci%C3%B3n-de-la-simulaci%C3%B3n)
    - [Regiones de código simuladas](https://github.com/jmorgadov/NumLab#regiones-de-c%C3%B3digo-simuladas)
- [Implementación](https://github.com/jmorgadov/NumLab#implementaci%C3%B3n)
  - [Motor de expresiones regulares](https://github.com/jmorgadov/NumLab#motor-de-expresiones-regulares)
  - [Tokenizador](https://github.com/jmorgadov/NumLab#tokenizador)
  - [Gramáticas](https://github.com/jmorgadov/NumLab#gram%C3%A1ticas)
  - [Árbol de Sintaxis Abstracta (AST)](https://github.com/jmorgadov/NumLab#%C3%A1rbol-de-sintaxis-abstracta-ast)
  - [Parser](https://github.com/jmorgadov/NumLab#parser)
  - [Visitors](https://github.com/jmorgadov/NumLab#visitors)
  - [Ejecución](https://github.com/jmorgadov/NumLab#ejecuci%C3%B3n)
    - [Tipos y funciones predefinidas](https://github.com/jmorgadov/NumLab#tipos-y-funciones-predefinidas)
    - [Contextos](https://github.com/jmorgadov/NumLab#contextos)
    - [Evaluación](https://github.com/jmorgadov/NumLab#evaluaci%C3%B3n)
- [Optimización de código](https://github.com/jmorgadov/NumLab#optimizaci%C3%B3n-de-c%C3%B3digo) 

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
 - `stats["contains_count"]`: cantidad de veces que se comprobó si un elemento está contenido en otro
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
a, b = 1, 1
print(a)
print(b)
for _ in range(98):
    a, b = b, a + b
    print(b)
endsim
```

Es posible utilizar `begsim` y `endsim` más de una vez en una misma ejecución
(en tal caso se recomienta usar `resetstats` antes de cada empezar de
simulación). Se pueden relizar simulaciónes dentro de simulaciones, en tal caso
se pasa a utilizar la configuración de la ultima simulación. Cada `endsim`
termina un nivel de simulación (la última que se haya hecho). Estas palabras
claves pueden estar en cualquier parte del código, la única restricción es que
no se pueden realizar más `endsim` que `begsim`.

## Implementación

**Numlab** es un lenguaje evaluado escrito en Python. A continuación se
exponen las características principales de la implementación de cada estapa.

### Autómatas

Para la creación de las algunas de las proximas funcionalidades, se realizaó
una implementación de un objeto de tipo `Automata` que permite simular una
máquina de estados de forma genérica. A los mismos se le pueden agregar
estados así como transiciones entre los mismos. Cada autómata tiene un estado
inicial y uno o varios estados finales.

La ejecución de una maquina de estados realizada con un autómata es bastante
simple. Dado una entrada iterable, se comienza en el estado inicial y se va
ejecutando cada transición hasta llegar a un estado final. En caso de llegar a
un estado en el que ninguna transición es válida, se termina la ejecución y la
entrada no es válida. En caso de terminar de recorrer la entrada se clasifica
la entrada como válida o inválida en dependencia de si se llegó a un estado
final o no respectivamente.

Los autómatas pueden tener transiciones **épsilon** entre estados, en este
caso, la ejecución se bifurca. En estos caso la maquina de estados se mueve
por todos los estaos posibles al mismo timepo. Esto da la posibliadad de
ejecutar autómatas no deterministas.

Se implementó además la opción de convertir un autómata no determinista (NFA)
a un autómata determinista (DFA). Esto se implementó utilizando el algoritmo
visto en clase (calculando los **goto** y **epsilon clausuras**).

### Motor de expresiones regulares

Las principales funcionalidades implementados son:

- Operador `*`: Matchea cero o más veces la expresión anterior.
- Operador `|`: Mathcea la expresión anterior o la siguiente.
- Operador `^`: Matchea cualquier expresion excepto la expresión que le prosigue.
- Caracter `.`: Matchea cualquier caracter (ASCII).
- Caracter `\`: Inicio de un caracter especial.
- Caracter `\d`: Matchea un dígito.
- Caracter `\a`: Matchea una letra minúscula.
- Caracter `\A`: Matchea una letra mayúscula.
- Parentesis `(` y `)`: Agrupa una expresión regular.

> Cualquier operador o caracter especal puede ser escapado con `\`.

Para la realización del motor de expresiones regulares se utilizó la clase
`Automata`. Para cada expresión regular se construye un autómata finito no
determinista (NFA) usando el algoritmo de Thompson y luego el mismo se
convierte a un DFA utlizando el método `to_dfa` de la clase `Automata`.

Se ofrecen además dos funciones para el matcheo de cadenas segun una expresión
regular: `match` (la cual tiene un comportamiento similar a `re.match`) y
`compile_patt` (la cual tiene un comportamiento similar a `re.compile`). La
ventaja principal de usar `compile_patt` es que se no es necesario crear un
autómata para cada vez que se desea matchear una cadena (ya que el autómata es
construido una sola vez).

### Tokenizador

Para la implementación del tokenizador se creó una clase `Tokenizer`. Esta
clase se encarga de tomar un texto y dividirlo en diferentes tipos de tokens.
Cada patrón que se agrega está definido por un nombre (tipo del token) y una
expresión regular (se hace uso del motor de expresiones regulares
implementado).

```python
tknz = Tokenizer()
tknz.add_pattern("NUMBER", r"\d\d*|\d\d*\.\d\d*")
```

Al tokenizar un texto, se revisan los patrones comenzando por el primero (en el
mismo orden en el que fueron agregados) y el primero que matchee con el inicio
de la cadena se establece como un token nuevo (se toma como lexema la subcadena
que matcheó con la expresión regular). Luego se vuelve a realizar esta
operación con el resto de la cadena, así sucesivamente hasta terminar la misma.
Si en algún punto no se encuentra un token que matchee con el inicio de la
cadena, se considera que la cadena no se puede tokenizar (con los tipos de
tokens establecidos).

Cada vez que se agrega un patrón al tokenizador se puede establecer una
función que se aplicará al lexema antes de guardar su valor en el token.

Por ejemplo, para quitar las comillas al tokenizar un **string**:

```python
tknz.add_pattern("STRING", r"'((^')|(\\'))*(^\\)'", lambda t: t[1:-1])
```

Esta función tambien puede ser utilizada para indicar que se quiere ignorar
los tokens de un tipo determinado. En tal caso basta con que la función devuelva
`None`:

```python
tknz.add_pattern("SPACE", r"( | \t)( |\t)*", lambda t: None)
```

Se ofrece también la opción de agregar `keywords` (palabras clave) para una
mayor comodidad. Esto se hace mediante el método `add_keywords()` el cual recibe
una lista de palabras. En el proceso de tokenización, si la subcadena matcheada
conicide con alguna de las palabras clave, entonces el tipo del token se
establece como `KEYWORD`.

En caso de que se quiera aplicar una función para procesar todos los tokens
obtenidos, se puede usar el decorador `process_tokens` de la clase `Tokenizer`.
Este debe ser usado en una función que reciba un solo argumento (la lista de
tokens) y devuelva una lista de tokens procesados.

```python
@tknz.process_tokens
def process_tokens(tokens):
    # ...
    return tokens
```

Finalmente, para obtener los tokens de un texto basta con usar la función
`tokenize`:

```python
tokens = tknz.tokenize("some text")
```

### Gramáticas

Se implementaron las clases `Grammar`, `NonTerminal`, `Terminal` y `Production`
las cuales son usadas para la representación de una gramática general. Se
implementó además un parser de gramáticas con el cual es posible crear
gramáticas dado un formato, esto permite definir la gramática del lenguaje en
un archivo y poder cambiarla fácilmente. Dado la sencillez del formato (el
lenguaje de las gramáticas), se implementó un sencillo parser recursivo
descendente para la creación de las mismas.

El formato especificado es el siguiente:

```
expression: production_1 | production_2 | ... | production_n
```

De forma equivalente, para mayor legibilidad:

```
expression:
    | production_1 
    | production_2
    | ...
    | production_n
```

Ejemplo:

```
Expr_AB:
    | 'a' Expr_AB 'b'
    | EPS
```

> EPS es un elemento especial en las gramáticas para representar *epsilon*

Las gramáticas luego pueden ser cargadas como se muestra a continuación:

```python
from grammar im port Grammar
gm = Grammar.open("expr_ab.gm")
```

Las gramáticas están compuestas por una lista de expresiones (no terminales).
Cada no terminal de la gramática, contiene una lista de producciones. Cada
producción contiene una lista de elementos (terminales o no terminales).

### Árbol de Sintaxis Abstracta (AST)

Para la creación de un AST se creó la clase abstracta `AST`. De esta clase
heredan todos las clases que representan los nodos del árbol de sintaxis 
abstracta del lenguaje. En la clase se implementa también un método `dump`
que permite mostrar el árbol de forma legible. Este método usa el
atributo `__slots__` mediante el cual se definen los atributos que se
quieren mostrar.

Ejemplo del árbol generado a partir del código:

```python
conf c1:
    max_time 5
    max_var_count 5

begsim c1
def foo(a, b):
    print("hola", a, b)

a, b = 1, 2
foo(a, b)
endsim
```

Árbol generado:
```text
Program:
   stmts: [
      ConfDefStmt:
         name: c1
         configs: [
            ConfOption:
               name: max_time
               value: ConstantExpr(0.5)
         ]
      Begsim:
         config: NameExpr('c1', ctx=ExprCtx.LOAD)
      ForStmt:
         target: NameExpr('i', ctx=ExprCtx.LOAD)
         iter_expr: (TupleExpr)
            elts: [
               CallExpr:
                  func: NameExpr('range', ctx=ExprCtx.LOAD)
                  args: [
                     ConstantExpr(100)
                  ]
            ]
            ctx: ExprCtx.LOAD
         body: [
            TupleExpr:
               elts: [
                  CallExpr:
                     func: NameExpr('print', ctx=ExprCtx.LOAD)
                     args: [
                        BinOpExpr:
                           left: NameExpr('i', ctx=ExprCtx.LOAD)
                           op: Operator.POW
                           right: ConstantExpr(2)
                     ]
               ]
               ctx: ExprCtx.LOAD
         ]
      Endsim:
   ]
```

Para definir cómo se construye cada nodo del AST se pueden asignar los
constructores a cada producción de la gramática usando la función
`assign_builders`. Esta función recibe un diccionario donde las llaves son la
representación textual de la producción y los valores son funciones que reciben
como argumentos los elementos de la producción. En caso de que el símbolo sea
un terminal la función recibirá dicho terminal, en caso de ser un no terminal,
la función recibirá el resultado de la ejecución algunas de las funciones
constructoras de las producciones que tengan como cabeza a dicho no terminal.

Por ejemplo, a continuación se muestran algunos de los constructores para
la gramática de **Numlab**:

```python
builders = {
    # -------------------------------------------------------------------------
    "program -> stmt program": lambda s, p: ast.Program([s] + p.stmts),
    "program -> NEWLINE program": lambda n, p: p,
    "program -> EPS": lambda: ast.Program([]),
    # -------------------------------------------------------------------------
    "stmt -> simple_stmt": lambda s: s,
    "stmt -> compound_stmt": lambda c: c,
    # -------------------------------------------------------------------------
    "stmt_list -> stmt": lambda s: [s],
    "stmt_list -> stmt stmt_list": lambda s, sl: [s] + sl,
    # -------------------------------------------------------------------------
    # ...
    # ...
```

### Parser

Para la implementación del parser principal del lenguaje se creó la clase
abstacta `Parser`. Usando esta clase como base se creó una clase `LR1Parser`,
la cual implementa un parser LR(1).

Para la realización del parser LR(1) fue necesario implementar las clases
`LR1Item` y `LR1Table`. La primera de estas clases representa un item del
parser, el cual contiene: la producción que lo genera, la posición del punto
(dot) en la producción y el terminal que le debe proseguir (lookahead).

La segunda clase (`LR1Table`) representa la tabla de transición del parser.
Cada posición de la tabla puede contener tres tipos de elementos: un **string**
`"OK"`, que indica que el estado es de aceptación; un valór numérico entero,
que indica el estado siguiente; o un no terminal de la gramática, el cual
representa que hay que realizar una reducción. Para no tener que recalcular la
tabla cada vez que se va a parsear un texto, la misma puede ser serializada y
luego cargada.

La construcción de la tabla se realizó siguiendo el algoritmo visto en las
conferencias de la asignatura (calculando los **goto** y las **clausuras** de
los estados).

Es en el proceso de parsing, al realizar una acción de reducción, que se
utilizan las funciones constructoras vistas en la sección anterior. En
dependencia de la producción que se está reduciendo, se llama a la función
constructora correspondiente.

Para una mayor comodidad se implementó también la clase `ParserManager`. Esta
clase ofrece, dado una gramática, un tokenizador (opcional) y un parser
(opcional, por defecto LR(1)), métodos como: `parse_file` (para parsear un
archivo), `parse` (para parsear un texto) y `parse_tokens` (para parsear una
lista de tokens directamete). Estas funciones devuelven el AST resultante del
proceso de parsing.

### Visitors

Una vez obtenido el AST de un programa es necesario realizar recorridos sobre
él. Para ello se implmentó una clase `Visitor` la cual contiene dos decoradores
`@visitor` y `@callback`. Por cada **visitor** que se quiera implementar para
el AST, se debe implementar una nueva clase que tenga como atributo de clase
una instancia de la clase `Visitor`. Luego, cada método de la clase que tenga
el decorador `@visitor`, se establecerá como una sobrecarga. Es por ello que
todos estos métodos deben tener sus argumentos tipados (esta es la forma en la
que el **visitor** sabe cual de los métodos de la clase debe llamar).

Por ejemplo:

```python
from numlab.lang.visitor import Visitor

class EvalVisitor:
    visitor_dec = Visitor().visitor

    @visitor_dec
    def eval(self, node: ast.Program):
        for stmt in node.stmts:
            stmt.eval(self)

    @visitor_dec
    def eval(self, node: ast.Stmt): ...

    # ...
```

El decorador `@callback` se utiliza para definir funciones que se van a llamar
cada vez que se llame a una función marcada como **visitor**. En el proyecto
uno de los usos quese le da a este decorador es para comprobar que el tiempo de
ejecución de una simulación es menor que el límite establecido en cada momento.

### Ejecución

Para la ejecución de un programa representado en un AST se implementó un
visitor `EvalVisitor` (muy similar al ejemplo de la sección anterior). A
continuación se muestran algunas de las características más importantes
implementadas en el proceso de evaluación.


#### Tipos y funciones predefinidas

Para representar los tipos predefinidos de **Numlab** se creó la clase `Type`.
Cada instancia de esta clase representa un tipo de **Numlab**, entre ellos:
`int`, `str`, `list`, etc (los tipos básicos existentes en python).

A cada tipo de le pude agregar atributos (las funciones también se agregan como
atributo). Además, cada tipo puede derivar de otro (permitiendo la herencia), por
consiguiente, en la resolución de un atributo si el mismo no está definido en el
tipo actual, se busca en el tipo padre (y así susesivamente).

Se implementaron tambíen varias de las funciones built-in de python en **Numlab**.
En la ejecución del código se puede acceder a estas funciones directamente.

#### Contextos

Para definir el contexto donde se encuentra cada vaiable, tipo o función que se
crea, se implementó la clase `Context`. Un **context** tiene un diccionario
con el nombre de cada objeto creado en el mismo y su respectivo valor. Cada contexto
tiene además una referencia al contexto padre (en caso de que exista). Esto
permite que al realizar la resolución de una variable, si la misma no se ecuentra
en el contexto actual, se busque en el contexto padre.

El contexto también es utilizado también en las secciones de código simuladas
para comprobar la cantidad de variables creadas (en caso de existir alguna
restricción sobre este valor).

#### Evaluación

Como se había mencionado anteriormente, la evaluación de un programa se realiza
mediante un **visitor**. En este **visitor** se implementaron las funciones
que definen cómo se evalúa cada uno de los nodos del AST.

En ocasiones, existen nodos que afectan la evaluación de otros, como por ejemplo
las palabras claves de control de flujo (`break`, `continue`, `return`, etc). Para
ello, la instancia del **visitor** cuenta con un diccionario `flags` que contiene
diversa información que se puede utlizar en común entre la evaluación de los nodos.

En estas evaluaciones es también donde se van guardando las estadísiticas de la
ejecución del programa (en un diccionario `stats` el cual tiene accesibilidad
incluso desde el código que se está ejecutando). Por ejemplo, al realizar un
llamado a una función, se incrementa el contador de llamados:

```python
class EvalVisitor:
    
    # ... Other eval methods

    @visitor
    def eval(self, node: ast.CallExpr):
        self.set_stat("call_count", self.stats["call_count"] + 1)
        # Call eval implementation ...

    # ... Other eval methods
```

## Optimización de código

Se implementó también un optimizador de código, el cual, mediante un algorítmo
genético, cambia la estructura de un AST para reducir el tiempo de ejecución.
Para ello se creó otro **visitor**, el cual se puede clasificar como un sistema
experto. Este **visitor**, busca en un programa determinado en qué nodos se
pueden realizar, bajo ciertas reglas, cambios que puedan reducir el tiempo de
ejecución.

Entre estas reglas se pueden mencionar por ejemplo, cambiar el orden de las
comprobaciónes en una condicional (o ciclo while) para que se evalúen primero
las condiciones que son más sencillas, o incluso, sustituir operaciones de
multiplicación por operaciones **shift** si es posible, etc.

Una vez se recorre el AST en busca de cambios, se crea un vector el cual
contiene en cada posición la información de dónde se puede realizar un cambio
(el nodo) y dos funciones: una que realiza el cambio y otra que devuelve el
nodo a su estado original.

Esta información se lleva a la ejecución de un algorítmo genético. La población
de este algoritmo consiste en vectores booleanos que indican si se debe realizar
un cambio en un nodo o no. Al evaluar un AST se realizan los cambios necesarios
y se obtiene el tiempo de ejecución (en caso de existir un error el tiempo de
ejecución será infinito).

La población inicial se genera aleatoriamente. El entrecruzamiento entre dos
vectores se realiza dividiéndolos en dos partes, he intercambiando las mismas,
esta forma de entrecruzamiento es posible ya que cada cambio es independiente.
La mutación consiste en cambiar aleatoriamente algún valor del vector.

Al ejecutar la optimización se obtiene el ast resultante de realizar los cambios
definidos por el mejor vector de la población (luego de algunas generaciones).

A continuación se muestra un ejemplo de código y su optimización:

```python
items = [1, 1, 1, 1, 1]

def foo():
    a = [i for i in range(100)]
    return items

for i in range(50):
    if i in [j for j in range(48, 500)] or i < 40: 
        a = i + 3
    if foo() and items[0] == 1:
        items.remove(1)
        
print(stats["time"])
```

En este código se puede ver que el primer `if` realiza dos comprobaciones. La
primera de ellas genera una lista de al rededor de 450 elementos cada vez que
se ejecuta el `if`, mientras que la segunda solamente compara dos valores.

Se puede observar además que existe otra comprobación, donde también se
realizan dos operaciones y la primera de ellas es más costosa temporalmente que
la segunda. Sin embargo en este caso la segunda operación es dependiente de la
primera, por lo que no se puede realizar antes. Esto no se comprueba en ningún
momento al extraer los cambios posibles debido a la complegidad que puede
presentar comprobar este tipo relaciones entre los nodos. Más adelante el
algoritmo genético es quien decidirá si es correcto realizar el cambio o no.

Al ejecutar este código se obtuvo un tiempo de ejecución promedio de 1.8
segundos. Al optimizar el AST, se detectaron dos cambios potenciales (el orden
de comprobación en las expresiones condicionales mencionadas anteriormente). El
algoritmo genético obtuvo como mejor resultado realizar el primer cambio y no
el segundo. Finalmente, el código optimizado tuvo un tiempo de ejecución de
aproximadamente 0.6 segundos.

