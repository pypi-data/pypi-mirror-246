import logging
import re
import time
import requests


"""
The Refresh header is a non-standard header extension introduced by Netscape.
It is mentioned by WHATWG in the HTML spec as being equivalent to the <mata refresh> tag.
https://html.spec.whatwg.org/multipage/semantics.html#conformance-attr-meta-http-equiv-refresh <- Refresh header
https://html.spec.whatwg.org/multipage/document-lifecycle.html#refresh <- meta refresh tag



NOTE: WHATWG says that it should be url={url}, but we'll accept any key or simply the {url}.
NOTE: The seperator between the time and url can be a semicolon or a comma. This is because it seems like many browsers support either (although I'd love to test this).
"""

log = logging.getLogger(__name__)

def hook(r: requests.Response, *args, **kwargs) -> requests.Response:
    """
    Process the Refresh header in the HTTP response and perform the necessary actions.

    Args:
        r (requests.Response): The HTTP response object.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        requests.Response: The modified HTTP response object.

    Raises:
        None

    """
    # Parse the Refresh header, if it exists.
    if 'Refresh' in r.headers:
        log.debug('Refresh header found in response. Processing...')
        refresh_header = r.headers['Refresh']

        # The refresh header value must be:
        # a non-negative integer
        # or a non-negative integer followed by a delimiter and a url
        refresh_time = None
        refresh_url = None

        # non-negative integer:
        if refresh_header.isdigit():
            # Extract the refresh time as an integer.
            refresh_time = int(refresh_header)
            
            # If the refresh time is negative, it is invalid.
            if refresh_time < 0:
                # Invalid header, perform no action.
                return r
            
            # In the case only the refresh time is specified, the url is the same as the current url.
            refresh_url = r.url
        else:
            # non-negative integer followed by a delimiter and a url:
            regex = re.compile(r'(\d+)([,;])(.*)')
            match = regex.match(refresh_header)
            if match:
                # Extract the refresh time as an integer.
                refresh_time = int(match.group(1))
                
                # If the refresh time is negative, it is invalid.
                if refresh_time < 0:
                    # Invalid header, perform no action.
                    return r
                
                # Extract the url.
                refresh_url = match.group(3)

        # If the refresh time or url is None, the header is invalid.
        if refresh_time is None or refresh_url is None:
            # Invalid header, perform no action.
            return r
        
        # Log the refresh time and url.
        log.debug('URL: %s, Refresh time: %s' % (refresh_url, refresh_time))

        # Wait for the refresh time.
        time.sleep(refresh_time)

        # Ensure cookies are preserved.
        kwargs['cookies'] = r.cookies

        # Make a request to the refresh url.
        return requests.get(refresh_url, *args, **kwargs)
    else:
        return r
    