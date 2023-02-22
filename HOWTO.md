# How to use the WebNN API

The WebNN API is currently available in Chrome 113 and later behind a flag. It initially supports XNNPACK CPU backend on Windows x86 & x64 platforms.

1) Download [Chrome Desktop](https://www.google.com/chrome/) on Windows.
2) Navigate to `chrome://flags` and enable `Experimental Web Platform features`.
3) Navigate to [WebNN image classification sample page](https://webmachinelearning.github.io/webnn-samples/image_classification/).
4) Select "WebNN (CPU)" backend, "NHWC" layout and "MobileNet V2" model.
5) Check the classification result.

Here is an example of how to use the API:

```javascript
const operandType = {type: 'float32', dimensions: [2, 2]};
const context = await navigator.ml.createContext();
const builder = new MLGraphBuilder(context);
// 1. Create a computational graph 'C = 0.2 * A + B'.
const constant = builder.constant(operandType, new Float32Array(4).fill(0.2));
const A = builder.input('A', operandType);
const B = builder.input('B', operandType);
const C = builder.add(builder.mul(A, constant), B);
// 2. Compile it into an executable.
const graph = await builder.build({'C': C});
// 3. Bind inputs to the graph and execute for the result.
const bufferA = new Float32Array(4).fill(1.0);
const bufferB = new Float32Array(4).fill(0.8);
const bufferC = new Float32Array(4);
const inputs = {'A': bufferA, 'B': bufferB};
const outputs = {'C': bufferC};
const result = await context.compute(graph, inputs, outputs);
// The computed result of [[1, 1], [1, 1]] is in the buffer associated with
// the output operand.
console.log('Output value: ' + result.outputs.C);
// Note: the result.outputs.C buffer is different from the bufferC, but it
// shares the same backing memory allocation.
```

You should see something along the lines of:

```
Output value: 1,1,1,1
```