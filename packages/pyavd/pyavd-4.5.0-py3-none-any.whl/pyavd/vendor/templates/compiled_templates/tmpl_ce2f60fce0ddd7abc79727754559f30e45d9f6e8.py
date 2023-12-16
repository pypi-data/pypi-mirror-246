from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/router-bgp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_bgp = resolve('router_bgp')
    l_0_distance_cli = resolve('distance_cli')
    l_0_paths_cli = resolve('paths_cli')
    l_0_rr_preserve_attributes_cli = resolve('rr_preserve_attributes_cli')
    l_0_namespace = resolve('namespace')
    l_0_temp = resolve('temp')
    l_0_neighbor_interfaces = resolve('neighbor_interfaces')
    l_0_row_default_encapsulation = resolve('row_default_encapsulation')
    l_0_row_nhs_source_interface = resolve('row_nhs_source_interface')
    l_0_evpn_hostflap_detection_window = resolve('evpn_hostflap_detection_window')
    l_0_evpn_hostflap_detection_threshold = resolve('evpn_hostflap_detection_threshold')
    l_0_evpn_hostflap_detection_expiry = resolve('evpn_hostflap_detection_expiry')
    l_0_evpn_hostflap_detection_state = resolve('evpn_hostflap_detection_state')
    l_0_evpn_gw_config = resolve('evpn_gw_config')
    l_0_path_selection_roles = resolve('path_selection_roles')
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
        t_3 = environment.filters['first']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'first' found.")
    try:
        t_4 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_5 = environment.filters['length']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'length' found.")
    try:
        t_6 = environment.filters['list']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'list' found.")
    try:
        t_7 = environment.filters['map']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'map' found.")
    try:
        t_8 = environment.filters['selectattr']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No filter named 'selectattr' found.")
    try:
        t_9 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_9(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_9((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp)):
        pass
        yield '\n### Router BGP\n\n#### Router BGP Summary\n\n| BGP AS | Router ID |\n| ------ | --------- |\n| '
        yield str(t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as'), '-'))
        yield ' | '
        yield str(t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id'), '-'))
        yield ' |\n'
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id')):
            pass
            yield '\n| BGP AS | Cluster ID |\n| ------ | --------- |\n| '
            yield str(t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as'), '-'))
            yield ' | '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id'))
            yield ' |\n'
        if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_defaults')) or t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'))):
            pass
            yield '\n| BGP Tuning |\n| ---------- |\n'
            for l_1_bgp_default in t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_defaults'), []):
                _loop_vars = {}
                pass
                yield '| '
                yield str(l_1_bgp_default)
                yield ' |\n'
            l_1_bgp_default = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'enabled'), True):
                pass
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time')):
                    pass
                    yield '| graceful-restart restart-time '
                    yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time')):
                    pass
                    yield '| graceful-restart stalepath-time '
                    yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time'))
                    yield ' |\n'
                yield '| graceful-restart |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), False):
                pass
                yield '| no graceful-restart-helper |\n'
            elif t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), True):
                pass
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time')):
                    pass
                    yield '| graceful-restart-helper restart-time '
                    yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time'))
                    yield ' |\n'
                elif t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'long_lived'), True):
                    pass
                    yield '| graceful-restart-helper long-lived |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'bestpath'), 'd_path'), True):
                pass
                yield '| bgp bestpath d-path |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_for_convergence'), True):
                pass
                yield '| update wait-for-convergence |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_install'), True):
                pass
                yield '| update wait-install |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), True):
                pass
                yield '| bgp default ipv4-unicast |\n'
            elif t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), False):
                pass
                yield '| no bgp default ipv4-unicast |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), True):
                pass
                yield '| bgp default ipv4-unicast transport ipv6 |\n'
            elif t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), False):
                pass
                yield '| no bgp default ipv4-unicast transport ipv6 |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes')):
                pass
                l_0_distance_cli = str_join(('distance bgp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes'), ))
                context.vars['distance_cli'] = l_0_distance_cli
                context.exported_vars.add('distance_cli')
                if (t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes')) and t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'))):
                    pass
                    l_0_distance_cli = str_join(((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes'), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'), ))
                    context.vars['distance_cli'] = l_0_distance_cli
                    context.exported_vars.add('distance_cli')
                yield '| '
                yield str((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths')):
                pass
                l_0_paths_cli = str_join(('maximum-paths ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths'), ))
                context.vars['paths_cli'] = l_0_paths_cli
                context.exported_vars.add('paths_cli')
                if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp')):
                    pass
                    l_0_paths_cli = str_join(((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli), ' ecmp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp'), ))
                    context.vars['paths_cli'] = l_0_paths_cli
                    context.exported_vars.add('paths_cli')
                yield '| '
                yield str((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'enabled'), True):
                pass
                l_0_rr_preserve_attributes_cli = 'bgp route-reflector preserve-attributes'
                context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
                context.exported_vars.add('rr_preserve_attributes_cli')
                if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'always'), True):
                    pass
                    l_0_rr_preserve_attributes_cli = str_join(((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli), ' always', ))
                    context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
                    context.exported_vars.add('rr_preserve_attributes_cli')
                yield '| '
                yield str((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli))
                yield ' |\n'
        l_0_temp = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['temp'] = l_0_temp
        context.exported_vars.add('temp')
        if not isinstance(l_0_temp, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_temp['bgp_vrf_listen_ranges'] = False
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs')):
            pass
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'listen_ranges')):
                    pass
                    if not isinstance(l_0_temp, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_0_temp['bgp_vrf_listen_ranges'] = True
                    break
            l_1_vrf = missing
        if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges')) or t_9(environment.getattr((undefined(name='temp') if l_0_temp is missing else l_0_temp), 'bgp_vrf_listen_ranges'), True)):
            pass
            yield '\n#### Router BGP Listen Ranges\n\n| Prefix | Peer-ID Include Router ID | Peer Group | Peer-Filter | Remote-AS | VRF |\n| ------ | ------------------------- | ---------- | ----------- | --------- | --- |\n'
            if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges')):
                pass
                def t_10(fiter):
                    for l_1_listen_range in fiter:
                        if ((t_9(environment.getattr(l_1_listen_range, 'peer_group')) and t_9(environment.getattr(l_1_listen_range, 'prefix'))) and (t_9(environment.getattr(l_1_listen_range, 'peer_filter')) or t_9(environment.getattr(l_1_listen_range, 'remote_as')))):
                            yield l_1_listen_range
                for l_1_listen_range in t_10(t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges'), 'peer_group')):
                    l_1_row_remote_as = resolve('row_remote_as')
                    _loop_vars = {}
                    pass
                    if t_9(environment.getattr(l_1_listen_range, 'peer_filter')):
                        pass
                        l_1_row_remote_as = '-'
                        _loop_vars['row_remote_as'] = l_1_row_remote_as
                    elif t_9(environment.getattr(l_1_listen_range, 'remote_as')):
                        pass
                        l_1_row_remote_as = environment.getattr(l_1_listen_range, 'remote_as')
                        _loop_vars['row_remote_as'] = l_1_row_remote_as
                    yield '| '
                    yield str(environment.getattr(l_1_listen_range, 'prefix'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_listen_range, 'peer_id_include_router_id'), '-'))
                    yield ' | '
                    yield str(environment.getattr(l_1_listen_range, 'peer_group'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_listen_range, 'peer_filter'), '-'))
                    yield ' | '
                    yield str((undefined(name='row_remote_as') if l_1_row_remote_as is missing else l_1_row_remote_as))
                    yield ' | default |\n'
                l_1_listen_range = l_1_row_remote_as = missing
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'listen_ranges')):
                    pass
                    def t_11(fiter):
                        for l_2_listen_range in fiter:
                            if ((t_9(environment.getattr(l_2_listen_range, 'peer_group')) and t_9(environment.getattr(l_2_listen_range, 'prefix'))) and (t_9(environment.getattr(l_2_listen_range, 'peer_filter')) or t_9(environment.getattr(l_2_listen_range, 'remote_as')))):
                                yield l_2_listen_range
                    for l_2_listen_range in t_11(t_2(environment.getattr(l_1_vrf, 'listen_ranges'), 'peer_group')):
                        l_2_row_remote_as = resolve('row_remote_as')
                        _loop_vars = {}
                        pass
                        if t_9(environment.getattr(l_2_listen_range, 'peer_filter')):
                            pass
                            l_2_row_remote_as = '-'
                            _loop_vars['row_remote_as'] = l_2_row_remote_as
                        elif t_9(environment.getattr(l_2_listen_range, 'remote_as')):
                            pass
                            l_2_row_remote_as = environment.getattr(l_2_listen_range, 'remote_as')
                            _loop_vars['row_remote_as'] = l_2_row_remote_as
                        yield '| '
                        yield str(environment.getattr(l_2_listen_range, 'prefix'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_listen_range, 'peer_id_include_router_id'), '-'))
                        yield ' | '
                        yield str(environment.getattr(l_2_listen_range, 'peer_group'))
                        yield ' | '
                        yield str(t_1(environment.getattr(l_2_listen_range, 'peer_filter'), '-'))
                        yield ' | '
                        yield str((undefined(name='row_remote_as') if l_2_row_remote_as is missing else l_2_row_remote_as))
                        yield ' | '
                        yield str(environment.getattr(l_1_vrf, 'name'))
                        yield ' |\n'
                    l_2_listen_range = l_2_row_remote_as = missing
            l_1_vrf = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups')):
            pass
            yield '\n#### Router BGP Peer Groups\n'
            for l_1_peer_group in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
                l_1_remove_private_as_setting = resolve('remove_private_as_setting')
                l_1_remove_private_as_ingress_setting = resolve('remove_private_as_ingress_setting')
                l_1_neighbor_rib_in_pre_policy_retain_row = resolve('neighbor_rib_in_pre_policy_retain_row')
                l_1_value = resolve('value')
                _loop_vars = {}
                pass
                yield '\n##### '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield '\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_9(environment.getattr(l_1_peer_group, 'type')):
                    pass
                    yield '| Address Family | '
                    yield str(environment.getattr(l_1_peer_group, 'type'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'shutdown'), True):
                    pass
                    yield '| Shutdown | '
                    yield str(environment.getattr(l_1_peer_group, 'shutdown'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled')):
                    pass
                    l_1_remove_private_as_setting = environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled')
                    _loop_vars['remove_private_as_setting'] = l_1_remove_private_as_setting
                    if ((environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled') == True) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'all'), True)):
                        pass
                        l_1_remove_private_as_setting = str_join(((undefined(name='remove_private_as_setting') if l_1_remove_private_as_setting is missing else l_1_remove_private_as_setting), ' (All)', ))
                        _loop_vars['remove_private_as_setting'] = l_1_remove_private_as_setting
                        if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'replace_as'), True):
                            pass
                            l_1_remove_private_as_setting = str_join(((undefined(name='remove_private_as_setting') if l_1_remove_private_as_setting is missing else l_1_remove_private_as_setting), ' (Replace AS)', ))
                            _loop_vars['remove_private_as_setting'] = l_1_remove_private_as_setting
                    yield '| Remove Private AS Outbound | '
                    yield str((undefined(name='remove_private_as_setting') if l_1_remove_private_as_setting is missing else l_1_remove_private_as_setting))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled')):
                    pass
                    l_1_remove_private_as_ingress_setting = environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled')
                    _loop_vars['remove_private_as_ingress_setting'] = l_1_remove_private_as_ingress_setting
                    if ((environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled') == True) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'replace_as'), True)):
                        pass
                        l_1_remove_private_as_ingress_setting = str_join(((undefined(name='remove_private_as_ingress_setting') if l_1_remove_private_as_ingress_setting is missing else l_1_remove_private_as_ingress_setting), ' (Replace AS)', ))
                        _loop_vars['remove_private_as_ingress_setting'] = l_1_remove_private_as_ingress_setting
                    yield '| Remove Private AS Inbound | '
                    yield str((undefined(name='remove_private_as_ingress_setting') if l_1_remove_private_as_ingress_setting is missing else l_1_remove_private_as_ingress_setting))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'enabled'), True):
                    pass
                    yield '| Allowas-in | Allowed, allowed '
                    yield str(t_1(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times'), '3 (default)'))
                    yield ' times |\n'
                if t_9(environment.getattr(l_1_peer_group, 'remote_as')):
                    pass
                    yield '| Remote AS | '
                    yield str(environment.getattr(l_1_peer_group, 'remote_as'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'local_as')):
                    pass
                    yield '| Local AS | '
                    yield str(environment.getattr(l_1_peer_group, 'local_as'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'route_reflector_client')):
                    pass
                    yield '| Route Reflector Client | Yes |\n'
                if t_9(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix')):
                    pass
                    yield '| Listen range prefix | '
                    yield str(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'next_hop_self'), True):
                    pass
                    yield '| Next-hop self | True |\n'
                if t_9(environment.getattr(l_1_peer_group, 'next_hop_unchanged'), True):
                    pass
                    yield '| Next-hop unchanged | True |\n'
                if t_9(environment.getattr(l_1_peer_group, 'update_source')):
                    pass
                    yield '| Source | '
                    yield str(environment.getattr(l_1_peer_group, 'update_source'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled')):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_row = environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled')
                    _loop_vars['neighbor_rib_in_pre_policy_retain_row'] = l_1_neighbor_rib_in_pre_policy_retain_row
                    if (t_9(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), True) and t_9(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'all'), True)):
                        pass
                        l_1_neighbor_rib_in_pre_policy_retain_row = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_row') if l_1_neighbor_rib_in_pre_policy_retain_row is missing else l_1_neighbor_rib_in_pre_policy_retain_row), ' (All)', ))
                        _loop_vars['neighbor_rib_in_pre_policy_retain_row'] = l_1_neighbor_rib_in_pre_policy_retain_row
                    yield '| RIB Pre-Policy Retain | '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_row') if l_1_neighbor_rib_in_pre_policy_retain_row is missing else l_1_neighbor_rib_in_pre_policy_retain_row))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'bfd'), True):
                    pass
                    yield '| BFD | True |\n'
                if t_9(environment.getattr(l_1_peer_group, 'ebgp_multihop')):
                    pass
                    yield '| Ebgp multihop | '
                    yield str(environment.getattr(l_1_peer_group, 'ebgp_multihop'))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'enabled'), True):
                    pass
                    yield '| Default originate | True |\n'
                if t_9(environment.getattr(l_1_peer_group, 'session_tracker')):
                    pass
                    yield '| Session tracker | '
                    yield str(environment.getattr(l_1_peer_group, 'session_tracker'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'send_community')):
                    pass
                    yield '| Send community | '
                    yield str(environment.getattr(l_1_peer_group, 'send_community'))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'maximum_routes')):
                    pass
                    if (environment.getattr(l_1_peer_group, 'maximum_routes') == 0):
                        pass
                        l_1_value = '0 (no limit)'
                        _loop_vars['value'] = l_1_value
                    else:
                        pass
                        l_1_value = environment.getattr(l_1_peer_group, 'maximum_routes')
                        _loop_vars['value'] = l_1_value
                    if (t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit')) or t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True)):
                        pass
                        l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ' (', ))
                        _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit')):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-limit ', environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit'), ))
                            _loop_vars['value'] = l_1_value
                            if t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True):
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ', ', ))
                                _loop_vars['value'] = l_1_value
                            else:
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ')', ))
                                _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-only)', ))
                            _loop_vars['value'] = l_1_value
                    yield '| Maximum routes | '
                    yield str((undefined(name='value') if l_1_value is missing else l_1_value))
                    yield ' |\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'enabled'), True):
                    pass
                    l_1_value = 'enabled'
                    _loop_vars['value'] = l_1_value
                    if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default')):
                        pass
                        l_1_value = str_join(('default ', environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default'), ))
                        _loop_vars['value'] = l_1_value
                    yield '| Link-Bandwidth | '
                    yield str((undefined(name='value') if l_1_value is missing else l_1_value))
                    yield ' |\n'
                if t_9(environment.getattr(l_1_peer_group, 'passive'), True):
                    pass
                    yield '| Passive | True |\n'
            l_1_peer_group = l_1_remove_private_as_setting = l_1_remove_private_as_ingress_setting = l_1_neighbor_rib_in_pre_policy_retain_row = l_1_value = missing
        l_0_temp = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['temp'] = l_0_temp
        context.exported_vars.add('temp')
        if not isinstance(l_0_temp, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_temp['bgp_vrf_neighbors'] = False
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs')):
            pass
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'neighbors')):
                    pass
                    if not isinstance(l_0_temp, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_0_temp['bgp_vrf_neighbors'] = True
                    break
            l_1_vrf = missing
        if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbors')) or t_9(environment.getattr((undefined(name='temp') if l_0_temp is missing else l_0_temp), 'bgp_vrf_neighbors'), True)):
            pass
            yield '\n#### BGP Neighbors\n\n| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive |\n| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- |\n'
            for l_1_neighbor in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbors'), 'ip_address'):
                l_1_inherited = resolve('inherited')
                l_1_neighbor_peer_group = resolve('neighbor_peer_group')
                l_1_peer_group = resolve('peer_group')
                l_1_neighbor_rib_in_pre_policy_retain = resolve('neighbor_rib_in_pre_policy_retain')
                l_1_value = resolve('value')
                l_1_value_allowas = resolve('value_allowas')
                l_1_active_parameter = missing
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_neighbor, 'peer_group')):
                    pass
                    l_1_inherited = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                    _loop_vars['inherited'] = l_1_inherited
                    l_1_neighbor_peer_group = environment.getattr(l_1_neighbor, 'peer_group')
                    _loop_vars['neighbor_peer_group'] = l_1_neighbor_peer_group
                    l_1_peer_group = t_3(environment, t_8(context, t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), []), 'name', 'arista.avd.defined', (undefined(name='neighbor_peer_group') if l_1_neighbor_peer_group is missing else l_1_neighbor_peer_group)))
                    _loop_vars['peer_group'] = l_1_peer_group
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'remote_as')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['remote_as'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'vrf')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['vrf'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'send_community')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['send_community'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'maximum_routes')):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['maximum_routes'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'allowas_in'), 'enabled'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['allowas_in'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'bfd'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['bfd'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'shutdown'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['shutdown'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'rib_in_pre_policy_retain'), 'enabled'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['rib_in_pre_policy_retain'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'route_reflector_client'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['route_reflector_client'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                    if t_9(environment.getattr((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group), 'passive'), True):
                        pass
                        if not isinstance(l_1_inherited, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_1_inherited['passive'] = str_join(('Inherited from peer group ', environment.getattr(l_1_neighbor, 'peer_group'), ))
                l_1_active_parameter = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                _loop_vars['active_parameter'] = l_1_active_parameter
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['remote_as'] = t_1(environment.getattr(l_1_neighbor, 'remote_as'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'remote_as'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['vrf'] = t_1(environment.getattr(l_1_neighbor, 'vrf'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'vrf'), 'default')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['send_community'] = t_1(environment.getattr(l_1_neighbor, 'send_community'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'send_community'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['bfd'] = t_1(environment.getattr(l_1_neighbor, 'bfd'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'bfd'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['shutdown'] = t_1(environment.getattr(l_1_neighbor, 'shutdown'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'shutdown'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['route_reflector_client'] = t_1(environment.getattr(l_1_neighbor, 'route_reflector_client'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'route_reflector_client'), '-')
                if t_9(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled')):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain = environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled')
                    _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_1_neighbor_rib_in_pre_policy_retain
                    if (t_9(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True) and t_9(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'all'), True)):
                        pass
                        l_1_neighbor_rib_in_pre_policy_retain = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain') if l_1_neighbor_rib_in_pre_policy_retain is missing else l_1_neighbor_rib_in_pre_policy_retain), ' (All)', ))
                        _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_1_neighbor_rib_in_pre_policy_retain
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['rib_in_pre_policy_retain'] = t_1((undefined(name='neighbor_rib_in_pre_policy_retain') if l_1_neighbor_rib_in_pre_policy_retain is missing else l_1_neighbor_rib_in_pre_policy_retain), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'rib_in_pre_policy_retain'), '-')
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['passive'] = t_1(environment.getattr(l_1_neighbor, 'passive'), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'passive'), '-')
                if t_9(environment.getattr(l_1_neighbor, 'maximum_routes')):
                    pass
                    if (environment.getattr(l_1_neighbor, 'maximum_routes') == 0):
                        pass
                        l_1_value = '0 (no limit)'
                        _loop_vars['value'] = l_1_value
                    else:
                        pass
                        l_1_value = environment.getattr(l_1_neighbor, 'maximum_routes')
                        _loop_vars['value'] = l_1_value
                    if (t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit')) or t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True)):
                        pass
                        l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ' (', ))
                        _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit')):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-limit ', environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit'), ))
                            _loop_vars['value'] = l_1_value
                            if t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True):
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ', ', ))
                                _loop_vars['value'] = l_1_value
                            else:
                                pass
                                l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), ')', ))
                                _loop_vars['value'] = l_1_value
                        if t_9(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True):
                            pass
                            l_1_value = str_join(((undefined(name='value') if l_1_value is missing else l_1_value), 'warning-only)', ))
                            _loop_vars['value'] = l_1_value
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['maximum_routes'] = t_1((undefined(name='value') if l_1_value is missing else l_1_value), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'maximum_routes'), '-')
                if t_9(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'enabled'), True):
                    pass
                    if t_9(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times')):
                        pass
                        l_1_value_allowas = str_join(('Allowed, allowed ', environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times'), ' times', ))
                        _loop_vars['value_allowas'] = l_1_value_allowas
                    else:
                        pass
                        l_1_value_allowas = 'Allowed, allowed 3 (default) times'
                        _loop_vars['value_allowas'] = l_1_value_allowas
                if not isinstance(l_1_active_parameter, Namespace):
                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                l_1_active_parameter['allowas_in'] = t_1((undefined(name='value_allowas') if l_1_value_allowas is missing else l_1_value_allowas), environment.getattr((undefined(name='inherited') if l_1_inherited is missing else l_1_inherited), 'allowas_in'), '-')
                yield '| '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'remote_as'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'vrf'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'shutdown'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'send_community'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'maximum_routes'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'allowas_in'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'bfd'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'rib_in_pre_policy_retain'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'route_reflector_client'))
                yield ' | '
                yield str(environment.getattr((undefined(name='active_parameter') if l_1_active_parameter is missing else l_1_active_parameter), 'passive'))
                yield ' |\n'
            l_1_neighbor = l_1_inherited = l_1_neighbor_peer_group = l_1_peer_group = l_1_active_parameter = l_1_neighbor_rib_in_pre_policy_retain = l_1_value = l_1_value_allowas = missing
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_vrf, 'neighbors')):
                    pass
                    for l_2_neighbor in environment.getattr(l_1_vrf, 'neighbors'):
                        l_2_neighbor_peer_group = resolve('neighbor_peer_group')
                        l_2_peer_group = resolve('peer_group')
                        l_2_value = resolve('value')
                        l_2_value_allowas = resolve('value_allowas')
                        l_2_neighbor_rib_in_pre_policy_retain = resolve('neighbor_rib_in_pre_policy_retain')
                        l_2_inherited_vrf = l_2_active_parameter_vrf = missing
                        _loop_vars = {}
                        pass
                        l_2_inherited_vrf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                        _loop_vars['inherited_vrf'] = l_2_inherited_vrf
                        if t_9(environment.getattr(l_2_neighbor, 'peer_group')):
                            pass
                            l_2_neighbor_peer_group = environment.getattr(l_2_neighbor, 'peer_group')
                            _loop_vars['neighbor_peer_group'] = l_2_neighbor_peer_group
                            l_2_peer_group = t_3(environment, t_8(context, t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), []), 'name', 'arista.avd.defined', (undefined(name='neighbor_peer_group') if l_2_neighbor_peer_group is missing else l_2_neighbor_peer_group)))
                            _loop_vars['peer_group'] = l_2_peer_group
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'remote_as')):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['remote_as'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'send_community')):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['send_community'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'maximum_routes')):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['maximum_routes'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'allowas_in'), 'enabled'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['allowas_in'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'bfd'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['bfd'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'shutdown'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['shutdown'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'rib_in_pre_policy_retain'), 'enabled'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['rib_in_pre_policy_retain'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'route_reflector_client'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['route_reflector_client'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                            if t_9(environment.getattr((undefined(name='peer_group') if l_2_peer_group is missing else l_2_peer_group), 'passive'), True):
                                pass
                                if not isinstance(l_2_inherited_vrf, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_inherited_vrf['passive'] = str_join(('Inherited from peer group ', environment.getattr(l_2_neighbor, 'peer_group'), ))
                        l_2_active_parameter_vrf = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), _loop_vars=_loop_vars)
                        _loop_vars['active_parameter_vrf'] = l_2_active_parameter_vrf
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['remote_as'] = t_1(environment.getattr(l_2_neighbor, 'remote_as'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'remote_as'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['send_community'] = t_1(environment.getattr(l_2_neighbor, 'send_community'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'send_community'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['bfd'] = t_1(environment.getattr(l_2_neighbor, 'bfd'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'bfd'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['shutdown'] = t_1(environment.getattr(l_2_neighbor, 'shutdown'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'shutdown'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['route_reflector_client'] = t_1(environment.getattr(l_2_neighbor, 'route_reflector_client'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'route_reflector_client'), '-')
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['passive'] = t_1(environment.getattr(l_2_neighbor, 'passive'), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'passive'), '-')
                        if t_9(environment.getattr(l_2_neighbor, 'maximum_routes')):
                            pass
                            if (environment.getattr(l_2_neighbor, 'maximum_routes') == 0):
                                pass
                                l_2_value = '0 (no limit)'
                                _loop_vars['value'] = l_2_value
                            else:
                                pass
                                l_2_value = environment.getattr(l_2_neighbor, 'maximum_routes')
                                _loop_vars['value'] = l_2_value
                            if (t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit')) or t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True)):
                                pass
                                l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), ' (', ))
                                _loop_vars['value'] = l_2_value
                                if t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit')):
                                    pass
                                    l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), 'warning-limit ', environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit'), ))
                                    _loop_vars['value'] = l_2_value
                                    if t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True):
                                        pass
                                        l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), ', ', ))
                                        _loop_vars['value'] = l_2_value
                                    else:
                                        pass
                                        l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), ')', ))
                                        _loop_vars['value'] = l_2_value
                                if t_9(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True):
                                    pass
                                    l_2_value = str_join(((undefined(name='value') if l_2_value is missing else l_2_value), 'warning-only)', ))
                                    _loop_vars['value'] = l_2_value
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['maximum_routes'] = t_1((undefined(name='value') if l_2_value is missing else l_2_value), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'maximum_routes'), '-')
                        if t_9(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'enabled'), True):
                            pass
                            if t_9(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times')):
                                pass
                                l_2_value_allowas = str_join(('Allowed, allowed ', environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times'), ' times', ))
                                _loop_vars['value_allowas'] = l_2_value_allowas
                            else:
                                pass
                                l_2_value_allowas = 'Allowed, allowed 3 (default) times'
                                _loop_vars['value_allowas'] = l_2_value_allowas
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['allowas_in'] = t_1((undefined(name='value_allowas') if l_2_value_allowas is missing else l_2_value_allowas), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'allowas_in'), '-')
                        if t_9(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled')):
                            pass
                            l_2_neighbor_rib_in_pre_policy_retain = environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled')
                            _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_2_neighbor_rib_in_pre_policy_retain
                            if (t_9(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True) and t_9(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'all'), True)):
                                pass
                                l_2_neighbor_rib_in_pre_policy_retain = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain') if l_2_neighbor_rib_in_pre_policy_retain is missing else l_2_neighbor_rib_in_pre_policy_retain), ' (All)', ))
                                _loop_vars['neighbor_rib_in_pre_policy_retain'] = l_2_neighbor_rib_in_pre_policy_retain
                        if not isinstance(l_2_active_parameter_vrf, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_active_parameter_vrf['rib_in_pre_policy_retain'] = t_1((undefined(name='neighbor_rib_in_pre_policy_retain') if l_2_neighbor_rib_in_pre_policy_retain is missing else l_2_neighbor_rib_in_pre_policy_retain), environment.getattr((undefined(name='inherited_vrf') if l_2_inherited_vrf is missing else l_2_inherited_vrf), 'rib_in_pre_policy_retain'), '-')
                        yield '| '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'remote_as'))
                        yield ' | '
                        yield str(environment.getattr(l_1_vrf, 'name'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'shutdown'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'send_community'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'maximum_routes'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'allowas_in'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'bfd'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'rib_in_pre_policy_retain'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'route_reflector_client'))
                        yield ' | '
                        yield str(environment.getattr((undefined(name='active_parameter_vrf') if l_2_active_parameter_vrf is missing else l_2_active_parameter_vrf), 'passive'))
                        yield ' |\n'
                    l_2_neighbor = l_2_inherited_vrf = l_2_neighbor_peer_group = l_2_peer_group = l_2_active_parameter_vrf = l_2_value = l_2_value_allowas = l_2_neighbor_rib_in_pre_policy_retain = missing
            l_1_vrf = missing
        l_0_neighbor_interfaces = []
        context.vars['neighbor_interfaces'] = l_0_neighbor_interfaces
        context.exported_vars.add('neighbor_interfaces')
        for l_1_neighbor_interface in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbor_interfaces'), 'name'):
            _loop_vars = {}
            pass
            context.call(environment.getattr((undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces), 'append'), l_1_neighbor_interface, _loop_vars=_loop_vars)
        l_1_neighbor_interface = missing
        for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
            _loop_vars = {}
            pass
            for l_2_neighbor_interface in t_2(environment.getattr(l_1_vrf, 'neighbor_interfaces'), 'name'):
                _loop_vars = {}
                pass
                context.call(environment.getattr(l_2_neighbor_interface, 'update'), {'vrf': environment.getattr(l_1_vrf, 'name')}, _loop_vars=_loop_vars)
                context.call(environment.getattr((undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces), 'append'), l_2_neighbor_interface, _loop_vars=_loop_vars)
            l_2_neighbor_interface = missing
        l_1_vrf = missing
        if (t_5((undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces)) > 0):
            pass
            yield '\n#### BGP Neighbor Interfaces\n\n| Neighbor Interface | VRF | Peer Group | Remote AS | Peer Filter |\n| ------------------ | --- | ---------- | --------- | ----------- |\n'
            for l_1_neighbor_interface in (undefined(name='neighbor_interfaces') if l_0_neighbor_interfaces is missing else l_0_neighbor_interfaces):
                l_1_vrf = l_1_peer_group = l_1_remote_as = l_1_peer_filter = missing
                _loop_vars = {}
                pass
                l_1_vrf = t_1(environment.getattr(l_1_neighbor_interface, 'vrf'), 'default')
                _loop_vars['vrf'] = l_1_vrf
                l_1_peer_group = t_1(environment.getattr(l_1_neighbor_interface, 'peer_group'), '-')
                _loop_vars['peer_group'] = l_1_peer_group
                l_1_remote_as = t_1(environment.getattr(l_1_neighbor_interface, 'remote_as'), '-')
                _loop_vars['remote_as'] = l_1_remote_as
                l_1_peer_filter = t_1(environment.getattr(l_1_neighbor_interface, 'peer_filter'), '-')
                _loop_vars['peer_filter'] = l_1_peer_filter
                yield '| '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' | '
                yield str((undefined(name='vrf') if l_1_vrf is missing else l_1_vrf))
                yield ' | '
                yield str((undefined(name='peer_group') if l_1_peer_group is missing else l_1_peer_group))
                yield ' | '
                yield str((undefined(name='remote_as') if l_1_remote_as is missing else l_1_remote_as))
                yield ' | '
                yield str((undefined(name='peer_filter') if l_1_peer_filter is missing else l_1_peer_filter))
                yield ' |\n'
            l_1_neighbor_interface = l_1_vrf = l_1_peer_group = l_1_remote_as = l_1_peer_filter = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'aggregate_addresses')):
            pass
            yield '\n#### BGP Route Aggregation\n\n| Prefix | AS Set | Summary Only | Attribute Map | Match Map | Advertise Only |\n| ------ | ------ | ------------ | ------------- | --------- | -------------- |\n'
            for l_1_aggregate_address in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'aggregate_addresses'), 'prefix'):
                l_1_as_set = resolve('as_set')
                l_1_summary_only = resolve('summary_only')
                l_1_advertise_only = resolve('advertise_only')
                l_1_attribute_map = l_1_match_map = missing
                _loop_vars = {}
                pass
                if t_9(environment.getattr(l_1_aggregate_address, 'as_set'), True):
                    pass
                    l_1_as_set = True
                    _loop_vars['as_set'] = l_1_as_set
                else:
                    pass
                    l_1_as_set = False
                    _loop_vars['as_set'] = l_1_as_set
                if t_9(environment.getattr(l_1_aggregate_address, 'summary_only'), True):
                    pass
                    l_1_summary_only = True
                    _loop_vars['summary_only'] = l_1_summary_only
                else:
                    pass
                    l_1_summary_only = False
                    _loop_vars['summary_only'] = l_1_summary_only
                l_1_attribute_map = t_1(environment.getattr(l_1_aggregate_address, 'attribute_map'), '-')
                _loop_vars['attribute_map'] = l_1_attribute_map
                l_1_match_map = t_1(environment.getattr(l_1_aggregate_address, 'match_map'), '-')
                _loop_vars['match_map'] = l_1_match_map
                if t_9(environment.getattr(l_1_aggregate_address, 'advertise_only'), True):
                    pass
                    l_1_advertise_only = True
                    _loop_vars['advertise_only'] = l_1_advertise_only
                else:
                    pass
                    l_1_advertise_only = False
                    _loop_vars['advertise_only'] = l_1_advertise_only
                yield '| '
                yield str(environment.getattr(l_1_aggregate_address, 'prefix'))
                yield ' | '
                yield str((undefined(name='as_set') if l_1_as_set is missing else l_1_as_set))
                yield ' | '
                yield str((undefined(name='summary_only') if l_1_summary_only is missing else l_1_summary_only))
                yield ' | '
                yield str((undefined(name='attribute_map') if l_1_attribute_map is missing else l_1_attribute_map))
                yield ' | '
                yield str((undefined(name='match_map') if l_1_match_map is missing else l_1_match_map))
                yield ' | '
                yield str((undefined(name='advertise_only') if l_1_advertise_only is missing else l_1_advertise_only))
                yield ' |\n'
            l_1_aggregate_address = l_1_as_set = l_1_summary_only = l_1_attribute_map = l_1_match_map = l_1_advertise_only = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn')):
            pass
            yield '\n#### Router BGP EVPN Address Family\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '\n- VPN import pruning is **enabled**\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop'), 'resolution_disabled'), True):
                pass
                yield '\n- Next-hop resolution is **disabled**\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_unchanged'), True):
                pass
                yield '- Next-hop-unchanged is explicitly configured (default behaviour)\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups')):
                pass
                yield '\n##### EVPN Peer Groups\n\n| Peer Group | Activate | Encapsulation |\n| ---------- | -------- | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'encapsulation'), 'default'))
                    yield ' |\n'
                l_1_peer_group = missing
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation')):
                pass
                yield '\n##### EVPN Neighbor Default Encapsulation\n\n| Neighbor Default Encapsulation | Next-hop-self Source Interface |\n| ------------------------------ | ------------------------------ |\n'
                l_0_row_default_encapsulation = t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation'), 'vxlan')
                context.vars['row_default_encapsulation'] = l_0_row_default_encapsulation
                context.exported_vars.add('row_default_encapsulation')
                l_0_row_nhs_source_interface = t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface'), '-')
                context.vars['row_nhs_source_interface'] = l_0_row_nhs_source_interface
                context.exported_vars.add('row_nhs_source_interface')
                yield '| '
                yield str((undefined(name='row_default_encapsulation') if l_0_row_default_encapsulation is missing else l_0_row_default_encapsulation))
                yield ' | '
                yield str((undefined(name='row_nhs_source_interface') if l_0_row_nhs_source_interface is missing else l_0_row_nhs_source_interface))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection')):
                pass
                yield '\n##### EVPN Host Flapping Settings\n\n| State | Window | Threshold | Expiry Timeout |\n| ----- | ------ | --------- | -------------- |\n'
                l_0_evpn_hostflap_detection_window = '-'
                context.vars['evpn_hostflap_detection_window'] = l_0_evpn_hostflap_detection_window
                context.exported_vars.add('evpn_hostflap_detection_window')
                l_0_evpn_hostflap_detection_threshold = '-'
                context.vars['evpn_hostflap_detection_threshold'] = l_0_evpn_hostflap_detection_threshold
                context.exported_vars.add('evpn_hostflap_detection_threshold')
                l_0_evpn_hostflap_detection_expiry = '-'
                context.vars['evpn_hostflap_detection_expiry'] = l_0_evpn_hostflap_detection_expiry
                context.exported_vars.add('evpn_hostflap_detection_expiry')
                if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), True):
                    pass
                    l_0_evpn_hostflap_detection_state = 'Enabled'
                    context.vars['evpn_hostflap_detection_state'] = l_0_evpn_hostflap_detection_state
                    context.exported_vars.add('evpn_hostflap_detection_state')
                    if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window')):
                        pass
                        l_0_evpn_hostflap_detection_window = str_join((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window'), ' Seconds', ))
                        context.vars['evpn_hostflap_detection_window'] = l_0_evpn_hostflap_detection_window
                        context.exported_vars.add('evpn_hostflap_detection_window')
                    l_0_evpn_hostflap_detection_threshold = t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold'), '-')
                    context.vars['evpn_hostflap_detection_threshold'] = l_0_evpn_hostflap_detection_threshold
                    context.exported_vars.add('evpn_hostflap_detection_threshold')
                    if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout')):
                        pass
                        l_0_evpn_hostflap_detection_expiry = str_join((environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout'), ' Seconds', ))
                        context.vars['evpn_hostflap_detection_expiry'] = l_0_evpn_hostflap_detection_expiry
                        context.exported_vars.add('evpn_hostflap_detection_expiry')
                else:
                    pass
                    l_0_evpn_hostflap_detection_state = 'Disabled'
                    context.vars['evpn_hostflap_detection_state'] = l_0_evpn_hostflap_detection_state
                    context.exported_vars.add('evpn_hostflap_detection_state')
                yield '| '
                yield str((undefined(name='evpn_hostflap_detection_state') if l_0_evpn_hostflap_detection_state is missing else l_0_evpn_hostflap_detection_state))
                yield ' | '
                yield str((undefined(name='evpn_hostflap_detection_window') if l_0_evpn_hostflap_detection_window is missing else l_0_evpn_hostflap_detection_window))
                yield ' | '
                yield str((undefined(name='evpn_hostflap_detection_threshold') if l_0_evpn_hostflap_detection_threshold is missing else l_0_evpn_hostflap_detection_threshold))
                yield ' | '
                yield str((undefined(name='evpn_hostflap_detection_expiry') if l_0_evpn_hostflap_detection_expiry is missing else l_0_evpn_hostflap_detection_expiry))
                yield ' |\n'
        l_0_evpn_gw_config = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), peer_groups=[], configured=False)
        context.vars['evpn_gw_config'] = l_0_evpn_gw_config
        context.exported_vars.add('evpn_gw_config')
        for l_1_peer_group in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
            l_1_address_family_evpn_peer_group = resolve('address_family_evpn_peer_group')
            _loop_vars = {}
            pass
            if (t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn')) and t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'))):
                pass
                l_1_address_family_evpn_peer_group = t_6(context.eval_ctx, t_8(context, t_1(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'), []), 'name', 'arista.avd.defined', environment.getattr(l_1_peer_group, 'name')))
                _loop_vars['address_family_evpn_peer_group'] = l_1_address_family_evpn_peer_group
                if t_9(environment.getattr(environment.getitem((undefined(name='address_family_evpn_peer_group') if l_1_address_family_evpn_peer_group is missing else l_1_address_family_evpn_peer_group), 0), 'domain_remote'), True):
                    pass
                    context.call(environment.getattr(environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'peer_groups'), 'append'), environment.getattr(l_1_peer_group, 'name'), _loop_vars=_loop_vars)
                    if not isinstance(l_0_evpn_gw_config, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_0_evpn_gw_config['configured'] = True
        l_1_peer_group = l_1_address_family_evpn_peer_group = missing
        if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'enable'), True):
            pass
            if not isinstance(l_0_evpn_gw_config, Namespace):
                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
            l_0_evpn_gw_config['configured'] = True
        if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'inter_domain'), True):
            pass
            if not isinstance(l_0_evpn_gw_config, Namespace):
                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
            l_0_evpn_gw_config['configured'] = True
        if t_9(environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'configured'), True):
            pass
            yield '\n##### EVPN DCI Gateway Summary\n\n| Settings | Value |\n| -------- | ----- |\n'
            if (t_5(environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'peer_groups')) > 0):
                pass
                yield '| Remote Domain Peer Groups | '
                yield str(t_4(context.eval_ctx, environment.getattr((undefined(name='evpn_gw_config') if l_0_evpn_gw_config is missing else l_0_evpn_gw_config), 'peer_groups'), ', '))
                yield ' |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'enable'), True):
                pass
                yield '| L3 Gateway Configured | True |\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'inter_domain'), True):
                pass
                yield '| L3 Gateway Inter-domain | True |\n'
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te')):
            pass
            yield '\n#### Router BGP IPv4 SR-TE Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'neighbors')):
                pass
                yield '\n##### IPv4 SR-TE Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'peer_groups')):
                pass
                yield '\n##### IPv4 SR-TE Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te')):
            pass
            yield '\n#### Router BGP IPv6 SR-TE Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'neighbors')):
                pass
                yield '\n##### IPv6 SR-TE Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'peer_groups')):
                pass
                yield '\n##### IPv6 SR-TE Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state')):
            pass
            yield '\n#### Router BGP Link-State Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'neighbors')):
                pass
                yield '\n##### Link-State Neighbors\n\n| Neighbor | Activate | Missing policy In action | Missing policy Out action |\n| -------- | -------- | ------------------------ | ------------------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'neighbors'), 'ip_address'):
                    l_1_missing_policy_in = l_1_missing_policy_out = missing
                    _loop_vars = {}
                    pass
                    l_1_missing_policy_in = t_1(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action'), '-')
                    _loop_vars['missing_policy_in'] = l_1_missing_policy_in
                    l_1_missing_policy_out = t_1(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action'), '-')
                    _loop_vars['missing_policy_out'] = l_1_missing_policy_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='missing_policy_in') if l_1_missing_policy_in is missing else l_1_missing_policy_in))
                    yield ' | '
                    yield str((undefined(name='missing_policy_out') if l_1_missing_policy_out is missing else l_1_missing_policy_out))
                    yield ' |\n'
                l_1_neighbor = l_1_missing_policy_in = l_1_missing_policy_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'peer_groups')):
                pass
                yield '\n##### Link-State Peer Groups\n\n| Peer Group | Activate | Missing policy In action | Missing policy Out action |\n| ---------- | -------- | ------------------------ | ------------------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'peer_groups'), 'name'):
                    l_1_missing_policy_in = l_1_missing_policy_out = missing
                    _loop_vars = {}
                    pass
                    l_1_missing_policy_in = t_1(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action'), '-')
                    _loop_vars['missing_policy_in'] = l_1_missing_policy_in
                    l_1_missing_policy_out = t_1(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action'), '-')
                    _loop_vars['missing_policy_out'] = l_1_missing_policy_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='missing_policy_in') if l_1_missing_policy_in is missing else l_1_missing_policy_in))
                    yield ' | '
                    yield str((undefined(name='missing_policy_out') if l_1_missing_policy_out is missing else l_1_missing_policy_out))
                    yield ' |\n'
                l_1_peer_group = l_1_missing_policy_in = l_1_missing_policy_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection')):
                pass
                yield '\n##### Link-State Path Selection Configuration\n\n| Settings | Value |\n| -------- | ----- |\n'
                if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles')):
                    pass
                    l_0_path_selection_roles = []
                    context.vars['path_selection_roles'] = l_0_path_selection_roles
                    context.exported_vars.add('path_selection_roles')
                    if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'producer'), True):
                        pass
                        context.call(environment.getattr((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), 'append'), 'producer')
                    if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True):
                        pass
                        context.call(environment.getattr((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), 'append'), 'consumer')
                    if t_9(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True):
                        pass
                        context.call(environment.getattr((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), 'append'), 'propagator')
                    yield '| Role(s) | '
                    yield str(t_4(context.eval_ctx, (undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), '<br>'))
                    yield ' |\n'
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4')):
            pass
            yield '\n#### Router BGP VPN-IPv4 Address Family\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '\n- VPN import pruning is **enabled**\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbors')):
                pass
                yield '\n##### VPN-IPv4 Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'peer_groups')):
                pass
                yield '\n##### VPN-IPv4 Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6')):
            pass
            yield '\n#### Router BGP VPN-IPv6 Address Family\n'
            if t_9(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '\n- VPN import pruning is **enabled**\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbors')):
                pass
                yield '\n##### VPN-IPv6 Neighbors\n\n| Neighbor | Activate | Route-map In | Route-map Out |\n| -------- | -------- | ------------ | ------------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbors'), 'ip_address'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_neighbor, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_neighbor, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_neighbor = l_1_route_map_in = l_1_route_map_out = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'peer_groups')):
                pass
                yield '\n##### VPN-IPv6 Peer Groups\n\n| Peer Group | Activate | Route-map In | Route-map Out |\n| ---------- | -------- | ------------ | ------------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'peer_groups'), 'name'):
                    l_1_route_map_in = l_1_route_map_out = missing
                    _loop_vars = {}
                    pass
                    l_1_route_map_in = t_1(environment.getattr(l_1_peer_group, 'route_map_in'), '-')
                    _loop_vars['route_map_in'] = l_1_route_map_in
                    l_1_route_map_out = t_1(environment.getattr(l_1_peer_group, 'route_map_out'), '-')
                    _loop_vars['route_map_out'] = l_1_route_map_out
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' | '
                    yield str((undefined(name='route_map_in') if l_1_route_map_in is missing else l_1_route_map_in))
                    yield ' | '
                    yield str((undefined(name='route_map_out') if l_1_route_map_out is missing else l_1_route_map_out))
                    yield ' |\n'
                l_1_peer_group = l_1_route_map_in = l_1_route_map_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection')):
            pass
            yield '\n#### Router BGP Path-Selection Address Family\n'
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'neighbors')):
                pass
                yield '\n##### Path-Selection Neighbors\n\n| Neighbor | Activate |\n| -------- | -------- |\n'
                for l_1_neighbor in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_neighbor, 'activate'), False))
                    yield ' |\n'
                l_1_neighbor = missing
            if t_9(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'peer_groups')):
                pass
                yield '\n##### Path-Selection Peer Groups\n\n| Peer Group | Activate |\n| ---------- | -------- |\n'
                for l_1_peer_group in t_2(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'peer_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_1_peer_group, 'activate'), False))
                    yield ' |\n'
                l_1_peer_group = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlan_aware_bundles')):
            pass
            yield '\n#### Router BGP VLAN Aware Bundles\n\n| VLAN Aware Bundle | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute | VLANs |\n| ----------------- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ | ----- |\n'
            for l_1_vlan_aware_bundle in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlan_aware_bundles'), 'name'):
                l_1_both_route_target = resolve('both_route_target')
                l_1_import_route_target = resolve('import_route_target')
                l_1_export_route_target = resolve('export_route_target')
                l_1_route_distinguisher = l_1_vlans = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
                _loop_vars = {}
                pass
                l_1_route_distinguisher = t_1(environment.getattr(l_1_vlan_aware_bundle, 'rd'), '-')
                _loop_vars['route_distinguisher'] = l_1_route_distinguisher
                l_1_vlans = t_1(environment.getattr(l_1_vlan_aware_bundle, 'vlan'), '-')
                _loop_vars['vlans'] = l_1_vlans
                if (t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'both')) or t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_export_evpn_domains'))):
                    pass
                    l_1_both_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'both'), []))
                    _loop_vars['both_route_target'] = l_1_both_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import')) or t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_evpn_domains'))):
                    pass
                    l_1_import_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import'), []))
                    _loop_vars['import_route_target'] = l_1_import_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export')) or t_9(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export_evpn_domains'))):
                    pass
                    l_1_export_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export'), []))
                    _loop_vars['export_route_target'] = l_1_export_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                l_1_redistribute_route = t_6(context.eval_ctx, t_1(environment.getattr(l_1_vlan_aware_bundle, 'redistribute_routes'), ''))
                _loop_vars['redistribute_route'] = l_1_redistribute_route
                l_1_no_redistribute_route = t_6(context.eval_ctx, t_7(context, t_1(environment.getattr(l_1_vlan_aware_bundle, 'no_redistribute_routes'), ''), 'replace', '', 'no ', 1))
                _loop_vars['no_redistribute_route'] = l_1_no_redistribute_route
                l_1_redistribution = ((undefined(name='redistribute_route') if l_1_redistribute_route is missing else l_1_redistribute_route) + (undefined(name='no_redistribute_route') if l_1_no_redistribute_route is missing else l_1_no_redistribute_route))
                _loop_vars['redistribution'] = l_1_redistribution
                yield '| '
                yield str(environment.getattr(l_1_vlan_aware_bundle, 'name'))
                yield ' | '
                yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_1(t_4(context.eval_ctx, (undefined(name='redistribution') if l_1_redistribution is missing else l_1_redistribution), '<br>'), '-'))
                yield ' | '
                yield str((undefined(name='vlans') if l_1_vlans is missing else l_1_vlans))
                yield ' |\n'
            l_1_vlan_aware_bundle = l_1_route_distinguisher = l_1_vlans = l_1_both_route_target = l_1_import_route_target = l_1_export_route_target = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')):
            pass
            yield '\n#### Router BGP VLANs\n\n| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |\n| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |\n'
            for l_1_vlan in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans'), 'id'):
                l_1_both_route_target = resolve('both_route_target')
                l_1_import_route_target = resolve('import_route_target')
                l_1_export_route_target = resolve('export_route_target')
                l_1_route_distinguisher = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
                _loop_vars = {}
                pass
                l_1_route_distinguisher = t_1(environment.getattr(l_1_vlan, 'rd'), '-')
                _loop_vars['route_distinguisher'] = l_1_route_distinguisher
                if (t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'both')) or t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_export_evpn_domains'))):
                    pass
                    l_1_both_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'both'), []))
                    _loop_vars['both_route_target'] = l_1_both_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import')) or t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_evpn_domains'))):
                    pass
                    l_1_import_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import'), []))
                    _loop_vars['import_route_target'] = l_1_import_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                if (t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export')) or t_9(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export_evpn_domains'))):
                    pass
                    l_1_export_route_target = t_6(context.eval_ctx, t_1(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export'), []))
                    _loop_vars['export_route_target'] = l_1_export_route_target
                    for l_2_rt in t_2(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export_evpn_domains')):
                        _loop_vars = {}
                        pass
                        context.call(environment.getattr((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), 'append'), str_join((environment.getattr(l_2_rt, 'domain'), ' ', environment.getattr(l_2_rt, 'route_target'), )), _loop_vars=_loop_vars)
                    l_2_rt = missing
                l_1_redistribute_route = t_6(context.eval_ctx, t_1(environment.getattr(l_1_vlan, 'redistribute_routes'), ''))
                _loop_vars['redistribute_route'] = l_1_redistribute_route
                l_1_no_redistribute_route = t_6(context.eval_ctx, t_7(context, t_1(environment.getattr(l_1_vlan, 'no_redistribute_routes'), ''), 'replace', '', 'no ', 1))
                _loop_vars['no_redistribute_route'] = l_1_no_redistribute_route
                l_1_redistribution = ((undefined(name='redistribute_route') if l_1_redistribute_route is missing else l_1_redistribute_route) + (undefined(name='no_redistribute_route') if l_1_no_redistribute_route is missing else l_1_no_redistribute_route))
                _loop_vars['redistribution'] = l_1_redistribution
                yield '| '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield ' | '
                yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='both_route_target') if l_1_both_route_target is missing else l_1_both_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='import_route_target') if l_1_import_route_target is missing else l_1_import_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_4(context.eval_ctx, t_1((undefined(name='export_route_target') if l_1_export_route_target is missing else l_1_export_route_target), ['-']), '<br>'))
                yield ' | '
                yield str(t_1(t_4(context.eval_ctx, (undefined(name='redistribution') if l_1_redistribution is missing else l_1_redistribution), '<br>'), '-'))
                yield ' |\n'
            l_1_vlan = l_1_route_distinguisher = l_1_both_route_target = l_1_import_route_target = l_1_export_route_target = l_1_redistribute_route = l_1_no_redistribute_route = l_1_redistribution = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws')):
            pass
            yield '\n#### Router BGP VPWS Instances\n\n| Instance | Route-Distinguisher | Both Route-Target | MPLS Control Word | Label Flow | MTU | Pseudowire | Local ID | Remote ID |\n| -------- | ------------------- | ----------------- | ----------------- | -----------| --- | ---------- | -------- | --------- |\n'
            for l_1_vpws_service in environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws'):
                _loop_vars = {}
                pass
                if ((t_9(environment.getattr(l_1_vpws_service, 'name')) and t_9(environment.getattr(l_1_vpws_service, 'rd'))) and t_9(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export'))):
                    pass
                    for l_2_pseudowire in t_2(environment.getattr(l_1_vpws_service, 'pseudowires'), 'name'):
                        l_2_row_mpls_control_word = resolve('row_mpls_control_word')
                        l_2_row_label_flow = resolve('row_label_flow')
                        l_2_row_mtu = resolve('row_mtu')
                        _loop_vars = {}
                        pass
                        if t_9(environment.getattr(l_2_pseudowire, 'name')):
                            pass
                            l_2_row_mpls_control_word = t_1(environment.getattr(l_1_vpws_service, 'mpls_control_word'), False)
                            _loop_vars['row_mpls_control_word'] = l_2_row_mpls_control_word
                            l_2_row_label_flow = t_1(environment.getattr(l_1_vpws_service, 'label_flow'), False)
                            _loop_vars['row_label_flow'] = l_2_row_label_flow
                            l_2_row_mtu = t_1(environment.getattr(l_1_vpws_service, 'mtu'), '-')
                            _loop_vars['row_mtu'] = l_2_row_mtu
                            yield '| '
                            yield str(environment.getattr(l_1_vpws_service, 'name'))
                            yield ' | '
                            yield str(environment.getattr(l_1_vpws_service, 'rd'))
                            yield ' | '
                            yield str(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export'))
                            yield ' | '
                            yield str((undefined(name='row_mpls_control_word') if l_2_row_mpls_control_word is missing else l_2_row_mpls_control_word))
                            yield ' | '
                            yield str((undefined(name='row_label_flow') if l_2_row_label_flow is missing else l_2_row_label_flow))
                            yield ' | '
                            yield str((undefined(name='row_mtu') if l_2_row_mtu is missing else l_2_row_mtu))
                            yield ' | '
                            yield str(environment.getattr(l_2_pseudowire, 'name'))
                            yield ' | '
                            yield str(environment.getattr(l_2_pseudowire, 'id_local'))
                            yield ' | '
                            yield str(environment.getattr(l_2_pseudowire, 'id_remote'))
                            yield ' |\n'
                    l_2_pseudowire = l_2_row_mpls_control_word = l_2_row_label_flow = l_2_row_mtu = missing
            l_1_vpws_service = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs')):
            pass
            yield '\n#### Router BGP VRFs\n\n'
            if t_6(context.eval_ctx, t_8(context, environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'evpn_multicast', 'arista.avd.defined', True)):
                pass
                yield '| VRF | Route-Distinguisher | Redistribute | EVPN Multicast |\n| --- | ------------------- | ------------ | -------------- |\n'
            else:
                pass
                yield '| VRF | Route-Distinguisher | Redistribute |\n| --- | ------------------- | ------------ |\n'
            for l_1_vrf in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
                l_1_route_distinguisher = l_1_redistribute = l_1_multicast = l_1_multicast_transit = l_1_multicast_out = missing
                _loop_vars = {}
                pass
                l_1_route_distinguisher = t_1(environment.getattr(l_1_vrf, 'rd'), '-')
                _loop_vars['route_distinguisher'] = l_1_route_distinguisher
                l_1_redistribute = t_7(context, t_1(environment.getattr(l_1_vrf, 'redistribute_routes'), [{'source_protocol': '-'}]), attribute='source_protocol')
                _loop_vars['redistribute'] = l_1_redistribute
                l_1_multicast = t_1(environment.getattr(l_1_vrf, 'evpn_multicast'), False)
                _loop_vars['multicast'] = l_1_multicast
                l_1_multicast_transit = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), False)
                _loop_vars['multicast_transit'] = l_1_multicast_transit
                l_1_multicast_out = []
                _loop_vars['multicast_out'] = l_1_multicast_out
                context.call(environment.getattr((undefined(name='multicast_out') if l_1_multicast_out is missing else l_1_multicast_out), 'append'), str_join(('IPv4: ', (undefined(name='multicast') if l_1_multicast is missing else l_1_multicast), )), _loop_vars=_loop_vars)
                context.call(environment.getattr((undefined(name='multicast_out') if l_1_multicast_out is missing else l_1_multicast_out), 'append'), str_join(('Transit: ', (undefined(name='multicast_transit') if l_1_multicast_transit is missing else l_1_multicast_transit), )), _loop_vars=_loop_vars)
                if t_6(context.eval_ctx, t_8(context, environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'evpn_multicast', 'arista.avd.defined', True)):
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_vrf, 'name'))
                    yield ' | '
                    yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                    yield ' | '
                    yield str(t_4(context.eval_ctx, (undefined(name='redistribute') if l_1_redistribute is missing else l_1_redistribute), '<br>'))
                    yield ' | '
                    yield str(t_4(context.eval_ctx, (undefined(name='multicast_out') if l_1_multicast_out is missing else l_1_multicast_out), '<br>'))
                    yield ' |\n'
                else:
                    pass
                    yield '| '
                    yield str(environment.getattr(l_1_vrf, 'name'))
                    yield ' | '
                    yield str((undefined(name='route_distinguisher') if l_1_route_distinguisher is missing else l_1_route_distinguisher))
                    yield ' | '
                    yield str(t_4(context.eval_ctx, (undefined(name='redistribute') if l_1_redistribute is missing else l_1_redistribute), '<br>'))
                    yield ' |\n'
            l_1_vrf = l_1_route_distinguisher = l_1_redistribute = l_1_multicast = l_1_multicast_transit = l_1_multicast_out = missing
        if t_9(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'session_trackers')):
            pass
            yield '\n#### Router BGP Session Trackers\n\n| Session Tracker Name | Recovery Delay (in seconds) |\n| -------------------- | --------------------------- |\n'
            for l_1_session_tracker in t_2(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'session_trackers'), 'name'):
                _loop_vars = {}
                pass
                yield '| '
                yield str(environment.getattr(l_1_session_tracker, 'name'))
                yield ' | '
                yield str(environment.getattr(l_1_session_tracker, 'recovery_delay'))
                yield ' |\n'
            l_1_session_tracker = missing
        yield '\n#### Router BGP Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/router-bgp.j2', 'documentation/router-bgp.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {'distance_cli': l_0_distance_cli, 'evpn_gw_config': l_0_evpn_gw_config, 'evpn_hostflap_detection_expiry': l_0_evpn_hostflap_detection_expiry, 'evpn_hostflap_detection_state': l_0_evpn_hostflap_detection_state, 'evpn_hostflap_detection_threshold': l_0_evpn_hostflap_detection_threshold, 'evpn_hostflap_detection_window': l_0_evpn_hostflap_detection_window, 'neighbor_interfaces': l_0_neighbor_interfaces, 'path_selection_roles': l_0_path_selection_roles, 'paths_cli': l_0_paths_cli, 'row_default_encapsulation': l_0_row_default_encapsulation, 'row_nhs_source_interface': l_0_row_nhs_source_interface, 'rr_preserve_attributes_cli': l_0_rr_preserve_attributes_cli, 'temp': l_0_temp})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=80&15=83&16=87&20=90&22=94&26=97&27=101&29=104&30=106&31=109&33=111&34=114&38=117&40=120&41=122&42=125&43=127&47=130&50=133&53=136&56=139&58=142&61=145&63=148&66=151&67=153&68=156&69=158&71=162&73=164&74=166&75=169&76=171&78=175&80=177&81=179&82=182&83=184&85=188&89=190&90=193&91=196&92=198&93=201&94=203&95=206&99=208&106=211&108=213&107=217&109=221&110=223&111=225&112=227&114=230&118=241&119=244&121=246&120=250&122=254&123=256&124=258&125=260&127=263&132=277&135=280&137=288&141=290&142=293&144=295&145=298&147=300&148=302&149=304&150=306&151=308&152=310&155=313&157=315&158=317&159=319&160=321&162=324&164=326&165=329&167=331&168=334&170=336&171=339&173=341&176=344&177=347&179=349&182=352&185=355&186=358&188=360&189=362&190=364&191=366&193=369&195=371&198=374&199=377&201=379&204=382&205=385&207=387&208=390&210=392&211=394&212=396&214=400&216=402&217=404&218=406&219=408&220=410&221=412&223=416&226=418&227=420&230=423&232=425&233=427&234=429&235=431&237=434&239=436&244=440&245=443&246=446&247=448&248=451&249=453&250=456&254=458&260=461&261=471&262=473&263=475&264=477&267=479&268=481&270=484&271=486&273=489&274=491&276=494&277=496&279=499&280=501&282=504&283=506&285=509&286=511&288=514&289=516&291=519&292=521&294=524&295=526&298=529&299=531&300=534&301=537&302=540&303=543&304=546&305=549&306=551&307=553&308=555&311=557&312=560&313=563&314=565&315=567&317=571&319=573&320=575&321=577&322=579&323=581&324=583&326=587&329=589&330=591&334=593&335=596&336=598&337=600&339=604&342=606&343=610&345=633&346=636&347=638&348=647&349=649&350=651&351=653&354=655&355=657&357=660&358=662&360=665&361=667&363=670&364=672&366=675&367=677&369=680&370=682&372=685&373=687&375=690&376=692&378=695&379=697&382=700&383=702&384=705&385=708&386=711&387=714&388=717&389=720&390=722&391=724&393=728&395=730&396=732&397=734&398=736&399=738&400=740&402=744&405=746&406=748&410=750&411=753&412=755&413=757&415=761&418=763&419=766&420=768&421=770&422=772&425=774&426=778&431=802&432=805&433=808&435=810&436=813&437=816&438=817&441=820&447=823&448=827&449=829&450=831&451=833&452=836&455=847&461=850&462=857&463=859&465=863&467=865&468=867&470=871&472=873&473=875&474=877&475=879&477=883&479=886&482=899&485=902&489=905&493=908&496=911&502=914&503=918&506=925&512=928&513=931&514=935&516=939&522=942&523=945&524=948&525=951&526=953&527=956&528=958&530=961&531=964&532=966&535=971&537=975&540=983&541=986&542=990&543=992&545=994&546=996&547=997&551=1001&552=1003&554=1006&555=1008&557=1011&563=1014&564=1017&566=1019&569=1022&573=1025&576=1028&582=1031&583=1035&584=1037&585=1040&588=1049&594=1052&595=1056&596=1058&597=1061&601=1070&604=1073&610=1076&611=1080&612=1082&613=1085&616=1094&622=1097&623=1101&624=1103&625=1106&629=1115&632=1118&638=1121&639=1125&640=1127&641=1130&644=1139&650=1142&651=1146&652=1148&653=1151&656=1160&662=1163&663=1165&664=1168&665=1170&667=1171&668=1173&670=1174&671=1176&673=1178&677=1180&680=1183&684=1186&690=1189&691=1193&692=1195&693=1198&696=1207&702=1210&703=1214&704=1216&705=1219&709=1228&712=1231&716=1234&722=1237&723=1241&724=1243&725=1246&728=1255&734=1258&735=1262&736=1264&737=1267&741=1276&744=1279&750=1282&751=1286&754=1291&760=1294&761=1298&765=1303&771=1306&772=1313&773=1315&774=1317&775=1319&776=1321&777=1324&780=1326&781=1328&782=1330&783=1333&786=1335&787=1337&788=1339&789=1342&792=1344&793=1346&794=1348&795=1351&798=1366&804=1369&805=1376&806=1378&807=1380&808=1382&809=1385&812=1387&813=1389&814=1391&815=1394&818=1396&819=1398&820=1400&821=1403&824=1405&825=1407&826=1409&827=1412&830=1425&836=1428&837=1431&838=1433&839=1439&840=1441&841=1443&842=1445&843=1448&849=1468&853=1471&860=1477&861=1481&862=1483&863=1485&864=1487&865=1489&866=1491&867=1492&868=1493&869=1496&871=1507&875=1514&881=1517&882=1521&889=1527'