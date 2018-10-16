# Migration Guide

This guide documents all of the changes between API Elements 0.6 and API
Elements 1.0.

## JSON Serialisation

In prior versions of API Elements, an Element (i.e. a type) could be
occasionally serialized as a [value](/element-definitions.html#values). This
behaviour has since been dropped, so that Elements are always serialized in
full form (i.e. as a type, not as a value). For example:

```json
{
  "element": "null",
  "meta": {
    "title": "empty"
  }
}
```

Elements must always be serialised as an element, for example the following
would be valid in API Elements 1.0:

```json
{
  "element": "null",
  "meta": {
    "title": {
      "element": "string",
      "content": "empty"
    }
  }
}
```

In previous versions of API Elements, both forms were valid so this is not a
breaking change. However, we found multiple implementations that were fragile
and could break when different forms were used.

## Changes to Elements

### Category Element

The `meta` attribute has been renamed to `metadata` in a [Category
Element](/element-definitions.html#category) for
clarity.

Before

```json
{
  "element": "category",
  "attributes": {
    "meta": {
      "element": "array",
      "content": [
        {
          "element": "member",
          "content": {
            "key": {
              "element": "string",
              "content": "HOST"
            },
            "value": {
              "element": "string",
              "content": "http://polls.apiblueprint.org/"
            }
          }
        }
      ]
    }
  }
}
```

After

```json
{
  "element": "category",
  "attributes": {
    "metadata": {
      "element": "array",
      "content": [
        {
          "element": "member",
          "content": {
            "key": {
              "element": "string",
              "content": "HOST"
            },
            "value": {
              "element": "string",
              "content": "http://polls.apiblueprint.org/"
            }
          }
        }
      ]
    }
  }
}
```

### Source Map Element

A [Source Map Element](/element-definitions.html#source-map) may contain an
optional line and column number to make it easier to handle source map
information. Computing the line and column number can often be expensive so it
may be provided by a parser. Note however that it is optional and it is down
the each individual tooling on whether it is present, some tools only provide
line and column number for source maps contained within Annotation Elements.

```json
{
  "element": "sourceMap",
  "content": [
    {
      "element": "array",
      "content": [
        {
          "element": "number",
          "attributes": {
            "line": {
              "element": "number",
              "content": 3
            },
            "column": {
              "element": "number",
              "content": 2
            }
          },
          "content": 4
        },
        {
          "element": "number",
          "attributes": {
            "line": {
              "element": "number",
              "content": 3
            },
            "column": {
              "element": "number",
              "content": 10
            }
          },
          "content": 12
        }
      ]
    }
  ]
}
```

### Data Structure Elements

#### Enumeration Element

The layout of the [Enum Element](/element-definitions.html#enum-element) has
been altered. The enumerations have been moved to an enumerations attribute of
the element and the content now represents the given value.

Enumerations themselves are an array of the possible enumerations.

Before

```json
{
  "element": "enum",
  "content": [
    {
      "element": "string",
      "content": "north"
    },
    {
      "element": "string",
      "content": "east"
    },
    {
      "element": "string",
      "content": "south"
    },
    {
      "element": "string",
      "content": "west"
    }
  ]
}
```

After

```json
{
  "element": "enum",
  "attributes": {
    "enumerations": {
      "element": "array",
      "content": [
        {
          "element": "string",
          "content": "north"
        },
        {
          "element": "string",
          "content": "east"
        },
        {
          "element": "string",
          "content": "south"
        },
        {
          "element": "string",
          "content": "west"
        }
      ]
    }
  }
}
```

The intent of the structure was that it represents an enumeration of `north`,
`east`, `south` and `west`. As the enumerations do not include a `fixed` type
attribute it represents an enumeration where any string is valid and not just
the fixed values. This created a limitation that tooling cannot determine the
difference between one of the fixed element enumerations, or a type with a
value. Thus, when the values are fixed they will now include a `fixed` type
attribute as follows:

```json
{
  "element": "enum",
  "attributes": {
    "enumerations": {
      "element": "array",
      "content": [
        {
          "element": "string",
          "attributes": {
            "typeAttributes": {
              "element": "array",
              "content": [
                {
                  "element": "string",
                  "content": "fixed"
                }
              ]
            }
          },
          "content": "north"
        },
        {
          "element": "string",
          "attributes": {
            "typeAttributes": {
              "element": "array",
              "content": [
                {
                  "element": "string",
                  "content": "fixed"
                }
              ]
            }
          },
          "content": "east"
        },
        {
          "element": "string",
          "attributes": {
            "typeAttributes": {
              "element": "array",
              "content": [
                {
                  "element": "string",
                  "content": "fixed"
                }
              ]
            }
          },
          "content": "south"
        },
        {
          "element": "string",
          "attributes": {
            "typeAttributes": {
              "element": "array",
              "content": [
                {
                  "element": "string",
                  "content": "fixed"
                }
              ]
            }
          },
          "content": "west"
        }
      ]
    }
  }
}
```
