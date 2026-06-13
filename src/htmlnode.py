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
    