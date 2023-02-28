# Observations

## Cached

### ASCII vs. UTF-8

[comparison:_literal,_lines_0.pdf](search_tools/cache/ascii/literal/go/comparison/literal_lines_0.pdf)

[comparison:_literal,_lines_0.pdf](search_tools/cache/utf8/literal/go/comparison/literal_lines_0.pdf)

> `xs -j 1` is for UTF-8 slower than for ASCII (for both, regex and literal search):
>
> `Σέρλοκ` -> `b'\xce\xa3\xce\xad\xcf\x81\xce\xbb\xce\xbf\xce\xba'`
> 
> *For plain*:
> 
> every character starts with `b'\xce'` -> try searching the first byte first takes long since it will match every
> second byte.
>
> *For regex*:
> 
> Maybe RE2 searches the first byte first as well... need to figure this out