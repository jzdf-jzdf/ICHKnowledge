# Profile and Prognosis of Spontaneous Lobar Intracerebral Hemorrhage: Comparison of 6-month Survival with STICH II and the MISTIE III Lobar Hemorrhage Subset  

Berthold Behle1 Kerim Beseoglu1 Thomas Beez1 Athanasios K. Petridis1 Igor Fischer1   
Daniel Hänggi1 Hans-Jakob Steiger1  

1 Department of Neurosurgery, Heinrich-Heine-University, Düsseldorf, Germany  

J Neurol Surg A Cent Eur Neurosurg 2022;83:20–26.  

Address for correspondence Hans-Jakob Steiger, MD, PhD, Department of Neurosurgery, Uniklinik, Moorenstr. 5, Düsseldorf 40225, Germany (e-mail: Steiger@uni-duesseldorf.de).  

# Abstract  

Background Randomized trials on spontaneous lobar intracerebral hemorrhage (ICH) provided no convincing evidence of the superiority of surgical treatment. Since recruitment in the trials was under the premise of equipoise, a selection bias toward patients who did not need surgery or were in hopeless condition must be suspected. The aim of the actual analysis was to compare outcome and patient profile of an unselected hospital series with recent randomized trials and to develop a prognostic model.  

Methods Of 821 patients with spontaneous ICH managed at the neurosurgical department of the University Hospital Düsseldorf between 2013 and 2018, 159 had lobar bleedings. Patient characteristics, hematoma volume, treatment modality, and 6-month survival were compared with STICH II and the subset of lobar hemorrhage in the MISTIE III trial. In addition, a prognostic model for 6-month survival in our patients was developed using a random forest classifier.  

# Keywords  

► lobar brain hemorrhage intracerebral hemorrhage STICH II trial surgery craniotomy outcome  

Results One hundred and seven patients were managed by surgical evacuation of the hematoma and 52 without surgical evacuation. Median hemorrhage volume in our surgical cohort was 66 and $42\mathsf{ml}$ in the conservative cohort, compared with 38 and $36\mathsf{mL}$ in the STICH II trial, and 46 and $47\mathsf{ml}$ in the surgical and conservative MISTIE III lobar hemorrhage subset. Median initial Glasgow Coma Scale (GCS) score was 12 in our surgical group and 11 in the conservative group, compared with 13 in the STICH II cohorts and 12 in the MISTIE III lobar hemorrhage subset. Median age in our surgical and conservative cohorts was 73 and 74 years, respectively, compared with 65 years in both STICH II cohorts and 68 years in the MISTIE II subsets. Twenty-nine percent of our surgical cohort and $55\%$ of our conservatively managed patients deceased within the first 6 months, compared with 18 and $24\%$ , respectively, in STICH II and 17 and $24\%$ in the MISTIE III subset. Our prognostic model identified large hemorrhage volumes and low admission GCS score as main unfavorable prognostic factors for 6-month survival. The random forest classifier achieved a predictive accuracy of $78\%$ and an area under curve (AUC)- value of $88\%$ regarding survival at 6 months, on a test set independent of the training set.  

Conclusions In comparison with our surgical group, the STICH II and MISTIE III cohorts, recruited under the premise of physician equipoise, underrepresented patients with large ICHs. The cohorts in the randomized trials were therefore biased toward patients with a favorable perspective under conservative management. Initial hematoma volume and admission GCS were the main prognostic factors in our patients.  

# Introduction  

The randomized trial “Early surgery versus initial conservative treatment in patients with spontaneous supratentorial intracerebral haematomas in the International Surgical Trial in Intracerebral Haemorrhage (STICH)” found no conclusive evidence of the benefit of surgery for lobar and deep-seated primary intracerebral hemorrhage (ICH).1,2 Assuming dependence on the hemorrhage location, the subsequent trial STICH II focused exclusively on lobar hemorrhage, a subgroup that was estimated to be more favorable than deep-seated ICH.3 However, the STICH II trial also failed to demonstrate superiority of surgery in terms of dichotomized functional outcome at 6 months when compared with conservative management alone. The next large randomized trial, MISTIE III, focused on minimal invasive technique but went back to lumped inclusion criteria, including deep-seated and lobar ICHs.4–6 As the preceding studies, MISTIE III could not demonstrate superiority of clot evacuation in terms of functional outcome at 6 months when compared with conservative management alone.  

