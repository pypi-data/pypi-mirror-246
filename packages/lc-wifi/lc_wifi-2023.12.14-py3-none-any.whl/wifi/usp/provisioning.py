import random
from collections import defaultdict
from devapp.app import app
from wifi.usp import usp
from absl import flags


flags.DEFINE_integer(
    'default_usp_bulk_interval',
    default=1800,
    help='Seconds between USP bulk data updates (light scans)',
)


def usp_get(cpeid, params, max_depth=0, msg=None):
    if not isinstance(params, list):
        params = [params]

    job_data = {'type': 'get', 'epid': cpeid, 'body': [params, max_depth]}
    app.debug(f'USP Get job ({msg})', cpeid=cpeid, job_data=job_data)
    usp.job(job_data, msg)
    app.debug('USP Get job result', cpeid=cpeid, job_data=job_data)
    return job_data


def usp_set(cpeid, update_objs, allow_partial=False, msg=None):
    # example upd_objs:
    # { 'Device.BulkData.': {'Enable': [True, True]} }

    if not isinstance(update_objs, dict):
        raise TypeError('update_objs must be a dictionary')

    update_objs_l = []
    for base, params in update_objs.items():
        params_l = [base, []]

        if not isinstance(params, dict):
            raise TypeError('update_objs must contain dictionaries of parameters')

        for param, param_opts in params.items():
            if (isinstance(param_opts, tuple) or isinstance(param_opts, list)) and len(
                param_opts
            ) >= 2:
                value = param_opts[0]
                required = param_opts[1]
            else:
                value = param_opts
                required = True

            params_l[1].append([param, value, bool(required)])

        update_objs_l.append(params_l)

    job_data = {
        'type': 'set',
        'epid': cpeid,
        'body': {'allow_partial': allow_partial, 'update_objs': update_objs_l},
    }
    app.debug(f'USP Set job ({msg})', cpeid=cpeid, job_data=job_data)
    usp.job(job_data, msg)
    app.debug('USP Set job result', cpeid=cpeid, job_data=job_data)
    return job_data


def usp_set_ez(cpeid, update_objs, msg=None):
    # example upd_objs:
    # { 'Device.BulkData.Enable': True }

    if not isinstance(update_objs, dict):
        raise TypeError('update_objs must be a dictionary')

    update_objs_full = defaultdict(dict)
    for param, value in update_objs.items():
        if '.' not in param:
            continue

        prefix, sep, param = param.rpartition('.')
        update_objs_full[prefix][param] = (value, True)

    return usp_set(cpeid, update_objs_full, msg=msg)


def usp_add(cpeid, create_objs, allow_partial=False, msg=None):
    # example create_objs:
    # { 'Device.LocalAgent.Subscription.': [ {'Enable': True, 'ID': 'test_sub'}, {'Enable': True, 'ID': 'test_sub2'} ] }

    if not isinstance(create_objs, dict):
        raise TypeError('create_objs must be a dictionary')

    create_objs_l = []
    for base, objs in create_objs.items():
        if not isinstance(objs, list):
            raise TypeError('create_objs must contain lists of objects')

        for obj in objs:
            if not isinstance(obj, dict):
                raise TypeError('objects in create_objs be dictionaries of parameters')

            params_l = [base, []]

            for param, param_opts in obj.items():
                if (
                    isinstance(param_opts, tuple) or isinstance(param_opts, list)
                ) and len(param_opts) >= 2:
                    value = param_opts[0]
                    required = param_opts[1]
                else:
                    value = param_opts
                    required = True

                params_l[1].append([param, value, bool(required)])

            create_objs_l.append(params_l)

    job_data = {
        'type': 'add',
        'epid': cpeid,
        'body': {'allow_partial': allow_partial, 'create_objs': create_objs_l},
    }
    app.debug(f'USP Add job ({msg})', cpeid=cpeid, job_data=job_data)
    usp.job(job_data, msg)
    app.debug('USP Add job result', cpeid=cpeid, job_data=job_data)
    return job_data


