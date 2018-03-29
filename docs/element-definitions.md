# Element Definitions

An Element MUST be a list of key-value pairs, also called _properties_, where keys are finite character strings. An `element` property referencing the Element's _type name_ as a finite character string also MUST be defined.

---

## Properties
An Element MUST define an `element` property. An Element MAY define `meta`, `attributes` and `content` properties.

<table class="markdown">
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
      <th>Optional?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>element</td>
      <td>type name as finite character string</td>
      <td>No</td>
    </tr>
    <tr>
      <td>meta</td>
      <td>meta information as key value pairs</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>attributes</td>
      <td>semantic information as key value pairs</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>content</td>
      <td>value specific to Element</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>

### `element` property

The `element` property MUST be defined and its value must be a finite character string. References the type of an Element.

### `attributes` property

The `attributes` property MAY be defined. If it is, it MUST hold a list of properties with Element values. Entries in `attributes` MAY be Element type specific.

### `meta` property

The `meta` property MAY be defined. If it is, it MUST hold a list of properties with Element values. Entries in `meta` SHOULD NOT be Element type specific and likewise SHOULD NOT hold semantic type information.

- `id` ([String](#string-element)) - identifier, MUST be unique throughout the document
- `ref` ([Ref](#ref-element)) - Pointer to referenced element or type
- `classes` ([Array](#array-element)[[String](#string-element)]) - Array of classifications for given element
- `title` ([String](#string-element)) - Human-readable title of element
- `description` ([String](#string-element)) - Human-readable description of element
- `links` ([Array](#array-element)[[Link Element](#link-element)]) - Meta links for a given element


### `content` property

The `content` property MAY be defined. If it is, it defines the value of an Element. The type of `content` SHALL be dependent on the Element type.


---

## Primitive Element types

<table class="markdown">
  <thead>
    <tr>
      <th>Type Element</th>
      <th>Name</th>
      <th>Example JSON value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="#null-element">Null</a></td>
      <td>null</td>
      <td><pre>null</pre></td>
    </tr>
    <tr>
      <td><a href="#boolean-element">Boolean</a></td>
      <td>boolean</td>
      <td>
        <pre>true</pre>
        <pre>false</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#number-element">Number</a></td>
      <td>number</td>
      <td>
        <pre>0</pre>
        <pre>-1.5</pre>
        <pre>6.53e-3</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#string-element">String</a></td>
      <td>string</td>
      <td>
        <pre>"Hello world"</pre>
        <pre>""</pre>
      </td>
    </tr>
  </tbody>
</table>

### Null Element
Type with domain of a single value. Called `unit` or `()` in some programming languages.
Note that both `nullptr` and `void` from C-style languages are unrelated concepts.

#### Properties
- `element` - `"null"`
- `content` - MUST hold unit if set

#### Example

The example below defines an Element matching only the null value.
```json
{
  "element": "null"
}
```

### Boolean Element

Type with domain of two values: true and false.
`content` property MUST contain a boolean value if set.

#### Properties
- `element` - `"boolean"`
- `attributes`
    - `typeAttributes` ([Array](#array-element)[[String](#string-element)])
        - `fixed` ([String](#string-element)) - domain reduces to value given in `content`
- `content` - ⊥ (false) or ⊤ (true)

#### Example

Type Element matching only boolean values (JSON `true`, `false`):

```json

{
  "element": "boolean"
}

```

Type Element matching only boolean "true" (JSON `true`):

```json

{
  "element": "boolean",
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
  "content": true
}

```


### Number Element

Type with domain of all rational numbers, i.e. floating-point numbers with finite precision.


#### Properties
- `element` - `"number"`
- `attributes`
  - `typeAttributes` ([Array](#array-element)[[String](#string-element)])
    - `fixed` ([String](#string-element)) - domain reduces to value given in `content`
- `content` - rational number

#### Example

Type Element matching only rationals. Matches JSON `number`.

```json

{
  "element": "number"
}

```

Type Element matching only the number `42`:

```json

{
  "element": "number",
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
  "content": 42
}

```

### String Element

Type with domain of all finite character strings.


#### Properties
- `element` - `"string"`
- `attributes`
  - `typeAttributes` ([Array](#array-element)[[String](#string-element)])
    - `fixed` ([String](#string-element))
      <p>Domain reduces to value given in `content`.</p>
- `content` - finite character string

#### Example

Type Element matching only character strings. Matches a `string` in JSON.

```json

{
  "element": "string"
}

```

Type Element matching only the character string `"rocket science"`.

```json

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
  "content": "rocket science"
}

```

---

## Structured Element Types

<table class="markdown">
  <thead>
    <tr>
      <th>Type Element</th>
      <th>Name</th>
      <th>Example JSON value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Array</td>
      <td>array</td>
      <td>
        <pre>[]</pre>
        <pre>[42]</pre>
        <pre>[42, "Hello world!"]</pre>
      </td>
    </tr>
    <tr>
      <td>Object</td>
      <td>object</td>
      <td>
        <pre>{}</pre>
        <pre>{"foo": 42, "bar": true}</pre>
      </td>
    </tr>
    <tr>
      <td>Enum</td>
      <td>enum</td>
      <td>
        depends on <pre>enumerations</pre> attribute content
      </td>
    </tr>
  </tbody>
</table>

Structured types MAY be further refined via flags in the `typeAttributes` property in `attributes`.

<table class="markdown">
  <thead>
    <tr>
      <th>Type Element</th>
      <th>Name</th>
      <th>Type Attribute</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Array</td>
      <td>array</td>
      <td>fixed</td>
      <td>tuple of Elements matching Elements in `content`; i. e. Π-type over Elements in `content`</td>
    </tr>
    <tr>
      <td>Array</td>
      <td>array</td>
      <td>fixedType</td>
      <td>list of Elements matching at least one of the Elements in `content`; i. e. typed list of Σ-type over Elements in `content`</td>
    </tr>
    <tr>
      <td>Object</td>
      <td>object</td>
      <td>fixed</td>
      <td></td>
    </tr>
    <tr>
      <td>Object</td>
      <td>object</td>
      <td>fixedType</td>
      <td>data structure strictly matching properties defined in its `content`</td>
    </tr>
    <tr>
      <td>Enum</td>
      <td>enum</td>
      <td>fixed</td>
      <td>Elements given in the "enumerations" array are interpreted as fixed</td>
    </tr>
  </tbody>
</table>


### Array Element

Type with domain of all finite lists.


#### Properties
- `element` - `"array"`
- `attributes`
  - `typeAttributes` ([Array](#array-element)[[String](#string-element)])
    - `fixed` ([String](#string-element))
      <p>Reduces domain to a positionally typed fixed-length list over types in content. This type class is usually called a <i>tuple</i>, <i>sum type</i> or <i>Π-type</i>.</p>
    - `fixedType` ([String](#string-element))
      <p>Reduces domain to a list of types given in `content`.
- `content` - finite list of Element

#### Example

Type Element matching only lists (JSON `array`).

```json

{
  "element": "array"
}

```

Type Element matching only pairs of (`string`, `number`).

```json

{
  "element": "array",
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
  "content": [
    {
      "element": "string"
    },
    {
      "element": "number"
    }
  ]
}

```

Type Element matching only lists of one of `string`, `number`.

```json

{
  "element": "array",
  "attributes": {
    "typeAttributes": {
      "element": "array",
      "content": [
        {
          "element": "string",
          "content": "fixedType"
        }
      ]
    }
  },
  "content": [
    {
      "element": "string"
    },
    {
      "element": "number"
    }
  ]
}

```

---

## API Element Types

### Href ([String](#string-element))

The value of the `Href` type  SHOULD be resolved as a URI-Reference per [RFC 3986][] and MAY be a relative reference to a URI.
The value of the `Href` type MUST NOT be a URI Template.

### Templated Href ([String](#string-element))

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
    - `classes` ([Array](#array-element))
        - `content` (array, fixed-type)
            - ([String](#string-element))
                - `content` (enum)
                    - messageBody (string) - Asset is an example of message-body
                    - messageBodySchema (string) - Asset is an schema for message-body
- `attributes`
    - `contentType` ([String](#string-element)) - Optional media type of the asset. When this is unset, the content type SHOULD be inherited from the `Content-Type` header of a parent HTTP Message Payload
    - `href` (Href) - Link to the asset
- `content` (string) - A textual representation of the asset

### Resource (Base API Element)

The Resource representation with its available transitions and its data.

#### Properties

- `element`: resource (string, fixed)
- `attributes`
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
    "title": {
      "element": "string",
      "content": "Question"
    },
    "description": {
      "element": "string",
      "content": "A Question object has the following attributes."
    }
  },
  "attributes": {
    "href": {
      "element": "string",
      "content": "/questions/{question_id}"
    },
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
- `attributes`
    - `relation` - ([String](#string-element)) - Link relation type as specified in [RFC 5988][].

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

    - `contentTypes` ([Array](#array-element)[[String](#string-element)]) - A collection of content types that MAY be used for the transition.
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
    "relation": {
      "element": "string",
      "content": "update"
    },
    "href": {
      "element": "string",
      "content": "https://polls.apiblueprint.org/questions/{question_id}"
    }
  },
  "content": []
}
```

### API Metadata (Member Element)

#### Properties

- `meta`
    - `classes` ([Array](#array-element))
        - `content` (array, fixed-type)
            - ([String](#string-element))
                - `content` (enum)
                    - user (string) - User-specific metadata. Metadata written in the source.
                    - adapter (string) - Serialization-specific metadata. Metadata provided by adapter.

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
    - `classes` ([Array](#array-element))
        - `content` (array, fixed-type)
            - ([String](#string-element))
                - `content` (enum)
                    - api (string) - Category is a API top-level group.
                    - resourceGroup (string) - Category is a set of resource.
                    - dataStructures (string) - Category is a set of data structures.
                    - scenario (string) - Category is set of steps.
                    - transitions (string) - Category is a group of transitions.
                    - authSchemes (string) - Category is a group of authentication and authorization scheme definitions
- `attributes`
    - `metadata` ([Array](#array-element)[API Metadata]) - Arbitrary metadata
- `content` (array[Base API Element])

#### Example

```json
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
      "content": "Polls API"
    }
  },
  "attributes": {
    "metadata": {
      "element": "array",
      "content": [
        {
          "element": "member",
          "meta": {
            "classes": {
              "element": "array",
              "content": [
                {
                  "element": "string",
                  "content": "user"
                }
              ]
            }
          },
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
          "content": "Question"
        }
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
- `attributes`
    - `contentType` ([String](#string-element)) - Optional media type of the content.
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
- `attributes`
    - `authSchemes` ([Array](#array-element)[Base API Element]) - An array of authentication and authorization schemes that apply to the transaction
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
        "method": {
          "element": "string",
          "content": "GET"
        },
        "href": {
          "element": "string",
          "content": "/questions/{question_id}"
        },
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
        "statusCode": {
          "element": "number",
          "content": 200
        }
      },
      "content": [
        {
          "element": "asset",
          "meta": {
            "classes": {
              "element": "array",
              "content": [
                {
                  "element": "string",
                  "content": "messageBody"
                }
              ]
            }
          },
          "attributes": {
            "contentType": {
              "element": "string",
              "content": "application/json"
            }
          },
          "content": "{\"name\": \"John\"}"
        }
      ]
    }
  ]
}
```

#### HTTP Headers ([Array](#array-element)[Member Element])

Ordered array of HTTP header-fields.

##### Properties

- `element`: httpHeaders (string, fixed)

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
    - `method` ([String](#string-element)) - HTTP request method. The method value SHOULD be inherited from a parent transition if it is unset.
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
    - `statusCode` ([Number](#number-element)) - HTTP response status code.

## Data Structure Elements

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
    "id": {
      "element": "string",
      "content": "B"
    }
  },
  "content": [
    {
      "element": "string",
      "meta": {
        "id": {
          "element": "string",
          "content": "A"
        }
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
    "id": {
      "element": "string",
      "content": "A"
    }
  },
  "content": "base element content"
}
```

```json
{
  "element": "A",
  "meta": {
    "id": {
      "element": "string",
      "content": "B"
    }
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
    "id": {
      "element": "string",
      "content": "B"
    }
  },
  "content": [
    {
      "element": "string",
      "meta": {
        "ref": {
          "element": "ref",
          "content": "A"
        }
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
|     boolean    |  [Boolean](#boolean-element) |     boolean    |  Boolean Type  |
|     string     |  [String](#string-element)  |     string     |   String Type  |
|     number     |  [Number](#number-element)  |     number     |   Number Type  |
|      array     |  [Array](#array-element)  |      array     |   Array Type   |
|        -       |         -        |      enum      |    Enum Type   |
|     object     |  Object Element  |     object     |   Object Type  |
|      null      |   Null Element   |        -       |        -       |

### Data Structure Element (Base API Element)

Base element for every Data Structure element.

The Data Structure Element adds attributes representing Data Structure _Type Definition_ and _Type Sections_.

Note: In Data Structure Refract _Nested Member Types_ _Type Section_ is the `content` of the element.

#### Properties

- `attributes`
    - `typeAttributes` ([Array](#array-element)) - _Type Definition_ attributes list, see _Type Attribute_  

        - `content` (array, fixed-type)

            Type attributes of a type definition.

            Note, if `sample` (or `default`) attribute is specified the value SHOULD be stored in the `samples` (or `default`) property instead of the element's `content`.

            - Items
                - ([String](#string-element))
                    - `content` (enum)
                        - required (string) - This element is required in parent's content
                        - optional (string) - This element is optional in parent's content
                        - fixed (string) - The `content` value is immutable.
                        - fixedType (string) - The type of `content` value is immutable.

    - `variable` ([Boolean](#boolean-element))

      The `content` value is either a _Variable Type Name_, or _Variable Property Name_.

      Note, if the `content` is a _Variable Value_ the `sample` type attribute
      should be used instead (see `typeAttributes`).

    - `samples` ([Array](#array-element)) - Array of alternative sample values for _Member Types_

          The type of items in `samples` array attribute MUST match the type of element.

    - `default` ([Element][]) - Default value for _Member Types_

          The type of of `default` attribute MUST match the type of element.

    - `validation` - Not used, reserved for a future use

### Type Reference ([Ref Element][])

This elements extends refract `Ref Element` to include optional referenced element.

#### Properties

- `element`: ref (string, fixed)
- `attributes`
    -  `resolved` ([Element][], optional) - Resolved element being referenced.

### Enum Type (Data Structure Element)

Enumeration type. Exclusive list of possible elements. The elements in content's array MUST be interpreted as mutually exclusive.

#### Properties

- `element`: enum (string, fixed)
- `attributes`
    - `enumerations` ([Array](#array-element)[[Data Structure Element][]])
- `content` ([Data Structure Element][])

#### Examples

##### MSON

```
- tag: green (enum[string])
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
          "attributes": {
            "enumerations": {
              "element": "array",
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
        "typeAttributes": {
          "element": "array",
          "content": [
            {
              "element": "string",
              "content": "required"
            },
            {
              "element": "string",
              "content": "fixed"
            }
          ]
        }
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
            "default": {
              "element": "number",
              "content": 0
            }
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
      "attributes": {
        "path": {
          "element": "string",
          "content": "content"
        }
      },
      "content": "User"
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
        "path": {
          "element": "string",
          "content": "content"
        },
        "resolved": {
          "element": "object",
          "meta": {
            "ref": {
              "element": "ref",
              "content": "User"
            }
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
      "content": "User"
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
    "id": {
      "element": "string",
      "content": "Address"
    },
    "title": {
      "element": "string",
      "content": "Address"
    },
    "description": {
      "element": "string",
      "content": "Description is here! Properties to follow."
    }
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
    "id": {
      "element": "string",
      "content": "User"
    }
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
    "id": {
      "element": "string",
      "content": "Customer"
    }
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
    "id": {
      "element": "string",
      "content": "Customer"
    }
  },
  "content": [
    {
      "element": "object",
      "meta": {
        "ref": {
          "element": "ref",
          "content": "User"
        }
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
- p: *42* (number)
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
          "content": "p"
        },
        "value": {
          "element": "number",
          "attributes": {
            "samples": {
              "element": "array",
              "content": [
                {
                  "element": "number",
                  "content": 42
                }
              ]
            }
          }
        }
      }
    }
  ]
}
```

#### Variable Property Name

##### MSON

```markdown
- *rel (Relation)*
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
          "element": "Relation",
          "attributes": {
            "variable": {
              "element": "boolean",
              "content": true
            }
          },
          "content": "rel"
        },
        "value": {
          "element": "string"
        }
      }
    }
  ]
}
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
{
  "element": "object",
  "content": [
    {
      "element": "member",
      "content": {
        "key": {
          "element": "string",
          "content": "p"
        },
        "value": {
          "element": "array",
          "content": [
            {
              "element": "generic",
              "content": "T"
            }
          ]
        }
      }
    }
  ]
}
```

## Parse Result Elements

### Parse Result (Base API Element)

A result of parsing of an API description document.

#### Properties

- `element`: parseResult (string, fixed)
- `content` (array, fixed-type)
    - (Category)
    - (Annotation)

#### Example

Given following API Blueprint document:

```apib
# GET /1
```

The parse result is (using null in `category` content for simplicity):

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
        }
      }
    },
    {
      "element": "annotation",
      "meta": {
        "classes": {
          "element": "array",
          "content": [
            {
              "element": "string",
              "content": "warning"
            }
          ]
        }
      },
      "attributes": {
        "code": {
          "element": "number",
          "content": 6
        },
        "sourceMap": {
          "element": "array",
          "content": [
            {
              "element": "sourceMap",
              "content": [
                {
                  "element": "array",
                  "content": [
                    {
                      "element": "number",
                      "content": 0
                    },
                    {
                      "element": "number",
                      "content": 9
                    }
                  ]
                }
              ]
            }
          ]
        }
      },
      "content": "action"
    }
  ]
}
```

### Annotation (Base API Element)

Annotation for a source file. Usually generated by a parser or adapter.

#### Properties

- `element`: annotation (string, fixed)
- `meta`
  - `classes` ([Array](#array-element))
      - `content` (array, fixed-type)
          - ([String](#string-element))
              - `content` (enum)
                  - error (string) - Annotation represents an error
                  - warning (string) - Annotation represents a warning

- `attributes`
    - `code` ([Number](#number-element)) - Parser-specific code of the annotation.
    Refer to parser documentation for explanation of the codes.

    - `sourceMap` ([Array](#array-element)[Source Map]) - Locations of the annotation in the source file.

- `content` (string) - Textual annotation.

    This is – in most cases – a human-readable message to be displayed to user.

#### Example

```json
{
  "element": "annotation",
  "meta": {
    "classes": {
      "element": "array",
      "content": [
        {
          "element": "string",
          "content": "warning"
        }
      ]
    }
  },
  "attributes": {
    "code": {
      "element": "number",
      "content": 6
    },
    "sourceMap": {
      "element": "array",
      "content": [
        {
          "element": "sourceMap",
          "content": [
            {
              "element": "array",
              "content": [
                {
                  "element": "number",
                  "content": 4
                },
                {
                  "element": "number",
                  "content": 12
                }
              ]
            },
            {
              "element": "array",
              "content": [
                {
                  "element": "number",
                  "content": 20
                },
                {
                  "element": "number",
                  "content": 12
                }
              ]
            }
          ]
        }
      ]
    }
  },
  "content": "action is missing a response"
}
```

### Source Map (Base API Element)

Source map of an Element.

Every Element MAY include a `sourceMap` attribute. Its content MUST
be an array of `Source Map` elements. The Source Map elements represent the
location(s) in source file(s) from which the element was composed.

If used, it represents the location of bytes in the source file.
This location SHOULD include the bytes used to build the parent element.

The Source Map element MUST NOT be used in its normal form
unless the particular application clearly implies what is the source file the
source map is pointing in.

A source map is a series of byte-blocks. These
blocks may be non-continuous. For example, a block in the series may not start
immediately after the previous block. Each block, however, is a continuous
series of bytes.

#### Properties

- `element`: sourceMap (string, fixed)
- `content` (array) - Array of byte blocks.
    - ([Array](#array-element)) - Continuous bytes block. A pair of byte index and byte count.
        - `content` (array, fixed-type)
            - ([Number](#number-element)) - Zero-based index of a byte in the source document.
                - attributes
                    - line - The line number the source map starts on.
                    - column - The column number of the line that the source map starts on.
            - ([Number](#number-element)) - Count of bytes starting from the byte index.
                - attributes
                    - line - The line number the source map ends on.
                    - column - The column number of the line that the source map ends on.

#### Example

```json
{
  "element": "sourceMap",
  "content": [
    {
      "element": "array",
      "content": [
        {
          "element": "number",
          "content": 4
        },
        {
          "element": "number",
          "content": 12
        }
      ]
    },
    {
      "element": "array",
      "content": [
        {
          "element": "number",
          "content": 4
        },
        {
          "element": "number",
          "content": 12
        }
      ]
    }
  ]
}
```

This reads, "The location starts at the 5th byte of the source file. It
includes the 12 subsequent bytes including the starting one. Then it
continues at the 21st byte for another 12 bytes."

#### Example

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

This reads, "The location starts at the 5th byte (the 2nd byte of line 3) of the source file. It includes 12 bytes, until column 10 on line 3".

**NOTE** *`line` and `column` are optional and may not always be available*.

### Link Relations

In addition to conforming to [RFC 5988][] for link relations, there are also additional link relations
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

## Authentication and Authorization Schemes

Authentication and authorization schemes MAY be defined within an API Elements document. These schemes are then used within the context of a resource to define which schemes to apply when making a transaction.

### Basic Authentication Scheme (Object Element)

This element may be used to define a basic authentication scheme implementation for an API as described in [RFC 2617](https://tools.ietf.org/html/rfc2617).

The element MAY have a username and password defined as member elements within the scheme, but these are not required.

- `username` (string, optional)
- `password` (string, optional)

#### Properties

- `element`: Basic Authentication Scheme (string, fixed)

#### Example

This example shows a custom basic authentication scheme being defined as `Custom Basic Auth`. This scheme is then used on an HTTP transaction within a resource. Please note this example is incomplete for the sake of keeping it short.

```json
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
              "content": "authSchemes"
            }
          ]
        }
      },
      "content": [
        {
          "element": "Basic Authentication Scheme",
          "meta": {
            "id": {
              "element": "string",
              "content": "Custom Basic Auth"
            }
          },
          "content": [
            {
              "element": "member",
              "content": {
                "key": {
                  "element": "string",
                  "content": "username"
                },
                "value": {
                  "element": "string",
                  "content": "john.doe"
                }
              }
            },
            {
              "element": "member",
              "content": {
                "key": {
                  "element": "string",
                  "content": "password"
                },
                "value": {
                  "element": "string",
                  "content": "1234password"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "element": "resource",
      "attributes": {
        "href": {
          "element": "string",
          "content": "/users"
        }
      },
      "content": [
        {
          "element": "transition",
          "content": [
            {
              "element": "httpTransaction",
              "attributes": {
                "authSchemes": {
                  "element": "array",
                  "content": [
                    {
                      "element": "Custom Basic Auth"
                    }
                  ]
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

### Token Authentication Scheme (Base API Element)

This describes an authentication scheme that uses a token as a way to authenticate and authorize. The token MAY exist as an HTTP header field or a query parameter.

- One of
    - `httpHeaderName` (string)
    - `queryParameterName` (string)

When used as a query parameter, an HREF Variable is not required to be defined within the scope of the resource or transition, but is rather infered from the used token authentications scheme.

#### Properties

- `element`: Token Authentication Scheme (string, fixed)
- `content` (array[Member Element])

#### Example

This example shows a custom token authentication scheme being defined as `Custom Token Auth` that uses a query parameter for the token. This scheme is then used on an HTTP transaction within a resource. Please note this example is incomplete for the sake of keeping it short.

```json
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
              "content": "authSchemes"
            }
          ]
        }
      },
      "content": [
        {
          "element": "Token Authentication Scheme",
          "meta": {
            "id": {
              "element": "string",
              "content": "Custom Token Auth"
            }
          },
          "content": [
            {
              "element": "member",
              "content": {
                "key": {
                  "element": "string",
                  "content": "queryParameterName"
                },
                "value": {
                  "element": "string",
                  "content": "api_key"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "element": "resource",
      "attributes": {
        "href": {
          "element": "string",
          "content": "/users"
        }
      },
      "content": [
        {
          "element": "transition",
          "content": [
            {
              "element": "httpTransaction",
              "attributes": {
                "authSchemes": {
                  "element": "array",
                  "content": [
                    {
                      "element": "Custom Token Auth"
                    }
                  ]
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

### OAuth2 Scheme (Base API Element)

This describes an authentication scheme that uses OAuth2 as defined in [RFC 6749](https://tools.ietf.org/html/rfc6749).

The element MAY have the following members to define additional information about the OAuth2 implementation.

- `scopes` (array[string])
- `grantType` (enum)
    - `authorization code`
    - `implicit`
    - `resource owner password credentials`
    - `client credentials`

Transition elements are used to define the URLs for the authorize and token endpoints for the OAuth2 schemes. When including these endpoints, the following link relations SHOULD be used.

- `authorize` - URL for the authorization endpoint
- `token` - URL for the token endpoint

The HREF values for these transitions MAY be either relative or absolute URLs.

#### Properties

- `element`: OAuth2 Scheme (string, fixed)
- `content` (array[Member Element, Transition])

#### Example

This example shows a custom OAuth2 scheme being defined as `Custom OAuth2`. This scheme is then used on an HTTP transaction within a resource. There are a couple of things to note about this example:

1. There are two scopes defined within the scheme, but only one is used within the context of the transaction.
1. Transitions are used to define the authorize and token endpoints.

Also, please note this example is incomplete for the sake of keeping it short.

```json
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
              "content": "authSchemes"
            }
          ]
        }
      },
      "content": [
        {
          "element": "OAuth2 Scheme",
          "meta": {
            "id": {
              "element": "string",
              "content": "Custom OAuth2"
            }
          },
          "content": [
            {
              "element": "member",
              "content": {
                "key": {
                  "element": "string",
                  "content": "scopes"
                },
                "value": {
                  "element": "array",
                  "content": [
                    {
                      "element": "string",
                      "content": "scope1"
                    },
                    {
                      "element": "string",
                      "content": "scope2"
                    }
                  ]
                }
              }
            },
            {
              "element": "member",
              "content": {
                "key": {
                  "element": "string",
                  "content": "grantType"
                },
                "value": {
                  "element": "string",
                  "content": "implicit"
                }
              }
            },
            {
              "element": "transition",
              "attributes": {
                "relation": {
                  "element": "string",
                  "content": "authorize"
                },
                "href": {
                  "element": "string",
                  "content": "/authorize"
                }
              }
            },
            {
              "element": "transition",
              "attributes": {
                "relation": {
                  "element": "string",
                  "content": "token"
                },
                "href": {
                  "element": "string",
                  "content": "/token"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "element": "resource",
      "attributes": {
        "href": {
          "element": "string",
          "content": "/users"
        }
      },
      "content": [
        {
          "element": "transition",
          "content": [
            {
              "element": "httpTransaction",
              "attributes": {
                "authSchemes": {
                  "element": "array",
                  "content": [
                    {
                      "element": "Custom OAuth2",
                      "content": [
                        {
                          "element": "member",
                          "content": {
                            "key": {
                              "element": "string",
                              "content": "scopes"
                            },
                            "value": {
                              "element": "array",
                              "content": [
                                {
                                  "element": "string",
                                  "content": "scope1"
                                }
                              ]
                            }
                          }
                        }
                      ]
                    }
                  ]
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

## Extending API Elements

An API Elements document MAY be extended by providing a [profile link](https://www.ietf.org/rfc/rfc6906.txt) that describes how non-specification elements should be handled.

Additionally, an `extension` element is provided as a way to extend API Elements documents to include additional data not expressed by the elements in this specification.

When the `extension` element is used, it SHOULD include a profile link that provides information on how the content and attributes SHOULD be handled. Additionally, the presence of an `extension` element MUST NOT change the meaning of the rest of the API Elements document in which it is found. In other words, a tool SHOULD be able to safely ignore an `extension` element.

For changes that need to make unsafe changes, a custom media type or profile SHOULD be used.

### Extension (Base API Element)

- `element`: extension (string, fixed)
- `content` (enum) - Custom content of extension element
    - (string)
    - (number)
    - (boolean)
    - (array)
    - (object)

### Example

This `extension` element has a custom content, and the meaning and handling instructions for this content.

```json
{
  "element": "extension",
  "meta": {
    "links": {
      "element": "array",
      "content": [
        {
          "element": "link",
          "attributes": {
            "relation": {
              "element": "string",
              "content": "profile"
            },
            "href": {
              "element": "string",
              "content": "http://example.com/extensions/info/"
            }
          }
        }
      ]
    }
  },
  "content": {
    "element": "object",
    "content": [
      {
        "element": "member",
        "content": {
          "key": {
            "element": "string",
            "content": "version"
          },
          "value": {
            "element": "string",
            "content": "1.0"
          }
        }
      }
    ]
  }
}
```

This specific extension adds an object for including information about an API that may be specific to an implementation—in this case, a version number of the API. The URL `http://example.com/extensions/info/` would then provide instructions on the meaning and structure of the `content`.

As a tool comes across this extension element, it would look at the profile URL to see if it understands this particular element. If not, it can ignore it safely, but if so, it can use it as it sees fit.

---


[MSON]: https://github.com/apiaryio/mson
[MSON Reference]: https://github.com/apiaryio/mson/blob/master/MSON%20Reference.md

[API Description Elements]: definitions/api-description-elements.md
[Data Structure Elements]: definitions/data-structure-elements.md
[Parse Result Elements]: definitions/parse-result-elements.md

[Data Structure Element]: #data-structure-element-element

[RFC 2119]: https://datatracker.ietf.org/doc/rfc2119/
[RFC 3986]: https://datatracker.ietf.org/doc/rfc3986/
[RFC 5988]: http://datatracker.ietf.org/doc/rfc5988/
[RFC 6570]: https://datatracker.ietf.org/doc/rfc6570/
[RFC 7230]: http://datatracker.ietf.org/doc/rfc7230/
