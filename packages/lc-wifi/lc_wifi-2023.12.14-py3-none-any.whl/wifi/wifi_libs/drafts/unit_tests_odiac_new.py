import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import unittest
import ODIAC24
#list данных, включающий выбранный радар для оптимизации
#а также содержит соседей,которых он видит в окружении
Data = [
{
'cpeid': '001095-14B7F887C74E', 
'channel': 1, 
'upper_channel': 11, 
'qual_current': 0.13431986290961834, 
'target_channel': 13, 
'type': 'R', 
'rssi': 0
}, 
{
'cpeid': '001095-B42A0EE13276', 
'channel': 1, 
'upper_channel': 11, 
'qual_current': 0.3279201891941372, 
'target_channel': 3, 
'type': 'F', 
'rssi': -73, 
'bandwidth': 20, 
'standard': 4
}, 
{
'cpeid': '001095-48003378DC9C', 
'channel': 1, 
'upper_channel': 11, 
'qual_current': 0.21535009107090458, 
'target_channel': 6, 
'type': 'F', 
'rssi': -73, 
'bandwidth': 20, 
'standard': 4
}
]

# выбранный радар
defRadar = {
'channel': 1, 
'rssi': 0, 
'bandwidth': 20, 
'standard': 4, 
'type': 'F', 
'ftype': 'R'
}

#детальное описание соседей в радаре, 
#например в Data сосед [1,-60,20,4,0,'F'], 
#соответственно его эфир описан под ключом серийного номера, но в примере просто 1
Neighbours = {
'001095-B42A0EE13276': [
{
'channel': 1, 
'rssi': -73, 
'bandwidth': 20, 
'standard': 4, 
'type': 'F', 
'ftype': 'F'
}, 
{
'channel': 1, 
'rssi': -73, 
'bandwidth': 20, 
'standard': 4, 
'type': 'F', 
'ftype': 'F'
}, 
{
'channel': 1, 
'rssi': 0, 
'bandwidth': 20, 
'standard': 4, 
'type': 'F', 
'ftype': 'R'
}, 
{
'channel': 1, 
'rssi': 0, 
'bandwidth': 20, 
'standard': 4, 
'type': 'R', 
'ftype': 'F'
}
], 
'001095-48003378DC9C': [
{
'channel': 1, 
'rssi': -73, 
'bandwidth': 20, 
'standard': 4, 
'type': 'F', 
'ftype': 'F'
}, 
{
'channel': 1, 
'rssi': -73, 
'bandwidth': 20, 
'standard': 4, 
'type': 'F', 
'ftype': 'F'
}, 
{
'channel': 1, 
'rssi': 0, 
'bandwidth': 20, 
'standard': 4, 
'type': 'F', 
'ftype': 'R'
}, 
{
'channel': 1, 
'rssi': 0, 
'bandwidth': 20, 
'standard': 4, 
'type': 'R', 
'ftype': 'F'
}
]
}
#сортировка по индексам ,
#а именно в качестве радара, которого мы пытаемся опттмизировать ,
# выбираем количество лучших коэффициентов и возвращаем их индекс,
# котрый равен номеру канала
bestchannels = [i[0] for i in sorted(enumerate([0.3333333333333333, 0.6330437177998064, 0.6767235543377977, 0.7720906552613077, 0.805356326421322, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), key=lambda x:x[1], reverse=True)]
#количество лучших каналов для перестановок , 
#что в дальнейшем вернет массив из 5 лучших вариантов
interval = 5
#коэффициент улучшения(%) при условии, 
#если он >= мы будем рассматривать стоит ли вообще переходить на канал или нет
koeff=10
curr_radar_quality = {
					'radar_channel': 1, 
					'radar_curr_qual': 0.3333333333333333
					}
friends_quaility = {
					'001095-B42A0EE13276': 
							{'radar_channel': 1, 
							'radar_curr_qual': 0.25}, 
					'001095-48003378DC9C': 
							{'radar_channel': 1, 
							'radar_curr_qual': 0.25}
							}
class CheckTestCases(unittest.TestCase):
	def test_RadarQualityCoefficients(self):
		self.assertEqual(ODIAC24.RadarQualityCoefficients(Data),
			[0.7830149853634231, 0.3846153846153846, 0.47619047619047616, 0.5882352941176471, 0.9090909090909091, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

	def test_FriendsRadarCoefficiebts(self):
		self.assertEqual(ODIAC24.FriendsRadarCoefficients(Neighbours),{'001095-B42A0EE13276': {'radar_channel': 1, 'radar_curr_qual': 0.6917416406224042}, '001095-48003378DC9C': {'radar_channel': 1, 'radar_curr_qual': 0.6917416406224042}})

	#def test_ChangeChRadar(self):
	#	self.assertEqual(ODIAC24.ChangeChRadar(defRadar,Neighbours,Data,curr_radar_quality,friends_quaility,koeff,bestchannels, interval),{'current_radar': 6, 'radar_curr_qual': 1.0, '001095-B42A0EE13276': {'radar_curr_qual': 0.25, 'radar_channel': 1}, '001095-48003378DC9C': {'radar_curr_qual': 0.25, 'radar_channel': 1}})
		


if __name__ == '__main__':
    unittest.main()
