"""Test configurations for `backpack.core.extensions.secondorder`
that is shared among the following secondorder methods:
- Diagonal of Gauss Newton
- Diagonal of Hessian
- MC Approximation of Diagonal of Gauss Newton
Required entries:
    "module_fn" (callable): Contains a model constructed from `torch.nn` layers
    "input_fn" (callable): Used for specifying input function
    "target_fn" (callable): Fetches the groundtruth/target classes 
                            of regression/classification task
    "loss_function_fn" (callable): Loss function used in the model
Optional entries:
    "device" [list(torch.device)]: List of devices to run the test on.
    "id_prefix" (str): Prefix to be included in the test name.
    "seed" (int): seed for the random number for torch.rand
"""


import torch
from test.core.derivatives.utils import classification_targets, regression_targets

SECONDORDER_SETTNGS = []

###############################################################################
#                                   examples                                  #
###############################################################################

example = {
    "input_fn": lambda: torch.rand(3, 10),
    "module_fn": lambda: torch.nn.Sequential(torch.nn.Linear(10, 5)),
    "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(),
    "target_fn": lambda: classification_targets((3,), 5),
    "device": [torch.device("cpu")],
    "seed": 0,
    "id_prefix": "example",
}
SECONDORDER_SETTNGS.append(example)

SECONDORDER_SETTNGS += [
    # classification
    {
        "input_fn": lambda: torch.rand(3, 10),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Linear(10, 7), torch.nn.Linear(7, 5)
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="mean"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    {
        "input_fn": lambda: torch.rand(3, 10),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Linear(10, 7), torch.nn.ReLU(), torch.nn.Linear(7, 5)
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="sum"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    # Regression
    {
        "input_fn": lambda: torch.rand(3, 10),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Linear(10, 7), torch.nn.Sigmoid(), torch.nn.Linear(7, 5)
        ),
        "loss_function_fn": lambda: torch.nn.MSELoss(reduction="mean"),
        "target_fn": lambda: regression_targets((3, 5)),
    },
]

###############################################################################
#                         test setting: Convolutional Layers                  #
###############################################################################

SECONDORDER_SETTNGS += [
    {
        "input_fn": lambda: torch.rand(3, 3, 7, 7),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Conv2d(3, 2, 2),
            torch.nn.ReLU(),
            torch.nn.Flatten(),
            torch.nn.Linear(72, 5),
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="mean"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    {
        "input_fn": lambda: torch.rand(3, 3, 7, 7),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Conv2d(3, 2, 2, bias=False),
            torch.nn.ReLU(),
            torch.nn.Flatten(),
            torch.nn.Linear(72, 5),
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="mean"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    {
        "input_fn": lambda: torch.rand(3, 3, 8, 8),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Conv2d(
                3, 6, 2, stride=4, padding=2, padding_mode="zeros", dilation=3
            ),
            torch.nn.ReLU(),
            torch.nn.Flatten(),
            torch.nn.Linear(54, 5),
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="mean"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    {
        "input_fn": lambda: torch.rand(3, 3, 7, 7),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Conv2d(3, 2, 2, padding=0, stride=2),
            torch.nn.ReLU(),
            torch.nn.Flatten(),
            torch.nn.Linear(18, 5),
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="mean"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    {
        "input_fn": lambda: torch.rand(3, 2, 7, 7),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Conv2d(2, 3, 2, padding=0, dilation=2),
            torch.nn.ReLU(),
            torch.nn.Flatten(),
            torch.nn.Linear(75, 5),
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="mean"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
]