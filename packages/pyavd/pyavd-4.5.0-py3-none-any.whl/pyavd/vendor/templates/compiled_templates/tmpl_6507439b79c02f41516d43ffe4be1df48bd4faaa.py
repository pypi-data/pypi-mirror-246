from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/dhcp-server.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ethernet_interfaces = resolve('ethernet_interfaces')
    l_0_ethernet_interfaces_dhcp_server = missing
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_4 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    l_0_ethernet_interfaces_dhcp_server = []
    context.vars['ethernet_interfaces_dhcp_server'] = l_0_ethernet_interfaces_dhcp_server
    context.exported_vars.add('ethernet_interfaces_dhcp_server')
    for l_1_ethernet_interface in t_2((undefined(name='ethernet_interfaces') if l_0_ethernet_interfaces is missing else l_0_ethernet_interfaces), 'name'):
        _loop_vars = {}
        pass
        if (t_4(environment.getattr(l_1_ethernet_interface, 'dhcp_server_ipv4'), True) or t_4(environment.getattr(l_1_ethernet_interface, 'dhcp_server_ipv4'), True)):
            pass
            context.call(environment.getattr((undefined(name='ethernet_interfaces_dhcp_server') if l_0_ethernet_interfaces_dhcp_server is missing else l_0_ethernet_interfaces_dhcp_server), 'append'), l_1_ethernet_interface, _loop_vars=_loop_vars)
    l_1_ethernet_interface = missing
    if (t_3((undefined(name='ethernet_interfaces_dhcp_server') if l_0_ethernet_interfaces_dhcp_server is missing else l_0_ethernet_interfaces_dhcp_server)) > 0):
        pass
        yield '\n## DHCP Server\n\n### DHCP Server Interfaces\n\n| Interface name | DHCP IPv4 | DHCP IPv6 |\n| -------------- | --------- | --------- |\n'
        for l_1_ethernet_interface in t_2((undefined(name='ethernet_interfaces_dhcp_server') if l_0_ethernet_interfaces_dhcp_server is missing else l_0_ethernet_interfaces_dhcp_server)):
            _loop_vars = {}
            pass
            yield '| '
            yield str(environment.getattr(l_1_ethernet_interface, 'name'))
            yield ' | '
            yield str(t_1(environment.getattr(l_1_ethernet_interface, 'dhcp_server_ipv4'), False))
            yield ' | '
            yield str(t_1(environment.getattr(l_1_ethernet_interface, 'dhcp_server_ipv6'), False))
            yield ' |\n'
        l_1_ethernet_interface = missing

blocks = {}
debug_info = '7=37&8=40&9=43&10=45&14=47&22=50&23=54'