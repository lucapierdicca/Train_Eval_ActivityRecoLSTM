import json
import os
import cv2


annotations = json.load(open('./Personal_Care/activity_net.v1-3.min.json','r'))


dataset_path = './Personal_Care'
video_folders = os.listdir(dataset_path)
video_folders = sorted([i for i in video_folders if i[0] == '_'])

dataset_video_annotations = {}

for classlbl in video_folders:
    for video in os.listdir(dataset_path+'/'+classlbl):
    	vcapture = cv2.VideoCapture(dataset_path+'/'+classlbl+'/'+video)
    	n_frame = int(vcapture.get(cv2.CAP_PROP_FRAME_COUNT))
    	fps = vcapture.get(cv2.CAP_PROP_FPS)

    	curr_ann = annotations['database'][video[:video.find('.')]]['annotations']
    	for j in curr_ann:
    		segment_time = int(j['segment'][1] - j['segment'][0])
    		segment_frame = fps*segment_time
    		j['segment_frame'] = segment_frame

    	dataset_video_annotations[video[:video.find('.')]] = {'annotations': curr_ann,
										'duration': annotations['database'][video[:video.find('.')]]['duration'],
										'n_frame':n_frame,
										'fps':fps}


tot_frames = 0
tot_segm_frames = 0
for i in dataset_video_annotations.values():
	for j in i['annotations']:
		tot_segm_frames = tot_segm_frames + j['segment_frame']
	tot_frames = tot_frames + i['n_frame']



n_segm = sorted([len(i['annotations']) for i in dataset_video_annotations.values()])


'''
import pickle
import matplotlib.pyplot as plt


losses = pickle.load(open('losses_.pickle','rb'))
#losses_cooc = pickle.load(open('losses_cooc.pickle','rb'))

plt.subplot(2,1,1)
plt.plot(losses['train_loss'], label='train_boo_loss')
plt.plot(losses['test_loss'], label='test_boo_loss')
#plt.plot(losses_cooc['train_loss'], '--', color='blue', label='train_cooc_loss')
#plt.plot(losses_cooc['test_loss'], '--', color='orange',label='test_cooc_loss')
plt.legend(loc='upper left')

plt.subplot(2,1,2)
plt.plot(losses['train_acc'], label='train_boo_acc')
plt.plot(losses['test_acc'], label='test_boo_acc')
#plt.plot(losses_cooc['train_acc'], '--', color='blue',label='train_cooc_acc')
#plt.plot(losses_cooc['test_acc'], '--', color='orange', label='test_cooc_acc')
plt.legend(loc='upper left')
plt.xlabel('epoch')
plt.show()
'''