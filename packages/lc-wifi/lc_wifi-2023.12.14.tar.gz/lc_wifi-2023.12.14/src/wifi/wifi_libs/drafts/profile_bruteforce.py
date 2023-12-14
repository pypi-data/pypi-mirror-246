import sys, os
import random
import argparse
import cProfile, pstats

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import networkx as nx

from collections import OrderedDict
class OrderedNodeGraph(nx.Graph):
	node_dict_factory=OrderedDict

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from BruteForceG2 import possible_channels_quality
import MetaGreedy as G2MG

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-N","--radars_number", type=int, default=1,
                        help="Number of radars in cluster (default 1)")
	parser.add_argument("--aliens_number", type=int, default=3,
                        help="Number of aliens per radar (default 3)")
	parser.add_argument("--upper_channel", type=int, default=13,
						help="The maximum possible Wi-Fi channel (default 13)")
	parser.add_argument("--random_rssi", type=bool, default=True,
						help="Defines to randomize RSSI or not (default True)")
	return parser.parse_args()


def make_radars(args):
	radars_l = [{'cpeid': i+100,
			     'channel': 1,
				 'upper_channel': args.upper_channel,
				 'qual_current': None} 
				   			for i in range(args.radars_number)]
	return radars_l

def make_devices(args, radars_l):
	devices_l = []
	for radar in radars_l:
		for device in radars_l:
			if radar['cpeid'] != device['cpeid']:
				devices_l.append({'radar_cpeid': radar['cpeid'], 
			  	  				  'dev_cpeid': device['cpeid'], 
			  	  				  'channel': 1, 
			  	  				  'rssi': None, 
			  	  				  'channel_width': 20, 
			  	  				  'standard': 4})
	for device_0 in devices_l:
		if device_0["rssi"] == None:
			if args.random_rssi:
				RSSI = -random.randint(46, 101)
			else:
				RSSI = -62
			for device_1 in devices_l:
				a = device_0["dev_cpeid"]
				b = device_1["radar_cpeid"]
				c = device_1["dev_cpeid"]
				d = device_0["radar_cpeid"]
				if a == b and c == d: 
					device_1["rssi"] = device_0["rssi"] = RSSI
	return devices_l


def add_aliens(args, radars_l, devices_l):
	Na = args.aliens_number
	for radar in radars_l:
		for i in range(Na):
			devices_l.append({'radar_cpeid': radar['cpeid'], 
							  'dev_cpeid': str(random.randint(200, 209)), 
							  'channel': random.randint(1, 13), 
							  'rssi': -random.randint(56, 111),
							  'channel_width': 20, 
							  'standard': 4})
	return devices_l

def draw_cluster(radars_l, devices_l):
	G = nx.Graph()
	checked = []
	for device_0 in devices_l:
		for device_1 in devices_l:
			if device_1["dev_cpeid"] not in checked: 
				if device_0["radar_cpeid"] == device_1["radar_cpeid"]:			
					G.add_edge(device_0["radar_cpeid"], device_1["dev_cpeid"],
															rssi=device_0["rssi"],
															channel=device_1["channel"])
		checked.append(device_0["radar_cpeid"])

	friends = [(u, v) for (u, v, d) in G.edges(data=True) if int(v) < 200]

	aliens_l = []
	for radar in radars_l:
		l = [(u, v) for (u, v, d) in G.edges(data=True) 
							if (int(v) >= 200) and (u == radar["cpeid"])]
		aliens_l.append(l)

	# nodes
	fr_nodes = [u for (u, v, d) in G.edges(data=True) if u in [r["cpeid"] for r in radars_l]]
	al_nodes = [v for (u, v, d) in G.edges(data=True) if int(v) >= 200]
	al_labels = {v:"Ch: "+str(d["channel"]) for (u, v, d) in G.edges(data=True) if int(v) >= 200}
	edge_labels = {(u,v):d["rssi"] for (u, v, d) in G.edges(data=True)}

	shells = [[u for u in fr_nodes], [v for v in al_nodes]]
	pos = nx.shell_layout(G, nlist=shells) # positions for all nodes
	
	nx.draw_networkx_nodes(fr_nodes, pos, node_size=1500)
	nx.draw_networkx_nodes(al_nodes, pos, node_size=1500, node_color='r')

	pos_higher = {}
	y_off = .1  # offset on the y axis

	for k, v in pos.items():
		pos_higher[k] = (v[0], v[1]+y_off)
	nx.draw_networkx_labels(al_nodes, pos_higher, labels=al_labels)


	# edges
	nx.draw_networkx_edges(G, pos, edgelist=friends,
	                       width=6)

	colors_l = list(colors._colors_full_map.values())
	for idx, alien in enumerate(aliens_l):
		nx.draw_networkx_edges(G, pos, edgelist=alien,
	                       width=4, alpha=0.5, edge_color=colors_l[idx], style='dashed')

	# labels
	nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
	nx.draw_networkx_edge_labels(G, pos_higher, edge_labels=edge_labels, font_weight='light')


	plt.axis('off')
	plt.show()


def run(radars_l, devices_l, option='all'):
	pr = cProfile.Profile()
	pr.enable()
	res = possible_channels_quality(radars_l, devices_l, what_cmbs=option)
	pr.disable()
	ps = pstats.Stats(pr, stream=sys.stdout)
	ps.print_stats()

	return res


if __name__ == '__main__':
	args = parse_args()
	radars_l = make_radars(args)
	devices_l = make_devices(args, radars_l)
	devices_l = add_aliens(args, radars_l, devices_l)
	if args.radars_number < 10:
		draw_cluster(radars_l, devices_l)
		print("Test #1 (channel quality based)")
		res = run(radars_l, devices_l, option='channel quality based')
		print(res)
	if args.radars_number < 6:
		print("Test #2 (all)")
		res = run(radars_l, devices_l)
		print(res)

	print("NEW ALGO")	
	pr = cProfile.Profile()
	pr.enable()
	res = G2MG.run(radars_l, devices_l)
	pr.disable()
	ps = pstats.Stats(pr, stream=sys.stdout)
	ps.print_stats()
	print(res)


