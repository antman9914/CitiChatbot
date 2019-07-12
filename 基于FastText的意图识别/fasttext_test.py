import fastText.FastText as ff

classifier = ff.load_model('data/try.model')
result_test = classifier.test('data/test.txt')[1]
print(result_test)