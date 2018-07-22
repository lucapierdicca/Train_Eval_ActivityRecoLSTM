import cv2
import os
import pickle

def video_dataset_stats():
    videos = []
    dataset_path = './PersonalCare'
    video_folders = os.listdir(dataset_path)
    video_folders = sorted([i for i in video_folders if i[0] == '_'])

    classlbl_to_id = {classlbl:id_ for id_,classlbl in enumerate(video_folders)}

    for classlbl in video_folders:
        for video in os.listdir(dataset_path+'/'+classlbl):
            curr_id = classlbl_to_id[classlbl]
            
            vcapture = cv2.VideoCapture(dataset_path+'/'+classlbl+'/'+video)
            n_frame = int(vcapture.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(vcapture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vcapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = vcapture.get(cv2.CAP_PROP_FPS)
            
            videos.append({'class_id':curr_id,
                            'n_frame':n_frame,
                            'size':str(width)+'x'+str(height),
                            'fps':fps})    

    agg = {}

    for i in videos:
        if i['class_id'] not in agg:
            agg[i['class_id']]=[(i['class_id'],i['fps'],i['n_frame'])]
        else:
            agg[i['class_id']].append((i['class_id'],i['fps'],i['n_frame']))

    return videos, agg



pickle_path = './PersonalCare/pickle'
dataset_detection_video = [pickle.load(open(pickle_path+'/'+video_pickle,'rb')) for video_pickle in os.listdir(pickle_path)]
    
classlbl_to_classid = {} 
classid = 0

for i in dataset_detection_video:
    classlbl = i['class_id'].lower().replace(' ','')
    if classlbl not in classlbl_to_classid:
        classlbl_to_classid[classlbl] = classid
        classid += 1

    i['class_id'] = classlbl_to_classid[classlbl]

    
with open('dataset_pickle_stats.csv','a') as file:   
    for i in dataset_detection_video:
        file.write(str(i['class_id'])+','+str(i['reduced_fps'])+','+str(i['final_nframes'])+'\n')


dataset_detection_video = [i for i in dataset_detection_video if (i['final_nframes']//i['reduced_fps']) >= 5]

with open('dataset_picklefiltered_stats.csv','a') as file:   
    for i in dataset_detection_video:
        file.write(str(i['class_id'])+','+str(i['reduced_fps'])+','+str(i['final_nframes'])+'\n')