The separation of lobar and deep-seated ICHs appears nonetheless sensible. Although in several reports including MISTIE III, the location of hemorrhage, basal ganglia, or lobar had a very modest impact on clinical outcome, this does not mean that the impact of surgical evacuation is the same for both locations.7,8 For lobar hemorrhage, STICH II showed a trend toward better outcome in the surgical group. If we want to define methodological weaknesses for the failure of the trial to meet the aim, a bias of the recruited patient groups must be suspected.9,10 Inclusion into the trial was based on equipoise, meaning that the referring physicians were uncertain with regard to a potential surgical indication. Therefore, we must suspect that the trial cohort was biased in favor of (1) small ICHs unlikely to benefit from evacuation and on the other hand (2) hopeless cases, particularly large hematomas in patients in poor neurologic conditions. Since equipoise depends on certain subjective factors, it could be hoped that in the ideal situation the overlap of the mentioned subgroups would represent the entire spectrum of patients with lobar ICH.  

Regarding the MISTIE cohorts, similar reservations must be pronounced. Only 500 of nearly 20,000 patients screened could be included in the trial due to restrictive inclusion criteria, for example, clinical and radiologic stability.4,6 The main limiter for inclusion in MISTIE III, in addition to primary equipoise, was the stability condition, meaning that ICH remained the same size (growth ${<}5\mathrm{mL}$ ) for at least 6 hours after diagnostic computed tomography (CT).  

Despite these unresolved issues, the results of the STICHand MISTIE trials affected the clinical practice. The proportion of patients undergoing surgical therapy for supratentorial ICH decreased. Kirkman et al analyzed the effects of the results of the STICH I trial on the management of spontaneous supratentorial ICH in Newcastle.11 Clot evacuation procedures in the neurosurgery department decreased significantly from 111 in 2002 to 53 in 2007. Corresponding case fatality rate at 30 days increased from $14\%$ in 2002 to $26\%$ in 2007.  

