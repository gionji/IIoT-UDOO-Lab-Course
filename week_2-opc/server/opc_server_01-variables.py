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

    # create the fist variable
    my_first_variable = my_first_object.add_variable( address_space, "MyFirstVariable", 0.0 )
    # create a hardtyped variable
    my_hardtyped_variable = my_first_object.add_variable(address_space, "MyHardtypedVariable", 0, ua.VariantType.Float)

    # allow the clients to update variable value
    my_first_variable.set_writable()

    # starting!
    server.start()
    print( "Server starting ...")

    # count the cycles
    count = 0

    while True:
        count = count + 1
        time.sleep(1)

        # use the counter as a dummy value
        value = count

        # assign the value to the varibles
        my_first_variable.set_value( value )
        my_hardtyped_variable.set_value( value )


if __name__ == "__main__":
    main()
