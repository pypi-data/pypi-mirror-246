from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/application-traffic-recognition.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_application_traffic_recognition = resolve('application_traffic_recognition')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition)):
        pass
        yield '!\napplication traffic recognition\n'
        if t_3(environment.getattr((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition), 'applications')):
            pass
            for l_1_application in t_1(environment.getattr(environment.getattr((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition), 'applications'), 'ipv4_applications'), 'name'):
                _loop_vars = {}
                pass
                yield '   !\n   application ipv4 '
                yield str(environment.getattr(l_1_application, 'name'))
                yield '\n'
                if t_3(environment.getattr(l_1_application, 'src_prefix_set_name')):
                    pass
                    yield '      source prefix field-set '
                    yield str(environment.getattr(l_1_application, 'src_prefix_set_name'))
                    yield '\n'
                if t_3(environment.getattr(l_1_application, 'dest_prefix_set_name')):
                    pass
                    yield '      destination prefix field-set '
                    yield str(environment.getattr(l_1_application, 'dest_prefix_set_name'))
                    yield '\n'
                for l_2_protocol in t_1(environment.getattr(l_1_application, 'protocols')):
                    l_2_config = missing
                    _loop_vars = {}
                    pass
                    l_2_config = [l_2_protocol]
                    _loop_vars['config'] = l_2_config
                    if (l_2_protocol == 'tcp'):
                        pass
                        if t_3(environment.getattr(l_1_application, 'tcp_src_port_set_name')):
                            pass
                            context.call(environment.getattr((undefined(name='config') if l_2_config is missing else l_2_config), 'append'), ('source port field-set ' + environment.getattr(l_1_application, 'tcp_src_port_set_name')), _loop_vars=_loop_vars)
                        if t_3(environment.getattr(l_1_application, 'tcp_dest_port_set_name')):
                            pass
                            context.call(environment.getattr((undefined(name='config') if l_2_config is missing else l_2_config), 'append'), ('destination port field-set ' + environment.getattr(l_1_application, 'tcp_dest_port_set_name')), _loop_vars=_loop_vars)
                    if (l_2_protocol == 'udp'):
                        pass
                        if t_3(environment.getattr(l_1_application, 'udp_src_port_set_name')):
                            pass
                            context.call(environment.getattr((undefined(name='config') if l_2_config is missing else l_2_config), 'append'), ('source port field-set ' + environment.getattr(l_1_application, 'udp_src_port_set_name')), _loop_vars=_loop_vars)
                        if t_3(environment.getattr(l_1_application, 'udp_dest_port_set_name')):
                            pass
                            context.call(environment.getattr((undefined(name='config') if l_2_config is missing else l_2_config), 'append'), ('destination port field-set ' + environment.getattr(l_1_application, 'udp_dest_port_set_name')), _loop_vars=_loop_vars)
                    yield '      protocol '
                    yield str(t_2(context.eval_ctx, (undefined(name='config') if l_2_config is missing else l_2_config), ' '))
                    yield '\n'
                l_2_protocol = l_2_config = missing
                if t_3(environment.getattr(l_1_application, 'protocol_ranges')):
                    pass
                    yield '      protocol '
                    yield str(t_2(context.eval_ctx, t_1(environment.getattr(l_1_application, 'protocol_ranges'), 'name'), ', '))
                    yield '\n'
            l_1_application = missing
        for l_1_category in t_1(environment.getattr((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition), 'categories'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   category '
            yield str(environment.getattr(l_1_category, 'name'))
            yield '\n'
            for l_2_app_details in t_1(t_1(environment.getattr(l_1_category, 'applications'), 'name'), 'service'):
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_2_app_details, 'service')):
                    pass
                    yield '      application '
                    yield str(environment.getattr(l_2_app_details, 'name'))
                    yield ' service '
                    yield str(environment.getattr(l_2_app_details, 'service'))
                    yield '\n'
                else:
                    pass
                    yield '      application '
                    yield str(environment.getattr(l_2_app_details, 'name'))
                    yield '\n'
            l_2_app_details = missing
        l_1_category = missing
        for l_1_application_profile in t_1(environment.getattr((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition), 'application_profiles'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   application-profile '
            yield str(environment.getattr(l_1_application_profile, 'name'))
            yield '\n'
            for l_2_application in t_1(t_1(environment.getattr(l_1_application_profile, 'applications'), 'name'), 'service'):
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_2_application, 'service')):
                    pass
                    yield '      application '
                    yield str(environment.getattr(l_2_application, 'name'))
                    yield ' service '
                    yield str(environment.getattr(l_2_application, 'service'))
                    yield '\n'
                else:
                    pass
                    yield '      application '
                    yield str(environment.getattr(l_2_application, 'name'))
                    yield '\n'
            l_2_application = missing
            for l_2_transport in t_1(environment.getattr(l_1_application_profile, 'application_transports')):
                _loop_vars = {}
                pass
                yield '      application '
                yield str(l_2_transport)
                yield ' transport\n'
            l_2_transport = missing
            for l_2_category in t_1(environment.getattr(l_1_application_profile, 'categories')):
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_2_category, 'service')):
                    pass
                    yield '      category '
                    yield str(environment.getattr(l_2_category, 'name'))
                    yield ' service '
                    yield str(environment.getattr(l_2_category, 'service'))
                    yield '\n'
                else:
                    pass
                    yield '      category '
                    yield str(environment.getattr(l_2_category, 'name'))
                    yield '\n'
            l_2_category = missing
        l_1_application_profile = missing
        if t_3(environment.getattr((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition), 'field_sets')):
            pass
            for l_1_prefix_set in t_1(environment.getattr(environment.getattr((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition), 'field_sets'), 'ipv4_prefixes'), 'name'):
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_1_prefix_set, 'name')):
                    pass
                    context.call(environment.getattr(environment.getattr(l_1_prefix_set, 'prefix_values'), 'sort'), _loop_vars=_loop_vars)
                    yield '   !\n   field-set ipv4 prefix '
                    yield str(environment.getattr(l_1_prefix_set, 'name'))
                    yield '\n      '
                    yield str(t_2(context.eval_ctx, environment.getattr(l_1_prefix_set, 'prefix_values'), ' '))
                    yield '\n'
            l_1_prefix_set = missing
            for l_1_port_set in t_1(environment.getattr(environment.getattr((undefined(name='application_traffic_recognition') if l_0_application_traffic_recognition is missing else l_0_application_traffic_recognition), 'field_sets'), 'l4_ports'), 'name'):
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_1_port_set, 'name')):
                    pass
                    context.call(environment.getattr(environment.getattr(l_1_port_set, 'port_values'), 'sort'), _loop_vars=_loop_vars)
                    yield '   !\n   field-set l4-port '
                    yield str(environment.getattr(l_1_port_set, 'name'))
                    yield '\n      '
                    yield str(t_2(context.eval_ctx, environment.getattr(l_1_port_set, 'port_values'), ', '))
                    yield '\n'
            l_1_port_set = missing

blocks = {}
debug_info = '7=30&10=33&11=35&13=39&14=41&15=44&17=46&18=49&20=51&21=55&22=57&23=59&24=61&26=62&27=64&30=65&31=67&32=69&34=70&35=72&38=74&40=77&41=80&46=83&48=87&49=89&50=92&51=95&53=102&57=106&59=110&60=112&61=115&62=118&64=125&67=128&68=132&70=135&71=138&72=141&74=148&78=152&79=154&80=157&81=159&83=161&84=163&87=166&88=169&89=171&91=173&92=175'