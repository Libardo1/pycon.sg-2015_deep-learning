import numpy as np

import theano
from theano import tensor

#from blocks import initialization
from blocks.bricks import Identity, Linear, Tanh, MLP, Softmax
from blocks.bricks.lookup import LookupTable
from blocks.bricks.recurrent import SimpleRecurrent, Bidirectional, BaseRecurrent
from blocks.bricks.parallel import Merge
#from blocks.bricks.parallel import Fork

from blocks.bricks.cost import CategoricalCrossEntropy
from blocks.initialization import IsotropicGaussian, Constant

from blocks.graph import ComputationGraph
from blocks.filter import VariableFilter
from blocks.roles import INPUT, WEIGHT, OUTPUT

vocab_size=4
embedding_dim=3
hidden_dim=5
labels_size=10

max_sentence_length = 29
mini_batch_size = 128

batch_of_sentences = (max_sentence_length, mini_batch_size)

"""
Cost functions that respect masks for variable-length input (produced with Padding)

https://groups.google.com/forum/#!topic/blocks-users/O-S45G6tpNY
Including target sequence mask in cost function for recurrent network

https://github.com/mila-udem/blocks/issues/653
Cost for recurrent networks

See mask reshape/multiplication for costs somewhere near :
https://github.com/mila-udem/blocks/blob/master/blocks/bricks/sequence_generators.py#L277
"""

"""
Deep BiRNN for Blocks

https://gist.github.com/rizar/183620f9cfec98f2acd4

This has additional classes that together can build a deep, bidirectional encoder
"""

"""
stack of LSTM

https://github.com/mila-udem/blocks/pull/688  :: Accepted! (Code is in 'blocks' core repo)

Update blocks from git in env 
pip install git+git://github.com/mila-udem/blocks.git@master
   -- suggests it needs '--upgrade' : Meh
   -- Direct approach with uninstall first (works without the git+git knobs):
         pip uninstall blocks
         # Fortunately, this doesn't touch the blocks-extras code (?)
         pip install git+git://github.com/mila-udem/blocks.git@master
   -- Alternative is to clone separately, and do :
         python setup.py install  
         # or
         python setup.py develop
         
Usage of RecurrentStack :
https://github.com/sotelo/poet/blob/master/poet.py
         
"""

"""
Comments indicate that a reshaping has to be done, so let's think 
about sizes of the arrays...

"""

lookup = LookupTable(vocab_size, embedding_dim)

rnn = Bidirectional(SimpleRecurrent(dim=hidden_dim, activation=Tanh()))

### But will need to reshape the rnn outputs to produce suitable input here...
gather = Linear(name='hidden_to_output', input_dim=hidden_dim, output_dim=labels_size)

### But will need to reshape the rnn outputs to produce suitable input here...
labels = Softmax()


## Now for the application of these units

x = tensor.lmatrix('data')
# Define the shape of x specifically... 
# looks like it should be max_sentence_length rows and mini_batch_size columns
tensor.reshape(x, batch_of_sentences  )

rnn_outputs = rnn.apply(lookup.apply(x))

pre_softmax = gather.apply(rnn_outputs)

y_hat = labels.apply(pre_softmax)


y = tensor.lmatrix('targets')
tensor.reshape(y, batch_of_sentences )

cost = CategoricalCrossEntropy().apply(y.flatten(), y_hat)

## Less explicit version
#mlp = MLP([Softmax()], [hidden_dim, labels_size],
#          weights_init=IsotropicGaussian(0.01),
#          biases_init=Constant(0))





#print(encoder.prototype.apply.sequences)
#dir(encoder.prototype.apply.sequences)

#combine = Merge(input_dims=dict(), output_dim=labels_size)
#labelled = Softmax( encoder )


#probs = encoder.apply(lookup.apply(x))
#cg = ComputationGraph([probs])

#probs = mlp.apply(encoder.apply(lookup.apply(x)))
#cost = CategoricalCrossEntropy().apply(y.flatten(), probs)
#cg = ComputationGraph([cost])

#print(cg.variables)
print( VariableFilter(roles=[OUTPUT])(cg.variables) )

#dir(cg.outputs)
#np.shape(cg.outputs)

#mlp = MLP([Softmax()], [embedding_dim*2, labels_size],
#          weights_init=IsotropicGaussian(0.01),
#          biases_init=Constant(0))
#mlp.initialize()

#fork = Fork([name for name in encoder.prototype.apply.sequences if name != 'mask'])
#fork.input_dim = dimension
#fork.output_dims = [dimension for name in fork.input_names]
#print(fork.output_dims)

cost = aggregation.mean(generator.cost_matrix(x[:, :]).sum(), x.shape[1])
cost.name = "sequence_log_likelihood"
model=Model(cost)

