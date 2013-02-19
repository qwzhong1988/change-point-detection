#! /usr/bin/python

# Generate some change-points for a list of given false positive rates, given
# some cpd scores.

from os import listdir, system
#FPR_LIST = [0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002,0.0021,0.0022,0.0023,0.0024,0.0025,0.0026,0.0027,0.0028,0.0029,0.003,0.0031,0.0032,0.0033,0.0034,0.0035,0.0036,0.0037,0.0038,0.0039,0.004,0.0041,0.0042,0.0043,0.0044,0.0045,0.0046,0.0047,0.0048,0.0049,0.005,0.0051,0.0052,0.0053,0.0054,0.0055,0.0056,0.0057,0.0058,0.0059,0.006,0.0061,0.0062,0.0063,0.0064,0.0065,0.0066,0.0067,0.0068,0.0069,0.007,0.0071,0.0072,0.0073,0.0074,0.0075,0.0076,0.0077,0.0078,0.0079,0.008,0.0081,0.0082,0.0083,0.0084,0.0085,0.0086,0.0087,0.0088,0.0089,0.009,0.0091,0.0092,0.0093,0.0094,0.0095,0.0096,0.0097,0.0098,0.0099,0.01]
FPR_LIST = [0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095]

KPRE = 300
GRANULARITY = 3
ALGORITHM = 'kliep'
ROOT_FOLDER = '/nfs/stak/students/a/andermic/Windows.Documents/Desktop/change-point-detection/results/30hz'
INPUT_PATH = ROOT_FOLDER + '/' + '%s_kpre%d' % (ALGORITHM, KPRE)
OUTPUT_FOLDER = 'predicted_changes_' + ALGORITHM
OUTPUT_PATH = ROOT_FOLDER + '/' + OUTPUT_FOLDER
if OUTPUT_FOLDER in listdir(ROOT_FOLDER):
    print 'There are existing results at %s.\n' % OUTPUT_PATH
    print 'These results will not be overwritten by this program, so delete them manually to continue.'
    #exit()
system('mkdir ' + OUTPUT_PATH)

score_files = [i for i in listdir(INPUT_PATH) if i[:6] == 'scores']
# Assume here that all score files contain the same number of entries
score_size = len(open(INPUT_PATH + '/' + score_files[1], 'r').readlines())

count = 0

for fpr in FPR_LIST:
    fpr_path = OUTPUT_PATH + '/' + str(fpr) 
    if str(fpr) not in listdir(OUTPUT_PATH):
        system('mkdir ' + fpr_path)

    fp_num = int(round(fpr*score_size))
    for score_file in score_files:
        cur_scores = [float(i) for i in open(INPUT_PATH + '/' + score_file, 'r').read().split('\n') if i != '']
        cur_scores = list(enumerate(cur_scores))
        cur_scores = [cur_scores[i] for i in range(len(cur_scores)) if i % GRANULARITY == 0]
        cur_scores.sort(key=lambda x:x[1], reverse=True)
        cur_scores = [(i[0] + KPRE + 1, i[1]) for i in cur_scores] #Add 1 to compensate for MATLAB's 1-based indexing
        cur_fps = 0
        have_changed = [True] + [False]*5 #For ticks 0,3600,7200,10880,14400,18000
        cps = []
        for score in cur_scores:
            changed_index = (score[0] - 1) / 3600
            if have_changed[changed_index]:
                cur_fps += 1
                if cur_fps > fp_num:
                    break
            else:
                have_changed[changed_index] = True
            cps.append(str(score[0]))
        cps.sort(key=lambda x: int(x)) 

        fstream = open(fpr_path + '/' + score_file[7:], 'w')
        fstream.write('ChangePointPredictions\n' + '\n'.join(cps))
        fstream.close()