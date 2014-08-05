Module(body=[
    FunctionDef(name='foo', args=arguments(args=[
        Name(id='a', ctx=Param()),
        Name(id='b', ctx=Param()),
        Name(id='c', ctx=Param()),
      ], vararg=None, kwarg=None, defaults=[]), body=[
        Return(value=BoolOp(op=And(), values=[
            Compare(left=Name(id='a', ctx=Load()), ops=[
                Eq(),
              ], comparators=[
                Name(id='b', ctx=Load()),
              ]),
            Compare(left=Name(id='b', ctx=Load()), ops=[
                Eq(),
              ], comparators=[
                Name(id='c', ctx=Load()),
              ]),
          ])),
      ], decorator_list=[]),
    Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
        Call(func=Name(id='foo', ctx=Load()), args=[
            Num(n=1),
            Num(n=1),
            Num(n=1),
          ], keywords=[], starargs=None, kwargs=None),
      ], keywords=[], starargs=None, kwargs=None)),
    Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
        Call(func=Name(id='foo', ctx=Load()), args=[
            Num(n=2),
            Num(n=1),
            Num(n=1),
          ], keywords=[], starargs=None, kwargs=None),
      ], keywords=[], starargs=None, kwargs=None)),
    Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
        Call(func=Name(id='foo', ctx=Load()), args=[
            Num(n=2),
            Num(n=2),
            Num(n=1),
          ], keywords=[], starargs=None, kwargs=None),
      ], keywords=[], starargs=None, kwargs=None)),
    Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
        Call(func=Name(id='foo', ctx=Load()), args=[
            Num(n=1),
            Num(n=2),
            Num(n=2),
          ], keywords=[], starargs=None, kwargs=None),
      ], keywords=[], starargs=None, kwargs=None)),
    Expr(value=Call(func=Name(id='PRINT', ctx=Load()), args=[
        Call(func=Name(id='foo', ctx=Load()), args=[
            Num(n=2),
            Num(n=2),
            Num(n=2),
          ], keywords=[], starargs=None, kwargs=None),
      ], keywords=[], starargs=None, kwargs=None)),
  ])