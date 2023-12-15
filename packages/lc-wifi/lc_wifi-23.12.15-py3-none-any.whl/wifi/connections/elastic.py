#!/usr/bin/env python
"""
writes to elasticsearch

We use the DSL to get to_dict-able type defs for the mapping,
For actual interactions we use the low level api (elasticsearch)

"""
# import urllib3

# urllib3.disable_warnings()

import os
import elasticsearch_dsl as ES

# import redis, json
import operators.con.elastic as E
from operators.con.elastic import byte, perc, short, long

env = os.environ


# fmt: off
def client_mac(client):
    return client['vendor']
def client_rssi(client):
    return client['SignalStrength']
def client_standard(client):
    return client['OperatingStandard']
def client_downrate(client):
    return client['LastDataDownlinkRate']

# by our typ or overwritten by our keyname:
def autoch(s):
    return True if str(s).lower() in ('1', 'true', 'on') else False

def security(r):
    return '%s:%s' % (
        r.get('EncryptionMode', 'NoEncr'),
        r.get('ModeEnabled', 'Not Enabled'),
    )

E.types.update(
    {
        autoch:          ES.Boolean,
        client_rssi:     ES.Byte,
        client_standard: ES.Keyword,
        client_downrate: ES.Long,
        client_mac:      ES.Keyword,
        security:        ES.Keyword,
        'scan_dt':       ES.Integer,
    }
)
# fmt: on
DI = 'DeviceInfo'


