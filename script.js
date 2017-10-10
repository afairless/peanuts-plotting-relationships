 
// adapted from:
// https://bl.ocks.org/mbostock/4062045
// Mike Bostock’s Block 4062045
 
var width = 960
var height = 600

var svg = d3.select('div#container')
    .append('svg')
    .attr('preserveAspectRatio', 'xMinYMin meet')
    .attr('viewBox', '0 0 960 600')
    .classed('svg-container', true);

var simulation = d3.forceSimulation()
    .force('link', d3.forceLink().id(function(d) { return d.id; }))
    .force('charge', d3.forceManyBody().strength(-800))
    .force('center', d3.forceCenter(width / 2, height / 2));

d3.json('network.json', function(error, graph) {
  if (error) throw error;

  var link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(graph.links)
      .enter().append('line')
      //
      // best choice for relative importance of relationships to characters in the strip
      .attr('stroke-width', function(d) { return 22 * Math.sqrt(d.proportion_coappearances); });
      //
      // best choice for showing prominence of relationships in the strip
      //.attr('stroke-width', function(d) { return (d.number_coappearances) / 60; });
      //
      // alternatives
      //.attr('stroke-width', function(d) { return 35 * (d.proportion_coappearances); });
      //.attr('stroke-width', function(d) { return 20 * Math.cbrt(d.proportion_coappearances); });
      //.attr('stroke-width', function(d) { return Math.sqrt(d.number_coappearances) / 1; });

  var node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(graph.nodes)
      .enter().append('circle')
      .attr('fill', function(d) { return d3.color(d.colors); })
      //.attr('r', function(d) { return d.n_appears / 150; })
      .attr('r', function(d) { return 3 * Math.log(d.n_appears); })
      //.attr('r', function(d) { return Math.sqrt(d.n_appears) / 3; })
      .on('mouseover', onMouseover)
      .call(d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended));

  node.append('title')
      .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on('tick', ticked);

  simulation.force('link')
      .links(graph.links);

  function ticked() {
    link
        .attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; });

    node
        .attr('cx', function(d) { return d.x; })
        .attr('cy', function(d) { return d.y; });
  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}



function onMouseover(elemData) {
// adapted from:
// https://jsfiddle.net/e8kq7bdp/1/
    d3.select('svg').selectAll('circle')
        .select( function(d) { return d===elemData?this:null;})
}

