import matplotlib
import matplotlib.pyplot as plt
import numpy as np

INCOME_PREMIUM_USER_PER_MONTH = 5
NUMBER_REQS_PER_USER_PER_MONTH = 40
NUMBER_REQS_PER_USER_PER_MONTH_FREE = 5

NUMBER_REQS_CHECKED_PER_EXPERT_PER_MONTH = 1000
PAYMENT_PER_EXPERT_PER_MONTH = 3000

FIXED_PAYMENT_PER_REQUEST_API = 0.0002
FIXED_PAYMENT_PER_MONTH = 275

RATIO_OF_FREE_USERS = 0.5

x = np.arange(1, 1000)

# number of expert checks required decreasses with the number of users
EXPERT_CHECK_RATIO = np.exp(-x / 1000)


costs = (
    # costs for free users API
    (
        NUMBER_REQS_PER_USER_PER_MONTH_FREE
        * FIXED_PAYMENT_PER_REQUEST_API
        * x
        * RATIO_OF_FREE_USERS
    )
    # costs for premium users API
    + (
        NUMBER_REQS_PER_USER_PER_MONTH
        * FIXED_PAYMENT_PER_REQUEST_API
        * x
        * (1 - RATIO_OF_FREE_USERS)
    )
    # fixed costs
    + FIXED_PAYMENT_PER_MONTH
    # costs for expert checks
    + (
        (x / NUMBER_REQS_CHECKED_PER_EXPERT_PER_MONTH * PAYMENT_PER_EXPERT_PER_MONTH)
        * EXPERT_CHECK_RATIO
    )
)


revenue = INCOME_PREMIUM_USER_PER_MONTH * x * (1 - RATIO_OF_FREE_USERS)

profit = revenue - costs
matplotlib.rcParams["axes.spines.left"] = False
matplotlib.rcParams["axes.spines.bottom"] = False
matplotlib.rcParams["axes.spines.right"] = False
matplotlib.rcParams["axes.spines.top"] = False
matplotlib.rcParams["lines.linewidth"] = 3

plt.grid(True, alpha=0.5)

plt.plot(x, costs, label="Costs")
plt.plot(x, revenue, label="Revenue")
plt.plot(x, profit, label="Profit")
plt.xlabel("Number of users")
plt.ylabel("Dollars ($)")
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.savefig("plot.png", dpi=300, bbox_inches="tight")

plt.figure()
plt.plot(x, EXPERT_CHECK_RATIO)
plt.xlabel("Number of users")
plt.ylabel("number of requests per month")
plt.savefig("plot_ratio.png", bbox_inches="tight")
