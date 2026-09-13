class HTMLNode():
    def __init__(self, tag: str|None = None, value: str|None = None, children: list["HTMLNode"]|None = None, props: dict[str, str]|None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self) -> str:
        raise NotImplementedError()
    def props_to_html(self) -> str:
        html = ""
        if self.props is None or len(self.props) == 0:
            return html
        for key in self.props:
            html = html + f' {key}="{self.props[key]}"'
        return html
    def __eq__(self, other: "HTMLNode"):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str]|None = None) -> None:
        super().__init__(tag = tag, value = value, props = props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.tag is "img":
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Props: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str]|None = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Nodes require a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent Nodes require children")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
