from lupa import LuaRuntime
import sys
lua = LuaRuntime(unpack_returned_tuples=True)
params = sys.argv[1:]
# func = lua.eval("function asd() %s end" % params.pop())
# func()

# def asd():
#     print(1)


# globals = lua.globals()

# for k in globals:
#     print(k)

# function(pyfunc,param1)
#     var_before=pyfunc(param1) 
# end

def py_func(p):
    return 'hello '+str(p)

# lua.execute('var_before=1;print(var_before);')
#eval返回的是一个lua call到py call的映射
pycall = lua.eval('function(pyfunc,param1) var_before=pyfunc(param1) end')
pycall(py_func,'world')
lua.execute('print(var_before)')