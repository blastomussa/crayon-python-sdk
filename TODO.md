# Things needed to release final package to PyPI before leaving Crayon

1. Transition to returning response object 
    a. Change REST Methods from returning json to returning requests.response() object 
    b. Update README  with info about response object 
    c. Update Examples to use response.json()