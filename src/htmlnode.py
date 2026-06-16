class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise(NotImplementedError)
    
    def props_to_html(self):
        resultstring = ""
        if not self.props:
            return resultstring
        else:
            for k,v in self.props.items():
                resultstring = resultstring + " "
                resultstring = resultstring + k + "=\"" + v + "\""
            return resultstring
        
    def __repr__(self):
        return f"HTML_Node({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)
    
    def to_html(self):
        if self.value == None:
            raise(ValueError)
        if self.tag == None:
            return str(self.value)
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"Leaf_Node({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props)

    def to_html(self):
        if self.tag == None:
            raise(ValueError)
        if self.children == None:
            raise(ValueError("This parents children are missing"))
        else:
            #tag = Continue here
            self.to_html()