There are no proper analyses that compared unselected hospital cases of lobar brain ICH with the study cohorts to affirm the value of the study results for clinical practice. The aim of the actual analysis was to compare an unselected series of lobar ICH with the STICH II cohort and MISTIE III subset of lobar hemorrhage, and to develop a predictive model for 6-month survival using current statistical methods. Dr. Daniel F. Hanley and the National Institute of Neurological Disorders and Stroke (https://www.ninds.nih.gov/) kindly provided the original MISTIE III dataset.  

# Methods  

After approval by the institutional ethics committee, charts and imaging of the 821 patients with ICH managed between 2013 and 2018 at the neurosurgical department of the University Hospital Düsseldorf were retrieved and analyzed for the present study. Following visual screening of the initial CTs and/or magnetic resonance imaging (MRI), and elimination of basal ganglia, posterior fossa, brainstem, and purely intraventricular hemorrhage, as well as aneurysm and venous thrombosis-related hemorrhages, 159 cases with idiopathic lobar ICHs remained for further analysis.  

# Clinical Treatment Protocol  

Care and active treatment of our patients followed current guidelines for the management of patients with primary ICH.1,12–15 Initial diagnosis was achieved with CT or MRI. Contrast CT or magnetic resonance angiography (MRA) was routinely added to exclude vascular pathology.  

Comatose patients with a Glasgow Coma Scale (GCS) score $<9$ were intubated and ventilated. Systolic blood pressure was maintained below $140\mathrm{mm}\mathrm{Hg}$ . Possible anticoagulants were stopped upon admission and antagonized if possible.  

Surgical indication for lobar brain hemorrhage was made for hematoma volumes larger than 50 to $100\mathrm{mL}$ , depending also on neurologic and general condition. We were reluctant with the surgical indication in situations of profound and already prolonged coma $\left(\mathbf{G}\mathbf{C}\mathbf{S}<9\right)$ . Surgical evacuation was performed by an image-guided small osteoplastic craniotomy except in cases of major associated perifocal edema. In these cases, we performed a decompressive craniectomy and enlargement duroplasty.  

An external ventricular drainage inserted by a separate burr hole was used in comatose patients $({\sfGCS}<9)$ and in cases of additional intraventricular hemorrhage.  

# Data Extraction and Analysis  

Data extracted from the patients’ records included patient age (numeric), anticoagulation (Boolean), hypertension (Boolean), additional ventricular hemorrhage (Boolean), surgical evacuation (Boolean), external ventricular drainage (Boolean), initial GCS (ordinal, numeric), hematoma volume (numeric), and survival at 6 months (Boolean). Hematoma volume was calculated by the following ellipsoid model: a b c/2.3,16,17  

Data analysis and graphical work was done using open source Python, and included the MatPlotlib module (https: $I/$ www.python.org) and the scikit-learn platform (https://scikitlearn.org/ stable/).  

Following descriptive statistics incomparisonwith the STICH II cohortsand MISTIE III lobarhemorrhagesubcohorts, a Pearson correlation matrix of the potential factors and survival at 6 months was calculated. For predictive modeling, the dataset was split 80 to $20\%$ as training and testing set.18 Prior to further analysis, the training dataset was corrected for imbalance of the two classes “dead at 6 months” and “alive a 6 months” by Synthetic Minority Over-sampling Technique (SMOTE).19 Predictive accuracy was screened for the classifiers available on the scikit-learn platform. The random forest classifier (RFC) was finally chosen, because it compared favorably with other sample-tested tools, such as K-nearest neighbor (KNN) classifier, Gaussian naïve Bayes (NB), Support Vector Classifier (SVC), Logistic Regression Classifier (LRC), Decision Tree Regressor (DTR), and bootstrapped Bagging Classifier (BAG).  

Stability of the predictions was assessed with k-fold $(k=10)$ cross-validation. The accuracy of the model was evaluated upon the correct prediction for the patients of the test set, regarding survival at 6 months.  

# Results  

The distribution of the analyzed parameters among the 159 patients is shown in ►Fig. 1. We managed 107 of our patients by surgical evacuation of the hematoma and 52 without surgical evacuation. In ►Table 1, the key features of our surgically and conservatively managed cohorts are compared with the cohorts of the STICH II trial and the lobar hemorrhage subset of the MISTIE III trial. The median hemorrhage volume was 66 in our surgical cohort and $42\mathrm{mL}$ in the conservative cohort, compared with 38 and $36\mathrm{mL}$ in the STICH II trial cohorts, and 46 and $47\mathrm{mL}$ in the MISTIE III lobar hemorrhage subset. Median initial GCS was 12 in our surgical group and 11 in the conservative group, compared with 13 in both STICH II cohorts and 12 in the MISTIE III subsets. The median age in our surgical and conservative group was 73 and 74 years, respectively, compared with 65 in both STICH II cohorts and 68 in the MISTIE III subsets.  

![](images/f5a879a312c2a1e500c8598f1855c31f2a516e3e3870025d0162ba4d02d192ae.jpg)  
Fig. 1 (a–j) Distribution of the key variables among our 159 patients with lobar intracerebral hemorrhage (AC, antithrombotic medication or anticoagulation; HTN, known hypertension; IVH, additional intraventricular hemorrhage; OP, surgical hematoma evacuation; EVD, external ventricular drainage; GCS, Glasgow Coma Scale; Vol, hematoma volume; Surv, 6-month survival).  

Table 1 Comparison of key features in the current series with randomized trials on surgical evacuation of lobar intracerebral hemorrhage   


<html><body><table><tr><td></td><td colspan="2">Mendelow et al3</td><td colspan="2">Hanley 2016a</td><td colspan="2">Current analysis</td></tr><tr><td></td><td>Surgical</td><td>Conservative</td><td>Surgical</td><td>Conservative</td><td>Surgical</td><td>Conservative</td></tr><tr><td>Age (median, IQR)</td><td>65 (55, 74)</td><td>65 (56,74)</td><td>68 (63,73.5)</td><td>68 (61,74)</td><td>73(64, 78)</td><td>74 (64, 79)</td></tr><tr><td>Known hypertension</td><td>68%</td><td>67%</td><td>74%</td><td>93%</td><td>86%</td><td>88%</td></tr><tr><td>Under antiplatelet or anticoagulant medication</td><td>22%</td><td>19%</td><td>50%</td><td>43%</td><td>52%</td><td>50%</td></tr><tr><td>Initial GCS (median, IQR)</td><td>13 (11,15)</td><td>13 (11, 15)</td><td>12 (9.25,14)</td><td>12 (9, 13)</td><td>12 (5, 14)</td><td>11 (5, 15)</td></tr><tr><td>Hematomavolume (mL,median, IQR,)</td><td>38 (24, 54)</td><td>36 (22,58)</td><td>46 (36,60)</td><td>47 (37,60)</td><td>66 (45,86)</td><td>42 (22,114)</td></tr><tr><td>Ventricularhemorrhage present</td><td>n.a.</td><td>n.a.</td><td>31%</td><td>43%</td><td>47%</td><td>52%</td></tr><tr><td>6-mo mortality</td><td>18%</td><td>24%</td><td>17%</td><td>24%</td><td>29%</td><td>55%</td></tr></table></body></html>

Abbreviations: GCS, Glasgow Coma Scale; IQR, interquartile range. aData on lobar hemorrhage from the MISTIE III trial were extracted from the original dataset, kindly supplied by Dr. Daniel F. Hanley and the National Institute of Neurological Disorders and Stroke (https://www.ninds.nih.gov/).  

Seventy-six patients $(71\%)$ undergoing surgical hematoma evacuation survived at 6 months compared with 23 $(45\%)$ without hematoma evacuation. In other words, $29\%$ of our surgical cohort and $55\%$ of our conservatively managed patients deceased within the first 6 months, compared with 18 and $24\%$ in STICH II, and 17 and $24\%$ in the MISTIE III subset. Overall, 99 $(62\%)$ of our patients were alive at 6 months compared with $79\%$ in the STICH II cohorts and $79\%$ in the MISTIE III lobar subset.  

In 77 patients $(48\%)$ , some intraventricular hemorrhage concurred with the ICH. Thirty patients $(19\%)$ were managed with an additional external ventricular drainage. Eighty-two patients $(51\%)$ used antiplatelet agents or anticoagulation at the time of admission and known hypertension was present in 138 patients $(87\%)$ .  

Pearson correlation matrix associated mainly large hemorrhage volumes, low GCS, and older age as main unfavorable prognostic factors for 6-month survival (►Figs. 2, 3). In addition, surgical therapy was moderately associated with a higher 6-month survival rate and intraventricular hemorrhage with a lower 6-month survival rate. Antiplatelet agents or anticoagulation as well as known hypertension had no visible impact on outcome.  

The RFC achieved a predictive accuracy of $78\%$ and an AUC of $88\%$ regarding survival at 6 months, on a test set independent of the training set. The complete metrics are given in ►Table 2. The cross-validation AUC score of the entire dataset was $79\pm16\%$ . The most important predictive feature was the volume of the hematoma with a feature importance of $34\%$ (►Table 3). Age and admission GCS and the use of surgical evacuation were of secondary importance, while the use of external ventricular drainage, additional intraventricular hemorrhage, antithrombotic treatment or anticoagulation, and hypertension had a minor importance.  

# Discussion  

In our surgical patients, the hematoma volume was substantially larger, patients were older, and admission GCS was lower than in the STICH II cohorts and the MISTIE III lobar hemorrhage subset. Correspondingly, the outcome in our surgical series was less favorable with a much higher case fatality rate at 6 months. Our conservatively managed patients had a lower admission GCS and smaller median hemorrhage volume than our surgically managed patients, and the case fatality rate was almost twice as high as in the surgically treated group. Therefore, we must conclude that the initial prognosis of the patients not undergoing surgical evacuation was seen as less favorable. In some cases, however, a documented or communicated treatment wish played a role for the decision. The question remains whether some of our conservatively managed patients could have fared better with a more active treatment.  

Case fatality rates of most acute intracranial disorders including brain hemorrhage have significantly decreased over the last decade, mainly due to better intensive care management and maybe also due to a less fatalistic attitude toward treatment at older age.11,12,20–22 Therefore, outcome of older series is difficult to compare with more recent reports. Recently, Maslehaty et al reported on a large series of 817 patients with lobar and deep ICH.23 They found at 30 days an outcome of Glasgow Outcome Scale (GOS) of 1 and 2 in $22.4\%$ of the surgically managed patients and $31\%$ in the conservatively treated group, thus also having a substantially worse outcome in the unoperated cases. Hessington et al reported in a retrospective analysis of a surgical series of lobar and deep ICH an overall favorable outcome with a 6-month case fatality rate of $18\%$ , which was not influenced by ICH location.24  

![](images/d3c88ae6372786b9dc6ec15478b9dd6baa67494fa96e89e0ef259c43381777d0.jpg)  
Fig. 2 Heat map of Pearson correlation matrix showing relations between patient characteristics, volume of hematoma, and survival at 6 months (AC, antithrombotic medication or anticoagulation; HTN, known hypertension; IVH, additional intraventricular hemorrhage; OP, surgical hematoma evacuation; EVD, external ventricular drainage; GCS, Glasgow Coma Scale; Vol, hematoma volume; Surv, 6-month survival).  

![](images/191d01b1e0c0b14ee2ef06f3af34ef1639f2c5114d0bfa8d8c20f42fa6ea9c8e.jpg)  
Fig. 3 (a,b) 3D scatterplots showing the distribution of the most important factors associated with 6-month survival. Green dots represen patients surviving and black crosses represent fatalities at 6 months. Hematoma volume is the most correlated factor.  

Similarly, Fahlström et al found in a nationwide Swedish retrospective analysis of surgical management of lobar and deep-seated ICH a favorable outcome with $17\%$ mortality rate at 30 days. Location, deep seated versus lobar, had a minor influence on outcome.25  

Broderick et al were the first to acknowledge the overwhelming importance of the volume of the hematoma to estimate 30-day mortality.16 Consecutively several prognostic scores were developed to predict the 30-day mortality.3,7 Accuracy of AUC values in the range of 80 to $85\%$ are reported. Prognostication for 6 months is naturally less precise than for 30 days. Using an RFC, we achieved correct prognostication regarding survival at 6 months with an accuracy of $78\%$ and an AUC of $88\%$ . A much higher accuracy of a prognostic model cannot be expected, due to unforeseeable factors such as input of next of kin during the months following acute treatment. Furthermore, our RFC confirmed the outstanding importance of hematoma volume to appreciate case fatality rate by 6 months (feature importance $34\%$ ). Age (feature importance $20\%$ ) and admission GCS (feature importance $15\%$ ), and the use of surgical evacuation (feature importance $12\%$ were of secondary importance, whereas the use of external ventricular drainage, additional intraventricular hemorrhage, antithrombotic treatment or anticoagulation, and hypertension had a minor importance.  

Table 2 Metrics of the random forest classifier on the test dataset   


<html><body><table><tr><td rowspan="2"></td><td>TN</td><td>FP</td><td rowspan="2">Accuracy</td><td rowspan="2">AUC</td><td rowspan="2">Precision</td><td rowspan="2">Recall (sensitivity)</td><td rowspan="2">F1</td></tr><tr><td>FN</td><td>TP</td></tr><tr><td>Dead at 6 mo</td><td>6</td><td>3</td><td rowspan="2">0.78</td><td rowspan="2">0.88</td><td rowspan="2">0.84</td><td rowspan="2">0.8</td><td rowspan="2">0.82</td></tr><tr><td></td><td></td><td></td></tr><tr><td>Alive at6mo</td><td>4</td><td>16</td><td></td><td></td><td></td><td></td><td></td></tr></table></body></html>

Abbreviations: TN, true negative (“dead at 6 months”); TP, true positive (“alive at 6 months”); FN, false negative; FP, false positive; accuracy, $(\mathsf{TP}+\mathsf{TN})/$ all; AUC, area under curve; Precision $=\mathsf{TP}/(\mathsf{TP}+\mathsf{FP})$ ; Recall $=\mathsf{TP}/(\mathsf{TP}+\mathsf{FN})$ ; $\mathsf{F}1=2\times$ ((Precision $\times$ Recall)/(Precision $^+$ Recall)).  

Table 3 Feature importance of random forest classifier   


<html><body><table><tr><td>Hematomavolume</td><td>0.343097</td></tr><tr><td>Age</td><td>0.202038</td></tr><tr><td></td><td>0.152229</td></tr><tr><td>Surgical evacuation</td><td>0.119304</td></tr><tr><td>Externalventriculardrainage</td><td>0.051312</td></tr><tr><td>Additional intraventricular hemorrhage</td><td>0.051006</td></tr><tr><td>Antithrombotictreatment,anticoagulation</td><td>0.043358</td></tr><tr><td>Hypertension</td><td>0.037656</td></tr></table></body></html>

Abbreviation: GCS, Glasgow Coma Scale.  

# Limitations  

Our analysis represents a historical post hoc evaluation in a single neurosurgical center, a fact that implies a certain selection of more seriously ill patients.  

We used mortality after 6 months to calculate the prediction model in contrast to functional outcome, such as modified Rankin Scale (mRS) or GOS. We chose mortality as the primary outcome parameter rather than a binarized functional parameter because we felt that it was less prone to interpretation.  

We used only hematoma volume as radiologic parameters for the model. We did not include radiologic criteria associated with hemorrhage expansion such as the black hole sign or spot sign. Including such parameters might improve predictive accuracy in future models.  

# Conclusion  

In conclusion, the patient profile of our unselected series differs substantially from the STICH II and the MISTIE III lobar hemorrhage cohorts toward unfavorable prognostic factors and worse outcome. Acute ICH appears to be ill suited for a proper randomized trial, which is also illustrated by the crossover rate of $25\%$ from the initially conservative arm of STICH II and by the minimal percentage of screened patients that finally could be included in the MISTIE III trial. Regarding the prediction modeling for ICH, a $78\%$ accurate prediction of 6-month survival was achieved using an RFC. The defined feature importance could be used to fine-tune current prognostic models.  

Disclosures None.  

Funding None.  

Acknowledgments Data on lobar hemorrhage from the MISTIE III trial were extracted from the original dataset, kindly supplied by Dr. Daniel F. Hanley and the National Institute of Neurological Disorders and Stroke (https://www.ninds.nih.gov/).  

# References  

1 Mayer SA, Rincon F. Treatment of intracerebral haemorrhage. Lancet Neurol 2005;4(10):662–672   
2 Mendelow AD, Gregson BA, Fernandes HM, et al; STICH investigators. Early surgery versus initial conservative treatment in patients with spontaneous supratentorial intracerebral haematomas in the International Surgical Trial in Intracerebral Haemorrhage (STICH): a randomised trial. Lancet 2005;365(9457):387–397   
3 Mendelow AD, Gregson BA, Rowan EN, Murray GD, Gholkar A, Mitchell PMSTICH II Investigators. Early surgery versus initial conservative treatment in patients with spontaneous supratentorial lobar intracerebral haematomas (STICH II): a randomised trial. Lancet 2013;382(9890):397–408   
4 Hanley DF, Thompson RE, Rosenblum M, et al; MISTIE III Investigators. Efficacy and safety of minimally invasive surgery with thrombolysis in intracerebral haemorrhage evacuation (MISTIE III): a randomised, controlled, open-label, blinded endpoint phase 3 trial. Lancet 2019;393(10175):1021–1032   
5 Vespa P, Hanley D, Betz J, et al; ICES Investigators. ICES (intraoperative stereotactic computed tomography-guided endoscopic surgery) for brain hemorrhage: a multicenter randomized controlled trial. Stroke 2016;47(11):2749–2755   
6 Ziai WC, McBee N, Lane K, et al; MISTIE III Investigators. A randomized 500-subject open-label phase 3 clinical trial of minimally invasive surgery plus alteplase in intracerebral hemorrhage evacuation (MISTIE III). Int J Stroke 2019;14(05):548–554   
7 Fahlström A, Nittby Redebrandt H, Zeberg H, et al. A grading scale for surgically treated patients with spontaneous supratentorial intracerebral hemorrhage: the Surgical Swedish ICH Score. J Neurosurg 2020;133(03):800–807   
8 Mattishent K, Kwok CS, Ashkir L, Pelpola K, Myint PK, Loke YK. Prognostic tools for early mortality in hemorrhagic stroke: systematic review and meta-analysis. J Clin Neurol 2015;11(04):339–348   
9 Kirkman MA, Greenwood N, Singh N, Tyrrell PJ, King AT, Patel HC. Difficulties with recruiting into neurosurgical clinical trials: the Surgical Trial in IntraCerebral Haemorrhage II as an example. Br J Neurosurg 2011;25(02):231–234   
10 Prasad KS, Gregson BA, Bhattathiri PS, Mitchell P, Mendelow ADSTICH Investigators. The significance of crossovers after randomization in the STICH trial. Acta Neurochir Suppl (Wien) 2006;96:61–64   
11 Kirkman MA, Mahattanakul W, Gregson BA, Mendelow AD. The effect of the results of the STICH trial on the management of spontaneous supratentorial intracerebral haemorrhage in Newcastle. Br J Neurosurg 2008;22(06):739–746, discussion 747   
12 Adeoye O, Woo D, Haverbusch M, et al. Surgical management and case-fatality rates of intracerebral hemorrhage in 1988 and 2005. Neurosurgery 2008;63(06):1113–1117, discussion 1117–1118   
13 Adeoye O, Woo D, Haverbusch M, et al. Eligibility for the surgical trial in intracerebral hemorrhage II study in a population-based cohort. Neurocrit Care 2008;9(02):237–241   
14 Morgenstern LB, Hemphill JC III, Anderson C, et al; American Heart Association Stroke Council and Council on Cardiovascular Nursing. Guidelines for the management of spontaneous intracerebral hemorrhage: a guideline for healthcare professionals from the American Heart Association/American Stroke Association. Stroke 2010;41(09):2108–2129   
15 Steiner T, Al-Shahi Salman R, Beer R, et al; European Stroke Organisation. European Stroke Organisation (ESO) guidelines for the management of spontaneous intracerebral hemorrhage. Int J Stroke 2014;9(07):840–855   
16 Broderick JP, Brott TG, Duldner JE, Tomsick T, Huster G. Volume of intracerebral hemorrhage. A powerful and easy-to-use predictor of 30-day mortality. Stroke 1993;24(07):987–993   
17 Webb AJ, Ullman NL, Morgan TC, et al; MISTIE and CLEAR Investigators. Accuracy of the ABC/2 score for intracerebral hemorrhage: systematic review and analysis of MISTIE, CLEAR-IVH, and CLEAR III. Stroke 2015;46(09):2470–2476   
18 Roberts SJ. Parametric and non-parametric unsupervised cluster analysis. Pattern Recognit 1997;30(02):261–272   
19 Chawla NV, Bowyer KW, Hall LO, Kegelmeyer WP. SMOTE: synthetic minority over-sampling technique. J Artif Intell Res 2002; 16:321–357   
20 Lovelock CE, Rinkel GJ, Rothwell PM. Time trends in outcome of subarachnoid hemorrhage: population-based study and systematic review. Neurology 2010;74(19):1494–1501   
21 La Pira B, Singh TD, Rabinstein AA, Lanzino G. Time trends in outcomes after aneurysmal subarachnoid hemorrhage over the past 30 years. Mayo Clin Proc 2018;93(12):1786–1793   
22 Kadar R, Rochford D, Omi E, Thomas Y, Patel K, Kulstad E. Trends in demographics and outcome of patients presenting with traumatic brain injury. Clin Exp Emerg Med 2019;6(02):113–118   
23 Maslehaty H, Petridis AK, Barth H, Doukas A, Mehdorn HM. Treatment of 817 patients with spontaneous supratentorial intracerebral hemorrhage: characteristics, predictive factors and outcome. Clin Pract 2012;2(03):e56   
24 Hessington A, Tsitsopoulos PP, Fahlström A, Marklund N. Favorable clinical outcome following surgical evacuation of deep-seated and lobar supratentorial intracerebral hemorrhage: a retrospective single-center analysis of 123 cases. Acta Neurochir (Wien) 2018; 160(09):1737–1747   
25 Fahlström A, Tobieson L, Redebrandt HN, et al. Differences in neurosurgical treatment of intracerebral haemorrhage: a nationwide observational studyof578 consecutive patients. Acta Neurochir (Wien) 2019;161(05):955–965  