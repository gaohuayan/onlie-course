from rest_framework.throttling import SimpleRateThrottle

class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'
    def get_cache_key(self, request, view):
        mobile = request.data.get('mobile') or request.query_params.get('mobile')
        if not mobile:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': mobile
        }