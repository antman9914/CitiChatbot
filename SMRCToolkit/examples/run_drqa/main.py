# coding: utf-8
from sogou_mrc.data.vocabulary import Vocabulary
from sogou_mrc.dataset.squad import SquadReader, SquadEvaluator
from sogou_mrc.model.drqa import DrQA
import logging
from sogou_mrc.utils.feature_extractor import FeatureExtractor
from sogou_mrc.data.batch_generator import BatchGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
data_folder = '../../data_folder'
embedding_folder = '../../embedding_folder'

# Prepare the dataset reader and evaluator.
# 准备数据集阅读器和鉴别器
print("step 1:准备数据集阅读器和鉴别器...")
train_file = data_folder + "train-v1.1.json"
dev_file = data_folder + "dev-v1.1.json"
reader = SquadReader()
train_data = reader.read(train_file)
eval_data = reader.read(dev_file)
evaluator = SquadEvaluator(dev_file)

# Build a vocabulary and load the pretrained embedding
# 构建词汇表并加载预训练嵌入
print("step 2:构建词汇表并加载预训练嵌入...")
vocab = Vocabulary(do_lowercase=False)
vocab.build_vocab(train_data + eval_data, min_word_count=3, min_char_count=10)
word_embedding = vocab.make_word_embedding(embedding_folder+"glove.840B.300d.txt")

# Use the feature extractor,which is only necessary when using linguistic features
# 用特征提取器。特征提取器只是在使用语言特征时才需要
print("step 3:用特征提取器(特征提取器只是在使用语言特征时才需要)...")
feature_transformer = FeatureExtractor(features=['match_lemma','match_lower','pos','ner','context_tf'],build_vocab_feature_names=set(['pos','ner']),word_counter=vocab.get_word_counter())
train_data = feature_transformer.fit_transform(dataset=train_data)
eval_data = feature_transformer.transform(dataset=eval_data)

# 构建用于训练和评估的批处理生成器，其中在使用语言特征时需要附加特征和特征词汇表
print("step 4:构建用于训练和评估的批处理生成器，其中在使用语言特征时需要附加特征和特征词汇表...")
train_batch_generator = BatchGenerator(vocab,train_data,training=True,batch_size=32,additional_fields=feature_transformer.features,feature_vocab=feature_transformer.vocab)
eval_batch_generator = BatchGenerator(vocab,eval_data,batch_size=32,additional_fields=feature_transformer.features,feature_vocab=feature_transformer.vocab)

# original paper adamax optimizer
# 导入内置模型并编译训练操作，调用train_and_evaluate等函数进行训练和评估
print("step 5:导入内置模型并编译训练操作，调用train_and_evaluate等函数进行训练和评估...")
model = DrQA(vocab, word_embedding,features=feature_transformer.features,feature_vocab=feature_transformer.vocab)
model.compile()
model.train_and_evaluate(train_batch_generator, eval_batch_generator,evaluator, epochs=40, eposides=2)
model.evaluate(eval_batch_generator,eval_data,evaluator)
print("finished")
