import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream


@pluginmatcher(re.compile(r"https?://(?:www\.)?rtpa\.es"))
class RTPA(Plugin):
    def _get_streams(self):
        hls_url = self.session.http.get(self.url, schema=validate.Schema(
            validate.parse_html(),
            validate.xml_xpath_string(".//video/source[@src][@type='application/x-mpegURL'][1]/@src")
        ))
        if not hls_url:
            return

        return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = RTPA
