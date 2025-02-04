from convst.utils import apply_one_kernel_one_sample
import numpy as np
import pytest

def init_numpy(dims):
    return np.random.random_sample(dims)
    
##########################################
#                                        #
#             Test strides               #
#                                        #
##########################################

@pytest.mark.parametrize("dims, weights, length, bias, padding, dilation", [
    (20, np.array([1,1,-2]), 3, -0.235, 0, 3),
    (20, np.array([1,1,-2]), 3, -0.235, 1, 1)
])
def test_one_sample(dims, weights, length, bias, padding, dilation):
    X = init_numpy(dims).astype(np.float32)
    X2 = apply_one_kernel_one_sample(X, dims, weights, length,
                                     bias, dilation, padding)
    if padding > 0 :
        x_pad = np.zeros(dims + 2 * padding, dtype=np.float32)
        x_pad[padding:-padding] = X
    else:
        x_pad = X
    res0 = np.array([0],dtype=np.float32)
    for j in range(length):
        res0[0] += weights[j] * x_pad[0 + (j * dilation)]
    res0[0] += bias
    assert X2.shape[0] == dims - ((length - 1) * dilation) + (2 * padding)
    assert X2[0] == res0[0]
    
