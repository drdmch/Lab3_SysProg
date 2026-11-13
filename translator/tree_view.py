import json

PAGE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AST</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
body { font-family: monospace; }
line { stroke: #999; }
circle { fill: white; stroke: steelblue; stroke-width: 2px; }
text { font-size: 12px; }
</style>
</head>
<body>
<h3>AST: TITLE</h3>
<svg></svg>
<script>
var data = TREE_DATA;

var root = d3.hierarchy(data);
var height = root.leaves().length * 30;
var width = root.height * 150;
d3.tree().size([height, width])(root);

var svg = d3.select('svg').attr('width', width + 200).attr('height', height + 40);
var g = svg.append('g').attr('transform', 'translate(50, 20)');

g.selectAll('line').data(root.links()).enter().append('line')
  .attr('x1', function(d) { return d.source.y; })
  .attr('y1', function(d) { return d.source.x; })
  .attr('x2', function(d) { return d.target.y; })
  .attr('y2', function(d) { return d.target.x; });

g.selectAll('circle').data(root.descendants()).enter().append('circle')
  .attr('cx', function(d) { return d.y; })
  .attr('cy', function(d) { return d.x; })
  .attr('r', 5);

g.selectAll('text').data(root.descendants()).enter().append('text')
  .attr('x', function(d) { return d.y; })
  .attr('y', function(d) { return d.x - 8; })
  .attr('text-anchor', 'middle')
  .text(function(d) { return d.data.name; });
</script>
</body>
</html>
'''


def to_json(node):
    children = []
    for child in node.children:
        children.append(to_json(child))
    return {'name': node.label(), 'children': children}


def save_html(tree, title, path):
    page = PAGE.replace('TREE_DATA', json.dumps(to_json(tree), ensure_ascii=False))
    page = page.replace('TITLE', title)
    f = open(path, 'w', encoding='utf-8')
    f.write(page)
    f.close()
