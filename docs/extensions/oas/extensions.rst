OpenAPI Specification Extensions
================================

This document is a profile for storing OpenAPI Specification Extensions within
an API Element extension.

The contents of an extension element with this profile will contain the
contents of the extensions is an object containing any vendor extensions found in
the underlying Swagger Description document.

For example, if a vendor extension with the key ``x-sts`` with a value true was
found in an OpenAPI document, it may be represented using the following
extension element::

    {
        "element": "extension",
        "meta": {
            "links": [
                {
                    "element": "link",
                    "attributes": {
                      "relation": "profile",
                      "href": "https://apielements.org/extensions/oas/extensions/"
                    }
                }
            ]
        },
        "content": {
            "element": "object",
            "content": [
                {
                    "element": "member",
                    "content": {
                        "key": {
                            "element": "string",
                            "content": "sts"
                        },
                        "value": {
                            "element": "boolean",
                            "content": true
                        }
                    }
                }
            ]
        }
    }
