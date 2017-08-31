# Examples

## API Description Formats

### API Blueprint Example

This shows an example of the parse results of an API Blueprint. Here is a very minimal example API Blueprint.

```markdown
# My API
## Foo [/foo]
```

When this document is parsed, it returns a serialization of API Elements that looks like the following.

```json
{
  "element": "parseResult",
  "content": [
    {
      "element": "category",
      "meta": {
        "classes": {
          "element": "array",
          "content": [
            {
              "element": "string",
              "content": "api"
            }
          ]
        },
        "title": {
          "element": "string",
          "content": "My API"
        }
      },
      "content": [
        {
          "element": "category",
          "meta": {
            "classes": {
              "element": "array",
              "content": [
                {
                  "element": "string",
                  "content": "resourceGroup"
                }
              ]
            },
            "title": {
              "element": "string",
              "content": ""
            }
          },
          "content": [
            {
              "element": "resource",
              "meta": {
                "title": {
                  "element": "string",
                  "content": "Foo"
                }
              },
              "attributes": {
                "href": {
                  "element": "string",
                  "content": "/foo"
                }
              },
              "content": []
            }
          ]
        }
      ]
    }
  ]
}
```

### Swagger / OpenAPI Format Example

This shows an example of the parse results of a Swagger document.

```json
{
  "swagger": "2.0",
  "info": {
    "title": "My API",
    "version": "1.0.0"
  },
  "paths": {
    "/foo": {}
  }
}
```

When this document is parsed, it returns a serialization of API Elements that looks like:

```json
{
  "element": "parseResult",
  "content": [
    {
      "element": "category",
      "meta": {
        "classes": {
          "element": "array",
          "content": [
            {
              "element": "string",
              "content": "api"
            }
          ]
        },
        "title": {
          "element": "string",
          "content": "My API"
        }
      },
      "content": [
        {
          "element": "resource",
          "attributes": {
            "href": {
              "element": "string",
              "content": "/foo"
            }
          },
          "content": []
        }
      ]
    }
  ]
}
```

As you can see, Swagger and API Blueprint both convey the same information resulting in almost the same parse results. This shows the importance of querying the results rather than looking for specific paths in the document.

## Data Structure

This section shows what individual and specific data structures look like when converted to API Elements. In the context of an API description or parse results, these structures will be nested within the document.

If you have an [MSON][] definition like the one below.

```markdown
# My List (array)
- 1 (number)
- 2 (number)
- 3 (number)
```

When the structure is parsed, it returns a serialization of API Elements that looks like:

```json
{
  "element": "array",
  "meta": {
    "id": {
      "element": "string",
      "content": "My List"
    }
  },
  "content": [
    {
      "element": "number",
      "content": 1
    },
    {
      "element": "number",
      "content": 2
    },
    {
      "element": "number",
      "content": 3
    }
  ]
}
```

And when it is converted to JSON, it looks like:

```json
[1, 2, 3]
```

[MSON]: https://github.com/apiaryio/mson
