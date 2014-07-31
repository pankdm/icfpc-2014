Module(body=[
    FunctionDef(name='foo', args=arguments(args=[], vararg=None, kwarg=None, defaults=[]), body=[
        Expr(value=Call(func=Name(id='ALLOCATE_ARRAY', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=15),
          ], keywords=[], starargs=None, kwargs=None)),
        Expr(value=Call(func=Name(id='SET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=0),
            Num(n=13),
          ], keywords=[], starargs=None, kwargs=None)),
        Expr(value=Call(func=Name(id='SET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=1),
            Num(n=2),
          ], keywords=[], starargs=None, kwargs=None)),
        Expr(value=Call(func=Name(id='SET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=5),
            Num(n=8),
          ], keywords=[], starargs=None, kwargs=None)),
        Assign(targets=[
            Name(id='x1', ctx=Store()),
          ], value=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=0),
          ], keywords=[], starargs=None, kwargs=None)),
        Assign(targets=[
            Name(id='x2', ctx=Store()),
          ], value=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=1),
          ], keywords=[], starargs=None, kwargs=None)),
        Assign(targets=[
            Name(id='x3', ctx=Store()),
          ], value=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=5),
          ], keywords=[], starargs=None, kwargs=None)),
        Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
            Tuple(elts=[
                Name(id='x1', ctx=Load()),
                Name(id='x2', ctx=Load()),
                Name(id='x3', ctx=Load()),
              ], ctx=Load()),
          ], keywords=[], starargs=None, kwargs=None)),
        Assign(targets=[
            Name(id='b', ctx=Store()),
          ], value=BinOp(left=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=1),
          ], keywords=[], starargs=None, kwargs=None), op=Add(), right=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=5),
          ], keywords=[], starargs=None, kwargs=None))),
        Assign(targets=[
            Name(id='c', ctx=Store()),
          ], value=BinOp(left=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=0),
          ], keywords=[], starargs=None, kwargs=None), op=Add(), right=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=1),
          ], keywords=[], starargs=None, kwargs=None))),
        Assign(targets=[
            Name(id='d', ctx=Store()),
          ], value=BinOp(left=BinOp(left=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=0),
          ], keywords=[], starargs=None, kwargs=None), op=Add(), right=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=1),
          ], keywords=[], starargs=None, kwargs=None)), op=Add(), right=Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
            Name(id='a', ctx=Load()),
            Num(n=5),
          ], keywords=[], starargs=None, kwargs=None))),
        Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
            Name(id='b', ctx=Load()),
          ], keywords=[], starargs=None, kwargs=None)),
        Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
            Name(id='c', ctx=Load()),
          ], keywords=[], starargs=None, kwargs=None)),
        Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
            Name(id='d', ctx=Load()),
          ], keywords=[], starargs=None, kwargs=None)),
        Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
            Call(func=Name(id='GET_ARRAY_VALUE', ctx=Load()), args=[
                Name(id='a', ctx=Load()),
                Num(n=10),
              ], keywords=[], starargs=None, kwargs=None),
          ], keywords=[], starargs=None, kwargs=None)),
      ], decorator_list=[]),
    Expr(value=Call(func=Name(id='foo', ctx=Load()), args=[], keywords=[], starargs=None, kwargs=None)),
  ])