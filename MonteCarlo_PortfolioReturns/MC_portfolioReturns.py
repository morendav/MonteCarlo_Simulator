#######################################
# Discount a future cash flow back by periods
#
# Options (parameters)
#
# Example:
#       python3 ./Bond_Schedule.py -v 100 0 -c 0.06 -s "fullyAmoritized" -n 12 -y 15
#
#       Providing a schedule of payments for a fullyamoritized bond, with effective monthly compounding rate of 6%, over 15 years.
#           Bond Present Value = 100, Future value = 0
#           rate = 6% annualized rate
#
#######################################
###     CodeBlock: Modules & Init Variables
#######################################
import numpy, random
import statistics as s
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter




### Monte Carlo - Config Variables
portfolio_size = 25                     ### the size of the holding portfolio
iterations = 10000                         ### the number of Monte  Calro sampling for the current model


### Read the sampling NPVs into memory
file = '/Users/z001mc0/Desktop/MonteCarloSim/Studio_Portfolio_Sampling.csv'     ### portfolio distributions, NPV calculcated
file_out = '/Users/z001mc0/Desktop/MonteCarloSim/wiMonteCarlo_PSize' + str(portfolio_size) + '_SSize' + str(iterations) + '.csv'
figure_out = '/Users/z001mc0/Desktop/MonteCarloSim/wiMonteCarlo_PSize' + str(portfolio_size) + '_SSize' + str(iterations) + '.png'


total_sample = pd.read_csv(file)
MC_output = pd.DataFrame()

### create the Monte Carlo output dataframe
column_names = ["TotalNetReturn","OnlyPositiveReturn"]
MC_Model_Returns = pd.DataFrame(columns = column_names)





#######################################
###     Function for NPV
###               net total return in total portfolio
###               and optionality (only investing in postiive NPV at the end of the holding period)
#######################################
def npv_portfolio (sample, col):
    ### Build dictionary based on column names, i.e. dataframe headers
    return_dict_output = {
    # col[0] : sample.sum(),
    # col[1] : sample [sample > 0].sum()

    ### only postitive Reccs
    col[0] : sample.sum() - (2*portfolio_size),
    col[1] : sample [sample > 0].sum() - (2*portfolio_size)
    }
    return return_dict_output





#######################################
###     Monte Carlo Simulation
#######################################
### Iterate over MC simulation size
for i in range(iterations):
    # sample the entire dataframe read from XL
    portfolio = total_sample['NPV'].sample(n=portfolio_size, random_state=i)
    # pass the sample through our NPV portfolio function
    port_return = npv_portfolio (portfolio, column_names)
    # build our MC return model
    MC_Model_Returns = MC_Model_Returns.append(port_return, ignore_index = True)
    print(i)

### Stats of model
net_mean = s.mean(MC_Model_Returns["TotalNetReturn"])
positive_mean = s.mean(MC_Model_Returns["OnlyPositiveReturn"])





#######################################
###     Plot MonteCarlo Simulation
#######################################
### Create x-axis limit
bins = numpy.linspace(MC_Model_Returns["TotalNetReturn"].min(), MC_Model_Returns["OnlyPositiveReturn"].max(), int(iterations/100))
### Create subplot 1: Total return vs Positive return NPV of portfoloio holdings over n iterations
ax1 = plt.subplot(2, 1, 1)
plt.hist(MC_Model_Returns["TotalNetReturn"], bins, alpha=0.5, color = 'r', label='Total Sample Portfolio Return', weights=numpy.ones(len(MC_Model_Returns["TotalNetReturn"])) / len(MC_Model_Returns["TotalNetReturn"]))
plt.hist(MC_Model_Returns["OnlyPositiveReturn"], bins, alpha=0.5, color = 'g', label='NPV, Only Positive Assets', weights=numpy.ones(len(MC_Model_Returns["OnlyPositiveReturn"])) / len(MC_Model_Returns["OnlyPositiveReturn"]))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.legend(loc='upper left')
plt.title('MonteCarlo Simulation: Portfolio Returns, Portfolio Size' + str(portfolio_size))
plt.ylabel('Return Occurrence')
### subplot 2 - box plot of returns net & only positive
ax2 = plt.subplot(2, 1, 2, sharex=ax1)
MC_Model_Returns.boxplot(vert=False, notch=True, sym='+')
ax2.yaxis.set_visible(False)


### stylize the plots
plt.style.use('seaborn-darkgrid')

### Show plot
# plt.show()
### save plot
plt.savefig(figure_out)





#######################################
###     Save Figures & Data
#######################################
MC_Model_Returns.to_csv(file_out)
with open (file_out, 'a') as fd:
    fd.write("\nAverage NET Portfolio," + str(net_mean))
    fd.write("\nAverage POSITIVE Portfolio," + str(positive_mean))
