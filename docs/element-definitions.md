# Element Reference

## Element

An _Element_ SHALL be a tuple (`element`, `meta`, `attributes`, `content`) where
 - `element` SHALL be a non-empty, finite character string identifying the _type_ of this Element
 - `meta` SHALL be a set of _properties_, some of which have [reserved semantics](#reserved-meta-properties)
 - `attributes` SHALL be a set of _properties_ defined by the _type_ of this Element
 - `content` SHALL be defined by the _type_ of this Element

Entries in `meta` SHOULD be independent of Element.
Entries in `attributes` MAY be Element specific.

### Property

A _property_ SHALL be a tuple (`key`, `value`) where
- `key` SHALL be a non-empty, finite character string
- `value` SHALL be an _Element_
- Two properties SHALL be equal if their keys are.

> The last statement defining equality on properties through their keys allows definition of _objects_ as _sets_ of properties.

### Values
Following values can be described in API Elements:
- _null_ value
- boolean values _true_ and _false_
- rational numbers, i.e. floating point numbers with finite precision
- finite character strings
- finite sets of properties
- finite lists of values

### Types
Types specify value categories. Every Element SHALL describe a type.

Note that because types may be restricted to exactly one value, an Element MAY match only a single value; such an Element still represents a type, not the value itself.

An Element can therefore be thought of as a predicate that holds if, and only if, given value is in its value category. Given `Number` is the predicate classifying rational numbers, `Number(42.0)` SHALL hold, whereas `Number("foobar")` SHALL NOT.

#### Subtypes
We say the type _S_ is a _subtype_ of type _T_ if, and only if, all values of _S_ are also values of _T_.

---

API Elements predefines three broad categories of Element types:
1. [Data Structure Element types](#data-structure-element-types) - Tools to define types, e.g. [string][], [array][], [object][]
2. [API Element types](#api-element-types) - Types specific to API description
3. [Parse Result Element types](#parse-result-element-types) - Types specific to document parsing, e.g. source map, parse result


### Reserved meta properties

Any of the following properties MAY be an entry of any Element's `meta`:

- `id` ([String][]) - Unique name of this Element; defines a named type; MUST be unique with respect to other `id`s in a document
- `ref` ([Ref](#ref-element)) - Pointer to referenced element or type
- `classes` ([Array][][[String][]]) - Classifications for given element
- `title` ([String][]) - Human-readable title of element
- `description` ([String][]) - Human-readable description of element
- `links` ([Array][][[Link Element](#link-element)]) - Meta links for a given element

### Examples

A primitive Element representing finite character strings is [String Element][], of type id `string`. Serialized into JSON, an Element representing `Hello world!` interpreted as a [String Element][] value:

```json
{
  "element": "string",
  "content": "Hello world!"
}
```


A less trivial example is the following `asset` Element. The specific semantic interpretation of an `asset` Element is well defined in the API Elements Reference section. What we essentially describe here is a JSON snippet `{"foo": "bar"}` defined in the message body of documentation.
```json
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
  "content": "{\"foo\": \"bar\"}"
}
```

---

## Data Structure Element types

### Overview

[API Elements](#api-element-types) and [Parse Result Elements](#parse-result-element-types) are all defined via Data Structure Elements.
The following table summarizes them very broadly.

<table class="markdown">
  <thead>
    <tr>
      <th>Name</th>
      <th>Type (JSON serialized)</th>
      <th>Value (JSON serialized)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="#null-element">null</a></td>
      <td>
        <pre>{
  "element": "null"
}</pre>
      </td>
      <td><pre>null</pre></td>
    </tr>
    <tr>
      <td><a href="#boolean-element">boolean</a></td>
      <td>
        <pre>{
  "element": "boolean"
}</pre>
      </td>
      <td>
        <pre>true</pre>
        <pre>false</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#number-element">number</a></td>
      <td>
        <pre>{
  "element": "number"
}</pre>
      </td>
      <td>
        <pre>0</pre>
        <pre>-1.5</pre>
        <pre>6.53e-3</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#string-element">string</a></td>
      <td>
        <pre>{
  "element": "string"
}</pre>
      </td>
      <td>
        <pre>"Hello world"</pre>
        <pre>""</pre>
      </td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td><a href="#array-element">array</a></td>
      <td>
        <pre>{
  "element": "array"
}</pre>
      </td>
      <td>
        <pre>[]</pre>
        <pre>[42, "Hello world!"]</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#member-element">member</a></td>
      <td>
        <pre>{
  "element": "member",
  "content": {
    "key": {
      "element": "string",
      "content": "foo"
    },
    "value": {
      "element": "string"
    }
  }
}</pre>
      </td>
      <td>
        Properties in JSON cannot be represented as standalone values. However, they exist as fragments of a JSON objects:
        <pre>"foo": ""</pre>
        <pre>"foo": "Hey!"</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#object-element">object</a></td>
      <td>
        <pre>{
  "element": "object"
}</pre>
      </td>
      <td>
        <pre>{}</pre>
        <pre>{
  "foo": "Hey!"
}</pre>
        <pre>{
  "bar": true
}</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#enum-element">enum</a></td>
      <td>
        <pre>{
  "element": "enum",
  "attributes": {
    "enumerations": {
      "element": "array",
      "content": [
        {
          "element": "string"
        },
        {
          "element": "number"
        }
      ]
    }
  }
}</pre>
      </td>
      <td>
        <pre>-45.9</pre>
        <pre>"Hello world!"</pre>
        <pre>""</pre>
        <pre>0</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#select-element">select</a> & <a href="#option-element">option</a></td>
      <td>
        <pre>{
  "element": "select",
  "content": [
    {
      "element": "option",
      "content": {
        "element": "string"
      }
    },
    {
      "element": "option",
      "content": {
        "element": "number"
      }
    }
  ]
}</pre>
      </td>
      <td>
        <pre>-45.9</pre>
        <pre>"Hello world!"</pre>
        <pre>""</pre>
        <pre>0</pre>
      </td>
    </tr>
    <tr>
      <td><a href="#extend-element">extend</a></td>
      <td>
        <pre>{
  "element": "extend",
  "content": [
    {
      "element": "object",
      "content": [
        {
          "element": "member",
          "content": {
            "key": {
              "element": "string",
              "content": "foo"
            },
            "value": {
              "element": "string"
            }
          }
        },
        {
          "element": "member"
          "content": {
            "key": {
              "element": "string",
              "content": "bar"
            },
            "value": {
              "element": "number"
            }
          }
        }
      ]
    },
    {
      "element": "object",
      "content": [
        {
          "element": "member"
          "content": {
            "key": {
              "element": "string",
              "content": "baz"
            },
            "value": {
              "element": "boolean"
            }
          }
        }
      ]
    }
  ]
}</pre>
      </td>
      <td>
        <pre>{}</pre>
        <pre>{
  "foo": "Hey!"
}</pre>
        <pre>{
  "bar": 42.3
}</pre>
        <pre>{
  "foo": "Hello",
  "bar": 3.14,
  "baz": true
}</pre>
      </td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td><a href="#ref-element">ref</a></td>
      <td>
        Given an named type such as
        <pre>{
  "element": "string",
  "meta": {
    "id": {
      "element": "string",
      "content": "SpecialString"
      }
    }
  }
}</pre>
A reference:
<pre>{
  "element": "ref"
  "content": "MyString"
}</pre>
      </td>
      <td>
        <pre>""</pre>
        <pre>"abc"</pre>
        <pre>"Hello world!"</pre>
      </td>
    </tr>
  </tbody>
</table>

---

### Fail Element
Type with empty domain. Attempts at instantiation of this Element SHALL fail.

#### Template
- `element` - `"fail"`

> Reserved for future use.

---

### Null Element
Type with domain of a single value.

#### Template
- `element` - `"null"`

#### Example

The example below defines an Element representing only the null value.
```json
{
  "element": "null"
}
```

---

### Boolean Element

Type with domain of two values: _true_ and _false_.

#### Template
- `element` - `"boolean"`
- `attributes`
  - `typeAttributes` ([Array][][[String][]])
    - `fixed` ([String][]) - The type this Element describes is restricted to the value given in `content`
  - `validation` - _reserved for future use_
  - `samples` ([Array][][[Boolean][]]]) - Alternative sample values for this Element; type of items in `samples` MUST match the type this Element describes
  - `default` ([Boolean][]) - Default value for this Element; type of `default` MUST match the type this Element describes
- `content` - _false_ or _true_

#### Example

Type Element representing only boolean values (JSON `true`, `false`):

```json

{
  "element": "boolean"
}

```

Type Element representing only boolean "true" (JSON `true`):

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

---

### Number Element

Type with domain of all rational numbers, i.e. floating-point numbers with finite precision.


#### Template
- `element` - `"number"`
- `attributes`
  - `typeAttributes` ([Array][][[String][]])
    - `fixed` ([String][]) - The type this Element describes is restricted to the value given in `content`
  - `validation` - _reserved for future use_
  - `samples` ([Array][][[Number][]]]) - Alternative sample values for this Element; type of items in `samples` MUST match the type this Element describes
  - `default` ([Number][]) - Default value for this Element; type of `default` MUST match the type this Element describes
- `content` - Rational number

#### Example

Type Element representing only rationals. Matches JSON number values.

```json

{
  "element": "number"
}

```

Type Element representing only the number `42`:

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

---

### String Element

Type with domain of all finite character strings.


#### Template
- `element` - `"string"`
- `attributes`
  - `typeAttributes` ([Array][][[String][]])
    - `fixed` ([String][]) - The type this Element describes is restricted to the value given in `content`.
  - `validation` - _reserved for future use_
  - `samples` ([Array][][[String][]]]) - Alternative sample values for this Element; type of items in `samples` MUST match the type this Element describes
  - `default` ([String][]) - Default value for this Element; type of `default` MUST match the type this Element describes
- `content` - Finite character string

#### Example

Type Element representing only finite character strings. Matches JSON string values.

```json

{
  "element": "string"
}

```

Type Element representing only the character string `"rocket science"`.

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

### Array Element

Type with domain of all finite lists of values.


#### Template
- `element` - `"array"`
- `attributes`
  - `typeAttributes` ([Array][][[String][]])
    - `fixed` ([String][]) - Restricts domain to a positionally typed fixed-length list over types in content.  Further applies the `fixed` type attribute to nested [Array][]s, [Object][]s and any other type defining content or default.
    - `fixedType` ([String][]) - Restricts domain to a list of types given in `content`.
  - `validation` - _reserved for future use_
  - `samples` ([Array][][[Array][]]]) - Alternative sample values for this Element; type of items in `samples` MUST match the type this Element describes
  - `default` ([Array][]) - Default value for this Element; type of `default` MUST match the type this Element describes
- `content` - Finite list of Elements

#### Examples

Type Element representing only lists (JSON `array`).

```json

{
  "element": "array"
}

```

Type Element representing only pairs of (`string`, `number`).

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

Type Element representing only lists where items are either a JSON `string` or a JSON `number`.

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

### Member Element
Type with domain of all [_properties_](#property).

#### Template
- `element` - `"member"`
- `attributes`
  - `typeAttributes` ([Array][][[String][]])
    - `required` ([String][]) - Property MUST be present in value represented by the containing [Object Element][]. I.e. restricts the domain of the containing Object Element type to one containing this property.
    - `optional` ([String][]) - Property MAY NOT be present in value represented by the containing [Object Element][]. I.e. expands the domain of the containing Object Element type to one not containing this property.
  - `variable` - ([Boolean][]) - Property key SHALL be interpreted as a variable name instead of a literal name
  - `validation` - _reserved for future use_
- `content`
  - `key` - An Element representing a key; MUST be set; SHOULD be a [String Element][]
  - `value` - An Element representing the value

#### Examples
See [Object Element][] for examples.

---

### Object Element

Type with domain of all finite sets of [_properties_](#property).


#### Template
- `element` - `"object"`
- `attributes`
  - `typeAttributes` ([Array][][[String][]])
    - `fixed` ([String][]) - Restricts domain to a fixed sized set of properties, making them implicitly required. Further applies the `fixed` type attribute to nested [Array][]s, [Object][]s and any other type defining content or default.
    - `fixedType` ([String][]) - Restricts domain to a fixed sized set of properties, making them implicitly required.
  - `validation` - _reserved for future use_
  - `samples` ([Array][][[Object][]]]) - Alternative sample values for this Element; type of items in `samples` MUST match the type this Element describes
  - `default` ([Object][]) - Default value for this Element; type of `default` MUST match the type this Element describes
- `content` - List of any of
  - [Member][] - Object property
  - [Extend](#extend-element) - MUST type a property
  - [Select](#select-element) - Contained [Option Element](#option-element)s MUST type properties
  - [Ref](#ref-element) - MUST reference an Object Element

[References](#ref-element) in the `content` of an Object Element SHALL be semantically equivalent to their substitution by items held in the content of the referenced Object Element. Less formally, Ref Elements in the content of Object Element represent in-place mixins.

#### Examples

Type Element representing only property lists (JSON `object`).

```json

{
  "element": "object"
}

```

Type Element representing only a specific property list instance (JSON `{"foo": false, "bar": "fun"}`).

```json

{
  "element": "object",
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
      "element": "member",
      "content": {
        "key": {
          "element": "string",
          "content": "foo"
        },
        "value": {
          "element": "boolean",
          "content": false
        }
      }
    },
    {
      "element": "member",
      "content": {
        "key": {
          "element": "string",
          "content": "foo"
        },
        "value": {
          "element": "string",
          "content": "fun"
        }
      }
    }
  ]
}

```

Type Element representing only a property list with key "foo" of value type `boolean` and with the key "bar" of value type `string` (JSON `{"foo": false, "bar": "fun"}`, `{"foo": true, "bar": ""}` etc.).

```json

{
  "element": "object",
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
      "element": "member",
      "content": {
        "key": {
          "element": "string",
          "content": "foo"
        },
        "value": {
          "element": "boolean",
          "content": false
        }
      }
    },
    {
      "element": "member",
      "content": {
        "key": {
          "element": "string",
          "content": "bar"
        },
        "value": {
          "element": "string",
          "content": "fun"
        }
      }
    }
  ]
}

```

---

### Enum Element

Type with domain of the union of values typed by Elements in the `enumerations` attribute. Also called tagged union or Σ-type.

#### Template
- `element` - `"enum"`
- `attributes`
  - `enumerations` ([Array][]) - List of Elements
  - `typeAttributes` ([Array][][[String][]])
    - `fixed` ([String][]) - Elements in `enumerations` SHALL be interpreted `fixed`.
  - `validation` - _reserved for future use_
  - `samples` ([Array][][[Element](#types)]]) - Alternative sample values for this Element; type of items in `samples` MUST match the type this Element describes
  - `default` ([Element](#types)) - Default value for this Element; type of `default` MUST match the type this Element describes
- `content` - An Element matching one of the Elements in the `enumerations` attribute

#### Examples

Type Element representing strings and numbers.

```json

{
  "element": "enum",
  "attributes": {
    "enumerations": [
      {
        "element": "string"
      },
      {
        "element": "number"
      }
    ]
  }
}

```

Type Element representing a specific string and all numbers.

```json

{
  "element": "enum",
  "attributes": {
    "enumerations": [
      {
        "element": "string",
        "attributes": {
          "typeAttributes": [
            "fixed"
          ]
        },
        "content": "Hello world!"
      },
      {
        "element": "number"
      }
    ]
  }
}

```

---

### Select Element

Type with domain of the union of values typed by [Option Elements](#option-element) in `content`. Select Element SHOULD only be used to denote alternative sets of properties in an [Object Element][].

#### Template
- `element` - `"select"`
- `attributes`
- `content` - Finite list of [Option Elements](#option-element)

---

### Option Element

Type with the domain of non-empty finite sets of [properties](#property). An Option Element MUST be contained in a [Select Element](#select-element) and its items MUST type [properties](#property).

#### Template
- `element` - `"option"`
- `attributes`
- `content` - Non-empty list of [Elements](#types) typing properties

---

### Extend Element

Type with domain of _merged_ Elements specified in `content`. All entries in `content` MUST type the same data structure type. [Ref Elements](#ref-element) encountered in `content` are dereferenced before merging.

Merging SHALL be defined based on the type of entries in `content` as follows:
- [Array Element][] - List concatenation
- [Object Element][] - Set union; if duplicit property keys are encountered during merging, all but the last SHALL be discarded; tooling SHOULD emit a warning in such a case.
- [Select Element](#select-element) - Option concatenation
- [String Element][] - Last entry in Extend Element SHALL be used, previous are ignored
- [Boolean Element][] - Last entry in Extend Element SHALL be used, previous are ignored
- [Number Element][] - Last entry in Extend Element SHALL be used, previous are ignored
- [Ref Element](#ref-element) - Substitute by referenced Element and apply one of the rules above

Extend Element SHOULD NOT be used to encode semantic inheritance; use the `id` meta property to define a named type and reference it through the child's `element` entry.

#### Template
- `element` - `"extend"`
- `content` - List of [Data Structure Elements](#data-structure-element-types) to be merged

---

### Ref Element

Ref Element MAY be used to reference elements in remote documents or elements in the local document.
The `ref` element _transcludes_ the contents of the element into the document in which it is referenced.

The following rules apply:

1. When referencing an element in the local document, the `id` of the element MAY be used
2. When referencing remote elements, an absolute URL or relative URL MAY be used
3. When a URL fragment exists in the URL given, it references the element with the matching `id` in the given document. The URL fragment MAY need to be URL decoded before making a match.
4. When a URL fragment does not exist, the URL references the root element
5. When `path` is used, it references the given property of the referenced element
6. When `path` is used in an element that includes the data of the pointer (such as with `ref`), the referenced path MAY need to be converted to a refract structure in order to be valid

Transclusion of a Ref Element SHALL be defined as follows:
1. If the Ref Element is held by an [Array][] Element and references an Array Element, its content entries SHALL be inserted in place of the Ref Element.
2. Else, if the Ref Element is held by an [Object][] Element and references an Object Element, its content entries SHALL be inserted in place of the Ref Element.
3. Otherwise, the Ref Element is substituted by the Element it references.

#### Template

- `element` - `"ref"`
- `attributes`
    - `path` (enum[String Element]) - Path of referenced element to transclude instead of element itself
        - element (default) - The complete referenced element
        - meta - The meta data of the referenced element
        - attributes - The attributes of the referenced element
        - content - The content of the referenced element
    - `validation` - _reserved for future use_
- `content` - URL to an Element in this document as a string

#### Examples

Elements MAY be referenced in remote or local documents.

##### Referencing Remote Element

```json
{
  "element": "ref",
  "content": "http://example.com/document#foo"
}
```

##### Referencing Local Elements

```json
{
  "element": "ref",
  "content": "foo"
}
```

##### Reference Parts of Elements

Given an element instance of:

```json
{
  "element": "array",
  "meta": {
    "id": "colors"
  },
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
```

And given an array where a reference is used as:

```json
{
  "element": "array",
  "content": [
    {
      "element": "string",
      "content": "blue"
    },
    {
      "element": "ref",
      "attributes": {
        "path": {
          "element": "string",
          "content": "content"
        }
      },
      "content": "colors"
    }
  ]
}
```

The resulting dereferenced array is:

```json
{
  "element": "array",
  "content": [
    {
      "element": "string",
      "content": "blue"
    },
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
```

### Link Element

Hyperlinking MAY be used to link to other resources, provide links to instructions on how to process a given element (by way of a [profile](#profiles) or other means), and may be used to provide meta data about the element in which it's found. The meaning and purpose of the hyperlink is defined by the link relation according to [RFC 5988](https://tools.ietf.org/html/rfc5988).

#### Template

- `element`: link (string, fixed)
- `attributes`
    - `relation` ([String][]) - Link relation type as specified in [RFC 5988](https://tools.ietf.org/html/rfc5988).
    - `href` ([String][]) - The URI for the given link
    - `validation` - _reserved for future use_

#### Example

The following shows a link with the relation of `foo` and the URL of `/bar`.

```json
{
  "element": "link",
  "attributes": {
    "relation":  {
      "element": "string",
      "content": "foo"
    },
    "href":  {
      "element": "string", 
      "content": "/bar"
    }
  }
}
```

---

## API Element Types

### Href ([String][])

The value of the `Href` type  SHOULD be resolved as a URI-Reference per [RFC 3986][] and MAY be a relative reference to a URI.
The value of the `Href` type MUST NOT be a URI Template.

### Templated Href ([String][])

The value of `Templated Href` type is to be used as a URI Template, as defined in [RFC 6570][].
The value of the `Templated Href` type is a template used to determine the target URI of the related resource or transition.
The value of the `Templated Href` type SHOULD be resolved as a URI-Reference per [RFC 3986][] and MAY be a relative reference to a URI.

### Href Variables (Object Type)

The definition is a Data Structure element `Object Type` where keys are respective URI Template variables.

#### Template

- `element`: hrefVariables (string, fixed)

### Data Structure (Base API Element)

Data structure definition using Data Structure elements.

#### Template

- `element`: dataStructure (string, fixed)
- `content` ([Data Structure Element](#data-structure-element-types))

### Asset (Base API Element)

Arbitrary data asset.

#### Template

- `element`: asset (string, fixed)
- `meta`
    - `classes` ([Array][])
        - `content` (array, fixed-type)
            - ([String][])
                - `content` (enum)
                    - messageBody (string) - Asset is an example of message-body
                    - messageBodySchema (string) - Asset is an schema for message-body
- `attributes`
    - `contentType` ([String][]) - Optional media type of the asset. When this is unset, the content type SHOULD be inherited from the `Content-Type` header of a parent HTTP Message Payload
    - `href` (Href) - Link to the asset
- `content` (string) - A textual representation of the asset

### Resource (Base API Element)

The Resource representation with its available transitions and its data.

#### Template

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

#### Template

- `element`: transition (string, fixed)
- `attributes`
    - `relation` - ([String][]) - Link relation type as specified in [RFC 5988][].

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

    - `contentTypes` ([Array][][[String][]]) - A collection of content types that MAY be used for the transition.
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

#### Template

- `meta`
    - `classes` ([Array][])
        - `content` (array, fixed-type)
            - ([String][])
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

#### Template

- `element`: category (string, fixed)
- `meta`
    - `classes` ([Array][])
        - `content` (array, fixed-type)
            - ([String][])
                - `content` (enum)
                    - api (string) - Category is a API top-level group.
                    - resourceGroup (string) - Category is a set of resource.
                    - dataStructures (string) - Category is a set of data structures.
                    - scenario (string) - Category is set of steps.
                    - transitions (string) - Category is a group of transitions.
                    - authSchemes (string) - Category is a group of authentication and authorization scheme definitions
- `attributes`
    - `metadata` ([Array][][API Metadata]) - Arbitrary metadata
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

#### Template

- `element`: copy (string, fixed)
- `attributes`
    - `contentType` ([String][]) - Optional media type of the content.
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

##### Template

- `element`: httpTransaction (string, fixed)
- `attributes`
    - `authSchemes` ([Array][][Base API Element]) - An array of authentication and authorization schemes that apply to the transaction
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

#### HTTP Headers ([Array][][Member Element])

Ordered array of HTTP header-fields.

##### Template

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

##### Template

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

##### Template

- `element`: httpRequest (string, fixed)
- `attributes`
    - `method` ([String][]) - HTTP request method. The method value SHOULD be inherited from a parent transition if it is unset.
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

##### Template

- `element`: httpResponse (string, fixed)
- `attributes`
    - `statusCode` ([Number][]) - HTTP response status code.


## Parse Result Element types


### Parse Result (Base API Element)

A result of parsing of an API description document.

#### Template

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

#### Template

- `element`: annotation (string, fixed)
- `meta`
  - `classes` ([Array][])
      - `content` (array, fixed-type)
          - ([String][])
              - `content` (enum)
                  - error (string) - Annotation represents an error
                  - warning (string) - Annotation represents a warning

- `attributes`
    - `code` ([Number][]) - Parser-specific code of the annotation.
    Refer to parser documentation for explanation of the codes.

    - `sourceMap` ([Array][][Source Map]) - Locations of the annotation in the source file.

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

#### Template

- `element`: sourceMap (string, fixed)
- `content` (array) - Array of byte blocks.
    - ([Array][]) - Continuous bytes block. A pair of byte index and byte count.
        - `content` (array, fixed-type)
            - ([Number][]) - Zero-based index of a byte in the source document.
                - attributes
                    - line - The line number the source map starts on.
                    - column - The column number of the line that the source map starts on.
            - ([Number][]) - Count of bytes starting from the byte index.
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

#### Template

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

#### Template

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

#### Template

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

---

## Profiles

The primary means by which users can provide semantic definitions and other meta information is through a profile. A profile MAY provide semantic information about an element and its data, it MAY provide specific instructions about elements such as how inheritance should work or how elements should be processed, and it MAY be used to modify understanding of existing elements in other profiles. The usage of a profile is not limited to these uses here, and SHOULD be left up to the profile author to define its use.

To point to a profile, you MAY use the [profile link relation](https://www.ietf.org/rfc/rfc6906.txt) as a meta link in your root element or in any other element. Profile links may also be found outside of the document itself in places like the [HTTP Link Header](http://www.w3.org/wiki/LinkHeader). Additionally, a profile link is not required in order to use the functionality a profile provides, as a media type MAY define the same things a profile.

Below is an example of how a profile link is used as a meta link.

```json
{
  "element": "foo",
  "meta": {
    "links": [
      {
        "element": "link",
        "attributes": {
          "relation": {
            "element": "string",
            "content": "profile"
          },
          "href": {
            "element": "string",
            "content": "http://example.com/profiles/foo"
          }
        }
      }
    ]
  },
  "content": "bar"
}
```

The example shows a `foo` element with a `profile` link. This profile link informs the parser this particular element is defined as part of the linked profile.

---


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

[String]: #string-element
[Number]: #number-element
[Boolean]: #boolean-element
[Array]: #array-element
[Object]: #object-element
[Member]: #member-element
