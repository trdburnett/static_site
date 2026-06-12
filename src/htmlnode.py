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
        if len(self.props) == 0:
            return resultstring
        else:
            for prop in self.props:
                resultstring.append(" ")
                resultstring.append(prop)
            return resultstring
        
    def __repr__(self):
        return f"HTML_Node({self.tag}, {self.value}, {self.children}, {props})"
    