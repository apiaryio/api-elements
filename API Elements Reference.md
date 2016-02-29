# API Elements Reference

**Version**: 1.0.0-rc1

<!--
  The TOC Atom lib doesn't like Markdown headings, so you have to remove items
  that are pulled from API Blueprint examples on accident.
-->

- [API Elements Reference](#api-elements-reference)
  - [About this Document](#about-this-document)
  - [Relationship of Elements](#relationship-of-elements)
  - [I. Base API Element Definition](#i-base-api-element-definition)
    - [Base API Element (object)](#base-api-element-object)
  - [II. Core API Elements](#ii-core-api-elements)
    - [Href (string)](#href-string)
    - [Templated Href (string)](#templated-href-string)
    - [Href Variables (Object Type)](#href-variables-object-type)
    - [Data Structure (Base API Element)](#data-structure-base-api-element)
    - [Asset (Base API Element)](#asset-base-api-element)
    - [Resource (Base API Element)](#resource-base-api-element)
    - [Transition (Base API Element)](#transition-base-api-element)
    - [Category (Base API Element)](#category-base-api-element)
    - [Copy (Base API Element)](#copy-base-api-element)
    - [Protocol-specific Elements](#protocol-specific-elements)
  - [III. Data Structure Elements](#iii-data-structure-elements)
    - [Inheritance and Expanded Element](#inheritance-and-expanded-element)
    - [Base Data Structure Element](#base-data-structure-element)
    - [Data Structure Element (Base API Element)](#data-structure-element-base-api-element)
    - [Type Reference (Ref Element)](#type-reference-ref-element)
    - [Boolean Type (Boolean Element)](#boolean-type-boolean-element)
    - [String Type (String Element)](#string-type-string-element)
    - [Number Type (Number Element)](#number-type-number-element)
    - [Array Type (Array Element)](#array-type-array-element)
    - [Object Type (Object Element)](#object-type-object-element)
    - [Enum Type (Data Structure Element)](#enum-type-data-structure-element)
    - [Examples](#examples)
  - [III. Parse Result Elements](#iii-parse-result-elements)
    - [Parse Result (Base API Element)](#parse-result-base-api-element)
    - [Annotation (Base API Element)](#annotation-base-api-element)
    - [Source Map (Base API Element)](#source-map-base-api-element)
    - [Link Relations](#link-relations)
  - [IV. Refract Elements](#iv-refract-elements)

## About this Document

This document conforms to [RFC 2119][], which says:

> The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

[MSON][] is used throughout this document.

## Relationship of Elements

One purpose of the API Elements reference is to allow consumers to decouple their implementations from the structure of the document. Because of this, when consuming documents of API Elements, it is recommended to write code that queries the tree rather than looking for defined paths.

It is also helpful to know the relationship between elements. The list below shows the relationship between the elements in this reference, but does not specify how the structure must be built.

- Category (API)
  - Copy
  - Data Structure
  - Category (Group of Resource Elements)
  - Resource
    - Copy
    - Data Structure
    - Category (Group of Transition Elements)
    - Transition
      - Copy
      - Transaction
        - Copy
        - HTTP Request
          - Asset
        - HTTP Response
          - Asset

This main API Category element MAY also be wrapped in a Parse Result element for conveying parsing information, such as source maps, warnings, and errors.

## I. Base API Element Definition

### Base API Element (object)

The Refract Element contains four properties: `element`, `meta`, `attributes`, and `content`, as defined below. This Element MAY be used recursively throughout the document, even as a value for each of its own meta or attributes.

#### Properties

- `element` (string, required)

    The `element` property defines the name of element. It MUST be a string that references an element, which SHOULD be defined.

- `meta` (enum)

    The `meta` property is a reserved object for Refract-specific values. When `meta` is an object, it MAY contain elements itself. The element definition SHOULD be used when interacting with `meta` and its properties and values.

    - Members
        - (object)
            - `id` - Unique Identifier, MUST be unique throughout the document
            - `ref` (Element Pointer) - Pointer to referenced element or type
            - `classes` (array[string]) - Array of classifications for given element
            - `title` (string) - Human-readable title of element
            - `description` (string) - Human-readable description of element
            - `links` (array[Link Element]) - Meta links for a given element
        - (array[Member Element])

- `attributes` (enum)

    The `attributes` property defines attributes about the given instance of the element, as specified by the `element` property. When `attributes` is an object, it MAY contain elements itself. The element definition SHOULD be used when interacting with `attributes` and its properties and values.

    The `attributes` are used later in this document for representing data structures.

    - Members
        - (object)
        - (array[Member Element])

- `content` (enum)

    The `content` property defines the content of the instance of the specified element. The value MAY be any of the Refract primitive types.

    - Members
        - (null)
        - (string)
        - (number)
        - (boolean)
        - (array)
        - (object)
        - (Base API Element)

#### Example

An element MAY look like this, where `foo` is the element name, `id` is a meta attribute for the `foo` element, and `content` is a string with a value of `bar`. Here, the `id` is `baz` and MAY be used for referencing.

```json
{
  "element": "foo",
  "meta": {
    "id": "baz"
  },
  "content": "bar"
}
```

## II. Core API Elements

### Href (string)

The value of the `Href` type  SHOULD be resolved as a URI-Reference per [RFC 3986][] and MAY be a relative reference to a URI.
The value of the `Href` type MUST NOT be a URI Template.

### Templated Href (string)

The value of `Templated Href` type is to be used as a URI Template, as defined in [RFC 6570][].
The value of the `Templated Href` type is a template used to determine the target URI of the related resource or transition.
The value of the `Templated Href` type SHOULD be resolved as a URI-Reference per [RFC 3986][] and MAY be a relative reference to a URI.

### Href Variables (Object Type)

The definition is a Data Structure element `Object Type` where keys are respective URI Template variables.

#### Properties

- `element`: hrefVariables (string, fixed)

### Data Structure (Base API Element)

Data structure definition using Data Structure elements.

#### Properties

- `element`: dataStructure (string, fixed)
- `content` (Data Structure Element)

### Asset (Base API Element)

Arbitrary data asset.

#### Properties

- `element`: asset (string, fixed)
- `meta`
    - `classes` (array, fixed)
        - (enum[string])
            - messageBody - Asset is an example of message-body
            - messageBodySchema - Asset is an schema for message-body
- `attributes` (object)
    - `contentType` (string) - Optional media type of the asset. When this is unset, the content type SHOULD be inherited from the `Content-Type` header of a parent HTTP Message Payload
    - `href` (Href) - Link to the asset
- `content` (string) - A textual representation of the asset

### Resource (Base API Element)

The Resource representation with its available transitions and its data.

#### Properties

- `element`: resource (string, fixed)
- `attributes` (object)
    - `href` (Templated Href) - URI Template of this resource.
    - `hrefVariables` (Href Variables) - Definition of URI Template variables used in the `href` property.
- `content` (array)
    - (Copy) - Resource description's copy text.
    - (Category) - A group of Transition elements
    - (Transition) - State transition available for this resource.

        The `content` MAY include multiple `Transition` elements.

    - (Data Structure) - Data structure representing the resource.

        The `content` MUST NOT include more than one `Data Structure`.

#### Example

```json
{
    "element": "resource",
    "meta": {
        "title": "Question",
        "description": "A Question object has the following attributes."
    },
    "attributes": {
        "href": "/questions/{question_id}",
        "hrefVariables": {
            "element": "hrefVariables",
            "content": [
                {
                    "element": "member",
                    "content": {
                        "key": {
                            "element": "string",
                            "content": "question_id"
                        }
                    }
                }
            ]
        }
    },
    "content": [
        {
            "element": "dataStructure"
        }
    ]
}
```

### Transition (Base API Element)

A transition is an available progression from one state to another state.
Exercising a transition initiates a transaction.

The content of this element is array of protocol-specific transactions.

Note: At the moment only the HTTP protocol is supported.

#### Properties

- `element`: transition (string, fixed)
- `attributes` (object)
    - `relation` - (string) - Link relation type as specified in [RFC 5988][].

        The value of `relation` attribute SHOULD be interpreted as a link relation
        between transition's parent resource and the transition's target resource
        as specified in the `href` attribute.

    - `href` (Templated Href) - The URI template for this transition.

        If present, the value of the `href` attribute SHOULD be used to resolve
        the target URI of the transition.

        If not set, the parent `resource` element `href` attribute SHOULD be
        used to resolve the target URI of the transition.

    - `hrefVariables` (Href Variables) - Input parameters.

        Definition of any input URI path segments or URI query parameters for this transition.

        If `href` and `hrefVariables` attributes aren't set, the parent `resource`
        element `hrefVariables` SHOULD be used to resolve the transition input
        parameters.

    - `data` (Data Structure) - Input attributes.

        Definition of any input message-body attribute for this transition.

    - `contentTypes` (array[String]) - A collection of content types that MAY be used for the transition.
- `content` (array)
    - (Copy) - Transition description's copy text.
    - (HTTP Transaction) - An instance of transaction example.

        Transaction examples are protocol-specific examples of a REST transaction
        that was initialized by exercising a transition.

        For the time being this reference document defines only HTTP-specific transaction
        data structures.

#### Example

```json
{
    "element": "transition",
    "attributes": {
        "relation": "update",
        "href": "https://polls.apiblueprint.org/questions/{question_id}"
    },
    "content": []
}
```

### Category (Base API Element)

Grouping element – a set of elements forming a logical unit of an API such as
group of related resources or data structures.

A category element MAY include additional classification of the category.
The classification MAY hint what is the content or semantics of the category.
The classification MAY be extended and MAY contain more than one classes.

For example a `category` element may be classified both as `resourceGroup` and
`dataStructures` to denote it includes both resource and data structures. It
may also include the `transitions` classification to denote it includes
transitions.

#### Properties

- `element`: category (string, fixed)
- `meta`
    - `classes` (array, fixed)
        - (enum[string])
            - api - Category is a API top-level group.
            - resourceGroup - Category is a set of resource.
            - dataStructures - Category is a set of data structures.
            - scenario - Category is set of steps.
            - transitions - Category is a group of transitions.
- `attributes`
    - `meta` (array[Member Element]) - Arbitrary metadata

        Note the "classes" of the Member Element can be used to distinguish the
        source of metadata as follows:

        - Class `user` - User-specific metadata. Metadata written in the source.
        - Class `adapter` - Serialization-specific metadata. Metadata provided by adapter.

- `content` (array[Base API Element])

#### Example

```json
{
    "element": "category",
    "meta": {
        "classes": [
            "api"
        ],
        "title": "Polls API"
    },
    "attributes": {
        "meta": [
            {
              "element": "member",
              "meta": {
                  "classes": ["user"]
              },
              "content": {
                  "key": {
                      "element": "string",
                      "content": "HOST",
                  },
                  "value": {
                      "element": "string",
                      "content": "http://polls.apiblueprint.org/"
                  }
              }
            }
        ]
    },
    "content": [
        {
            "element": "category",
            "meta": {
                "classes": [
                    "resourceGroup"
                ],
                "title": "Question"
            },
            "content": [
                {
                    "element": "copy",
                    "content": "Resources related to questions in the API."
                }
            ]
        }
    ]
}
```

### Copy (Base API Element)

Copy element represents a copy text—a textual information in API description.
Its content is a string and it MAY include information about the media type
of the copy's content.

Unless specified otherwise, a copy element's content represents the
description of its parent element and SHOULD be used instead of parent
element's description metadata.

#### Properties

- `element`: copy (string, fixed)
- `attributes` (object)
    - `contentType`: *text/plain* (string) - Optional media type of the content.
- `content` (string)

#### Example

Given an API description with following layout:

- Group
    - Copy "Lorem Ipsum"
    - Resource "A"
    - Resource "B"
    - Copy "Dolor Sit Amet"

```json
{
    "element": "category",
    "content": [
        {
            "element": "copy",
            "content": "Lorem Ipsum"
        },
        {
            "element": "resource"
        },
        {
            "element": "resource"
        },
        {
            "element": "copy",
            "content": "Dolor Sit Amet"
        }
    ]
}
```

### Protocol-specific Elements

#### HTTP Transaction (Base API Element)

Example of an HTTP Transaction. The example's content consist of a request-response
message pair. A transaction example MUST contain exactly one HTTP request and one HTTP response message.

##### Properties

- `element`: httpTransaction (string, fixed)
- `content` (array) - Request and response message pair (tuple).
    - (Copy) - HTTP Transaction description's copy text.
    - (HTTP Request Message)

        The `content` MUST include exactly one `HTTP Request Message` element.

    - (HTTP Response Message)

        The `content` MUST include exactly one `HTTP Response Message` element.

##### Example

```json
{
    "element": "httpTransaction",
    "content": [
        {
            "element": "httpRequest",
            "attributes": {
                "method": "GET",
                "href": "/questions/{question_id}",
                "hrefVariables": {
                    "element": "hrefVariables",
                    "content": [
                        {
                            "element": "member",
                            "content": {
                                "key": {
                                    "element": "string",
                                    "content": "question_id"
                                }
                            }
                        }
                    ]
                }
            },
            "content": []
        },
        {
            "element": "httpResponse",
            "attributes": {
                "statusCode": 200
            },
            "content": [
                {
                    "element": "asset",
                    "meta": {
                        "classes": ["messageBody"]
                    },
                    "attributes": {
                      "contentType": "application/json"
                    },
                    "content": "{\"name\": \"John\"}"
                }
            ]
        }
    ]
}
```

#### HTTP Headers (Array Type)

Ordered array of HTTP header-fields.

##### Properties

- `element`: `httpHeaders`
- `content` (array[Member Element])

##### Example

```json
{
    "element": "httpHeaders",
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "Content-Type"
                },
                "value": {
                    "element": "string",
                    "content": "application/json"
                }
            }
        }
    ]
}
```

#### HTTP Message Payload (Base API Element)

Payload of an HTTP message including headers, data structures, or assets.

##### Properties

- `attributes`
    - `headers` (HTTP Headers)
- `content` (array)
    - (Copy) - Payload description's copy text.
    - (Data Structure) - Data structure describing the payload.

        The `content` MUST NOT contain more than one `Data Structure`.

    - (Asset) - A data asset associated with the payload's body.

        This asset MAY represent payload body or body's schema.

        The `content` SHOULD NOT contain more than one asset of its respective type.

#### HTTP Request Message (HTTP Message Payload)

HTTP request message.

##### Properties

- `element`: httpRequest (string, fixed)
- `attributes`
    - `method` (string) - HTTP request method. The method value SHOULD be inherited from a parent transition if it is unset.
    - `href` (Templated Href) - URI Template for this HTTP request.

        If present, the value of the `href` attribute SHOULD be used to resolve
        the target URI of the http request.

        If not set, the `href` attribute which was used to resolve the target
        URI of the parent transition SHOULD be used to resolve the URI of
        the http request.

    - `hrefVariables` (Href Variables) - Input parameters

        Definition of any input URI path segments or URI query parameters for this transition.

        If `href` and `hrefVariables` attributes aren't set, the `hrefVariables` attribute
        which was used to resolve the input parameters of the parent transition SHOULD
        be used to resolve the http request input parameters.


#### HTTP Response Message (HTTP Message Payload)

HTTP response message.

##### Properties

- `element`: httpResponse (string, fixed)
- `attributes`
    - `statusCode` (number) - HTTP response status code.

## III. Data Structure Elements

### Inheritance and Expanded Element

This reference document is built around the idea of defining recursive data structures. To provide abstraction, for convenience reasons and to not repeat ourselves, these structures can be named (using an _identifier_) and reused. In this reference document, the reusable data structures are called _Named Types_.

By default, Refract does not enforce inheritance of data, though element definitions are inherited from the defined element types. To inherit data in Refract, the `extend` element is used to merge one or more elements into a final element. In the Data Structure elements, however, when the data is defined, it inherits data from the element definition. Data Structure itself uses inheritance this way, and the Data Structure Refract elements mimics the behavior to provide simplicity and consistency across Data Structure representations.

Often, before an Data Structure Refract can be processed, referenced _Named Types_ have to be resolved. Resolving references to _Named Types_ is tedious and error prone. As such an Data Structure processor can resolve references to produce a complete Data Structure Refract. That is, a Refract that does not include unresolved references to other data structures. This is referred to as _reference expansion_ or simply _expansion_.

In other words, an expanded element is one that does not contain any _Identifier_ (defined below) referencing any other elements than those defined in Data Structure elements.

The expanded Refract MUST, however, keep the track of what data structure was expanded and what from where and it MUST preserve the order of any member elements.

#### Example

Extending the element "A" to form new element "B":

```json
{
  "element": "extend",
  "meta": {
    "id": "B"
  },
  "content": [
    {
      "element": "string",
      "meta": {
        "id": "A"
      },
      "content": "base element content"
    },
    {
      "element": "string",
      "content": "derived content"
    }
  ]
}
```

Because of the implicit inheritance in the Data Structure elements, the
example above can be written as follows:

```json
{
  "element": "string",
  "meta": {
    "id": "A"
  },
  "content": "base element content"
}
```

```json
{
  "element": "A",
  "meta": {
    "id": "B"
  },
  "content": "derived content"
}
```

Resolving the Data Structure elements implicit inheritance and expanding
the references from the example above we get:

```json
{
  "element": "extend",
  "meta": {
    "id": "B"
  },
  "content": [
    {
      "element": "string",
      "meta": {
        "ref": "A"
      },
      "content": "base element content"
    },
    {
      "element": "string",
      "content": "derived content"
    }
  ]
}
```

### Base Data Structure Element

In this reference document, every data structure is a sub-type of another data structure, and, therefore, it is directly or indirectly derived from one of the Data Structure _Base Types_. This is expressed as an inheritance of elements in Data Structure Refract, where the predecessor of an element is referred to as element's _Base Element_.

Note: Not every Data Structure _Base Type_ is presented in Refract primitive types and vice versa – see the table below.

#### Type comparison

| JSON primitive |      Refract     | [MSON][] Base Type | Data Structure Elements |
|:--------------:|:----------------:|:------------------:|:------------------------:|
|     boolean    |  Boolean Element |     boolean    |  Boolean Type  |
|     string     |  String Element  |     string     |   String Type  |
|     number     |  Number Element  |     number     |   Number Type  |
|      array     |   Array Element  |      array     |   Array Type   |
|        -       |         -        |      enum      |    Enum Type   |
|     object     |  Object Element  |     object     |   Object Type  |
|      null      |   Null Element   |        -       |        -       |

### Data Structure Element (Base API Element)

Base element for every Data Structure element.

The Data Structure Element adds attributes representing Data Structure _Type Definition_ and _Type Sections_.

Note: In Data Structure Refract _Nested Member Types_ _Type Section_ is the `content` of the element.

#### Properties

- `attributes`
    - `typeAttributes` (array) - _Type Definition_ attributes list, see _Type Attribute_  

      Type attributes of a type definition.

      Note, if `sample` (or `default`) attribute is specified the value SHOULD be stored in the `samples` (or `default`) property instead of the element's `content`.

      - Items
          - (enum[string])
              - required - This element is required in parent's content
              - optional - This element is optional in parent's content
              - fixed - The `content` value is immutable.

    - `variable` (boolean)

      The `content` value is either a _Variable Type Name_, or _Variable Property Name_.

      Note, if the `content` is a _Variable Value_ the `sample` type attribute
      should be used instead (see `typeAttributes`).

    - `samples` (array) - Array of alternative sample values for _Member Types_

          The type of items in `samples` array attribute MUST match the type of element's `content`.

    - `default` - Default value for _Member Types_

          The type of of `default` attribute MUST match the type of element's `content`.

    - `validation` - Not used, reserved for a future use

### Type Reference (Ref Element)

This elements extends refract `Ref Element` to include optional referenced element.

#### Properties

- `element` ref (string, fixed)
- `attributes`
    -  `resolved` (Element, optional) - Resolved element being referenced.

### Boolean Type (Boolean Element)

- Include [Data Structure Element][]

### String Type (String Element)

- Include [Data Structure Element][]

### Number Type (Number Element)

- Include [Data Structure Element][]

### Array Type (Array Element)

- Include [Data Structure Element][]

### Object Type (Object Element)

- Include [Data Structure Element][]

### Enum Type (Data Structure Element)

Enumeration type. Exclusive list of possible elements. The elements in content's array MUST be interpreted as mutually exclusive.

#### Properties

- `element`: enum (string, fixed)
- `content` (array[[Data Structure Element][]])

#### Examples

##### MSON

```
- tag (enum[string])
    - red
    - green
```

##### Data Structure Refract

```json
{
    "element": "object",
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "tag"
                },
                "value": {
                    "element": "enum",
                    "content": [
                        {
                            "element": "string",
                            "content": "red"
                        },
                        {
                            "element": "string",
                            "content": "green"
                        }
                    ]
                }
            }
        }
    ]
}
```

### Examples

#### Anonymous Object Type

##### MSON

```
- id: 42
```

##### Data Structure Refract

```json
{
    "element": "object",
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "id"
                },
                "value": {
                    "element": "string",
                    "content": "42"
                }
            }
        }
    ]
}
```

#### Type Attributes

##### MSON

```
- id: 42 (required, fixed)
```

##### Data Structure Refract

```json
{
    "element": "object",
    "content": [
        {
            "element": "member",
            "attributes": {
                "typeAttributes": [
                    "required",
                    "fixed"
                ]
            },
            "content": {
                "key": {
                    "element": "string",
                    "content": "id"
                },
                "value": {
                    "element": "string",
                    "content": "42"
                }
            }
        }
    ]
}
```

#### Default Value

##### MSON

```
- id (number)
    - default: 0
```

##### Data Structure Refract

```json
{
    "element": "object",
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "id"
                },
                "value": {
                    "element": "number",
                    "attributes": {
                        "default": 0
                    }
                }
            }
        }
    ]
}
```

#### One Of

##### MSON

```
- city
- One Of
    - state
    - province
```

##### Data Structure Refract

```json
{
    "element": "object",
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "city"
                }
            }
        },
        {
            "element": "select",
            "content": [
                {
                    "element": "option",
                    "content": [
                        {
                            "element": "member",
                            "content": {
                                "key": {
                                    "element": "string",
                                    "content": "state"
                                }
                            }
                        }
                    ]
                },
                {
                    "element": "option",
                    "content": [
                        {
                            "element": "member",
                            "content": {
                                "key": {
                                    "element": "string",
                                    "content": "province"
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

#### Mixin

##### MSON

```apib
# User (object)
- name: John
```

```apib
- id
- Include (User)
```

##### Data Structure Refract

Using the `ref` element to reference an the content of an element.

```json
{
    "element": "object",
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "id"
                }
            }
        },
        {
            "element": "ref",
            "content": {
                "href": "User",
                "path": "content"
            }
        }
    ]
}
```

Using "Type Reference" (`ref`) element with the `resolved` attribute:

```json
{
    "element": "object",
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "id"
                }
            }
        },
        {
            "element": "ref",
            "attributes": {
                "resolved": {
                    "element": "object",
                    "meta": {
                        "ref": "User"
                    },
                    "content": [
                        {
                            "element": "member",
                            "content": {
                                "key": {
                                    "element": "string",
                                    "content": "name"
                                },
                                "value": {
                                    "element": "string",
                                    "content": "John"
                                }
                            }
                        }
                    ]
                }
            },
            "content": {
                "href": "User",
                "path": "content"
            }
        }
    ]
}
```

#### Named Type

##### MSON

```
# Address (object)

Description is here! Properties to follow.

## Properties

- street
```

##### Data Structure Refract

```json
{
    "element": "object",
    "meta": {
        "id": "Address",
        "title": "Address",
        "description": "Description is here! Properties to follow."
    },
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "street"
                }
            }
        }
    ]
}
```

#### Referencing & Expansion

##### MSON

```markdown
# User (object)
- name

# Customer (User)
- id
```

##### Data Structure Refract

```json
{
    "element": "object",
    "meta": {
        "id": "User"
    },
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "name"
                }
            }
        }
    ]
}
```

```json
{
    "element": "User",
    "meta": {
        "id": "Customer"
    },
    "content": [
        {
            "element": "member",
            "content": {
                "key": {
                    "element": "string",
                    "content": "id"
                }
            }
        }
    ]
}
```

##### Expanded Data Structure Refract

```json
{
    "element": "extend",
    "meta": {
        "id": "Customer"
    },
    "content": [
        {
            "element": "object",
            "meta": {
                "ref": "User"
            },
            "content": [
                {
                    "element": "member",
                    "content": {
                        "key": {
                            "element": "string",
                            "content": "id"
                        }
                    }
                }
            ]
        },
        {
            "element": "object",
            "content": [
                {
                    "element": "member",
                    "content": {
                        "key": {
                            "element": "string",
                            "content": "id"
                        }
                    }
                }
            ]
        }
    ]
}
```

#### Variable Value

##### MSON

```markdown
- p: *42*
```

##### Data Structure Refract

```json
["object", {}, {}, [
  ["member", {}, {}, {
    "key": ["string", {}, {}, "p"],
    "value": ["string", {}, {"samples": [42]}, null]
  }]
]]
```

#### Variable Property Name

##### MSON

```markdown
- *rel (Relation)*
```

##### Data Structure Refract

```json
["object", {}, {}, [
  ["member", {}, {}, {
    "key": ["Relation", {}, {"variable": true}, "rel"],
    "value": ["string", {}, {}, null]
  }]
]]
```

#### Variable Type Name

**Proposal – not yet implemented**

Note this needs an introduction of a new Data Structure element for any type - `generic`.

##### MSON

```markdown
- p (array[*T*])
```

##### Data Structure Refract

```json
["object", {}, {}, [
  ["member", {}, {}, {
    "key": ["string", {}, {}, "p"],
    "value": ["array", {}, {}, [
        ["generic", {}, {}, "T"]
    ]]
  }]
]]
```
## III. Parse Result Elements

### Parse Result (Base API Element)

A result of parsing of an API description document.

#### Properties

- `element`: parseResult (string, fixed)
- `content` (array)
    - (Category)
    - (Annotation)

#### Example

Given following API Blueprint document:

```apib
# GET /1
```

The parse result is (using null in `category` content for simplicity):

```json
["parseResult", {}, {}, [
    ["category", {"classes": ["api"]}, {"sourceMap": [[0,9]]}, null],
    ["annotation", {"classes": ["warning"]}, { "code": 6, "sourceMap": [{ "element": "sourceMap", "content": [[0,9]] }] }, "action is missing a response"]
  ]
]
```

### Annotation (Base API Element)

Annotation for a source file. Usually generated by a parser or adapter.

#### Properties

- `element`: annotation (string, fixed)
- `meta`
  - `classes` (array, fixed)
      - (enum[string])
          - error - Annotation represents an error
          - warning - Annotation represents a warning

- `attributes`
    - `code` (number) - Parser-specific code of the annotation.
    Refer to parser documentation for explanation of the codes.

    - `sourceMap` (array[Source Map]) - Locations of the annotation in the source file.

- `content` (string) - Textual annotation.

    This is – in most cases – a human-readable message to be displayed to user.

#### Example

```json
{
  "element": "annotation",
  "meta": {
    "classes": ["warning"]
  },
  "attributes": {
    "code": 6,
    "sourceMap": [
      {
        "element": "sourceMap",
        "content": [[4, 12], [20, 12]]
      }
    ]
  },
  "content": "action is missing a response"
}
```

### Source Map (Base API Element)

Source map of an Element.

Every refract element MAY include a `sourceMap` attribute. Its content MUST
be an array of `Source Map` elements. The Source Map elements represent the
location(s) in source file(s) from which the element was composed.

If used, it represents the location of characters in the source file.
This location SHOULD include the characters used to build the parent element.

The Source Map element MUST NOT be used in its normal ("unrefracted") form
unless the particular application clearly implies what is the source file the
source map is pointing in.

A source map is a series of character-blocks. These
blocks may be non-continuous. For example, a block in the series may not start
immediately after the previous block. Each block, however, is a continuous
series of characters.

#### Properties

- `element`: sourceMap (string, fixed)
- `content` (array) - Array of character blocks.
    - (array, fixed) - Continuous characters block. A pair of character index and character count.
      - (number) - Zero-based index of a character in the source document.
      - (number) - Count of characters starting from the character index.

#### Example

```json
{
    "element": "...",
    "attributes": {
        "sourceMap": [
            {
                "element": "sourceMap",
                "content": [[4, 12], [20, 12]]
            }
        ]
    }
}
```

This reads, "The location starts at the 5th character of the source file. It
includes the 12 subsequent characters including the starting one. Then it
continues at the 21st character for another 12 characters."

### Link Relations

In addition to conforming to [RFC 5988][] for link relations per the [base specification](https://github.com/refractproject/refract-spec/blob/master/refract-spec.md), there are also additional link relations
available for parse results.

#### Origin Link Relation

The `origin` link relation defines the origin of a given element. This link can
point to specific tooling that was used to parse or generate a given element.

#### Inferred Link Relation

The `inferred` link relation gives a hint to whether or not an element was
inferred or whether it was found in the originating document. The presence of
the `inferred` link tells the user that the element was created based on some
varying assumptions, and the URL to which the link points MAY provide an
explanation on how and why it was inferred.

## IV. Refract Elements

These elements and definitions are referenced as part of the base Refract specification for the purpose of identifying, referencing, and pointing to elements and their respective meta, attributes, or content.

* [String Element][]
* [Number Element][]
* [Boolean Element][]
* [Array Element][]
* [Object Element][]
* [Ref Element][]
* [Element Pointer][]
* [Link Element][]

---


[MSON]: https://github.com/apiaryio/mson
[MSON Reference]: https://github.com/apiaryio/mson/blob/master/MSON%20Reference.md
[Refract]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md

[API Description Elements]: definitions/api-description-elements.md
[Data Structure Elements]: definitions/data-structure-elements.md
[Parse Result Elements]: definitions/parse-result-elements.md

[Data Structure Element]: #data-structure-element-element

[String Element]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#string-element-element
[Number Element]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#number-element-element
[Boolean Element]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#boolean-element-element
[Array Element]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#array-element-element
[Object Element]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#object-element-element
[Ref Element]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#ref-element-element
[Element Pointer]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#element-pointer-enum
[Link Element]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md#link-element-element

[RFC 2119]: https://datatracker.ietf.org/doc/rfc2119/
[RFC 3986]: https://datatracker.ietf.org/doc/rfc3986/
[RFC 5988]: http://datatracker.ietf.org/doc/rfc5988/
[RFC 6570]: https://datatracker.ietf.org/doc/rfc6570/
[RFC 7230]: http://datatracker.ietf.org/doc/rfc7230/
