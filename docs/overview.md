# API Elements Overview

**Version**: 1.0.0-rc1

## About API Elements

API Elements exist to provide a standard and canonical way to interact with the elements of an API. These elements are usually found in description formats, such as API Blueprint and Swagger/OpenAPI Format, and are used in various contexts. The idea is that consumers of API Elements can use this single format while providing support for the other formats.

An element is an individual piece that makes up an API. These can range from defining a resource or an HTTP request.

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
    - Resource
        - Copy
        - Data Structure
        - Category (Group of Transition Elements)
        - Transition
            - Copy
            - Transaction
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

This structure is based on [Refract][], and is expanded and defined better in the [element definition](./element.definitions.md) file.

Here is an example of what an element MAY look like.

```json
{
  "element": "string",
  "meta": {
    "id": "foo",
    "title": "Foo",
    "description": "My foo element"
  },
  "content": "bar"
}
```

Additional examples are provided throughout this documentation. As this shows, though, it allows for API Elements to only define data, but also metadata as well. This is especially important when providing source maps and adding human readable titles to values.

## Consuming Documents

As mentioned, for consumers, it is important to not couple code to the specific structure of an API Elements document. The common pattern is to reference elements by specifying a specific and strict path to those elements, but it is recommended to try to avoid this for sake of evolvability and safety.

Given that API Elements use [Refract][], the structure of the document is recursive by nature. When looking for specific elements, it is best then to walk the tree to look for a match. Querying the tree means that your code will be decoupled from not only from specific API description documents, but it will also be decoupled from the structure of those documents.

[Refract]: https://github.com/refractproject/refract-spec/blob/master/refract-spec.md
[MSON]: https://github.com/apiaryio/mson
[RFC 2119]: https://datatracker.ietf.org/doc/rfc2119/
