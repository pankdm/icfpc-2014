## Team "Snakes vs Lambdas" @ ICFPC 2014

Teamb members:
 * A.D.
 * A.M.
 * D.P.
 * P.K.

### Short version:

#### Lambda-man AI


We've used BFS for computing cost function of each of the possible moves. Cost fucntion depends on:

1. Shortest distances to pills
2. Distance to closest pill
3. Distance to closest ghost
4. Distance to fruit
5. Fright mode


To fit in the time limit we've limited positions that are considered in BFS to the window of size 31 x 31 with the center in Lambda-man.
This algorithm was implemented in python, see smart_algo_implementation.py

For implementing Lambda-man AI, we've used some simplified dialect of Python, which was translated to syntax tree.
Then the tree was used for generation of Lambda-man CPU assembly language. This allowed us to do development of algorithm in python using our world emulator (emulator.py), while compilator to Lambda-man CPU assembly language was developed.
The compilator was implemented using python module ast and supports some features that are not part of original Lambda-man CPU (for example arrays).

### Ghosts AI

It selects the cell which is the closest to lambda-man according to Manhattan distance (abs(x1 - x2) + abs(y1 - y2)). It will also try to choose the furthest cell if Lambda-man is in fright mode.
The code was written mostly manualy with some tools that simplify implementation of code by generation of functions and some other features.

Also we implementation interpretator of Lambda-man assembly language, but we didn't get to the point where we could get benefits from it.

****
****

## Long version:

### Compiling the Snake
or
### How to translate from python to another language in 3 days

#### Introduction

I mostly want to share some of my thoughts as well as findings and tricks that I discovered while writing a code.
Some of them may sound as a message from captain obvious but anyway.
Besides I’d like to have a write up for future reference in order to avoid mistakes and repeat good decisions.


This contest is usually designed to show the power of functional programming languages compared to imperative one.
I am not really convinced that functional languages (Haskell, Lisp, etc) are somehow significantly better than "usual" languages, like C++ or Python.
But I will be more than happy to see any particular examples where functionality rocks.
Further in this writeup I will try to provide specific code examples showing practical examples of using python.


Task from this year’s contest required writing an AI for packman and ghosts in some pretty low-level programming languages invented by contest organizers.

We participated in a team of four people using python as a programming language and shared folder in dropbox as a repository.

***

After reading the description we were choosing between two different approaches to this task: either develop write in low level language itself (let’s call lambda-man language) gradually introducing more and more complex control structures and features; or write in some existing high level language and then write a compiler from it to lambda-man language.

But anyway we need a world emulator for any of this approach.
The emulator is pretty straight forward so I omit details about it.

### Lambda-man language interpreter

I was working on interpreter of lambda-man language.

Coming from c++ background I am a big fan of OOP (though it is probably more common for java world). So I started with creation of class `VM` which is essentially a state of lambda man virtual machine. And is responsible for executing instructions.

Basically, this state consists of following data: 2 lists (one for data, one for control commands) and a pointer to current frame.

Frame is pretty simple. It just has 2 fields: the list of variables and a pointer to parent.

Then I created a class for each of the operations.
This allowed me to have more readable names (than just 2-letters ones).
For example, class for `LD` operation looks like this:

```python
class LoadEnv(AbstractOp):
     name = 'LD'
     arity = 2

     def mutate(self, vm):
          n, i = self.args

          # go n frames up
          frame = go_to_nth_parent(vm.current_frame, n)
          assert frame.tag != Tag.DUMMY_FRAME

          # push the i-th element
          value = frame.values[i]
          vm.data_stack.append(value)
          vm.counter += 1
```

Also I was able to avoid more code duplication by extracting logic of similar command (`ADD, SUB, MUL, DIV` and others that just take 2 values from the stack and puts back result) to class `IntOperation`:

```python
class IntOperation(AbstractOp):
     def mutate(self, vm):
          # self.func should be reloaded
          self.mutate_arithmetic(vm, self.func)

     @staticmethod
     def mutate_arithmetic(vm, func):
          v2 = vm.data_stack.pop()
          v1 = vm.data_stack.pop()
          assert (v1.tag == Tag.INTEGER)
          assert (v2.tag == Tag.INTEGER)
          c = func(v1.n, v2.n)
          vm.data_stack.append(VmInteger(c))
          vm.counter += 1
```

So the code for addition became very simple:

```python
class IntAddition(IntOperation):
     name = 'ADD'
     @staticmethod
     def func(x, y):
          return x + y
```

### Python --> Lisp compiler

The next day I googled internet for AST (Abstract syntax tree) and found that there is nice library for producing and sat for python code.

This looked very promising.
Besides it would be very convenient to write a program in python so that we can always test in emulator directly (as it is also written in python) and produce the lambda-man instructions only for submitting.

