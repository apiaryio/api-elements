# API Elements Overview

**Version**: 1.0.0-rc1

**Mime Type**: TBD

## About API Elements

The purpose of API Elements is to provide a single, unifying structure for describing APIs across all API description formats and serialization formats. There currently exists several formats one can choose when defining an API, from API Blueprint to Swagger—which is now known as the OpenAPI Format. There are also many serialization formats such as XML or JSON. Without a way to parse these formats to the same structure, developers are required to handle each format one-by-one, each in a different way and each translating to their internal domain model. This is tedious, time-consuming, and requires each maintainer to stay in step with every format they support.

API Elements solves this complex problem in a simple way. It allows parsers to parse to a single structure and allows tool builders to consume one structure for all formats.

If there is one thing API description formats have taught us, it is that a single contract provides the best and fastest way to design and iterate on an API. Developers building the API can move independently as they progress towards the defined contract found in the API Blueprint or Swagger document. Conversely, API consumers can build tools for consuming the API based on the API definition document.

This same pattern has proven to be just as valuable for building API description formats and tooling. API Elements is the contract for producing and consuming the many description and serialization formats and allows everyone to move quickly and independently.

## What is an Element?

API Elements is made up of many small elements that have a rich semantic meaning given their value and context. An element is an individual piece that makes up an API, and can range from defining a resource to providing an example of an HTTP request.

The API Elements project defines elements used for:

1. Describing an API
1. Describing data structures used within that API
1. Describing parse results when parsing API-related documents

These elements also seek to provide a way to decouple APIs and their semantics from the implementation details.

## Relationship of Elements

One purpose of the API Elements reference is to allow consumers to decouple their implementations from the structure of the document. Because of this, when consuming documents of API Elements, it is recommended to write code that queries the tree rather than looking for defined paths.

It is also helpful to know the relationship between elements. The list below shows the relationship between the elements in this reference, but does not specify how the structure must be built.

- Category (API)
    - Copy
    - Data Structure
    - Category (Group of Resource Elements)
    - Category (Group of Authentication and Authorization Scheme Definitions)
    - Category (Group of Resource Elements representing hosts)
    - Resource
        - Copy
        - Data Structure
        - Category (Group of Transition Elements)
        - Transition
            - Copy
            - HTTP Transaction
                - Copy
                - HTTP Request
                    - Copy
                    - Data Structure
                    - Asset
                - HTTP Response
                    - Copy
                    - Data Structure
                    - Asset

This main API Category element MAY also be wrapped in a Parse Result element for conveying parsing information, such as source maps, warnings, and errors.

## Basic Element

Every element defined with API Elements has four primary pieces of data.

- `element` (string) - defines the type of element used
- `meta` (object) - an object that includes metadata about the element
- `attributes` (object) - user-specified attributes for a given element
- `content` - value of the element based on its type

This structure defined in detail in the [Element Definitions](./element-definitions.html) document.

Here is an example of what an Element MAY look like serialized into JSON.

```json
{
  "element": "string",
  "meta": {
    "id": {
      "element": "string",
      "content": "foo"
    },
    "title": {
      "element": "string",
      "content": "Foo"
    },
    "description": {
      "element": "string",
      "content": "My foo element"
    }
  },
  "content": "bar"
}
```

Additional examples are provided throughout this documentation for specific API Elements. As this shows, though, it allows for API Elements to not only define data, but also metadata as well. This is especially important when providing source maps and adding human readable titles to values.

## Consuming Documents

As mentioned, for consumers, it is important to not couple code to the specific structure of an API Elements document. The common pitfall is to reference elements by specifying a specific and strict path to those elements, but it is recommended to try to avoid this for sake of evolvability and safety.

For example, to get the first HTTP Transaction element from an API Elements tree.

Relying on a fixed tree structure:

```js
const transaction = apielements.content[0].content[0].content[0].content[0].content[0]
```

Querying the tree in a way that does not use a strict path:

```js
import query from 'refract-query';
const transaction = query(apielements, {element: 'httpTransaction'})[0];
```

The structure of an API Elements document is recursive by nature. When looking for specific elements, it is best to walk the API Elements tree to look for a match. Querying the API Elements tree will decouple your code from specific API description syntax. Also, it decouples your code from the specific structure of these documents as long as they are semantically equivalent.

[MSON]: https://github.com/apiaryio/mson
[RFC 2119]: https://datatracker.ietf.org/doc/rfc2119/
