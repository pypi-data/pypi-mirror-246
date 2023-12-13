# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from dataclasses import asdict
from ipaddress import IPv4Address, IPv6Address

import pytermor as pt

from es7s.cli._base_opts_params import CMDTYPE_BUILTIN, IpParamType
from es7s.cli._decorators import catch_and_log_and_exit, cli_argument, cli_command
from es7s.shared import format_variable
from es7s.shared import get_stdout
from es7s.shared.styles import VarTableStyles


@cli_command(
    name=__file__,
    short_help="get associated country for IP address",
    type=CMDTYPE_BUILTIN,
)
@cli_argument("ADDRESS", type=IpParamType(), required=False)
@catch_and_log_and_exit
class invoker:
    """
    @TODO fix click ARGUMENT output
    """

    def __init__(self, **kwargs):
        from es7s.shared import GeoIpResolver

        self._geo_ip_resolver = GeoIpResolver()
        self._vts = VarTableStyles()
        self._run(**kwargs)

    def _run(self, address: IPv4Address | IPv6Address = None):
        kv = asdict(self._geo_ip_resolver.make_request(address))
        longest_key = max(len(k) for k in kv.keys())
        for k, v in kv.items():
            get_stdout().echo_rendered(
                pt.Fragment(k.rjust(longest_key), self._vts.VARIABLE_KEY_FMT)
                + pt.Fragment(": ", self._vts.VARIABLE_PUNCT_FMT)
                + format_variable(v)
            )
