# -*- coding: utf8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
from osync import OSync, Endpoints as Ep
from pytest import fixture, raises
import re


class TestOSyncRegulars:
    def test_instantiation_with_explicit_port(self):
        sync = OSync(endpoint=Ep.source, port=49151)
        assert isinstance(sync, OSync)

    def test_instantiation_with_random_port(self):
        sync = OSync(endpoint=Ep.source, port=None)
        assert isinstance(sync, OSync)

    def test_started_source_with_explicit_port_printed(self, capsys):
        port = 49151
        sync = OSync(endpoint=Ep.source, port=port)
        sync.start()
        out, _ = capsys.readouterr()
        match = re.search('port {}'.format(port), out, re.IGNORECASE)
        assert match, (
            'Expected to see a port {} printed to STDOUT. '
            'Instead: {}').format(port, out)

    def test_started_source_with_random_port_printed(self, capsys):
        sync = OSync(endpoint=Ep.source, port=None)
        sync.start()
        out, _ = capsys.readouterr()
        match = re.search('port \d+', out, re.IGNORECASE)
        assert match, (
            'Expected to see a port number printed to STDOUT. '
            'Instead: {}').format(out)


class TestOSyncExceptionals:
    def test_exception_on_empty_endpoint(self):
        with raises(AssertionError):
            OSync(endpoint=None)

    def test_exception_on_invalid_endpoint(self):
        with raises(AssertionError):
            OSync(endpoint='invalid')

    def test_invalid_nonnumeric_port(self):
        with raises(AssertionError):
            OSync(endpoint=Ep.source, port='invalid')

    def test_unrecommended_port(self, recwarn):
        OSync(endpoint=Ep.source, port=1023)
        w = recwarn.pop(RuntimeWarning)
        assert issubclass(w.category, RuntimeWarning)