So I started learning how to use this library.
Using ast module was as easy as most of the things in python (see http://xkcd.com/353/)

As a proof of concept I decided to start with the simplest program I could imagine. It should contain the following

1. Usage of integers (it is the simplest data structures of vm)
2. Usage of `DBUG` instruction, because we need to somehow observe the behavior of program which is only supported by this command

So this leads us to:
```python
PRINT(5)
```
(I was using `PRINT` function instead of `DBUG` for readability)


Here is the AST of it:

```python
Module(body=[
    Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
        Num(n=5),
      ], keywords=[], starargs=None, kwargs=None)),
  ])
```

Unfortunately the official python documentation for ast is very meager, but there was a nice unofficial one: http://greentreesnakes.readthedocs.org/en/latest/.

According to it, preferred way of dealing with AST is subclassing the `ast.Visitor` class and implementing various
`visit_FooBar` methods, where `ast.FooBar` is the class you need the visitor to traverse.

We will implement `visit_Num` and `visit_Call` functions

I haven't found the canonical way of yielding the result form this functions so I decided to use a convention
that `visit_*` method should return sequence of LambdaMan VM commands which when executed will change the state of vm accordingly.

I encapsulated this result as a class `ByteCode`. Looking back I think this was not the best design decision.
At first the only data it  has was the `output` and some helper methods to debug_print it.
I thought it will have more in the future so I created a class for it.
But time showed that output was the only field it has at the end of development
and some helper function (like `append_byte_code`) to avoid code like this

```python
byte_code.output += other.output
```


Unfortunately neither `.visit` nor `.visit_*` methods doesn’t return anything so you need to do it on your own.
Thanks to dynamic typing in python you can return whatever you want from the function (though you need to brace yourself  of  consequences)

We proceeded with the classic test driven development (TDD):
When you need to implement a feature or fix a bug:

1. write a test for it
2. make sure it fails
3. write a code that fixes the test
4. ???
5. Profit!

One can argue that in TDD you need to write full test coverage for feature in step 1.
But I  disagree with this definition as it goes against agile philosophy of small iterations.


In our case the sample code `PRINT(5)` is essentially a test already.
Whereas `ast.Visitor` is implemented in the way that it will silently traverse the nodes of type `X`  with unimplemented `visit_X` method.
Which is obviously good, because you don’t want to implement all the possible `visit_X` methods.
But in our case it was not really: I believe that program should fail as fast as possible if something goes wrong.
So I wrapped `ast.Visitor.visit` method with my own, where I check that `.visit` always returns an instance of class `ByteCode`:


``` python
    def visit(self, node):
        byte_code = ast.NodeVisitor.visit(self, node)
        assert isinstance(byte_code, ByteCode), str(byte_code)
        return byte_code
```

I am referring to this kind of asserts as "type checker for poor” as they are done only at runtime.
But sadly there is no other way in python.

Lets make a natural agreement that bytecode for 5 will put a number 5 on the stack. So bytecode for print will be just equal to `DebugPrint` (`DBUG`).

But using only numbers and debug printing is kind of hard write an AI. So we need to support more features in simple python.

In the process of supporting new features I was mostly doing the following in order:

1. create the file with simple example of usage of new syntax
2. look at the astt of code in it
3. find name of the element that you currently don’t support
4. implement corresponding `visit_X` method.

Often there was 3.5: pay the technical debt (refactoring the hacky parts).
I want to emphasize that timely refactoring is very important.
Some may say that the contest time is so small that you there is no time for beautiful code.
But in reality this turns out to be "I don’t have time to sharpen the saw, because I need to saw”.
If you are going to make more modifications in code: it’s worth investing time to make them easier and bug-less.
Time spent on finding and fixing bugs is usually significantly higher than implementing the feature.

Further was support of arithmetic functions (`ADD, SUB, MUL, DIV`) for which I implemented `visit_BinOp` method and
defined dict, which represents byte code that should be returned depending on the type of node.op
```python
    value = {
        ast.Add: IntAddition(),
        ast.Sub: IntSubtraction(),
        ast.Mult: IntMultiplication(),
        ast.Div: IntDivision()
    }
```

Compare statements (>, >=, ==) were done analogously by implementing `visit_Compare` and introducing the value:

```python
    value = {
        ast.Gt: CompareGreater(),
        ast.GtE: CompareGreaterOrEqual(),
        ast.Eq: CompareEqual()
    }
```

Okay, now it is something. But still far from being helpful in writing AI.

Next goal was calling user-defined functions.
Lambda-man vm has good built-in support for them.

Basically using commands `LoadFunction(address)` and `CallFunction(n)` you will jump to `address` and will have `n` local variables
filled with the last `n` values from the stack.
The only problem is that address should be absolute which it leads us to obvious solution: labels.

Here comes new byte code commands:

1. `Label(label)` and
2. `LoadFunctionLabel(label)`.

At the last step of compilation process the second will be translated to the absolute address of the first.


First we need to parse function definition in `visit_FunctionDef`. we will produce new byte code ApplyFunction containing the following information:

1. name of the function
2. number of arguments
3. byte code of the function body

And then, when we encounter actual function call we put commands
```
LoadFunctionLabel(func_name)
CallFunction(n)
```

During the last step of compilation we produce byte code for the whole program with the following structure:
```
JumpLabel(main_label)
Label(function1)
  # Byte code of function1's body
Label(function2)
  # Byte code of function2' body
...
Label(main_label)
  # Byte code of main
```

Also I implemented `visit_Name` method to support access to function parameters
by their name.
For example, for function `foo(x, y)` we will store mapping
```
‘x’ —> 0
‘y’ —> 1
```
in the dict
And whenever we encounter `x` while parsing body of foo we use the byte code `LoadEnv(0, 0 /* index of x*/)` to
push value of `x` to data stack.

Okay, now you have parameters in functions, how to support local variables?

They can be supported similar to parameters of function.
We will allocate all the local variables as dummy parameters for function.

So first, we parse the function body to know how many local variables we need to allocate.
And during the parsing, for each assignment (e.g. `a = 10`) we also store the mapping from variable name to the next free index.
This mapping will be used in the same way when we need to access this variable.

Then the most important missing feature for lambda-man ai was arrays. It’s hard to do BFS without arrays (built-in support for lists was too inefficient : you need to rebuilt the entire prefix of the list if you change only one element).

At first I thought that you can just allocate required number of elements on the stack and use them as an array. But reading more carefully specification I realized that you can only access the top element of data stack (unsurprisingly: that's why  it is called stack). So this idea will not work.

But then we realized that we can do the same trick with frames. We can allocate contigous segment of frame variables and use them as array cells.

So I began implementing this.
At first I refactored places in compiler where we create new variable and access from being implemented as just dictionary and being called from various places to using methods of class `ScopeVariable`.



We agreed on the following API:
```
a = ALLOCATE_ARRAY(size)
SET_ARRAY_VALUE(a, index, value)
GET_ARRAY_VALUE(a, index)
```

Soon I realized that `VM` can access frame variables only by integers:
You dont have any level if indirection. This restriction makes the whole idea of arrays useless.

But then was insight that we can write byte code that will execute `LoadEnv(0, x)`, where `x` is the top value of the stack.
This byte code is basically the following pseudo code:
```
if (x == 0) LoadEnv(0, 0)
if (x == 1) LoadEnv(0, 1)
…
if (x == XMAX) LoadEnv(0, XMAX)
```
Then we would jump to that byte code, execute the desired `LoadEnv` and then return back by using `JOIN` command.

There was a problem with this approach is that we need to store x somewhere.
And we reinvented the wheel by introducing “registers”.
We decided to allocate some fixed amount of first frame variables as dedicated.
This increases cost of calling the functions (we need to fill with zeros the stack before calling) but we expected to need no more then 5 registers, so this overhead was considered to be small.
And it will be an issue we can always try to optimize this part (for example considering other ways of calling functions or adding option specifying that function doesn’t need these register).


Another problem with this approach was that  accessing variable costed O(N), where N is the index of variable in array.
Which is not really great.
But this byte code for `LoadEnv(0, x)` could be easily optimized by using binary search to complexity O(log N), which is good enough.

`StoreToEnv(0, x)` was done similarly.

Having `LoadEnv(0, x)` and `StoreToEnv(0, x)` makes the rest of support for arrays pretty straight forward.
We just needed to associate array name with offset in `ScopeVariable` and use proper indexing, whenever `GET_ARRAY` and `SET_ARRAY` were called.


Having implemented support of arrays we almost reached the end of contest, but the the work and lambda man AI was done in parallel so we only needed to translate this python program to lambda-man instructions and submit it.

***

I was mainly working on compiler so I can share only a few words about AI algorithms.

### Lambda-man AI

A few words about ai algorithm that we implemented.
Our AI on each step executes a BFS for the window of size 31 * 31 with the center in packman and computes a cost function.
This function depends on the following parameters:

1. Shortest distances to pill
2. Distance to closest pill
3. Distance to closest ghost
4. Distance to fruit
5. Fright mode


### Ghosts AI

It selects the cell which is the closest to lambda-man according to Manhattan distance `abs(x1 - x2) + abs(y1 - y2)`. It will also try to choose the furthest cell if Lambda-man is in fright mode.The code was written mostly manually with some tools that simplify implementation of code by generation of functions and some other features.

### Results

We made to 25th place in overall ranking (see RESULTS.txt).
