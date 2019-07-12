# coding: utf-8
import sys
sys.path.append("/root/ZX/SMRCToolkit")
from sogou_mrc.data.vocabulary import Vocabulary
from sogou_mrc.dataset.squad import SquadReader, SquadEvaluator
from sogou_mrc.dataset.cmrc import CMRCReader,CMRCEvaluator
import tensorflow as tf
import logging

tf.logging.set_verbosity(tf.logging.ERROR)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
data_folder = '/root/ZX/SMRCToolkit/cmrc_data_folder/'
embedding_folder = '/root/ZX/SMRCToolkit/embedding_folder'
train_file = data_folder+"cmrc2018_train.json"
dev_file = data_folder+"cmrc2018_dev.json"

reader = CMRCReader()
print("CMRCReader created")
train_data = reader.read(train_file)
print("train_data read")
eval_data = reader.read(dev_file)
print("eval_data read")
evaluator = CMRCEvaluator(dev_file)
print("evaluator created")