# neural-pdf-classification
---
Neural-pdf-classification is a proof of concept [classifier](https://en.wikipedia.org/wiki/Linear_classifier) for extracting data from PDF files (namely different parts of the document - titles headers and so on). It's built on top of a [feed forward neural network](https://en.wikipedia.org/wiki/Feedforward_neural_network) and is trained using [backward propagation of errors](https://en.wikipedia.org/wiki/Backpropagation).



#### Introduction

To understand how a neural network can classify a PDF document we need to make the document abstract. The document basically consists of a series of pages. These pages consist of characters, which in turn forms words, which in turn forms sentences. Each word (or combination of characters) is placed on a set position within the page. It is also of a certain height and width. We can break this down into the following.

##### Document
| Features      |
|:-------------:|
|Series of pages|

##### Page
| Features      |
|:-------------:|
|Series of words|
|Page number    |

##### Word
| Features               |
|:----------------------:|
|Position on x-axis      |
|Position on y-axis (row)|
|Width                   |
|Height                  |
|Font size               |
|Further styling         |
|Content                 |
|Character count         |

##### Interpreting the data

The above data is our raw data - this is what we have got to work with. Depending on what we want to extract from the document, we can do different things. Let us say that we want  to extract the title, headings and body. What raw values determine whether it's a heading or a title etc.?

This is where the task gets more difficult. What determines what values corresponds to i.e. a heading is subjective and will change from document to document. What this means is that there is no linear solution to the problem. We cannot simply say that "if the width is 150px and there are seven characters, it is a heading". 

What we can do, however, is to make assumptions. A title will most likely be the biggest text in the document. It is not likely to be used very often, and it can be relatively short. Understanding what i.e. a title may say in numbers gives us insight in the next step of the procedure.

##### Neural networks

Neural networks are known to solve hard problems by being taught what to do. Nerual networks are most likely as close to magic as programming will ever be. An in-depth guide on neural networks are out of the scope of this article but to simplify the matters, here is a short, simplified, overview.

![Cortesy of Wikimedia][neural network]

[neural network]: https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Colored_neural_network.svg/296px-Colored_neural_network.svg.png

[Neural networks](https://en.wikipedia.org/wiki/Artificial_neural_network) (in this case a [feed forward network](https://en.wikipedia.org/wiki/Feedforward_neural_network)) takes a set amount of numerical inputs, processes them through a set amount of hidden inputs and spews out the result from a set amount of numerical outputs. Each circle is called a neuron. The arrows (or synapses) between the neurons indicate how their values travel through the network. Each time the value passes a synapse, it is multiplied by a weight. This weight determines how important the value is to the output(s). The hidden neurons is where the magic happens. These intermediate neurons can vary in amount and the amount of hidden neurons are not related to the amount of inputs or outputs. There can also be numerous layers of neurons to let the network carry out more computations before finally giving us the output.

The weights can be hard coded or taught. How to teach a neural network to perform the correct calculations is a subject on it's own. In this article we'll settle with a simplified overview of backpropagation. Backpropagation feeds the network with an input and calculates how far off the network's output was from a predetermined result. This value is used to change the network's weights to slowly allow it to calculate better outputs.

#### Using a neural network to classify a document

As previously mentioned, a neural network takes a number of inputs and calculates a number of outputs. In our case of classifying what type of text a word is (title, heading, body etc.) we use the inputs from our raw data and expect the output to represent the type. 

##### Chosing the inputs

From the previously shown table, we can see that there are a number of inputs at our disposal.

| Features               |
|:----------------------:|
|Position on x-axis      |
|Position on y-axis (row)|
|Width                   |
|Height                  |
|Font size               |
|Further styling         |
|Content                 |
|Character count         |

Instead of feeding every input to the neural network, we are going to make some qualified assumptions of the importance of each input. Where on a page i.e. a title is found is of importance - it is not very likely to appear at the bottom of the sixth page. The size of the word / sentence is also of importance. A title will most likely be bigger than the rest of the text. What the title says, however is of less importance. A title is also likely to be as short as possible, therefore the character count can be considered important.

| Chosen inputs          |
|:----------------------:|
|Position on x-axis      |
|Position on y-axis (row)|
|Width                   |
|Height                  |
|Font size               |
|Further styling         |
|Character count         |

To make measurements the same for all types of pages, positions, width and height is calculated to be relative to that of the document. So instead of having a width of 500px we end up with a width of i.e. 0.5 (50%). 

##### Determining the wanted outputs

To train the network to calculate expected results, we have to give it inputs as well as an expected output. This is called a training set. Depending on the network model, amount of training items and learning iterations it can take from a couple of seconds to minutes to teach a neural network for this purpose. 

An easy way of producing a training set for your purpose is to review numerous documents, walking through the different parts and extract their raw data (the inputs we use) along with what they are (title, heading, body etc.). Doing this you may end up with a table containing items like the following.

|                        |"Learning how to bake" | "Step one" | 
|:----------------------:|:---------------------:|:----------:|
|Position on x-axis      |0.25                   |0.1         |
|Position on y-axis (row)|0.5                    |0.8         |
|Width                   |0.5                    |0.3         |
|Height                  |26                     |16          |
|Font size               |26                     |16          |
|Further styling         |-                      |-           |
|Character count         |20                     |8           |
|Type                    |Title                  |Heading     |

As previously mentioned, inputs and outputs are numerical. This makes it hard for us to expect "Title" as an output from the network. Instead we come up with an indexed table of outputs.

|Index|Text   |
|:---:|:-----:|
|0    |Body   |
|0.5  |Title  |
|1    |Heading|

Now that we know how a neural network use inputs and outputs to learn, we can teach it and check out the results.

##### Results <sup>1<sup>

|                      |1     |2    |3     |
|:--------------------:|:----:|:---:|:----:|
|Time to train         |19s   |14s  |10s   |
|Number of iterations  |10000 |1000 |10000 |
|Items in training set |520   |520  |520   |
|Input nuerons         |4     |4    |4     |
|Hidden neurons        |30    |15   |5     |
|Output neurons        |1     |1    |1     |
|accuracy              |99.7%|99.82%|98.75%|

As you can see, the accuracy of neural networks can be used to cope with many problems such as classification.

<sub>1. The training set is from a single document and the tests are carried out on the same document. The accuracy will however be similar if trained to recognise multiple different document layouts.</sub>

#### Further work

To improve the information extraction numerous steps can be taken. Topics from text could be taught and predicted, keywords could be extracted and so on.