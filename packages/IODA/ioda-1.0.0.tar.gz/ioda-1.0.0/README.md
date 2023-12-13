# Inside Outside Detection (IODA)

## Abstract

### Background
Laparoscopic videos are increasingly being used for surgical artificial intelligence (AI) and big data analysis. The purpose of this study was to ensure data privacy in video recordings of laparoscopic surgery by censoring extraabdominal parts. An inside-outside-discrimination algorithm (IODA) was developed to ensure privacy protection whilst maximizing the remaining video data.

### Methods
IODAs neural network architecture was based on a pretrained AlexNet augmented with a long-short-term-memory. The data set for algorithm training and testing contained a total of 100 laparoscopic surgery videos of 23 different operations with a total video length of 207 hours (124 min ± 100 min per video) resulting in 18,507,217 frames (185,965 ± 149,718 frames per video). Each video frame was tagged either as abdominal cavity, trocar, operation site, outside for cleaning, or translucent trocar. For algorithm testing, a stratified 5-fold cross-validation was used.

### Results
The distribution of annotated classes were abdominal cavity 81.39%, trocar 1.39%, outside operation site 16.07%, outside for cleaning 1.08%, and translucent trocar 0.07%. Algorithm training on binary or all five classes showed similar excellent results for classifying outside frames with a mean F1-score of 0.96 ± 0.01 and 0.97 ± 0.01, sensitivity of 0.97 ± 0.02 and 0.0.97 ± 0.01 and a false positive rate of 0.99 ± 0.01 and 0.99 ± 0.01, respectively.

### Conclusion
IODA is able to discriminate between inside and outside with a high certainty. In particular, only a few outside frames are misclassified as inside and therefore at risk for privacy breach. The anonymized videos can be used for multi-centric development of surgical AI, quality management or educational purposes. In contrast to expensive commercial solutions, IODA is made open source and can be improved by the scientific community.

## Cross-validation of IODA
Cross-validation of IODA using a custom data set can be done using the "run_cross_validation.sh" script.
The experiments variable needs to be changed to the location of the custom data set.
Additional parameters, like batch size or the number of epochs, can be changed at the top of the script.

## Trained models
The repository contains the trained models from the cross-validation experiments described in the paper (trained_models/) as well as a model trained on the complete data set (src/IODA/IODA_model.pt).
As mentioned in the paper, the human annotator did make some mistakes annotating the videos.
These mistakes were corrected before training the model on the complete data set. 
The parameters used for training are: batch size = 32, step = 5, epochs = 5.

## Anonymizing videos using the docker image
A pre-built docker image of this repository can be found on [docker hub](https://hub.docker.com/r/a0schulze/ioda).
The repository also contains the script "anonymize.sh" that can be used to anonymize videos using the docker image.
The scripts expects the path to the folder that contains the video, the file name of the video and the file name
of the anonymized video that will be saved in the same folder.
Anonymization uses the model trained on the complete data set.

## PyPI
This project is also available on [PyPI](https://pypi.org/project/ioda).
