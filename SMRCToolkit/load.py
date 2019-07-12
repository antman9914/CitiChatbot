# coding: utf-8
import sys
sys.path.append("/root/ZX/SMRCToolkit")
from sogou_mrc.data.vocabulary import Vocabulary
from sogou_mrc.dataset.cmrc import CMRCReader, CMRCEvaluator
from sogou_mrc.model.qanet import QANET
import tensorflow as tf
import logging
from sogou_mrc.data.batch_generator import BatchGenerator
from Print import printT
tf.logging.set_verbosity(tf.logging.ERROR)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

data_folder = '/root/ZX/SMRCToolkit/cmrc_data_folder/'
dev_file = data_folder + "cmrc2018_dev.json"

reader = CMRCReader()
eval_data = reader.read(dev_file)

# print(eval_data)

evaluator = CMRCEvaluator(dev_file)

vocab = Vocabulary()
vocab_save_path='/root/SMRCToolkit/vocab_save_folder/vocab.json'
vocab.load(vocab_save_path) # load vocab from save path

test_batch_generator = BatchGenerator(vocab, eval_data, batch_size=60)

save_dir='/root/ZX/SMRCToolkit/model_save_folder'+'/best_weights'
model = QANET(vocab)
model.load(save_dir)
res = model.inference(test_batch_generator) # inference on test data
printT(res)