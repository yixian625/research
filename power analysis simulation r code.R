# In this file, I created codes to run simulations to determine the number of participants that I need, 
# given my study design and estimated parameters from pilot study.

# Here, I have a 2(Disclosure depth: low vs. high)*3(Similarity: low vs. medium vs. high) repeated measure design
# All participants goes through all six conditions (represented by six computerized avatars who disclose different
# personal information to the participants depending on their specific condition), and rate their liking of all the
# six avatars/conditions.

# The codes below do the following things:
# 1. Estimate the parameters. Specifically, based on the grand mean and the average standard deviation from the pilot data, 
# I estimated the population means for the six different conditions, given the anticipated effect sizes.

# 2. Build a "shell" dataframe with the participants' ID, conditions, and simulation/iteration numbers

# 3. Using the parameters defined above to build a covariance matrix for the six conditions

# 4. Run the simuluation-- for each iteration, draw samples from a multivariate normal distribution for each of the six conditions, 
# given the population means, standard deviations, and covariance matrix defined in above steps; repeat for all the iterations

# 5. Consolidate the simulated data to the shell dataframe

# 6. Run ANOVA model on the simulated data for each iteration, and calcualte the proportion of iterations with significant p values.
# This proportion is the power obtained given the parameters.


#########################codes start here ##################################


# guess the pupulation means (mu) for all the conditions
# estimated mean from pilot data: mean rating across avatars=4.3; mean std=1.5

grand_mean=4.3
mean_std=1.5


# estimated effect size for *disclosure depth* from Collins & Miller (1994) d=.324
# here we are being conservative and just use a small effect size
estimated_d=.2

# estimate the marginal means for the high vs. low disclosure depth avatars
# let marginal mean rating for high-depth avatars be x1;
# let marginal mean rating for low-depth avatars be x2.
# get values of x1 and x2 based on:
# { (x1+x2)/2= grand mean
#   cohen's d = (x1-x2)/ SD }

marginal_means_given_effect<- function(mean, std, d){
  x1=(std*d+mean*2)/2
  x2=(mean*2-std*d)/2
  return(c(x1, x2))
}

# calculate the estimated mean for high-depth avatars(mean_hd) and low-depth avatars(mean_ld)
mean_hd= marginal_means_given_effect(grand_mean, mean_std, estimated_d)[1]
mean_ld= marginal_means_given_effect(grand_mean, mean_std, estimated_d)[2]

# estimate the means for the three similarity conditions *within* the low disclosure depth level
# let the low, medium, high, similarity level be x1, x2, x3, respectively
# assuming a *small* effect size d=0.2, which is the difference between x3 and x1, with x2 lying inbetween

# get the values of x1, x2, x3, based on:
# { x3= x2+(x2-x1)
#   (X1+x2+x3)/3= mean_ld
#   cohen's d=(x3-x1)/sd }

cell_means_given_effect <- function(mean, std, d){
  x2=mean
  x1=mean-(std*d/2)
  x3=2*x2-x1
  return(c(x1, x2, x3))
}

# calculate estimated cell means for low-sim, medium-sim, and high-sim avatars within the low depth level 
# (mean_ld_ls, mean_ld_ms, mean_ld_hs, respectively)

mean_ld_ls=cell_means_given_effect(mean_ld, mean_std, 0.2)[1]
mean_ld_ms=cell_means_given_effect(mean_ld, mean_std, 0.2)[2]
mean_ld_hs=cell_means_given_effect(mean_ld, mean_std, 0.2)[3]

# calculate estimated cell means for low-sim, medium-sim, and high-sim avatars within the *high* depth level 
# (mean_hd_ls, mean_hd_ms, mean_hd_hs, respectively)
# assuming a *moderate* effect size of similarity d=0.5 within the *high* disclosure depth level
# this creates an interaction between similarity and disclosure depth on rating

mean_hd_ls=cell_means_given_effect(mean_hd, mean_std, 0.5)[1]
mean_hd_ms=cell_means_given_effect(mean_hd, mean_std, 0.5)[2]
mean_hd_hs=cell_means_given_effect(mean_hd, mean_std, 0.5)[3]


## following codes adapted from: 
# https://cognitivedatascientist.com/2015/12/14/power-simulation-in-r-the-repeated-measures-anova-5/


# define the parameter
mu= c(mean_ld_ls, mean_ld_ms, mean_ld_hs, mean_hd_ls, mean_hd_ms, mean_hd_hs) #estimated true population mean
sigma= 1.5 # population standard deviation
rho= 0.5 # correlation between repeated measures (within-subject correlation)
nsubs= 70 # number of subjects
nsims= 5000 # number of similulations to run

# create the two IV factors

condition= data.frame(
  Sim= rep(c(1, 2, 3), nsubs *2), # define similarity with 3 levels
  Depth= rep(c(1, 2), nsubs, each=3) # define disclosure depth with 2 levels
)

head(condition, n=12)

# create a factor for the subject ID
# define subject number as a factor so r knows that its categorical not ordinal/numeric

subject=factor(sort(rep(1:nsubs, 6))) # each Ss ID is repeated 6 times because they go through 6 conditions

# combine the subject IV factor with the condition matrix

df= data.frame(subject, condition)
head(df, n=12)

# build a covariance matrix based on the parameters previously defined

# 1. create a 6*6 matrix as we have 6 conditions (containing sd for all conditions)

sigma.mat = rep(sigma, 6)
S.matrix= matrix(sigma.mat, ncol = length(sigma.mat), nrow = length(sigma.mat))

# 2. calculate covariance between each two conditions

Sigma.matrix <- t(S.matrix) * S.matrix * rho 

# put the variances on the diagonal
diag(Sigma.matrix) <- sigma^2

# Running the simulation

# stack all the individual simulated data frames into one long data frame
df_all= df[rep(seq_len(nrow(df)), nsims), ] # generate a sequence equal the number of rows for each simulation, and repeat that for the number of simulations defined (nsims)

# sort and name the simulation runs as the index
df_all$simulation = sort(rep(seq_len(nsims), nrow(df)))
df_all


# sample the observed data from a multivariate normal distribution
# using MASS::mvrnorm with the parameters mu and Sigma created earlier
# and bind to the existing df


require(MASS)

set.seed(1234) # set a seed for the following simulation so that the results would always be the same

make.y = expression(as.vector(t(mvrnorm(nsubs, mu, Sigma.matrix))))
df_all$y = as.vector(replicate(nsims, eval(make.y)))             

# use do(), the general purpose complement to the specialized data 
# manipulation functions available in dplyr, to run the ANOVA on
# each section of the grouped data frame created by group_by

#install.packages("car")
#install.packages('backports')
#install.packages("broom")

require(dplyr)
require(car)
require(broom)

mods <- df_all %>% 
  group_by(simulation) %>% 
  do(model = aov(y ~ Sim * Depth + Error(subject / (Sim*Depth)), qr=FALSE, data = .)) 


# extract p-values for each effect and store in a data frame
p = data.frame(
  mods %>% do(as.data.frame(tidy(.$model[[3]])$p.value[1])),
  mods %>% do(as.data.frame(tidy(.$model[[4]])$p.value[1])),
  mods %>% do(as.data.frame(tidy(.$model[[5]])$p.value[1])))
colnames(p) = c('Sim','Depth','Interaction')


power = apply(as.matrix(p), 2, 
              function(x) round(mean(ifelse(x < .05, 1, 0) * 100),0))
              
cat ("# of Subjects Needed to Achieve the Power Shown Below =", nsubs, "\n")
power
