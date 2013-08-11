#----------------------------------------------------------------------
# Copyright (c) 2011-2013 Raytheon BBN Technologies
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and/or hardware specification (the "Work") to
# deal in the Work without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Work, and to permit persons to whom the Work
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Work.
#
# THE WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE WORK OR THE USE OR OTHER DEALINGS
# IN THE WORK.
#----------------------------------------------------------------------

import amsoil.core.log
import amsoil.core.pluginmanager as pm
from amsoil.core import serviceinterface
from DelegateBase import DelegateBase
from HandlerBase import HandlerBase
from Exceptions import *

ma_logger = amsoil.core.log.getLogger('mav1')
xmlrpc = pm.getService('xmlrpc')

# RPC handler for Member Authority (MA) API calls
class MAv1Handler(HandlerBase):
    def __init__(self):
        super(MAv1Handler, self).__init__(ma_logger)

    # This call is unprotected: no checking of credentials
    # Return version of MA API including object model
    def get_version(self):
        try:
            return self._delegate.get_version()
        except Exception as e:
            return self._errorReturn(e)

    # This call is unprotected: no checking of credentials
    # Return public information about members specified in options
    # filter and query fields
    def lookup_public_member_info(self, credentials, options):
        try:
            return self._delegate.lookup_public_member_info(credentials, options)
        except Exception as e:
            return self._errorReturn(e)

    # This call is protected
    # Return private information about members specified in options
    # filter and query fields
    # Authorized by client cert and credentials
    def lookup_private_member_info(self, credentials, options):
        client_cert = self.requestCertificate()
        method = 'lookup_private_member_info'
        try:
            self._guard.validate_call(client_cert, method, \
                                          credentials, options)
            results = self._delegate.lookup_private_member_info(client_cert, \
                                                                    credentials, \
                                                                    options)

            if results['code'] == NO_ERROR:
                results_value = results['value']
                new_results_value = self._guard.protect_results(client_cert, method, credentials, results_value)
                results = self._successReturn(new_results_value)

            return results

        except Exception as e:
            return self._errorReturn(e)

    # This call is protected
    # Return identifying information about members specified in options
    # filter and query fields
    # Authorized by client cert and credentials
    def lookup_identifying_member_info(self, credentials, options):
        client_cert = self.requestCertificate()
        method = 'lookup_identifying_member_info'
        try:
            self._guard.validate_call(client_cert, method, \
                                          credentials, options)
            results = self._delegate.lookup_identifying_member_info(client_cert, \
                                                                        credentials, \
                                                                        options)
            if results['code'] == NO_ERROR:
                results_value = results['value']
                new_results_value = self._guard.protect_results(client_cert, method, credentials, results_value)
                results = self._successReturn(new_results_value)

            return results

        except Exception as e:
            return self._errorReturn(e)

    # This call is protected
    # Update given member with new data provided in options
    # Authorized by client cert and credentials
    def update_member_info(self, member_urn, credentials, options):
        client_cert = self.requestCertificate()
        method = 'update_member_info'
        try:
            self._guard.validate_call(client_cert, method,
                                          credentials, options, \
                                          {'member_urn' : member_urn})
            results = self._delegate.update_member_info(client_cert, member_urn, \
                                                            credentials, options)
            if results['code'] == NO_ERROR:
                results_value = results['value']
                new_results_value = self._guard.protect_results(client_cert, method, credentials, results_value)
                results = self._successReturn(new_results_value)

            return results
        except Exception as e:
            return self._errorReturn(e)


# Base class for implementations of MA API
# Must be  implemented in a derived class, and that derived class
# must call setDelegate on the handler
class MAv1DelegateBase(DelegateBase):

    def __init__(self):
        super(MAv1DelegateBase, self).__init__(ma_logger)
    
    # This call is unprotected: no checking of credentials
    def get_version(self):
        raise CHAPIv1NotImplementedError('')

    # This call is unprotected: no checking of credentials
    def lookup_public_member_info(self, credentials, options):
        print "MAv1DelegateBase.lookup_public_member_info " + \
            "CREDS = %s OPTIONS = %s" % \
            (str(credentials), str(options))
        raise CHAPIv1NotImplementedError('')

    # This call is protected
    def lookup_private_member_info(self, client_cert, credentials, options):
        raise CHAPIv1NotImplementedError('')

    # This call is protected
    def lookup_identifying_member_info(self, client_cert, credentials, options):
        raise CHAPIv1NotImplementedError('')

    # This call is protected
    def update_member_info(self, client_cert, member_urn, credentials, options):
        raise CHAPIv1NotImplementedError('')