class Attrs:
    """ELK Parameters Definitions"""

    _default_index = 'wifi'

    # no default -> omit if missing
    # fmt: off
    id                         = 'id'
    ts                         = ['ts'                             , E.to_date_time, 0]
    hardware                   = DI + '.HardwareVersion'
    software                   = DI + '.SoftwareVersion'
    vendor                     = DI + '.Manufacturer'
    model                      = DI + '.ModelName'
    uptime                     = DI + '.UpTime:int'
    mem_usage                  = DI + '.MemoryStatus.usage:int'
    cpu_usage                  = DI + '.ProcessStatus.CPUUsage:int'
    region                     = 'region'
    collector_code             = 'collector.code:int'
    collector_hostname         = 'collector.hostname'
    conf                       = 'conf'
    cid                        = 'metadata.service_id'
    location                   = ['metadata.location'               , E.geo_point     ]
    accessid                   = 'metadata.accessid'
    group_type                 = 'metadata.group_type'

    axwifi_score               = ['score.value'                     , int             ]

    # wifi optimization
    wifi_2_reported_channel    = ['2.Radio.Channel'                 , byte            ]
    wifi_2_enabled             = ['2.Radio.enabled'                 , bool            ]
    wifi_2_standard            = ['2.Radio.op_standard'             , byte            ]
    wifi_2_autochannel         = ['2.Radio.AutoChannelEnable'       , autoch          ]
    wifi_2_channel             = ['2.expert.cur_ch'                 , byte            ]
    wifi_2_bandwidth           = ['2.expert.cur_bw'                 , byte            ]
    wifi_2_qual_current        = ['2.expert.cur_q'                  , perc            ]
    wifi_2_target_channel      = ['2.expert.target_ch'              , byte            ]
    wifi_2_qual_possible       = ['2.expert.target_q'               , perc            ]
    wifi_2_delta_qual          = ['2.expert.delta_q'                , perc            ]
    wifi_2_neighbors_count     = ['2.expert.neighbors.total'        , short           ]
    wifi_2_neighbors_friends   = ['2.expert.neighbors.friends'      , short           ]
    wifi_2_neighbors_extenders = ['2.expert.neighbors.extenders'    , short           ]
    wifi_2_neighbors_aci       = ['2.expert.neighbors.aci'          , short           ]
    wifi_2_neighbors_cci       = ['2.expert.neighbors.cci'          , short           ]
    wifi_2_neighbors_aci_cci   = ['2.expert.neighbors.aci_cci'      , short           ]
    wifi_2_scan_dt             = ['2.scan_dt'                       , int             ]
    wifi_2_allow_enforce       = ['metadata.allow_auto_enforce_2'   , bool            ]
    wifi_2_axwifi_change_ch    = ['2.changes.axwifi'                , bool            ]
    wifi_2_manual_change_ch    = ['2.changes.manual'                , bool            ]
    wifi_2_auto_change_ch      = ['2.changes.auto'                  , bool            ]
    wifi_2_denied_by_cond      = ['2.expert.denied_by_condition'    , bool            ]

    wifi_5_reported_channel    = ['5.Radio.Channel'                 , short           ]
    wifi_5_enabled             = ['5.Radio.enabled'                 , bool            ]
    wifi_5_standard            = ['5.Radio.op_standard'             , byte            ]
    wifi_5_autochannel         = ['5.Radio.AutoChannelEnable'       , autoch          ]
    wifi_5_channel             = ['5.expert.cur_ch'                 , short           ]
    wifi_5_radio_channel       = ['5.expert.cur_radio_ch'           , short           ]
    wifi_5_bandwidth           = ['5.expert.cur_bw'                 , short           ]
    wifi_5_qual_current        = ['5.expert.cur_q'                  , perc            ]
    wifi_5_target_channel      = ['5.expert.target_ch'              , short           ]
    wifi_5_qual_possible       = ['5.expert.target_q'               , perc            ]
    wifi_5_delta_qual          = ['5.expert.delta_q'                , perc            ]
    wifi_5_neighbors_count     = ['5.expert.neighbors.total'        , short           ]
    wifi_5_neighbors_friends   = ['5.expert.neighbors.friends'      , short           ]
    wifi_5_neighbors_extenders = ['5.expert.neighbors.extenders'    , short           ]
    wifi_5_neighbors_interf    = ['5.expert.neighbors.interfering'  , short           ]
    wifi_5_on_dfs              = ['5.expert.cur_on_dfs'             , bool            ]
    wifi_5_scan_dt             = ['5.scan_dt'                       , int             ]
    wifi_5_allow_enforce       = ['metadata.allow_auto_enforce_5'   , bool            ]
    wifi_5_axwifi_change_ch    = ['5.changes.axwifi'                , bool            ]
    wifi_5_manual_change_ch    = ['5.changes.manual'                , bool            ]
    wifi_5_auto_change_ch      = ['5.changes.auto'                  , bool            ]
    wifi_5_denied_by_cond      = ['5.expert.denied_by_condition'    , bool            ]

    # recommendations
    cpe_rec_total              = ['cpe.recommendations.total'                      ,     int      ]
    cpe_rec_cpu                = ['cpe.recommendations.detail.cpu_usage'           ,     bool     ]
    cpe_rec_mem                = ['cpe.recommendations.detail.mem_usage'           ,     bool     ]

    # pme
    pme_high_cpu                = ['cpe.pme.detail.pme_high_cpu'       , bool ]
    pme_high_memory             = ['cpe.pme.detail.pme_high_memory'    , bool ]
    pme_2_neighbors_zero        = ['2.pme.detail.pme_2_neighbors_zero' , bool ]
    pme_2_quality_drop          = ['2.pme.detail.pme_2_quality_drop'   , bool ]
    pme_2_extender_drop         = ['2.pme.detail.pme_2_extender_drop'  , bool ]
    pme_2_mesh_drop             = ['2.pme.detail.pme_2_mesh_drop'      , bool ]
    pme_5_quality_drop          = ['5.pme.detail.pme_2_quality_drop'   , bool ]
    pme_5_extender_drop         = ['5.pme.detail.pme_2_extender_drop'  , bool ]
    pme_5_mesh_drop             = ['5.pme.detail.pme_2_mesh_drop'      , bool ]
    pme_5_neighbors_zero        = ['5.pme.detail.pme_5_neighbors_zero' , bool ]
    forced_reboot               = ['tmp.forced_reboot'                , int  ]
    forced_optimize_2           = ['tmp.forced_optimize_2'             , int  ]
    forced_optimize_5           = ['tmp.forced_optimize_5'             , int  ]
            

    wifi_2_rec_total           = ['2.recommendations.total'                        ,     int      ]
    wifi_2_rec_sec_enc         = ['2.recommendations.detail.security_encryption'   ,     bool     ]
    wifi_2_rec_sec_mod         = ['2.recommendations.detail.security_mode'         ,     bool     ]
    wifi_2_rec_radio_op        = ['2.recommendations.detail.radio_op_standards'    ,     bool     ]
    wifi_2_rec_cli_cov         = ['2.recommendations.detail.clients_coverage'      ,     bool     ]
    wifi_2_rec_cli_op_std      = ['2.recommendations.detail.clients_op_standards'  ,     bool     ]
    wifi_2_rec_steer_int       = ['2.recommendations.detail.steering_interf'       ,     bool     ]
    wifi_2_rec_steer_perf      = ['2.recommendations.detail.steering_perf'         ,     bool     ]
    wifi_2_rec_cli_steer_speed = ['2.recommendations.detail.clients_steering_speed',     bool     ]
    wifi_2_rec_sec_wps_pin     = ['2.recommendations.detail.security_wps_pin'      ,     bool     ]
    wifi_2_rec_sec_open_wifi   = ['2.recommendations.detail.security_open_wifi'    ,     bool     ]
    wifi_2_rec_extender_weak_signal = ['2.recommendations.detail.extender_weak_signal',     bool  ]
    wifi_2_rec_mesh_weak_signal     = ['2.recommendations.detail.mesh_weak_signal'    ,     bool  ]
    wifi_2_rec_extender_extreme_signal = ['2.recommendations.detail.extender_extreme_signal',     bool  ]
    wifi_2_rec_mesh_extreme_signal     = ['2.recommendations.detail.mesh_extreme_signal'    ,     bool  ]

    wifi_5_rec_total           = ['5.recommendations.total'                           ,     int      ]
    wifi_5_rec_sec_enc         = ['5.recommendations.detail.security_encryption'      ,     bool     ]
    wifi_5_rec_sec_mod         = ['5.recommendations.detail.security_mode'            ,     bool     ]
    wifi_5_rec_radio_op        = ['5.recommendations.detail.radio_op_standards'       ,     bool     ]
    wifi_5_rec_cli_cov         = ['5.recommendations.detail.clients_coverage'         ,     bool     ]
    wifi_5_rec_cli_op_std      = ['5.recommendations.detail.clients_op_standards'     ,     bool     ]
    wifi_5_rec_steer_int       = ['5.recommendations.detail.steering_interf'          ,     bool     ]
    wifi_5_rec_steer_perf      = ['5.recommendations.detail.steering_perf'            ,     bool     ]
    wifi_5_rec_cli_steer_cov   = ['5.recommendations.detail.clients_steering_coverage',     bool     ]
    wifi_5_rec_sec_wps_pin     = ['5.recommendations.detail.security_wps_pin'         ,     bool     ]
    wifi_5_rec_sec_open_wifi   = ['5.recommendations.detail.security_open_wifi'       ,     bool     ]
    wifi_5_rec_extender_weak_signal = ['5.recommendations.detail.extender_weak_signal',     bool     ]
    wifi_5_rec_mesh_weak_signal     = ['5.recommendations.detail.mesh_weak_signal'    ,     bool     ]
    wifi_5_rec_extender_extreme_signal = ['5.recommendations.detail.extender_extreme_signal',     bool     ]
    wifi_5_rec_mesh_extreme_signal     = ['5.recommendations.detail.mesh_extreme_signal'    ,     bool     ]

    # radio statistics
    wifi_2_stats_bytes_in      = ['2.Radio.Stats.BytesReceived'     , long            ]
    wifi_2_stats_bytes_out     = ['2.Radio.Stats.BytesSent'         , long            ]
    wifi_2_stats_pkts_in       = ['2.Radio.Stats.PacketsReceived'   , long            ]
    wifi_2_stats_pkts_out      = ['2.Radio.Stats.PacketsSent'       , long            ]
    wifi_2_stats_err_in        = ['2.Radio.Stats.ErrorsReceived'    , long            ]
    wifi_2_stats_err_out       = ['2.Radio.Stats.ErrorsSent'        , long            ]
    wifi_2_stats_noise         = ['2.Radio.Stats.Noise'             , long            ]

    wifi_5_stats_bytes_in      = ['5.Radio.Stats.BytesReceived'     , long            ]
    wifi_5_stats_bytes_out     = ['5.Radio.Stats.BytesSent'         , long            ]
    wifi_5_stats_pkts_in       = ['5.Radio.Stats.PacketsReceived'   , long            ]
    wifi_5_stats_pkts_out      = ['5.Radio.Stats.PacketsSent'       , long            ]
    wifi_5_stats_err_in        = ['5.Radio.Stats.ErrorsReceived'    , long            ]
    wifi_5_stats_err_out       = ['5.Radio.Stats.ErrorsSent'        , long            ]
    wifi_5_stats_noise         = ['5.Radio.Stats.Noise'             , long            ]

    # ssid security
    ssid_2_1_security          = ['2.SSID.1.Security'              , security      , ''    ]
    ssid_2_2_security          = ['2.SSID.2.Security'              , security      , ''    ]

    ssid_5_5_security          = ['5.SSID.5.Security'              , security      , ''    ]
    ssid_5_6_security          = ['5.SSID.6.Security'              , security      , ''    ]

    # ssid statistics
    ssid_2_1_stats_bytes_in  = ['2.SSID.1.Stats.BytesReceived'     , long            ]
    ssid_2_1_stats_bytes_out = ['2.SSID.1.Stats.BytesSent'         , long            ]
    ssid_2_1_stats_pkts_in   = ['2.SSID.1.Stats.PacketsReceived'   , long            ]
    ssid_2_1_stats_pkts_out  = ['2.SSID.1.Stats.PacketsSent'       , long            ]
    ssid_2_1_stats_err_in    = ['2.SSID.1.Stats.ErrorsReceived'    , long            ]
    ssid_2_1_stats_err_out   = ['2.SSID.1.Stats.ErrorsSent'        , long            ]

    ssid_2_2_stats_bytes_in  = ['2.SSID.2.Stats.BytesReceived'     , long            ]
    ssid_2_2_stats_bytes_out = ['2.SSID.2.Stats.BytesSent'         , long            ]
    ssid_2_2_stats_pkts_in   = ['2.SSID.2.Stats.PacketsReceived'   , long            ]
    ssid_2_2_stats_pkts_out  = ['2.SSID.2.Stats.PacketsSent'       , long            ]
    ssid_2_2_stats_err_in    = ['2.SSID.2.Stats.ErrorsReceived'    , long            ]
    ssid_2_2_stats_err_out   = ['2.SSID.2.Stats.ErrorsSent'        , long            ]

    ssid_5_5_stats_bytes_in  = ['5.SSID.5.Stats.BytesReceived'     , long            ]
    ssid_5_5_stats_bytes_out = ['5.SSID.5.Stats.BytesSent'         , long            ]
    ssid_5_5_stats_pkts_in   = ['5.SSID.5.Stats.PacketsReceived'   , long            ]
    ssid_5_5_stats_pkts_out  = ['5.SSID.5.Stats.PacketsSent'       , long            ]
    ssid_5_5_stats_err_in    = ['5.SSID.5.Stats.ErrorsReceived'    , long            ]
    ssid_5_5_stats_err_out   = ['5.SSID.5.Stats.ErrorsSent'        , long            ]

    ssid_5_6_stats_bytes_in  = ['5.SSID.6.Stats.BytesReceived'     , long            ]
    ssid_5_6_stats_bytes_out = ['5.SSID.6.Stats.BytesSent'         , long            ]
    ssid_5_6_stats_pkts_in   = ['5.SSID.6.Stats.PacketsReceived'   , long            ]
    ssid_5_6_stats_pkts_out  = ['5.SSID.6.Stats.PacketsSent'       , long            ]
    ssid_5_6_stats_err_in    = ['5.SSID.6.Stats.ErrorsReceived'    , long            ]
    ssid_5_6_stats_err_out   = ['5.SSID.6.Stats.ErrorsSent'        , long            ]

    # clients counters
    ssid_2_1_clients_count     = ['2.ssid.1.clients.total'          , short           ]
    ssid_2_1_clients_sig_av    = ['2.ssid.1.clients.sig_avg'        , short           ]
    ssid_2_1_clients_low_rssi  = ['2.ssid.1.clients.low_rssi'       , short           ]
    ssid_2_1_clients_good_rssi = ['2.ssid.1.clients.good_rssi'      , short           ]
    ssid_2_1_clients_i1_rssi   = ['2.ssid.1.clients.i1_rssi'        , short           ]
    ssid_2_1_clients_i2_rssi   = ['2.ssid.1.clients.i2_rssi'        , short           ]
    ssid_2_1_clients_i3_rssi   = ['2.ssid.1.clients.i3_rssi'        , short           ]
    ssid_2_1_clients_i4_rssi   = ['2.ssid.1.clients.i4_rssi'        , short           ]
    ssid_2_1_clients_i5_rssi   = ['2.ssid.1.clients.i5_rssi'        , short           ]

    ssid_2_2_clients_count     = ['2.ssid.2.clients.total'          , short           ]
    ssid_2_2_clients_sig_av    = ['2.ssid.2.clients.sig_av'         , short           ]
    ssid_2_2_clients_low_rssi  = ['2.ssid.2.clients.low_rssi'       , short           ]
    ssid_2_2_clients_good_rssi = ['2.ssid.2.clients.good_rssi'      , short           ]
    ssid_2_2_clients_i1_rssi   = ['2.ssid.2.clients.i1_rssi'        , short           ]
    ssid_2_2_clients_i2_rssi   = ['2.ssid.2.clients.i2_rssi'        , short           ]
    ssid_2_2_clients_i3_rssi   = ['2.ssid.2.clients.i3_rssi'        , short           ]
    ssid_2_2_clients_i4_rssi   = ['2.ssid.2.clients.i4_rssi'        , short           ]
    ssid_2_2_clients_i5_rssi   = ['2.ssid.2.clients.i5_rssi'        , short           ]

    ssid_5_5_clients_count     = ['5.ssid.5.clients.total'          , short           ]
    ssid_5_5_clients_sig_av    = ['5.ssid.5.clients.sig_avg'        , short           ]
    ssid_5_5_clients_low_rssi  = ['5.ssid.5.clients.low_rssi'       , short           ]
    ssid_5_5_clients_good_rssi = ['5.ssid.5.clients.good_rssi'      , short           ]
    ssid_5_5_clients_i1_rssi   = ['5.ssid.5.clients.i1_rssi'        , short           ]
    ssid_5_5_clients_i2_rssi   = ['5.ssid.5.clients.i2_rssi'        , short           ]
    ssid_5_5_clients_i3_rssi   = ['5.ssid.5.clients.i3_rssi'        , short           ]
    ssid_5_5_clients_i4_rssi   = ['5.ssid.5.clients.i4_rssi'        , short           ]
    ssid_5_5_clients_i5_rssi   = ['5.ssid.5.clients.i5_rssi'        , short           ]

    ssid_5_6_clients_count     = ['5.ssid.6.clients.total'          , short           ]
    ssid_5_6_clients_sig_av    = ['5.ssid.6.clients.sig_avg'        , short           ]
    ssid_5_6_clients_low_rssi  = ['5.ssid.6.clients.low_rssi'       , short           ]
    ssid_5_6_clients_good_rssi = ['5.ssid.6.clients.good_rssi'      , short           ]
    ssid_5_6_clients_i1_rssi   = ['5.ssid.6.clients.i1_rssi'        , short           ]
    ssid_5_6_clients_i2_rssi   = ['5.ssid.6.clients.i2_rssi'        , short           ]
    ssid_5_6_clients_i3_rssi   = ['5.ssid.6.clients.i3_rssi'        , short           ]
    ssid_5_6_clients_i4_rssi   = ['5.ssid.6.clients.i4_rssi'        , short           ]
    ssid_5_6_clients_i5_rssi   = ['5.ssid.6.clients.i5_rssi'        , short           ]

    # clients statistics
    ssid_2_1_client_intervals_i1_lddr_mean    = ['2.ssid.1.clients.intervals.i1.lddr.mean'       , long          ]
    ssid_2_1_client_intervals_i1_lddr_max     = ['2.ssid.1.clients.intervals.i1.lddr.max'        , long          ]
    ssid_2_1_client_intervals_i1_lddr_min     = ['2.ssid.1.clients.intervals.i1.lddr.min'        , long          ]
    ssid_2_1_client_intervals_i1_lddr_median  = ['2.ssid.1.clients.intervals.i1.lddr.median'     , long          ]
    ssid_2_1_client_intervals_i1_lddr_stdev   = ['2.ssid.1.clients.intervals.i1.lddr.stdev'      , long          ]
    ssid_2_1_client_intervals_i1_ldur_mean    = ['2.ssid.1.clients.intervals.i1.ldur.mean'       , long          ]
    ssid_2_1_client_intervals_i1_ldur_max     = ['2.ssid.1.clients.intervals.i1.ldur.max'        , long          ]
    ssid_2_1_client_intervals_i1_ldur_min     = ['2.ssid.1.clients.intervals.i1.ldur.min'        , long          ]
    ssid_2_1_client_intervals_i1_ldur_median  = ['2.ssid.1.clients.intervals.i1.ldur.median'     , long          ]
    ssid_2_1_client_intervals_i1_ldur_stdev   = ['2.ssid.1.clients.intervals.i1.ldur.stdev'      , long          ]
    ssid_2_1_client_intervals_i1_esent_mean   = ['2.ssid.1.clients.intervals.i1.esent.mean'      , long          ]
    ssid_2_1_client_intervals_i1_esent_max    = ['2.ssid.1.clients.intervals.i1.esent.max'       , long          ]
    ssid_2_1_client_intervals_i1_esent_min    = ['2.ssid.1.clients.intervals.i1.esent.min'       , long          ]
    ssid_2_1_client_intervals_i1_esent_median = ['2.ssid.1.clients.intervals.i1.esent.median'    , long          ]
    ssid_2_1_client_intervals_i1_esent_stdev  = ['2.ssid.1.clients.intervals.i1.esent.stdev'     , long          ]
    ssid_2_1_client_intervals_i1_erec_mean    = ['2.ssid.1.clients.intervals.i1.erec.mean'       , long          ]
    ssid_2_1_client_intervals_i1_erec_max     = ['2.ssid.1.clients.intervals.i1.erec.max'        , long          ]
    ssid_2_1_client_intervals_i1_erec_min     = ['2.ssid.1.clients.intervals.i1.erec.min'        , long          ]
    ssid_2_1_client_intervals_i1_erec_median  = ['2.ssid.1.clients.intervals.i1.erec.median'     , long          ]
    ssid_2_1_client_intervals_i1_erec_stdev   = ['2.ssid.1.clients.intervals.i1.erec.stdev'      , long          ]

    ssid_2_1_client_intervals_i2_lddr_mean    = ['2.ssid.1.clients.intervals.i2.lddr.mean'       , long          ]
    ssid_2_1_client_intervals_i2_lddr_max     = ['2.ssid.1.clients.intervals.i2.lddr.max'        , long          ]
    ssid_2_1_client_intervals_i2_lddr_min     = ['2.ssid.1.clients.intervals.i2.lddr.min'        , long          ]
    ssid_2_1_client_intervals_i2_lddr_median  = ['2.ssid.1.clients.intervals.i2.lddr.median'     , long          ]
    ssid_2_1_client_intervals_i2_lddr_stdev   = ['2.ssid.1.clients.intervals.i2.lddr.stdev'      , long          ]
    ssid_2_1_client_intervals_i2_ldur_mean    = ['2.ssid.1.clients.intervals.i2.ldur.mean'       , long          ]
    ssid_2_1_client_intervals_i2_ldur_max     = ['2.ssid.1.clients.intervals.i2.ldur.max'        , long          ]
    ssid_2_1_client_intervals_i2_ldur_min     = ['2.ssid.1.clients.intervals.i2.ldur.min'        , long          ]
    ssid_2_1_client_intervals_i2_ldur_median  = ['2.ssid.1.clients.intervals.i2.ldur.median'     , long          ]
    ssid_2_1_client_intervals_i2_ldur_stdev   = ['2.ssid.1.clients.intervals.i2.ldur.stdev'      , long          ]
    ssid_2_1_client_intervals_i2_esent_mean   = ['2.ssid.1.clients.intervals.i2.esent.mean'      , long          ]
    ssid_2_1_client_intervals_i2_esent_max    = ['2.ssid.1.clients.intervals.i2.esent.max'       , long          ]
    ssid_2_1_client_intervals_i2_esent_min    = ['2.ssid.1.clients.intervals.i2.esent.min'       , long          ]
    ssid_2_1_client_intervals_i2_esent_median = ['2.ssid.1.clients.intervals.i2.esent.median'    , long          ]
    ssid_2_1_client_intervals_i2_esent_stdev  = ['2.ssid.1.clients.intervals.i2.esent.stdev'     , long          ]
    ssid_2_1_client_intervals_i2_erec_mean    = ['2.ssid.1.clients.intervals.i2.erec.mean'       , long          ]
    ssid_2_1_client_intervals_i2_erec_max     = ['2.ssid.1.clients.intervals.i2.erec.max'        , long          ]
    ssid_2_1_client_intervals_i2_erec_min     = ['2.ssid.1.clients.intervals.i2.erec.min'        , long          ]
    ssid_2_1_client_intervals_i2_erec_median  = ['2.ssid.1.clients.intervals.i2.erec.median'     , long          ]
    ssid_2_1_client_intervals_i2_erec_stdev   = ['2.ssid.1.clients.intervals.i2.erec.stdev'      , long          ]

    ssid_2_1_client_intervals_i3_lddr_mean    = ['2.ssid.1.clients.intervals.i3.lddr.mean'       , long          ]
    ssid_2_1_client_intervals_i3_lddr_max     = ['2.ssid.1.clients.intervals.i3.lddr.max'        , long          ]
    ssid_2_1_client_intervals_i3_lddr_min     = ['2.ssid.1.clients.intervals.i3.lddr.min'        , long          ]
    ssid_2_1_client_intervals_i3_lddr_median  = ['2.ssid.1.clients.intervals.i3.lddr.median'     , long          ]
    ssid_2_1_client_intervals_i3_lddr_stdev   = ['2.ssid.1.clients.intervals.i3.lddr.stdev'      , long          ]
    ssid_2_1_client_intervals_i3_ldur_mean    = ['2.ssid.1.clients.intervals.i3.ldur.mean'       , long          ]
    ssid_2_1_client_intervals_i3_ldur_max     = ['2.ssid.1.clients.intervals.i3.ldur.max'        , long          ]
    ssid_2_1_client_intervals_i3_ldur_min     = ['2.ssid.1.clients.intervals.i3.ldur.min'        , long          ]
    ssid_2_1_client_intervals_i3_ldur_median  = ['2.ssid.1.clients.intervals.i3.ldur.median'     , long          ]
    ssid_2_1_client_intervals_i3_ldur_stdev   = ['2.ssid.1.clients.intervals.i3.ldur.stdev'      , long          ]
    ssid_2_1_client_intervals_i3_esent_mean   = ['2.ssid.1.clients.intervals.i3.esent.mean'      , long          ]
    ssid_2_1_client_intervals_i3_esent_max    = ['2.ssid.1.clients.intervals.i3.esent.max'       , long          ]
    ssid_2_1_client_intervals_i3_esent_min    = ['2.ssid.1.clients.intervals.i3.esent.min'       , long          ]
    ssid_2_1_client_intervals_i3_esent_median = ['2.ssid.1.clients.intervals.i3.esent.median'    , long          ]
    ssid_2_1_client_intervals_i3_esent_stdev  = ['2.ssid.1.clients.intervals.i3.esent.stdev'     , long          ]
    ssid_2_1_client_intervals_i3_erec_mean    = ['2.ssid.1.clients.intervals.i3.erec.mean'       , long          ]
    ssid_2_1_client_intervals_i3_erec_max     = ['2.ssid.1.clients.intervals.i3.erec.max'        , long          ]
    ssid_2_1_client_intervals_i3_erec_min     = ['2.ssid.1.clients.intervals.i3.erec.min'        , long          ]
    ssid_2_1_client_intervals_i3_erec_median  = ['2.ssid.1.clients.intervals.i3.erec.median'     , long          ]
    ssid_2_1_client_intervals_i3_erec_stdev   = ['2.ssid.1.clients.intervals.i3.erec.stdev'      , long          ]

    ssid_2_1_client_intervals_i4_lddr_mean    = ['2.ssid.1.clients.intervals.i4.lddr.mean'       , long          ]
    ssid_2_1_client_intervals_i4_lddr_max     = ['2.ssid.1.clients.intervals.i4.lddr.max'        , long          ]
    ssid_2_1_client_intervals_i4_lddr_min     = ['2.ssid.1.clients.intervals.i4.lddr.min'        , long          ]
    ssid_2_1_client_intervals_i4_lddr_median  = ['2.ssid.1.clients.intervals.i4.lddr.median'     , long          ]
    ssid_2_1_client_intervals_i4_lddr_stdev   = ['2.ssid.1.clients.intervals.i4.lddr.stdev'      , long          ]
    ssid_2_1_client_intervals_i4_ldur_mean    = ['2.ssid.1.clients.intervals.i4.ldur.mean'       , long          ]
    ssid_2_1_client_intervals_i4_ldur_max     = ['2.ssid.1.clients.intervals.i4.ldur.max'        , long          ]
    ssid_2_1_client_intervals_i4_ldur_min     = ['2.ssid.1.clients.intervals.i4.ldur.min'        , long          ]
    ssid_2_1_client_intervals_i4_ldur_median  = ['2.ssid.1.clients.intervals.i4.ldur.median'     , long          ]
    ssid_2_1_client_intervals_i4_ldur_stdev   = ['2.ssid.1.clients.intervals.i4.ldur.stdev'      , long          ]
    ssid_2_1_client_intervals_i4_esent_mean   = ['2.ssid.1.clients.intervals.i4.esent.mean'      , long          ]
    ssid_2_1_client_intervals_i4_esent_max    = ['2.ssid.1.clients.intervals.i4.esent.max'       , long          ]
    ssid_2_1_client_intervals_i4_esent_min    = ['2.ssid.1.clients.intervals.i4.esent.min'       , long          ]
    ssid_2_1_client_intervals_i4_esent_median = ['2.ssid.1.clients.intervals.i4.esent.median'    , long          ]
    ssid_2_1_client_intervals_i4_esent_stdev  = ['2.ssid.1.clients.intervals.i4.esent.stdev'     , long          ]
    ssid_2_1_client_intervals_i4_erec_mean    = ['2.ssid.1.clients.intervals.i4.erec.mean'       , long          ]
    ssid_2_1_client_intervals_i4_erec_max     = ['2.ssid.1.clients.intervals.i4.erec.max'        , long          ]
    ssid_2_1_client_intervals_i4_erec_min     = ['2.ssid.1.clients.intervals.i4.erec.min'        , long          ]
    ssid_2_1_client_intervals_i4_erec_median  = ['2.ssid.1.clients.intervals.i4.erec.median'     , long          ]
    ssid_2_1_client_intervals_i4_erec_stdev   = ['2.ssid.1.clients.intervals.i4.erec.stdev'      , long          ]

    ssid_2_1_client_intervals_i5_lddr_mean    = ['2.ssid.1.clients.intervals.i5.lddr.mean'       , long          ]
    ssid_2_1_client_intervals_i5_lddr_max     = ['2.ssid.1.clients.intervals.i5.lddr.max'        , long          ]
    ssid_2_1_client_intervals_i5_lddr_min     = ['2.ssid.1.clients.intervals.i5.lddr.min'        , long          ]
    ssid_2_1_client_intervals_i5_lddr_median  = ['2.ssid.1.clients.intervals.i5.lddr.median'     , long          ]
    ssid_2_1_client_intervals_i5_lddr_stdev   = ['2.ssid.1.clients.intervals.i5.lddr.stdev'      , long          ]
    ssid_2_1_client_intervals_i5_ldur_mean    = ['2.ssid.1.clients.intervals.i5.ldur.mean'       , long          ]
    ssid_2_1_client_intervals_i5_ldur_max     = ['2.ssid.1.clients.intervals.i5.ldur.max'        , long          ]
    ssid_2_1_client_intervals_i5_ldur_min     = ['2.ssid.1.clients.intervals.i5.ldur.min'        , long          ]
    ssid_2_1_client_intervals_i5_ldur_median  = ['2.ssid.1.clients.intervals.i5.ldur.median'     , long          ]
    ssid_2_1_client_intervals_i5_ldur_stdev   = ['2.ssid.1.clients.intervals.i5.ldur.stdev'      , long          ]
    ssid_2_1_client_intervals_i5_esent_mean   = ['2.ssid.1.clients.intervals.i5.esent.mean'      , long          ]
    ssid_2_1_client_intervals_i5_esent_max    = ['2.ssid.1.clients.intervals.i5.esent.max'       , long          ]
    ssid_2_1_client_intervals_i5_esent_min    = ['2.ssid.1.clients.intervals.i5.esent.min'       , long          ]
    ssid_2_1_client_intervals_i5_esent_median = ['2.ssid.1.clients.intervals.i5.esent.median'    , long          ]
    ssid_2_1_client_intervals_i5_esent_stdev  = ['2.ssid.1.clients.intervals.i5.esent.stdev'     , long          ]
    ssid_2_1_client_intervals_i5_erec_mean    = ['2.ssid.1.clients.intervals.i5.erec.mean'       , long          ]
    ssid_2_1_client_intervals_i5_erec_max     = ['2.ssid.1.clients.intervals.i5.erec.max'        , long          ]
    ssid_2_1_client_intervals_i5_erec_min     = ['2.ssid.1.clients.intervals.i5.erec.min'        , long          ]
    ssid_2_1_client_intervals_i5_erec_median  = ['2.ssid.1.clients.intervals.i5.erec.median'     , long          ]
    ssid_2_1_client_intervals_i5_erec_stdev   = ['2.ssid.1.clients.intervals.i5.erec.stdev'      , long          ]

    ssid_2_1_client_good_lddr_mean            = ['2.ssid.1.clients.good.lddr.mean'               , long          ]
    ssid_2_1_client_good_lddr_max             = ['2.ssid.1.clients.good.lddr.max'                , long          ]
    ssid_2_1_client_good_lddr_min             = ['2.ssid.1.clients.good.lddr.min'                , long          ]
    ssid_2_1_client_good_lddr_median          = ['2.ssid.1.clients.good.lddr.max'                , long          ]
    ssid_2_1_client_good_lddr_stdev           = ['2.ssid.1.clients.good.lddr.min'                , long          ]
    ssid_2_1_client_good_ldur_mean            = ['2.ssid.1.clients.good.ldur.mean'               , long          ]
    ssid_2_1_client_good_ldur_max             = ['2.ssid.1.clients.good.ldur.max'                , long          ]
    ssid_2_1_client_good_ldur_min             = ['2.ssid.1.clients.good.ldur.min'                , long          ]
    ssid_2_1_client_good_ldur_median          = ['2.ssid.1.clients.good.ldur.max'                , long          ]
    ssid_2_1_client_good_ldur_stdev           = ['2.ssid.1.clients.good.ldur.min'                , long          ]
    ssid_2_1_client_good_esent_mean           = ['2.ssid.1.clients.good.esent.mean'              , long          ]
    ssid_2_1_client_good_esent_max            = ['2.ssid.1.clients.good.esent.max'               , long          ]
    ssid_2_1_client_good_esent_min            = ['2.ssid.1.clients.good.esent.min'               , long          ]
    ssid_2_1_client_good_esent_median         = ['2.ssid.1.clients.good.esent.max'               , long          ]
    ssid_2_1_client_good_esent_stdev          = ['2.ssid.1.clients.good.esent.min'               , long          ]
    ssid_2_1_client_good_erec_mean            = ['2.ssid.1.clients.good.erec.mean'               , long          ]
    ssid_2_1_client_good_erec_max             = ['2.ssid.1.clients.good.erec.max'                , long          ]
    ssid_2_1_client_good_erec_min             = ['2.ssid.1.clients.good.erec.min'                , long          ]
    ssid_2_1_client_good_erec_median          = ['2.ssid.1.clients.good.erec.max'                , long          ]
    ssid_2_1_client_good_erec_stdev           = ['2.ssid.1.clients.good.erec.min'                , long          ]

    ssid_2_1_client_global_lddr_mean          = ['2.ssid.1.clients.global.lddr.mean'             , long          ]
    ssid_2_1_client_global_lddr_max           = ['2.ssid.1.clients.global.lddr.max'              , long          ]
    ssid_2_1_client_global_lddr_min           = ['2.ssid.1.clients.global.lddr.min'              , long          ]
    ssid_2_1_client_global_lddr_median        = ['2.ssid.1.clients.global.lddr.max'              , long          ]
    ssid_2_1_client_global_lddr_stdev         = ['2.ssid.1.clients.global.lddr.min'              , long          ]
    ssid_2_1_client_global_ldur_mean          = ['2.ssid.1.clients.global.ldur.mean'             , long          ]
    ssid_2_1_client_global_ldur_max           = ['2.ssid.1.clients.global.ldur.max'              , long          ]
    ssid_2_1_client_global_ldur_min           = ['2.ssid.1.clients.global.ldur.min'              , long          ]
    ssid_2_1_client_global_ldur_median        = ['2.ssid.1.clients.global.ldur.max'              , long          ]
    ssid_2_1_client_global_ldur_stdev         = ['2.ssid.1.clients.global.ldur.min'              , long          ]
    ssid_2_1_client_global_esent_mean         = ['2.ssid.1.clients.global.esent.mean'            , long          ]
    ssid_2_1_client_global_esent_max          = ['2.ssid.1.clients.global.esent.max'             , long          ]
    ssid_2_1_client_global_esent_min          = ['2.ssid.1.clients.global.esent.min'             , long          ]
    ssid_2_1_client_global_esent_median       = ['2.ssid.1.clients.global.esent.max'             , long          ]
    ssid_2_1_client_global_esent_stdev        = ['2.ssid.1.clients.global.esent.min'             , long          ]
    ssid_2_1_client_global_erec_mean          = ['2.ssid.1.clients.global.erec.mean'             , long          ]
    ssid_2_1_client_global_erec_max           = ['2.ssid.1.clients.global.erec.max'              , long          ]
    ssid_2_1_client_global_erec_min           = ['2.ssid.1.clients.global.erec.min'              , long          ]
    ssid_2_1_client_global_erec_median        = ['2.ssid.1.clients.global.erec.max'              , long          ]
    ssid_2_1_client_global_erec_stdev         = ['2.ssid.1.clients.global.erec.min'              , long          ]

    ssid_5_5_client_intervals_i1_lddr_mean    = ['5.ssid.5.clients.intervals.i1.lddr.mean'       , long          ]
    ssid_5_5_client_intervals_i1_lddr_max     = ['5.ssid.5.clients.intervals.i1.lddr.max'        , long          ]
    ssid_5_5_client_intervals_i1_lddr_min     = ['5.ssid.5.clients.intervals.i1.lddr.min'        , long          ]
    ssid_5_5_client_intervals_i1_lddr_median  = ['5.ssid.5.clients.intervals.i1.lddr.median'     , long          ]
    ssid_5_5_client_intervals_i1_lddr_stdev   = ['5.ssid.5.clients.intervals.i1.lddr.stdev'      , long          ]
    ssid_5_5_client_intervals_i1_ldur_mean    = ['5.ssid.5.clients.intervals.i1.ldur.mean'       , long          ]
    ssid_5_5_client_intervals_i1_ldur_max     = ['5.ssid.5.clients.intervals.i1.ldur.max'        , long          ]
    ssid_5_5_client_intervals_i1_ldur_min     = ['5.ssid.5.clients.intervals.i1.ldur.min'        , long          ]
    ssid_5_5_client_intervals_i1_ldur_median  = ['5.ssid.5.clients.intervals.i1.ldur.median'     , long          ]
    ssid_5_5_client_intervals_i1_ldur_stdev   = ['5.ssid.5.clients.intervals.i1.ldur.stdev'      , long          ]
    ssid_5_5_client_intervals_i1_esent_mean   = ['5.ssid.5.clients.intervals.i1.esent.mean'      , long          ]
    ssid_5_5_client_intervals_i1_esent_max    = ['5.ssid.5.clients.intervals.i1.esent.max'       , long          ]
    ssid_5_5_client_intervals_i1_esent_min    = ['5.ssid.5.clients.intervals.i1.esent.min'       , long          ]
    ssid_5_5_client_intervals_i1_esent_median = ['5.ssid.5.clients.intervals.i1.esent.median'    , long          ]
    ssid_5_5_client_intervals_i1_esent_stdev  = ['5.ssid.5.clients.intervals.i1.esent.stdev'     , long          ]
    ssid_5_5_client_intervals_i1_erec_mean    = ['5.ssid.5.clients.intervals.i1.erec.mean'       , long          ]
    ssid_5_5_client_intervals_i1_erec_max     = ['5.ssid.5.clients.intervals.i1.erec.max'        , long          ]
    ssid_5_5_client_intervals_i1_erec_min     = ['5.ssid.5.clients.intervals.i1.erec.min'        , long          ]
    ssid_5_5_client_intervals_i1_erec_median  = ['5.ssid.5.clients.intervals.i1.erec.median'     , long          ]
    ssid_5_5_client_intervals_i1_erec_stdev   = ['5.ssid.5.clients.intervals.i1.erec.stdev'      , long          ]

    ssid_5_5_client_intervals_i2_lddr_mean    = ['5.ssid.5.clients.intervals.i2.lddr.mean'       , long          ]
    ssid_5_5_client_intervals_i2_lddr_max     = ['5.ssid.5.clients.intervals.i2.lddr.max'        , long          ]
    ssid_5_5_client_intervals_i2_lddr_min     = ['5.ssid.5.clients.intervals.i2.lddr.min'        , long          ]
    ssid_5_5_client_intervals_i2_lddr_median  = ['5.ssid.5.clients.intervals.i2.lddr.median'     , long          ]
    ssid_5_5_client_intervals_i2_lddr_stdev   = ['5.ssid.5.clients.intervals.i2.lddr.stdev'      , long          ]
    ssid_5_5_client_intervals_i2_ldur_mean    = ['5.ssid.5.clients.intervals.i2.ldur.mean'       , long          ]
    ssid_5_5_client_intervals_i2_ldur_max     = ['5.ssid.5.clients.intervals.i2.ldur.max'        , long          ]
    ssid_5_5_client_intervals_i2_ldur_min     = ['5.ssid.5.clients.intervals.i2.ldur.min'        , long          ]
    ssid_5_5_client_intervals_i2_ldur_median  = ['5.ssid.5.clients.intervals.i2.ldur.median'     , long          ]
    ssid_5_5_client_intervals_i2_ldur_stdev   = ['5.ssid.5.clients.intervals.i2.ldur.stdev'      , long          ]
    ssid_5_5_client_intervals_i2_esent_mean   = ['5.ssid.5.clients.intervals.i2.esent.mean'      , long          ]
    ssid_5_5_client_intervals_i2_esent_max    = ['5.ssid.5.clients.intervals.i2.esent.max'       , long          ]
    ssid_5_5_client_intervals_i2_esent_min    = ['5.ssid.5.clients.intervals.i2.esent.min'       , long          ]
    ssid_5_5_client_intervals_i2_esent_median = ['5.ssid.5.clients.intervals.i2.esent.median'    , long          ]
    ssid_5_5_client_intervals_i2_esent_stdev  = ['5.ssid.5.clients.intervals.i2.esent.stdev'     , long          ]
    ssid_5_5_client_intervals_i2_erec_mean    = ['5.ssid.5.clients.intervals.i2.erec.mean'       , long          ]
    ssid_5_5_client_intervals_i2_erec_max     = ['5.ssid.5.clients.intervals.i2.erec.max'        , long          ]
    ssid_5_5_client_intervals_i2_erec_min     = ['5.ssid.5.clients.intervals.i2.erec.min'        , long          ]
    ssid_5_5_client_intervals_i2_erec_median  = ['5.ssid.5.clients.intervals.i2.erec.median'     , long          ]
    ssid_5_5_client_intervals_i2_erec_stdev   = ['5.ssid.5.clients.intervals.i2.erec.stdev'      , long          ]

    ssid_5_5_client_intervals_i3_lddr_mean    = ['5.ssid.5.clients.intervals.i3.lddr.mean'       , long          ]
    ssid_5_5_client_intervals_i3_lddr_max     = ['5.ssid.5.clients.intervals.i3.lddr.max'        , long          ]
    ssid_5_5_client_intervals_i3_lddr_min     = ['5.ssid.5.clients.intervals.i3.lddr.min'        , long          ]
    ssid_5_5_client_intervals_i3_lddr_median  = ['5.ssid.5.clients.intervals.i3.lddr.median'     , long          ]
    ssid_5_5_client_intervals_i3_lddr_stdev   = ['5.ssid.5.clients.intervals.i3.lddr.stdev'      , long          ]
    ssid_5_5_client_intervals_i3_ldur_mean    = ['5.ssid.5.clients.intervals.i3.ldur.mean'       , long          ]
    ssid_5_5_client_intervals_i3_ldur_max     = ['5.ssid.5.clients.intervals.i3.ldur.max'        , long          ]
    ssid_5_5_client_intervals_i3_ldur_min     = ['5.ssid.5.clients.intervals.i3.ldur.min'        , long          ]
    ssid_5_5_client_intervals_i3_ldur_median  = ['5.ssid.5.clients.intervals.i3.ldur.median'     , long          ]
    ssid_5_5_client_intervals_i3_ldur_stdev   = ['5.ssid.5.clients.intervals.i3.ldur.stdev'      , long          ]
    ssid_5_5_client_intervals_i3_esent_mean   = ['5.ssid.5.clients.intervals.i3.esent.mean'      , long          ]
    ssid_5_5_client_intervals_i3_esent_max    = ['5.ssid.5.clients.intervals.i3.esent.max'       , long          ]
    ssid_5_5_client_intervals_i3_esent_min    = ['5.ssid.5.clients.intervals.i3.esent.min'       , long          ]
    ssid_5_5_client_intervals_i3_esent_median = ['5.ssid.5.clients.intervals.i3.esent.median'    , long          ]
    ssid_5_5_client_intervals_i3_esent_stdev  = ['5.ssid.5.clients.intervals.i3.esent.stdev'     , long          ]
    ssid_5_5_client_intervals_i3_erec_mean    = ['5.ssid.5.clients.intervals.i3.erec.mean'       , long          ]
    ssid_5_5_client_intervals_i3_erec_max     = ['5.ssid.5.clients.intervals.i3.erec.max'        , long          ]
    ssid_5_5_client_intervals_i3_erec_min     = ['5.ssid.5.clients.intervals.i3.erec.min'        , long          ]
    ssid_5_5_client_intervals_i3_erec_median  = ['5.ssid.5.clients.intervals.i3.erec.median'     , long          ]
    ssid_5_5_client_intervals_i3_erec_stdev   = ['5.ssid.5.clients.intervals.i3.erec.stdev'      , long          ]

    ssid_5_5_client_intervals_i4_lddr_mean    = ['5.ssid.5.clients.intervals.i4.lddr.mean'       , long          ]
    ssid_5_5_client_intervals_i4_lddr_max     = ['5.ssid.5.clients.intervals.i4.lddr.max'        , long          ]
    ssid_5_5_client_intervals_i4_lddr_min     = ['5.ssid.5.clients.intervals.i4.lddr.min'        , long          ]
    ssid_5_5_client_intervals_i4_lddr_median  = ['5.ssid.5.clients.intervals.i4.lddr.median'     , long          ]
    ssid_5_5_client_intervals_i4_lddr_stdev   = ['5.ssid.5.clients.intervals.i4.lddr.stdev'      , long          ]
    ssid_5_5_client_intervals_i4_ldur_mean    = ['5.ssid.5.clients.intervals.i4.ldur.mean'       , long          ]
    ssid_5_5_client_intervals_i4_ldur_max     = ['5.ssid.5.clients.intervals.i4.ldur.max'        , long          ]
    ssid_5_5_client_intervals_i4_ldur_min     = ['5.ssid.5.clients.intervals.i4.ldur.min'        , long          ]
    ssid_5_5_client_intervals_i4_ldur_median  = ['5.ssid.5.clients.intervals.i4.ldur.median'     , long          ]
    ssid_5_5_client_intervals_i4_ldur_stdev   = ['5.ssid.5.clients.intervals.i4.ldur.stdev'      , long          ]
    ssid_5_5_client_intervals_i4_esent_mean   = ['5.ssid.5.clients.intervals.i4.esent.mean'      , long          ]
    ssid_5_5_client_intervals_i4_esent_max    = ['5.ssid.5.clients.intervals.i4.esent.max'       , long          ]
    ssid_5_5_client_intervals_i4_esent_min    = ['5.ssid.5.clients.intervals.i4.esent.min'       , long          ]
    ssid_5_5_client_intervals_i4_esent_median = ['5.ssid.5.clients.intervals.i4.esent.median'    , long          ]
    ssid_5_5_client_intervals_i4_esent_stdev  = ['5.ssid.5.clients.intervals.i4.esent.stdev'     , long          ]
    ssid_5_5_client_intervals_i4_erec_mean    = ['5.ssid.5.clients.intervals.i4.erec.mean'       , long          ]
    ssid_5_5_client_intervals_i4_erec_max     = ['5.ssid.5.clients.intervals.i4.erec.max'        , long          ]
    ssid_5_5_client_intervals_i4_erec_min     = ['5.ssid.5.clients.intervals.i4.erec.min'        , long          ]
    ssid_5_5_client_intervals_i4_erec_median  = ['5.ssid.5.clients.intervals.i4.erec.median'     , long          ]
    ssid_5_5_client_intervals_i4_erec_stdev   = ['5.ssid.5.clients.intervals.i4.erec.stdev'      , long          ]

    ssid_5_5_client_intervals_i5_lddr_mean    = ['5.ssid.5.clients.intervals.i5.lddr.mean'       , long          ]
    ssid_5_5_client_intervals_i5_lddr_max     = ['5.ssid.5.clients.intervals.i5.lddr.max'        , long          ]
    ssid_5_5_client_intervals_i5_lddr_min     = ['5.ssid.5.clients.intervals.i5.lddr.min'        , long          ]
    ssid_5_5_client_intervals_i5_lddr_median  = ['5.ssid.5.clients.intervals.i5.lddr.median'     , long          ]
    ssid_5_5_client_intervals_i5_lddr_stdev   = ['5.ssid.5.clients.intervals.i5.lddr.stdev'      , long          ]
    ssid_5_5_client_intervals_i5_ldur_mean    = ['5.ssid.5.clients.intervals.i5.ldur.mean'       , long          ]
    ssid_5_5_client_intervals_i5_ldur_max     = ['5.ssid.5.clients.intervals.i5.ldur.max'        , long          ]
    ssid_5_5_client_intervals_i5_ldur_min     = ['5.ssid.5.clients.intervals.i5.ldur.min'        , long          ]
    ssid_5_5_client_intervals_i5_ldur_median  = ['5.ssid.5.clients.intervals.i5.ldur.median'     , long          ]
    ssid_5_5_client_intervals_i5_ldur_stdev   = ['5.ssid.5.clients.intervals.i5.ldur.stdev'      , long          ]
    ssid_5_5_client_intervals_i5_esent_mean   = ['5.ssid.5.clients.intervals.i5.esent.mean'      , long          ]
    ssid_5_5_client_intervals_i5_esent_max    = ['5.ssid.5.clients.intervals.i5.esent.max'       , long          ]
    ssid_5_5_client_intervals_i5_esent_min    = ['5.ssid.5.clients.intervals.i5.esent.min'       , long          ]
    ssid_5_5_client_intervals_i5_esent_median = ['5.ssid.5.clients.intervals.i5.esent.median'    , long          ]
    ssid_5_5_client_intervals_i5_esent_stdev  = ['5.ssid.5.clients.intervals.i5.esent.stdev'     , long          ]
    ssid_5_5_client_intervals_i5_erec_mean    = ['5.ssid.5.clients.intervals.i5.erec.mean'       , long          ]
    ssid_5_5_client_intervals_i5_erec_max     = ['5.ssid.5.clients.intervals.i5.erec.max'        , long          ]
    ssid_5_5_client_intervals_i5_erec_min     = ['5.ssid.5.clients.intervals.i5.erec.min'        , long          ]
    ssid_5_5_client_intervals_i5_erec_median  = ['5.ssid.5.clients.intervals.i5.erec.median'     , long          ]
    ssid_5_5_client_intervals_i5_erec_stdev   = ['5.ssid.5.clients.intervals.i5.erec.stdev'      , long          ]

    ssid_5_5_client_good_lddr_mean            = ['5.ssid.5.clients.good.lddr.mean'               , long          ]
    ssid_5_5_client_good_lddr_max             = ['5.ssid.5.clients.good.lddr.max'                , long          ]
    ssid_5_5_client_good_lddr_min             = ['5.ssid.5.clients.good.lddr.min'                , long          ]
    ssid_5_5_client_good_lddr_median          = ['5.ssid.5.clients.good.lddr.max'                , long          ]
    ssid_5_5_client_good_lddr_stdev           = ['5.ssid.5.clients.good.lddr.min'                , long          ]
    ssid_5_5_client_good_ldur_mean            = ['5.ssid.5.clients.good.ldur.mean'               , long          ]
    ssid_5_5_client_good_ldur_max             = ['5.ssid.5.clients.good.ldur.max'                , long          ]
    ssid_5_5_client_good_ldur_min             = ['5.ssid.5.clients.good.ldur.min'                , long          ]
    ssid_5_5_client_good_ldur_median          = ['5.ssid.5.clients.good.ldur.max'                , long          ]
    ssid_5_5_client_good_ldur_stdev           = ['5.ssid.5.clients.good.ldur.min'                , long          ]
    ssid_5_5_client_good_esent_mean           = ['5.ssid.5.clients.good.esent.mean'              , long          ]
    ssid_5_5_client_good_esent_max            = ['5.ssid.5.clients.good.esent.max'               , long          ]
    ssid_5_5_client_good_esent_min            = ['5.ssid.5.clients.good.esent.min'               , long          ]
    ssid_5_5_client_good_esent_median         = ['5.ssid.5.clients.good.esent.max'               , long          ]
    ssid_5_5_client_good_esent_stdev          = ['5.ssid.5.clients.good.esent.min'               , long          ]
    ssid_5_5_client_good_erec_mean            = ['5.ssid.5.clients.good.erec.mean'               , long          ]
    ssid_5_5_client_good_erec_max             = ['5.ssid.5.clients.good.erec.max'                , long          ]
    ssid_5_5_client_good_erec_min             = ['5.ssid.5.clients.good.erec.min'                , long          ]
    ssid_5_5_client_good_erec_median          = ['5.ssid.5.clients.good.erec.max'                , long          ]
    ssid_5_5_client_good_erec_stdev           = ['5.ssid.5.clients.good.erec.min'                , long          ]

    ssid_5_5_client_global_lddr_mean          = ['5.ssid.5.clients.global.lddr.mean'             , long          ]
    ssid_5_5_client_global_lddr_max           = ['5.ssid.5.clients.global.lddr.max'              , long          ]
    ssid_5_5_client_global_lddr_min           = ['5.ssid.5.clients.global.lddr.min'              , long          ]
    ssid_5_5_client_global_lddr_median        = ['5.ssid.5.clients.global.lddr.max'              , long          ]
    ssid_5_5_client_global_lddr_stdev         = ['5.ssid.5.clients.global.lddr.min'              , long          ]
    ssid_5_5_client_global_ldur_mean          = ['5.ssid.5.clients.global.ldur.mean'             , long          ]
    ssid_5_5_client_global_ldur_max           = ['5.ssid.5.clients.global.ldur.max'              , long          ]
    ssid_5_5_client_global_ldur_min           = ['5.ssid.5.clients.global.ldur.min'              , long          ]
    ssid_5_5_client_global_ldur_median        = ['5.ssid.5.clients.global.ldur.max'              , long          ]
    ssid_5_5_client_global_ldur_stdev         = ['5.ssid.5.clients.global.ldur.min'              , long          ]
    ssid_5_5_client_global_esent_mean         = ['5.ssid.5.clients.global.esent.mean'            , long          ]
    ssid_5_5_client_global_esent_max          = ['5.ssid.5.clients.global.esent.max'             , long          ]
    ssid_5_5_client_global_esent_min          = ['5.ssid.5.clients.global.esent.min'             , long          ]
    ssid_5_5_client_global_esent_median       = ['5.ssid.5.clients.global.esent.max'             , long          ]
    ssid_5_5_client_global_esent_stdev        = ['5.ssid.5.clients.global.esent.min'             , long          ]
    ssid_5_5_client_global_erec_mean          = ['5.ssid.5.clients.global.erec.mean'             , long          ]
    ssid_5_5_client_global_erec_max           = ['5.ssid.5.clients.global.erec.max'              , long          ]
    ssid_5_5_client_global_erec_min           = ['5.ssid.5.clients.global.erec.min'              , long          ]
    ssid_5_5_client_global_erec_median        = ['5.ssid.5.clients.global.erec.max'              , long          ]
    ssid_5_5_client_global_erec_stdev         = ['5.ssid.5.clients.global.erec.min'              , long          ]

    # delta_quals
    wifi_2_delta_qual = ['2.expert.delta_q' , perc]
    wifi_5_delta_qual = ['5.expert.delta_q' , perc]

    # fmt:on