def usp_add_resp_paths(job_data):
    paths = []

    try:
        created_objs = job_data['resp']['Response']['AddResp']['created_obj_results']
    except KeyError:
        return paths

    for obj in created_objs:
        try:
            paths.append(obj['oper_status']['oper_success']['instantiated_path'])
        except KeyError:
            continue
    return paths


def usp_del(cpeid, obj_paths, allow_partial=False, msg=None):
    if not isinstance(obj_paths, list):
        obj_paths = [obj_paths]
    job_data = {
        'type': 'delete',
        'epid': cpeid,
        'body': {'allow_partial': allow_partial, 'obj_paths': obj_paths},
    }
    app.debug(f'USP Delete job ({msg})', cpeid=cpeid, job_data=job_data)
    usp.job(job_data, msg)
    app.debug('USP Delete job result', cpeid=cpeid, job_data=job_data)
    return job_data


class USPProvisioning:
    default_bulk_params_exclude = []
    default_rt_params = []
    default_rt_objs = ['Device.Hosts.Host.']
    default_rt_ops = ['Device.WiFi.NeighboringWiFiDiagnostic()']
    default_rt_events = ['Device.Boot!']

    base_name = 'axwifi'

    bulk_profile_base = 'Device.BulkData.Profile.'
    bulk_profile_search = f'{bulk_profile_base}[Name=="{base_name}"].'
    bulk_profile_max_params = 'Device.BulkData.MaxNumberOfParameterReferences'
    bulk_profile_max_params_default = 64
    bulk_profile_state = 'Device.BulkData.Enable'

    bulk_profile_ref_placeholder = 'BULK_PROFILE'
    controller_ref_placeholder = 'CONTROLLER'

    subscription_base = 'Device.LocalAgent.Subscription.'
    subscription_max_reflist = 256
    subscription_push_id = f'{base_name}_push'
    subscription_rt_vc_id = f'{base_name}_realtime_valuechange'
    subscription_rt_oc_id = f'{base_name}_realtime_objectcreation'
    subscription_rt_od_id = f'{base_name}_realtime_objectdeletion'
    subscription_rt_op_id = f'{base_name}_realtime_operationcomplete'
    subscription_rt_ev_id = f'{base_name}_realtime_events'
    subscription_search = [
        f'{subscription_base}[ID=="{subscription_push_id}"].',
        f'{subscription_base}[ID=="{subscription_rt_vc_id}"].',
        f'{subscription_base}[ID=="{subscription_rt_oc_id}"].',
        f'{subscription_base}[ID=="{subscription_rt_od_id}"].',
        f'{subscription_base}[ID=="{subscription_rt_op_id}"].',
        f'{subscription_base}[ID=="{subscription_rt_ev_id}"].',
    ]

    controller_base = 'Device.LocalAgent.Controller.'

    @classmethod
    def delete_subscriptions(cls, cpeid):
        return usp_del(
            cpeid,
            cls.subscription_search,
            allow_partial=True,
            msg='Delete existing AXWIFI subscription(s)',
        )

    @classmethod
    def delete_bulk_profiles(cls, cpeid):
        return usp_del(
            cpeid,
            cls.bulk_profile_search,
            allow_partial=True,
            msg='Delete existing AXWIFI bulk profile(s)',
        )

    @classmethod
    def get_default_bulk_params(cls, job_data):
        #default parameters (LightScanParams) are tailored for direct gets, not bulk
        replacements = {
            cls.bulk_profile_base: cls.bulk_profile_ref_placeholder,
            cls.controller_base: cls.controller_ref_placeholder
        }

        #ensure reporting of parameters regarding the bulk profile and controller
        required = [
            'BULK_PROFILE.ReportingInterval',
            'CONTROLLER.MTP.*.Enable',
            'CONTROLLER.MTP.*.Protocol'
        ]

        #exclude Device.LocalAgent.Controller., as our own is already in required
        remove = set(['Device.LocalAgent.Controller.'])

        result = set(required)

        for param in usp.lightscan.params_by_cpeid(job_data)[0]:
            if param in remove:
                continue

            placeholder = None

            for match, replacement in replacements.items():
                if param.startswith(match):
                    param = param[len(match):]
                    placeholder = replacement
                    break

            if placeholder is not None:
                #remove hardcoded object # from LightScanParams
                param = param.split('.', 1)[-1]
                #prepend placeholder, which will be replaced by real reference with object #
                param = f'{placeholder}.{param}'

            result.add(param)

        return list(result)

    @classmethod
    def get_cpe_max_bulk_params(cls, cpeid):
        data = usp_get(
            cpeid, cls.bulk_profile_max_params, msg='Get maximum bulk profile parameters'
        )
        return int(data['resp_dict'][cls.bulk_profile_max_params])

    @classmethod
    def get_controller_ref_from_subscr(cls, cpeid, subscription_ref):
        param = f'{subscription_ref}Recipient'
        data = usp_get(cpeid, param, msg='Get own controller reference')
        return data['resp_dict'][param]

    @classmethod
    def generate_time_ref(cls):
        days = random.randint(1, 28)
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        return '2023-01-%02dT%02d:%02d:%02dZ' % (days, hours, minutes, seconds)

    @classmethod
    def add_bulk_profile(cls, cpeid, interval):
        create = {
            cls.bulk_profile_base: [
                {
                    'Enable': '1',
                    'Name': cls.base_name,
                    'ReportingInterval': str(interval),
                    #'Protocol': protocol,
                    #'EncodingType': encoding_type,
                    'TimeReference': cls.generate_time_ref(),
                }
            ]
        }
        resp = usp_add(cpeid, create, msg=f'Adding bulk profile {cls.base_name}')
        created = usp_add_resp_paths(resp)
        if len(created):
            return created[0]
        else:
            raise RuntimeError(
                f'Unable to add bulk profile {cls.base_name}, response code {resp["resp_status"]}'
            )

    @classmethod
    def replace_param_placeholders(cls, params, bulk_ref, controller_ref):
        if not isinstance(params, list):
            params = [params]

        result = []
        for param in params:
            placeholder = None
            replacement = None

            if bulk_ref and param.startswith(cls.bulk_profile_ref_placeholder):
                placeholder = cls.bulk_profile_ref_placeholder
                replacement = bulk_ref
            elif controller_ref and param.startswith(cls.controller_ref_placeholder):
                placeholder = cls.controller_ref_placeholder
                replacement = controller_ref

            if placeholder is not None:
                param = param[len(placeholder):]
                if param.startswith('.') and replacement.endswith('.'):
                    param = param[1:]
                param = replacement + param

            result.append(param)
        return result

    @classmethod
    def add_bulk_profile_params(
        cls,
        cpeid,
        bulk_ref,
        controller_ref,
        params,
        params_exclude,
        bulk_max_params=bulk_profile_max_params_default,
    ):
        if not params:
            return

        params = cls.replace_param_placeholders(params, bulk_ref, controller_ref)
        params_exclude = cls.replace_param_placeholders(
            params_exclude, bulk_ref, controller_ref
        )

        params_full = [{'Reference': (param, False)} for param in params]
        for param in params_exclude:
            params_full.append({'Reference': (param, False), 'Exclude': True})
        create = {f'{bulk_ref}Parameter.': params_full}

        if (bulk_max_params not in (-1, 0, None, '')) and len(
            params_full
        ) > bulk_max_params:
            params_full = params_full[:bulk_max_params]
            app.warning('Bulk profile parameters truncated.')

        resp = usp_add(
            cpeid,
            create,
            allow_partial=True,
            msg=f'Adding bulk profile {cls.base_name} parameters',
        )
        if resp['resp_status'] != 200:
            raise RuntimeError(
                f'Unable to add bulk profile {cls.base_name} parameters, response code '
                + resp['resp_status']
            )
        return usp_add_resp_paths(resp)

    @classmethod
    def enable_bulk_service(cls, cpeid):
        return usp_set_ez(
            cpeid, {cls.bulk_profile_state: "1"}, msg='Enable USP bulk data service'
        )

    @classmethod
    def add_subscription(
        cls,
        cpeid,
        subscr_id,
        type,
        params,
        bulk_ref=None,
        controller_ref=None,
        retry=False,
    ):
        if not params:
            return

        params = cls.replace_param_placeholders(params, bulk_ref, controller_ref)

        create = {
            cls.subscription_base: [
                {
                    'Enable': '1',
                    'ID': subscr_id,
                    'Alias': subscr_id,
                    'NotifType': type,
                    'ReferenceList': cls.convert_to_reflist(params),
                    'Persistent': '1',
                    'NotifRetry': str(int(retry)),
                }
            ]
        }
        resp = usp_add(cpeid, create, msg=f'Adding subscription {subscr_id}')
        created = usp_add_resp_paths(resp)
        if len(created):
            return created[0]
        else:
            raise RuntimeError(
                f'Unable to add subscription {subscr_id}, response code {resp["resp_status"]}'
            )

    @classmethod
    def convert_to_reflist(cls, params):
        if not isinstance(params, list):
            return params

        reflist = ','.join(params)

        if cls.subscription_max_reflist and (len(reflist) > cls.subscription_max_reflist):
            app.warning('Subscription reflist truncated.')
            if len(params) > 1:
                reflist = reflist[: cls.subscription_max_reflist]
                reflist = reflist.rsplit(',', 1)[0]
            else:
                reflist = ''

        return reflist

    @classmethod
    def is_provisioned(cls, job_data):
        job_data['is_provisioned'] = None

        cpeid = job_data.get('epid', job_data.get('id'))
        if not cpeid:
            msg = 'No epid to check.'
            job_data['err'] = msg
            app.error(msg, job_data=job_data)
            return job_data

        app.info('Checking USP CPE provisioning.', cpeid=cpeid)
        search = list(cls.subscription_search)
        search.append(cls.bulk_profile_search)
        data = usp_get(cpeid, search, msg='Check CPE provisioning', max_depth=1)
        job_data['provisioned_response'] = data

        try:
            prov = job_data['is_provisioned'] = bool(len(data['resp_dict']))
            prov = 'already' if prov else 'not'
            app.info(f'USP CPE {prov} provisioned.', cpeid=cpeid)
        except KeyError:
            app.warning('Unable to determine USP CPE provisioning state.', cpeid=cpeid)

        return job_data

    @classmethod
    def provision(cls, job_data):
        cpeid = job_data.get('epid', job_data.get('id'))
        if not cpeid:
            msg = 'No epid to provision.'
            job_data['err'] = msg
            app.error(msg, job_data=job_data)
            return job_data

        bulk_interval = job_data.get('bulk_interval', flags.FLAGS.default_usp_bulk_interval)
        bulk_params = job_data.get('bulk_params', cls.get_default_bulk_params(job_data))

        bulk_params_exclude = job_data.get(
            'bulk_params_exclude', cls.default_bulk_params_exclude
        )
        if bulk_params and not bulk_interval:
            msg = 'Must specify bulk_interval.'
            job_data['err'] = msg
            app.error(msg, job_data=job_data)
            return job_data

        if bulk_params_exclude and not bulk_params:
            msg = 'Must specify bulk_params to be able to use bulk_params_exclude.'
            job_data['err'] = msg
            app.error(msg, job_data=job_data)
            return job_data

        rt_params = job_data.get('rt_params', cls.default_rt_params)
        rt_objs = job_data.get('rt_objs', cls.default_rt_objs)
        rt_ops = job_data.get('rt_ops', cls.default_rt_ops)
        rt_events = job_data.get('rt_events', cls.default_rt_events)

        prov = bool(
            len(bulk_params) +
            len(rt_params) +
            len(rt_objs) +
            len(rt_ops) +
            len(rt_events)
        )
        prov = 'provision' if prov else 'deprovision'
        app.info(f'About to {prov} USP CPE.', cpeid=cpeid)

        bulk_max_params = cls.bulk_profile_max_params_default
        try:
            bulk_max_params = cls.get_cpe_max_bulk_params(cpeid)
        except Exception as e:
            app.warning(
                'Unable to get maximum number of bulk parameters, '
                f'continuing with default {bulk_max_params}.',
                cpeid=cpeid,
                ex=e,
            )

        try:
            cls.delete_subscriptions(cpeid)
        except Exception as e:
            app.warning(
                'Unable to delete existing subscriptions, continuing.', cpeid=cpeid, ex=e
            )

        try:
            cls.delete_bulk_profiles(cpeid)
        except Exception as e:
            app.warning(
                'Unable to delete existing bulk profiles, continuing.', cpeid=cpeid, ex=e
            )

        bulk_profile_ref = None
        controller_ref = None
        if bulk_params:
            bulk_max_params = cls.bulk_profile_max_params_default
            try:
                bulk_max_params = cls.get_cpe_max_bulk_params(cpeid)
            except Exception as e:
                app.warning(
                    'Unable to get maximum number of bulk parameters, '
                    f'continuing with default {bulk_max_params}.',
                    cpeid=cpeid,
                    ex=e,
                )

            try:
                bulk_profile_ref = cls.add_bulk_profile(cpeid, bulk_interval)
            except Exception as e:
                msg = 'Unable to add bulk profile, exiting.'
                job_data['err'] = msg
                job_data['ex'] = e
                app.error(msg, job_data=job_data, ex=e)
                return job_data

            try:
                bulk_subscription_ref = cls.add_subscription(
                    cpeid, cls.subscription_push_id, 'Event', f'{bulk_profile_ref}Push!'
                )
            except Exception as e:
                msg = 'Unable to add bulk profile subscription, exiting.'
                job_data['err'] = msg
                job_data['ex'] = e
                app.error(msg, job_data=job_data, ex=e)
                return job_data

            try:
                controller_ref = cls.get_controller_ref_from_subscr(
                    cpeid, bulk_subscription_ref
                )
            except Exception as e:
                app.warning(
                    'Unable to get controller reference from bulk profile subscription, continuing. '
                    f'Parameters with {cls.controller_ref_placeholder} references will not work.',
                    cpeid=cpeid,
                    ex=e,
                )

            try:
                cls.add_bulk_profile_params(
                    cpeid,
                    bulk_profile_ref,
                    controller_ref,
                    bulk_params,
                    bulk_params_exclude,
                    bulk_max_params,
                )
            except Exception as e:
                msg = 'Unable to add bulk profile parameters, exiting.'
                job_data['err'] = msg
                job_data['ex'] = e
                app.error(msg, job_data=job_data, ex=e)
                return job_data

            try:
                cls.enable_bulk_service(cpeid)
            except Exception as e:
                msg = 'Unable to activate bulk service, exiting.'
                job_data['err'] = msg
                job_data['ex'] = e
                app.error(msg, job_data=job_data, ex=e)
                return job_data

        rt_subscriptions = {
            cls.subscription_rt_vc_id: ('ValueChange', rt_params, False),
            cls.subscription_rt_oc_id: ('ObjectCreation', rt_objs, True),
            cls.subscription_rt_od_id: ('ObjectDeletion', rt_objs, True),
            cls.subscription_rt_op_id: ('OperationComplete', rt_ops, True),
            cls.subscription_rt_ev_id: ('Event', rt_events, True),
        }

        for subscr_id, (subscr_type, subscr_params, retry) in rt_subscriptions.items():
            try:
                cls.add_subscription(
                    cpeid,
                    subscr_id,
                    subscr_type,
                    subscr_params,
                    bulk_ref=bulk_profile_ref,
                    controller_ref=controller_ref,
                    retry=retry
                )
            except Exception as e:
                msg = f'Unable to add {subscr_id} {subscr_type} subscription, exiting.'
                job_data['err'] = msg
                job_data['ex'] = e
                app.error(msg, job_data=job_data, ex=e)
                return job_data

        msg = f'USP CPE {prov}ed successfully.'
        job_data['done'] = msg
        app.info(msg, cpeid=cpeid)
        return job_data

    @classmethod
    def deprovision(cls, job_data=None):
        if job_data is None:
            job_data = {}
        job_data.update({
            'bulk_params': [],
            'bulk_interval': 0,
            'bulk_params_exclude': [],
            'rt_params': [],
            'rt_objs': [],
            'rt_ops': [],
            'rt_events': []
        })
        return cls.provision(job_data)
