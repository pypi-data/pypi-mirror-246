# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 17:48:48 2019

@author: Jane Doe 2
"""

"""
First number is a Device Channel (IF5G(ch, dev_ch, rssi))
Numbers inside second dict are Channels.
"""

iw_rus = {
    32: {32: 1.0, 34: 0.5, 'Left':5150, 'Right':5170, 
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    34: {34: 1.0, 32: 1.0, 'Left': 5150, 'Right': 5190, 
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
    36: {36: 1.0, 38: 0.5, 42: 0.25, 50: 0.125, 'Left':5170, 'Right':5190,
           'DFS': False, 'BW': 20, 'TPC': True, 'SRD': False},
    38: {38: 1.0, 42: 0.5, 36: 1.0, 40: 1.0, 50: 0.25, 'Left':5170,'Right':5210,
           'DFS': False, 'BW': 40, 'TPC': True, 'SRD': False},
    40: {40: 1.0, 38: 0.5, 42: 0.25, 50: 0.125, 'Left':5190, 'Right':5210,
           'DFS': False, 'BW': 20, 'TPC': True, 'SRD': False},
    42: {
        42: 1.0,
        38: 1.0,
        48: 1.0,
        46: 1.0,
        44: 1.0,
        36: 1.0,
        40: 1.0,
        50: 0.5, 'Left':5170, 'Right':5250,
        'DFS': False,
        'BW': 80,
        'TPC': True,
        'SRD': False
    },
    44: {44: 1.0, 46: 0.5, 42: 0.25, 50: 0.125, 'Left':5210, 'Right':5230,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    46: {46: 1.0, 44: 1.0, 42: 0.5, 50: 0.25, 48: 1.0,'Left':5210, 'Right':5250,
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
    48: {48: 1.0, 46: 0.5, 42: 0.25, 50: 0.125, 'Left':5230, 'Right':5250,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    50: {
        50: 1.0,
        36: 1.0,
        38: 1.0,
        40: 1.0,
        42: 1.0,
        44: 1.0,
        46: 1.0,
        48: 1.0,
        52: 1.0,
        54: 1.0,
        56: 1.0,
        58: 1.0,
        60: 1.0,
        62: 1.0,
        64: 1.0, 'Left':5170, 'Right': 5330,
        'DFS': True,
        'BW': 160,
        'TPC': True,
        'SRD': False
    },
    52: {52: 1.0, 58: 0.25, 54: 0.5, 50: 0.125, 'Left':5250, 'Right':5270,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
           
    54: {54: 1.0, 58: 0.5, 56: 1.0, 50: 0.25, 52: 1.0, 'Left':5250, 'Right':5290,
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
           
    56: {56: 1.0, 54: 0.5, 50: 0.125, 58: 0.25, 'Left':5270, 'Right':5290,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    58: {
        58: 1.0,
        50: 0.5,
        52: 1.0,
        54: 1.0,
        56: 1.0,
        60: 1.0,
        62: 1.0,
        64: 1.0, 'Left': 5250, 'Right': 5330,
        'DFS': True,
        'BW': 80,
        'indoors': True,
        'TPC': True,
        'SRD': False
    },
    60: {60: 1.0, 50: 0.125, 58: 0.25, 62: 0.5, 'Left':5290, 'Right':5310,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
           
    62: {62: 1.0, 60: 1.0, 64: 1.0, 50: 0.25, 58: 0.5, 'Left': 5290, 'Right':5330,
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
           
    64: {64: 1.0, 50: 0.125, 58: 0.25, 62: 0.5, 'Left':5310, 'Right':5330,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
           
    68: {68: 1.0, 'Left':5330, 'Right':5350,'DFS': False, 'BW': 20, 'indoors': True, 
           'TPC': True, 'SRD': False},
    
    132: {132: 1.0, 134: 0.5, 138: 0.25, 'Left':5650, 'Right':5670,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},
     
    134: {134: 1.0, 132: 1.0, 136: 1.0, 'Left':5650, 'Right':5690,
            'DFS': False, 'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},        
            
    136: {136: 1.0, 134: 0.5, 138: 0.25, 'Left':5670, 'Right':5690,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},
            
    138: {138: 1.0, 136: 1.0, 134: 1.0, 132:1.0, 140:1.0, 142:1.0, 144:1.0,
            'Left':5650, 'Right':5730,
            'DFS': False, 'BW': 80, 'indoors': False, 'TPC': True, 'SRD': False},
            
    140: {140: 1.0, 138: 0.25, 142: 0.5,'Left':5690, 'Right':5710,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},
            
    142: {142: 1.0, 144: 1.0, 140: 1.0, 138: 0.5, 'Left':5690, 'Right':5730,
            'DFS': False, 'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},        
            
    144: {144: 1.0, 138: 0.25, 142: 0.5, 'Left':5710, 'Right':5730,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': False, 'SRD': False},
            
    149: {149: 1.0, 151: 0.5, 155: 0.25,'Left':5735, 'Right':5755,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': False, 'SRD': False},
            
    151: {151: 1.0, 153: 1.0, 155: 0.5, 149: 1.0, 'Left':5735, 'Right':5775,
            'DFS': False, 'BW': 40, 'indoors': False, 'TPC': False, 'SRD': False},
            
    153: {153: 1.0, 151: 0.5, 155: 0.25,'Left':5755, 'Right':5775,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': False, 'SRD': False},
    155: {
        155: 1.0,
        151: 1.0,
        153: 1.0,
        157: 1.0,
        159: 1.0,
        149: 1.0,
        114: 0.5,
        161: 1.0,
        'DFS': False,
        'BW': 80, 'Left': 5735, 'Right':5815,
        'indoors': True,
        'TPC': True,
        'SRD': False
           },
    157: {157: 1.0, 159: 0.5, 155: 0.25, 'Left':5775, 'Right':5795,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
            
    159: {159: 1.0, 155: 0.5, 157: 1.0, 161: 1.0, 'Left':5775, 'Right':5815,
            'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
            
    161: {161: 1.0, 159: 0.5, 155: 0.25, 'Left':5795, 'Right':5815,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
            
    165: {165: 1.0, 'Left':5815, 'Right':5835,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},   
}


iw_euro = {
    32: {32: 1.0, 34: 0.5, 'Left':5150, 'Right':5170, 
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    34: {34: 1.0, 32: 1.0, 'Left': 5150, 'Right': 5190, 
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
    36: {36: 1.0, 38: 0.5, 42: 0.25, 36: 1.0, 50: 0.125, 'Left':5170, 'Right':5190,
           'DFS': False, 'BW': 20, 'TPC': True, 'SRD': False},
    38: {38: 1.0, 42: 0.5, 36: 1.0, 40: 1.0, 50: 0.25, 'Left':5170,'Right':5210,
           'DFS': False, 'BW': 40, 'TPC': True, 'SRD': False},
    40: {40: 1.0, 38: 0.5, 42: 0.25, 50: 0.125, 'Left':5190, 'Right':5210,
           'DFS': False, 'BW': 20, 'TPC': True, 'SRD': False},
    42: {
        42: 1.0,
        38: 1.0,
        48: 1.0,
        46: 1.0,
        44: 1.0,
        42: 1.0,
        36: 1.0,
        40: 1.0,
        50: 0.5, 'Left':5170, 'Right':5250,
        'DFS': False,
        'BW': 80,
        'TPC': True,
        'SRD': False
    },
    44: {44: 1.0, 46: 0.5, 42: 0.25, 50: 0.125, 'Left':5210, 'Right':5230,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    46: {46: 1.0, 44: 1.0, 42: 0.5, 50: 0.25, 48: 1.0,'Left':5210, 'Right':5250,
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
    48: {48: 1.0, 46: 0.5, 42: 0.25, 50: 0.125, 'Left':5230, 'Right':5250,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    50: {
        50: 1.0,
        36: 1.0,
        38: 1.0,
        40: 1.0,
        42: 1.0,
        44: 1.0,
        46: 1.0,
        48: 1.0,
        52: 1.0,
        54: 1.0,
        56: 1.0,
        58: 1.0,
        60: 1.0,
        62: 1.0,
        64: 1.0, 'Left':5170, 'Right': 5330,
        'DFS': True,
        'BW': 160,
        'TPC': True,
        'SRD': False
    },
    52: {52: 1.0, 58: 0.25, 54: 0.5, 50: 0.125, 'Left':5250, 'Right':5270,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
           
    54: {54: 1.0, 58: 0.5, 56: 1.0, 50: 0.25, 52: 1.0, 'Left':5250, 'Right':5290,
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
           
    56: {56: 1.0, 54: 0.5, 50: 0.125, 58: 0.25, 'Left':5270, 'Right':5290,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
    58: {
        58: 1.0,
        50: 0.5,
        52: 1.0,
        54: 1.0,
        56: 1.0,
        60: 1.0,
        62: 1.0,
        64: 1.0, 'Left': 5250, 'Right': 5330,
        'DFS': True,
        'BW': 80,
        'indoors': True,
        'TPC': True,
        'SRD': False
    },
    60: {60: 1.0, 50: 0.125, 58: 0.25, 62: 0.5, 'Left':5290, 'Right':5310,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
           
    62: {62: 1.0, 60: 1.0, 64: 1.0, 50: 0.25, 58: 0.5, 'Left': 5290, 'Right':5330,
           'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True, 'SRD': False},
           
    64: {64: 1.0, 50: 0.125, 58: 0.25, 62: 0.5,
           'Left':5310, 'Right':5330,
           'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
           
    68: {68: 1.0, 
           'Left':5330, 'Right':5350,'DFS': False, 'BW': 20, 'indoors': True, 
           'TPC': True, 'SRD': False},
     
    96: {96: 1.0, 'DFS':True,  
           'Left':5470, 'Right':5490, 'BW': 20, 'indoors': True, 
           'TPC': True, 'SRD': False},      
      
    100: {100: 1.0, 102:0.5, 106:0.25,114:0.125, 'Left':5330, 'Right':5350,'DFS': True, 'BW': 20, 'indoors': False, 
           'TPC': True, 'SRD': False},   
            
    102: {102: 1.0, 100:1.0, 104:1.0, 106:0.5, 114:0.25,  
            'Left':5490, 'Right':5530,'DFS': True, 
            'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},      
    
    104: {104: 1.0, 102:0.5, 106:0.25,114:0.125,
            'Left':5510, 'Right':5530,'DFS': True, 
            'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},           
            
    106: {106: 1.0, 104:1.0, 102:1.0, 100:1.0, 108:1.0, 110:1.0, 112:1.0, 
            114: 0.5, 
            'Left':5490, 'Right':5570,'DFS': True, 
            'BW': 80, 'indoors': False, 'TPC': True, 'SRD': False},                  
  
    108: {108: 1.0, 110:0.5, 106:0.25, 114:0.125,  
            'Left':5530, 'Right':5550,'DFS': True, 
            'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},   
            
    110: {110: 1.0, 108:1.0, 106:0.5, 112:1.0, 114:0.25, 
            'Left':5530, 'Right':5570,'DFS': True, 
            'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},           
            
    112: {112: 1.0, 110:0.5,  114:0.125, 106:0.25, 
            'Left':5550, 'Right':5570,'DFS': True, 
            'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},           
        
    114: {114: 1.0, 100:1.0, 102:1.0, 104:1.0, 106:1.0, 108:1.0, 
            110:1.0, 112:1.0, 116:1.0, 118:1.0, 120:1.0, 122:1.0,
            124:1.0, 126:1.0, 128:1.0, 
            'Left':5490, 'Right':5650,'DFS': True, 
            'BW': 160, 'indoors': False, 'TPC': True, 'SRD': False},  
            
    116: {116: 1.0, 114:0.125, 118:0.5, 122:0.25, 
            'Left':5570, 'Right':5590,'DFS': True, 
            'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},           
     
    118: {118: 1.0, 116:1.0, 120:1.0, 122:0.5, 114:0.25,  
            'Left':5570,'Right':5610,'DFS': True, 
            'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},           
       
    120: {120: 1.0, 118:0.5, 114:0.125, 122:0.25, 
            'Left':5590, 'Right':5610,'DFS': True, 
            'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},           
     
    122: {122: 1.0, 120:1.0, 118:1.0, 116:1.0, 114:0.5, 124:0.25, 126:0.5,
            128:0.25, 
            'Left':5570, 'Right':5650,'DFS': True, 
            'BW': 80, 'indoors': False, 'TPC': True, 'SRD': False},           
     
    124: {124: 1.0, 126:0.5, 114:0.125, 122:0.25,
            'Left':5610, 'Right':5630,'DFS': True, 
            'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},           
    
    126: {126: 1.0, 124:1.0, 122:0.5, 114:0.25, 
            128:1.0,  
            'Left':5610, 'Right':5650,'DFS': True, 
            'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},           
   
    128: {128: 1.0, 126:0.5, 122:0.25, 114:0.125,  
            'Left':5630, 'Right':5650,'DFS': True, 
            'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},           
         
          
    132: {132: 1.0, 134: 0.5, 138: 0.25,
            'Left':5650, 'Right':5670,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},
     
    134: {134: 1.0, 132: 1.0, 136: 1.0, 138:0.5, 
            'Left':5650, 'Right':5690,
            'DFS': False, 'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},        
            
    136: {136: 1.0, 134: 0.5, 138: 0.25,
            'Left':5670, 'Right':5690,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},
            
    138: {138: 1.0, 136: 1.0, 134: 1.0, 132:1.0, 140:1.0, 142:1.0, 144:1.0,
            'Left':5650, 'Right':5730,
            'DFS': False, 'BW': 80, 'indoors': False, 'TPC': True, 'SRD': False},
            
    140: {140: 1.0, 138: 0.25, 142: 0.5,
            'Left':5690, 'Right':5710,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': True, 'SRD': False},
            
    142: {142: 1.0, 144: 1.0, 140: 1.0, 138: 0.5, 
            'Left':5690, 'Right':5730,
            'DFS': False, 'BW': 40, 'indoors': False, 'TPC': True, 'SRD': False},        
            
    144: {144: 1.0, 138: 0.25, 142: 0.5, 
            'Left':5710, 'Right':5730,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': False, 'SRD': False},
            
    149: {149: 1.0, 151: 0.5, 155: 0.25,
            'Left':5735, 'Right':5755,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': False, 'SRD': False},
            
    151: {151: 1.0, 153: 1.0, 155: 0.5, 149: 1.0, 
            'Left':5735, 'Right':5775,
            'DFS': False, 'BW': 40, 'indoors': False, 'TPC': False, 'SRD': False},
            
    153: {153: 1.0, 151: 0.5, 155: 0.25,
            'Left':5755, 'Right':5775,
            'DFS': False, 'BW': 20, 'indoors': False, 'TPC': False, 'SRD': False},
    155: {
        155: 1.0,
        149: 1.0,
        151: 1.0,
        153: 1.0,
        157: 1.0,
        159: 1.0,        
        161: 1.0,
        'DFS': False,
        'BW': 80, 'Left': 5735, 'Right':5815,
        'indoors': True,
        'TPC': True,
        'SRD': False
           },
    157: {157: 1.0, 159: 0.5, 155: 0.25, 'Left':5775, 'Right':5795,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
            
    159: {159: 1.0, 155: 0.5, 157: 1.0, 161: 1.0, 'Left':5775, 
            'Right':5815, 'DFS': False, 'BW': 40, 'indoors': True, 'TPC': True,
            'SRD': False},
            
    161: {161: 1.0, 159: 0.5, 155: 0.25, 'Left':5795, 'Right':5815,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
            
    165: {165: 1.0, 'Left':5815, 'Right':5835,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
            
    169: {169: 1.0, 'Left':5835, 'Right':5855,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False}, 
             
    173: {173: 1.0, 'Left':5855, 'Right':5875,
            'DFS': False, 'BW': 20, 'indoors': True, 'TPC': True, 'SRD': False},
}


iw_usa = {}

