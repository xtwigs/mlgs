from cmath import inf
import torch


def gradient_attack(logits: torch.Tensor, x: torch.Tensor, y: torch.Tensor,
                    epsilon: float, norm: str = "2",
                    loss_fn=torch.nn.functional.cross_entropy):
    """
    Perform a single-step projected gradient attack (PGD) on the input x.

    Parameters
    ----------
    logits: torch.Tensor of shape [B, K], where B is the batch size and K is 
            the number of classes. 
        The logits for each sample in the batch.
    x: torch.Tensor of shape [B, C, N, N], where B is the batch size, C is the 
       number of channels, and N is the image dimension.
        The input batch of images. Note that x.requires_grad must have been 
        active before computing the logits (otherwise will throw ValueError).
    y: torch.Tensor of shape [B, 1]
        The labels of the input batch of images.
    epsilon: float
        The desired strength of the perturbation. That is, the perturbation 
        (before the projection step) will have a norm of exactly epsilon as 
        measured by the desired norm (see argument: norm). Therefore, epsilon
        implicitly fixes the step size of the PGD update.
    norm: str, can be ["1", "2", "inf"]
        The norm with which to measure the perturbation. E.g., when norm="1", 
        the perturbation (before the projection step) will have a L_1 norm of 
        exactly epsilon (see argument: epsilon).
    loss_fn: function
        The loss function used to construct the attack. By default, this is 
        simply the cross entropy loss.

    Returns
    -------
    torch.Tensor of shape [B, C, N, N]: the perturbed input samples.
    """
    norm = str(norm)
    assert norm in ["1", "2", "inf"]

    ##########################################################
    # YOUR CODE HERE

    class_prob = torch.nn.functional.softmax(logits, dim=1)
    loss = loss_fn(class_prob, y)
    loss.backward()
    gradients = x.grad

    if norm in ("1", "2"):
        norm_l2 = torch.linalg.norm(gradients, int(norm), dim=(1,2,3), keepdim=True)
        x_pert = x + epsilon*gradients/norm_l2
    
    elif norm == "inf":
        x_pert = x + epsilon*gradients.sign()
    
    x_pert = x_pert.clamp(0,1.0)

    ##########################################################

    return x_pert.detach()
