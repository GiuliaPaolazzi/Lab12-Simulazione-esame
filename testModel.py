from model.model import Model

model=Model()

model.buildGraph('7.4', '7.8')

print(model.getNumNodes())
print(model.getNumEdges())