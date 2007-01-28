def xml_node_get_text(node):
    ans = ""
    for n in node.childNodes:
        if n.nodeType == n.TEXT_NODE:
            ans = ans + n.data
    return ans
