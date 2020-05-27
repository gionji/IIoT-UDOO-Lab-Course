import sys
sys.path.insert(0, "..")

from opcua import ua, Server,

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


## OPC methods definition 1
# method to be exposed through server
def odd_or_even(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants
@uamethod
def multiply(parent, x, y):
    print("double method call with parameter: ", x , y)
    return x * y




def main():
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    server_namespace = "http://examples.freeopcua.github.io"
    address_space = server.register_namespace( server_namespace )

    # get Objects node, this is where we should put our custom stuff
    objects_node = server.get_objects_node()

    # Add the ocp objects (vars, features,...)
    # cresting the first object
    my_first_object = objects_node.add_object(address_space, "MyFirstObject")

    ## Two different methods definitions
    # First
    method_1_node = my_first_object.add_method(
                                                address_space,
                                                "method_1_description",
                                                odd_or_even,
                                                [ua.VariantType.Int32],
                                                [ua.VariantType.Boolean]
                                              )

    # Second
    inarg_1 = ua.Argument()
    inarg_1.Name = "Argument_1"
    inarg_1.DataType = ua.NodeId(ua.ObjectIds.Float32)
    inarg_1.ValueRank = -1
    inarg_1.ArrayDimensions = []
    inarg_1.Description = ua.LocalizedText("Method argument 1 description")
    inarg_2 = ua.Argument()
    inarg_2.Name = "Argument_2"
    inarg_2.DataType = ua.NodeId(ua.ObjectIds.Float32)
    inarg_2.ValueRank = -1
    inarg_2.ArrayDimensions = []
    inarg_2.Description = ua.LocalizedText("Method argument 2 description")
    outarg = ua.Argument()
    outarg.Name = "Result"
    outarg.DataType = ua.NodeId(ua.ObjectIds.Float32)
    outarg.ValueRank = -1
    outarg.ArrayDimensions = []
    outarg.Description = ua.LocalizedText("Output argument description")

    method_2_node = my_first_object.add_method( address_space,
                                                "method_2_description",
                                                multiply,
                                                [inarg_1, inarg_2],
                                                [outarg]
                                              )



    # starting!
    server.start()
    print( "Server starting ...")


    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
