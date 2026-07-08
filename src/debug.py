from md2txt import markdown_to_blocks, block_to_block_type, BlockType, text_to_textnodes
from textnode import text_node_to_html_node
#print("Debug is empty")
page_blocks = (markdown_to_blocks("""# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev)."""))

#block_and_type = []
#for block in page_blocks:
#    block_and_type.append((block, block_to_block_type(block)))
#for item in block_and_type:
#    print(item)

paragraph_blocks = []
for block in page_blocks:
    if block_to_block_type(block) == BlockType.PARAGRAPH:
        paragraph_blocks.append(block)
for block in paragraph_blocks:
    #print(block)
    paragraph_text_nodes = text_to_textnodes(block)
for node in paragraph_text_nodes:
    #print(node)
    print(text_node_to_html_node(node))