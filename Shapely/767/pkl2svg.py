#!Python

import shapely
import shapely.geometry
import pickle, sys, json

class Parameters:
	def __init__(self):
		self.hatch_distance=0.75
		self.bb=list(map(str,(1.9, 0.7, 12, 9.5)))
		self.line_width=0.02
		
params=Parameters()

print('shapely version: '+shapely.__version__)

ifname=sys.argv[1]

if ifname.endswith('pkl'):
	import shapely.wkt
	outline=pickle.load(open(ifname,'rb'))
	ofname=ifname.replace('.pkl','.svg')
	wkt_ofname=ifname.replace('.pkl','.wkt')
	wkt_of=open(wkt_ofname,'w')
	wkt_of.write(shapely.wkt.dumps(outline))
	geo_ofname=ifname.replace('.pkl','.geo')
	geo_of=open(geo_ofname,'w')
	geo_of.write(json.dumps(shapely.geometry.mapping(outline)))
elif ifname.endswith('wkt'):
	import shapely.wkt
	outline=shapely.wkt.loads(open(ifname,'r').read())
	ofname=ifname.replace('.wkt','.svg')
elif ifname.endswith('geo'):
	outline=shapely.geometry.shape(open(ifname,'r').read())
	ofname=ifname.replace('.wkt','.svg')
else:
	sys.stderr.write('Cannot read format of "%s"\n'%ifname)
	sys.exit(1)


offset=outline.buffer(-params.hatch_distance,join_style=shapely.geometry.JOIN_STYLE.mitre,resolution=3)


of=open( ofname, 'w' )

of.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="'+" ".join(params.bb)+'">\n')
of.write(outline.svg().replace('stroke-width="2.0"','stroke-width="%f"'%params.line_width))
of.write(offset.svg().replace('stroke-width="2.0"','stroke-width="%f"'%params.line_width))
of.write('</svg>\n')

