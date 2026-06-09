# Combination of Hematoma Volume and Perihematoma Radiomics Analysis on Baseline CT Scan Predicts the Growth of Perihematomal Edema  

Jia Wang1 $\cdot$ Xing Xiong2 · Jinzhao Zou1 $\cdot$ Jianxiong Fu1 · Yili Yin1 $\cdot$ Jing Ye1  

Received: 23 February 2022 / Accepted: 11 July 2022 / Published online: 9 August 2022   
$\circledcirc$ The Author(s), under exclusive licence to Springer-Verlag GmbH Germany 2022  

# Abstract  

Purpose The aim is to explore the potential value of CT-based radiomics in predicting perihematomal edema (PHE) volumes after acute intracerebral hemorrhage (ICH) from admission to $^{241}$ .  

Methods A total of 231 patients newly diagnosed with acute ICH at two institutes were analyzed retrospectively. The patients were randomly divided into training $(N{=}117)$ and internal validation cohort $(N=45)$ from institute 1 with a ratio of 7:3. According to radiomics features extracted from baseline CT, the radiomics signatures were constructed. Multiple logistic regression analysis was used for clinical radiological factors and then the nomogram model was generated to predict the extent of PHE according to the optimal radiomics signature and the clinical radiological factors. The receiver operating characteristic (ROC) curve was used to evaluate the discrimination performance. The calibration curve and Hosmer-Lemeshow test were used to evaluate the consistency between the predicted and actual probability. The support vector regression (SVR) model was constructed to predict the overall value of follow-up PHE. The performance of the models was evaluated on the internal and independent validation cohorts.  

Results The perihematoma $5\mathrm{mm}$ radiomics signature (AUC: 0.875) showed good ability to discriminate the small relative PHE(rPHE) from large rPHE volumes, comparing to intrahematoma radiomics signature (AUC: 0.711) or perihematoma $10\mathrm{mm}$ radiomics signature (AUC: 0.692) on the training cohort. The AUC of the combined nomogram model was 0.922 for the training cohort, 0.945 and 0.902 for the internal and independent validation cohorts, respectively. The calibration curves and Hosmer–Lemeshow test of the nomogram model suggested that the predictive performance and actual outcome were in favorable agreement. The SVR model also predicted the overall value of follow-up rPHE (root mean squared error, 0.60 and 0.45; Pearson correlation coefficient, 0.73 and 0.68; $P{<}0.001$ ).  

Conclusion Among patients with acute ICH, the established nomogram and SVR model with favorable performance can offer a noninvasive tool for the prediction of PHE after ICH.  

Keywords Intracerebral hemorrhage $^*$ Cerebral edema $^*$ CT $\cdot$ Radiomics $\cdot$ Nomogram  

# Introduction  

Intracerebral hemorrhage (ICH) is a severe neurological disease with high morbidity and mortality [1]. It accounts for only $15\%$ of all strokes, yet it is one of the most disabling forms of stroke. So far, no effective treatment for ICH has been developed.  

Secondary perihematomal edema (PHE) is closely related to the poor prognosis and mortality in patients with ICH and leads to high cranial pressure and neurological deterioration [2, 3]. It develops within $^{241}$ after ICH and rapidly increases over the first 3 days, reaching its peak within 2 weeks [4]. The formation of secondary PHE after  

ICH is a complex mechanism that is still not fully understood.  

It is generally believed that the occurrence and development of PHE are related to the direct compression of the hematoma on surrounding tissues, lysis of red blood cells, coagulation cascade, and inflammation [5, 6]. In recent years, secondary brain damage caused by PHE has been considered a potential therapeutic target. To date, the clinical benefits of interventions for ICH expansion are still ambiguous [1]. A recent study has demonstrated that secondary brain injury, in the form of PHE, may lead to worse outcomes in the experimental model of ICH [7].  

Noncontrast computed tomography (NCCT) is the most common diagnostic tool for patients with acute ICH. Several novel markers based on NCCT, such as irregular shape, swirl sign, blend sign, black hole sign, and island sign, have been recently proposed as predictors of early hematoma expansion [8]. Previous studies have used automatic or semiautomatic methods to measure PHE based on threshold or edge detection algorithms on NCCT images [9, 10]. In addition, some imaging predictors, including absent ipsilateral venous filling and jugular venous reflux, have been proposed to assess PHE development [11, 12]; however, these markers require additional examinations, which may not be feasible for urgent and unstable patients.  

Radiomics is a relatively new method that extracts many features from medical images using data characterization algorithms [13–15]. It integrates quantitative imaging features with clinical parameters using machine learning and statistical analysis methods. Radiomics analysis has been widely carried out for clinical decision support in oncology. Recently, Xie et al. suggested an NCCT-based radiomics model to predict hematoma expansion [14]; however, no prior study has applied radiomics analysis to the ICH-derived PHE growth.  

In this study, we used NCCT-based radiomics analysis to identify the associations between the quantitative imaging features and the pathophysiology of intrahematoma and perihematoma areas. We developed a quantitative model, including radiomics and clinical information, to predict early PHE growth after ICH.  

# Material and Methods  

# Patients  

The Ethics Committee approved this study of institutes, and the need for informed consent was waived.  

A total of 231 patients newly diagnosed with acute ICH at two institutes between March 2017 and September 2020 were enrolled in this analysis. All patients underwent CT plain scan within $^{6\mathrm{h}}$ of symptom onset and $^{24\mathrm{h}}$ of baseline scan. In addition, all patients underwent blood pressure control and routine dehydration treatment. Inclusion criteria were: $(1)\geq18$ years of age; (2) spontaneous supratentorial ICH confirmed on CT; (3) known time of ICH onset; $(4)>1$  

![](images/e21dd69d69bbd885d0868b333b89a803615166b9b8fca7c2b936af91b3eb8f90.jpg)  
Fig. 1 The flowchart of the study population  

CT scan available and completed within $^{6\mathrm{h}}$ and $^{241}$ of onset.  

Exclusion criteria were: (1) primary intraventricular hemorrhage or subarachnoid hemorrhage; (2) subsequent surgery or interventional therapy before the $^{241}$ followup CT scan; (3) any cause of secondary ICH confirmed by surgery or follow-up by cerebral vascular imaging; (4) severe image artifacts.  

The eligible patients of institute 1 were randomly divided into the training and internal validation cohorts at a ratio of 7:3, and patients of institute 2 were collected as the independent cohort. The study flowchart is shown in Fig. 1.  

# CT Examination  

All examinations were performed on multi-detector CT scanners (GE Healthcare, Chicago, IL, USA; United imaging, Shanghai, China). The scanning parameters were tube voltage $120\mathrm{kV}$ , tube current $200{-}360\mathrm{mA}$ , field of view  

$320\mathrm{mm}$ , matrix $512\times512$ , and layer thickness $5\mathrm{mm}$ . The scanning ranged from the top of the skull to the base.  

# Lesion Segmentation  

Electronic files of the baseline and 24-hour CT images transferred from the picture archiving and communication system (PACS) were saved as DICOM files and were then loaded into an open software (3D-Slicer, Version 4.10.2). Region of interest (ROI) was delineated semi-automatically following a previous protocol [16, 17] by two neuroradiologists (with 10 and 4 years of experience, respectively) who were blinded to clinical data. This method of NCCT-based PHE measurement showed excellent interrater reliability at baseline and $^{241}$ post-ICH. The perihematoma region (PHR) was dilated $5\mathrm{mm}$ and $10\mathrm{mm}$ in three dimensions automatically after the intrahematoma region (IHR) was drawn. All cerebrospinal fluid, large vessels, skull, intraventricular extension, and calcification around the hematoma were manually excluded from each ROI. An example of the segmentation is shown in Fig. 2.  

![](images/23b778f96b73c551da8e9fca514787579a1db095d3324245c283afca84b05639.jpg)  
Fig. 2 Segmentation of ROI. Contouring was drawn within the borders of the hematoma. The segmented hematoma was within the green contour slice by slice. The PHR was automatically dilated $5\mathrm{mm}$ and $10\mathrm{mm}$ in three dimensions after the IHR was drawn. The PHR- $\cdot5\mathrm{mm}$ was within the blue contour and the PHR- $10\mathrm{mm}$ was yellow. PHR peri-hematoma region, $IHR$ intra-hematoma region, $ROI$ region of interest  

Table 1 Parameters of support vector regression trained using the tune method   


<html><body><table><tr><td>Options</td><td>Type</td><td>Epsilon</td><td>Kernel</td><td>Cost</td><td>Gamma</td><td>Number of supportvectors</td></tr><tr><td>Parameters</td><td>Eps-regression</td><td>0.1</td><td>Radial</td><td>10</td><td>0.01</td><td>107</td></tr></table></body></html>  

# Measurement of Hematoma and Perihematomal Edema Volume  

Baseline and follow-up ICH and PHE volumes were automatically calculated using the 3D slicer software and an inhouse algorithm. The absolute PHE volume was calculated by subtracting the hematoma volume from the hematoma plus PHE volumes. The relative PHE (rPHE) was defined as absolute PHE volume divided by hematoma volume. The patients were then grouped into the large rPHE group and small rPHE group according to median rPHE.  

# Clinical and Radiological Analysis  

The clinical factor evaluations were performed by reviewing medical records, including age, gender, time to initial CT scan, admission blood pressure, and Glasgow coma scale (GCS) score, as well as the history of smoking, and alcohol consumption, hypertension, diabetes, anticoagulant therapy. The radiological factors based on baseline NCCT images were simultaneously assessed, including baseline hematoma volume (BHV), hematoma location, and secondary intraventricular hemorrhage.  

# Radiomics Feature Extraction and Selection  

A total of 1942 morphological, histogram, and texture features were extracted from each voxel of interest (VOI) using pyradiomics. Before selecting features, the feature values of all VOIs were normalized with a $Z$ -score: $\left(\mathtt{x}-\upmu\right)/\mathrm{~\upsigma~}$ , where $\mathbf{X}$ is the feature value, $\upmu$ is the average of the feature values among all patients, and σ is the corresponding standard deviation to eliminate the unit limit for each feature. Single-factor logistic regression analysis was carried out to select highly significant and correlated features. Then the least absolute shrinkage and selection operator (LASSO) regression method was performed based on maximum area under curve (AUC) criteria in the training cohort. A 10- fold cross-validation method was adopted to choose the optimized subset of features. Radscore was calculated by summing the selected features that were weighted by corresponding coefficients for each patient.  

# Radiomics Analysis and Development of the Nomogram Model  

The receiver operator characteristic (ROC) curve was used to assess the performance of the radiomics signatures of IHR and PHR features. The radiomics signature with the highest AUC was selected. A nomogram model was built based on significant clinical radiological factors and the selected radiomics signature by introducing stepwise multivariate logistic regression analysis. ROC analysis was used to evaluate the discrimination performance. Then, the constructed model from the training cohort was applied to the validation cohort, as the same method described above. The sensitivity and specificity in the training and the validation cohort were calculated based on the Youden index. The calibration curve and Hosmer-Lemeshow test were used to evaluate the consistency between predicted and actual probability.  

# Predicting the Follow-up rPHE Value with the Support Vector Regression Model  

The second model was constructed based on the support vector regression (SVR) with a radial kernel. It was trained using the tune method with $\mathrm{gamma}=10^{\wedge}(-4:4)$ and $\mathrm{cost}=10^{\wedge}(-5:5)$ to choose the best parameters. It was also estimated during a 10-cross-validation procedure on the training cohort (Table 1). The SVR model with the best root mean squared error (RMSE) score in the training cohort was assessed in the internal and independent validation cohorts. RMSE and the Pearson correlation coefficient were reported for the validation cohorts.  

# Statistical Analysis  

Statistical analyses were performed using IBM $\mathrm{SPSS^{\textregistered}}$ Statistics (version 22.0, IBM, Armonk, NY, USA) and R statistical software (version 3.6.2, Vienna, Austria). An independent t-test or Mann-Whitney U test was applied for the continuous variables, and the Chi-square test was applied for the categorical variables between the two cohorts as appropriate. The comparison of ROC curves was evaluated using DeLong’s method in MedCalc Statistical Software (version 15.6.1). A two-tailed $p<0.05$ value was considered to be statistically significant.  

# Results  

# Patients  

After excluding infratentorial hemorrhages $(n=51)$ ), primary intraventricular hemorrhages $(n=24)$ ) and patients who underwent subsequent surgery or interventional therapy $\left(n=77\right)$ ), 231 patients with ICH (166 men, 65 women; age: $63.51\pm12.80$ years, mean $\pm$ standard deviation; range:  

20–93 years) were enrolled. There were no significant differences in baseline clinical and radiological factors between the cohorts (all $p{>}0.05\$ ). The median absolute PHE volume on follow-up CT was $12.34~\mathrm{mL}$ (range 6.04–24.17 mL) and rPHE was 0.74 (range 0.42–1.06). Patients were divided into small and large rPHE groups according to the median rPHE of 0.74.  

Consequently, 117 patients were included in the training cohort, 45 patients in the internal validation cohort, and 69 patients in the independent cohort. The rates of the large rPHE group were $49.57\%$ (58 of 117), $48.89\%$ (22 of 45), and $59.42\%$ (41 of 69) in the training, internal, and independent validation cohorts, respectively. There were significant differences in BHV between the training and validation cohorts $(p<0.001)$ . The average hematoma volume of the large rPHE group was larger than that of the small rPHE group in the training cohort (26.55 vs. $11.88\mathrm{ml}$ ; $p<0.001,$ ), internal cohort (24.11 vs. $8.60\mathrm{ml}$ ; $p<0.001\$ ) and independent cohort (31.02 vs. $10.90\mathrm{ml}$ ; $p<0.001\$ ). No other statistically significant difference in clinical and radiological factors was observed between groups in cohorts (all $p{>}0.05$ , Table 2).  

Table 2 Comparison of patient baseline characteristics between large rPHE and small rPHE groups   


<html><body><table><tr><td rowspan="2">Characteristics</td><td colspan="3">Training cohort (n=117)</td><td colspan="3">Internal validation cohort (n=45)</td></tr><tr><td>Small rPHE (N= 59)</td><td>Large rPHE (N=58)</td><td>p</td><td>Small rPHE (N=23)</td><td>Large rPHE (N=22)</td><td>p</td></tr><tr><td>Age in yearsa</td><td>62.79 ± 13.12</td><td>65.16 ± 12.51</td><td>0.325</td><td>62.50</td><td>64.71</td><td>0.567</td></tr><tr><td>Male, n (%)</td><td>45 (76.27)</td><td>42 (72.41)</td><td>0.633</td><td>± 11.95 17 (73.91)</td><td>± 11.56 14 (63.64)</td><td>0.457</td></tr><tr><td>Hypertension, n (%)</td><td>47 (79.66)</td><td>48 (82.76)</td><td>0.668</td><td>16 (69.57)</td><td>17 (77.27)</td><td>0.559</td></tr><tr><td>Diabetes, n (%)</td><td>8 (13.56)</td><td>4 (6.90)</td><td>0.362</td><td>0 (0.00)</td><td>2 (9.09)</td><td>0.233</td></tr><tr><td>Alcohol consumption, n (%)</td><td>18 (30.51)</td><td>22 (37.93)</td><td>0.397</td><td>5 (21.74)</td><td>5 (22.73)</td><td>0.936</td></tr><tr><td>Smoking, n (%)</td><td>15 (25.42)</td><td>18 (31.03)</td><td>0.5</td><td>6 (26.09)</td><td>7 (31.82)</td><td>0.672</td></tr><tr><td>Admission SBP≥160 (mmHg),n (%)</td><td>32 (54.24)</td><td>36 (62.07)</td><td>0.391</td><td>7 (30.43)</td><td>12 (54.55)</td><td>0.102</td></tr><tr><td>Admission DBP≥100 (mmHg),n (%)</td><td>29 (49.15)</td><td>35 (60.34)</td><td>0.224</td><td>3 (13.04)</td><td>6 (27.27)</td><td>0.412</td></tr><tr><td>Admission GCS score ≥8, n (%)</td><td>27 (45.76)</td><td>34 (58.62)</td><td>0.164</td><td>15 (65.22)</td><td>20 (90.91)</td><td>0.087</td></tr><tr><td>Time to initial CT scana (h)</td><td>3.48</td><td>3.94</td><td>0.189</td><td>3.14</td><td>4.10</td><td>0.167</td></tr><tr><td>Baseline hematoma volumea (ml)</td><td>± 1.87 11.88</td><td>± 1.84 26.55</td><td><0.001</td><td>± 2.14 8.60</td><td>± 1.92 24.11</td><td><0.001</td></tr><tr><td>IVH, n (%)</td><td>± 6.15</td><td>± 19.68</td><td></td><td>± 5.48</td><td>± 18.74</td><td></td></tr><tr><td>Location in basal ganglia or thalamus, n (%)</td><td>30 (50.85) 53 (89.83)</td><td>34 (58.62) 50 (86.21)</td><td>0.398 0.546</td><td>8 (34.78) 19 (82.61)</td><td>6 (27.27) 19 (86.36)</td><td>0.586 1</td></tr></table></body></html>

GCS Glasgow coma scale, $SD$ standard deviation, IVH intraventricular hemorrhage, PHE Perihematomal edema, SBP Systolic blood pressure, $DBP$ Diastolic pressure a Data are presented as mean $\pm$ SD  

Table 3 Performance of baseline hematoma volume, radiomics signature, and nomogram model   


<html><body><table><tr><td>Cohort</td><td>Variate</td><td>AUC (95% CI)</td><td>Sensitivity</td><td>Specificity</td></tr><tr><td rowspan="3">Training cohort</td><td>Baseline hematoma volume</td><td>0.778 (0.691-0.849)</td><td>0.828</td><td>0.661</td></tr><tr><td>Radiomics signature</td><td>0.875 (0.801-0.929)</td><td>0.862</td><td>0.763</td></tr><tr><td>Nomogram model</td><td>0.922 (0.691-0.849)</td><td>0.707</td><td>0.966</td></tr><tr><td rowspan="3">Internal validation cohort</td><td>Baselinehematomavolume</td><td>0.842 (0.702-0.933)</td><td>0.864</td><td>0.739</td></tr><tr><td>Radiomics signature</td><td>0.862 (0.726-0.946)</td><td>0.636</td><td>1.000</td></tr><tr><td>Nomogram model</td><td>0.945 (0.833-0.991)</td><td>0.864</td><td>0.870</td></tr><tr><td rowspan="3">Independent validation cohort</td><td>Baseline hematoma volume</td><td>0.835 (0.727-0.914)</td><td>1.000</td><td>0.634</td></tr><tr><td>Radiomics signature</td><td>0.861 (0.756-0.932)</td><td>0.821</td><td>0.902</td></tr><tr><td>Nomogram model</td><td>0.902 (0.807-0.961)</td><td>0.893</td><td>0.829</td></tr></table></body></html>  

![](images/89422950b73283d43086d78eeec3e6c85ba3cf5bddbec88fea3ef2a61ec4f258.jpg)  
Fig. 3 a Comparison of ROC curves between the HR, PHR$5\mathrm{mm}$ , and PHR- $\cdot10\mathrm{mm}$ radiomics signature for predicting PHE growth in the training cohort. b The candidate features and the corresponding coefficients from the PHR-5 mm. $ROC$ receiver operating characteristic, PHE perihematomal edema, IHR intrahematoma region, $PHR$ perihematoma region, GLCM gray level co-occurrence matrix, GLRLM gray level run length matrix, NGTDM neighborhood gray tone difference matrix, GLSZM gray level size zone matrix  

# Feature Extraction and Selection  

The inter-reader ICC between two radiologists ranged from 0.856 to 0.932, and all features had good consistency on IHR, PHR-5 mm, and PHR-10 mm segmentation. Then, 315, 240, and 102 features were retained, respectively, after eliminating the redundant and irrelevant features. Finally, 13, 19, and 6 most valuable features were selected using the LASSO algorithm, respectively.  

# Radiomics Signature Building and Assessment of the Performance  

The LASSO provided the optimal radiomics signatures with values of $\mathrm{AUC}=0.711$ , 0.875, and 0.692 for IHR, PHR$5\mathrm{mm}$ , and PHR- $10\mathrm{mm}$ in the training cohort, respectively. The ROC curves of the radiomics signatures on the training cohort are showed in Fig. 3a. For each cohort, the PHR$5\mathrm{mm}$ radiomics signature achieved the highest AUC (training cohort: 0.875; internal validation cohort: 0.862; independent validation cohort: 0.861; all $p<0.05$ ). The candidate features and the corresponding coefficients from the PHR-5 mm are shown in Fig. 3b.  

![](images/b4e8857f3653a91a6303c4356166c1c7c42cb1dbfa75176397c81bdb5a350528.jpg)  
Fig. 4 Comparisons of ROC curves between the nomogram model, radiomics signature, and baseline hematoma volume for the prediction of PHE growth on the training (a), internal (b), and independent (c) validation cohorts. $ROC$ receiver operating characteristic  

# Development and Predictive Performance of the Nomogram Model  

The logistic regression analysis was applied on the basis of the PHR- $\cdot5\mathrm{mm}$ radiomics signature and the BHV. In the training cohort, the nomogram model showed best predictive performance (AUC: 0.922, $95\%$ CI: 0.691–0.849, sensitivity: 0.707, specificity: 0.966, $p{=}0.044$ , $<0.001$ , respectively) compared to the radiomics signature (AUC: 0.875, $95\%$ CI: 0.801–0.929, sensitivity: 0.862, specificity: 0.763) and the BHV (AUC: 0.778, $95\%$ CI: 0.691–0.849, sensitivity: 0.828, specificity: 0.661) alone. Moreover, the AUC of the nomogram model (0.945 and 0.902, sensitivity: 0.864 and 0.893, specificity: 0.870 and 0.829) was higher than that of the PHR- $\cdot5\mathrm{mm}$ radiomics signature (0.862 and 0.861, sensitivity: 0.636 and 0.821, specificity: 1.000 and 0.902) and the BHV (0.842 and 0.835, sensitivity: 0.864 and 1.000, specificity: 0.739 and 0.634) on the internal and independent validation cohorts (Table 3). The ROC curves for the PHR-5 mm radiomics signature, BHV, and nomogram model on the internal and independent validation cohorts are shown in Fig. 4. The nomogram model was conducted to visualize the results (Fig. 5a).  

The calibration curves of the nomogram model on the internal and independent validation cohorts are presented in Fig. 5b, c. There was no statistical significance between internal and independent validation cohorts $\overset{\vartriangle}{\boldsymbol{p}}=0.882$ and 0.710, respectively) by the Hosmer–Lemeshow test. The results suggested that the predictive performance and actual outcome had favorable agreement.  

![](images/a7a9c6facdf66c86773c40670886276ad28602c35abafc0e815c632529da9726.jpg)  
Fig. 6 a The bubble plot shows the baseline hematoma volume and radiomics signature for all individual patients, the size of the bubbles represents the rPHE values, and the colors represent different cohorts. b The scatter plot shows the consistency between the predictive and actual rPHE values  

# Predicting the Follow-up rPHE Value with Support Vector Regression Model  

The second model based on the SVR model was able to accurately predict the follow-up rPHE value, with RMSE of 0.60 and 0.45, Pearson correlation coefficient of 0.73 and 0.68 (both $p<0.001,$ ) on the internal and independent validation cohorts, respectively. The predictive rPHE values corresponding to the BHV and radiomics signature for all individual patients of the internal and independent validation cohorts are shown in Fig. 6a, and the predictive rPHE values together with the actual values are shown in Fig. 6b.  

# Discussion  

In this study, we examined the ability of NCCT-based radiomics features from intrahematoma and perihematoma regions to predict PHE growth in the first $^{241}$ after ICH. PHR-5 mm radiomics signature improved the discrimination ability of the IHR or PHR- $10\mathrm{mm}$ radiomics signatures. From this finding, the performance of the nomogram model combining the PHR-5 mm radiomics signature and the BHV was evaluated and validated. The nomogram model outperformed the radiomics signature and the clinical-radiological parameter. We could also predict the overall value of rPHE growth in the validation cohorts.  

Radiomics is a relatively new tool mainly applied in oncology [18–20], while only a few studies used radiomics analysis to assess hemorrhagic lesions. Zhang et al. found that radiomics features extracted from the NCCT scan can differentiate AVM-related intraparenchymal hematomas from other lesions with high accuracy [21], while other studies have investigated the radiomics heterogeneity of expanded hematoma [14, 22]. PHE may cause neurological deterioration due to biological injury and additional mass effects beyond that of the hematoma [23]. Jauch et al. [24] reported that absolute PHE volume doubles, on average, during the first $^{241}$ after hemorrhage in patients with ICH imaged within $^{3\mathrm{h}}$ of onset. Another study [25] suggested using rPHE values $20\mathrm{h}$ after baseline CT scan as a significant independent predictor of 12-week functional outcome in patients with hyperacute ICH. Therefore, a radiomicsbased predictive analysis focusing on early PHE growth after ICH could be an auxiliary valuable therapeutic strategy to improve clinical outcomes.  

With the degradation of hemoglobin and other substances in the hematoma, the inflammatory factors are chemoattracted and induced, which promotes secondary damage to the surrounding tissues of the hematoma, resulting in the production of PHE [23]. Studies have shown that patients with cerebral hemorrhage have hypoperfusion and decreased oxygen metabolism rate in the surrounding tissues of the hematoma after $^{24\mathrm{h}}$ of onset [26, 27]. Radiomics features extracted from the intrahematoma and perihematoma areas may provide information both on the hematoma and its surrounding microenvironment, which have an important role in the prediction of PHE growth. Our study confirmed the superiority of the PHR-5 mm radiomics approach and suggested that the radiomics features of the surrounding area encompassing the hematoma may be a more unique and reliable indicator of the state of the hematoma microenvironment, which may differ according to the degree of PHE. The distance of the surrounding area was taken from previous studies [28, 29].  

On the PHR-5 mm segmentation, 14 of 19 valuable features were deprived of wavelet images. The wavelet transformation can decompose a three-dimensional image into low-frequency and/or high-frequency components at different scales and, in turn, help to perform local analysis and more effectively detect the image edge [30]. The top 2 features contributing to the predictive model were WaveletHLH_GLSZM_SizeZoneNonUniformityNormalized and Wavelet-LHL_NGTDM_Busyness with coefficients of 0.395 and 0.290. The SizeZoneNonUniformityNormalized measures the variability of size zone volumes throughout the image, with a lower value indicating more homogeneity among zone size volumes in the image [31]. On the other hand, a high value for busyness indicates a ‘busy’ image, with rapid intensity changes between pixels and their neighborhood, implying a more heterogeneous composition in the image [32]. The average values of the two features were higher in the large rPHE group compared to the small rPHE group (0.22 vs. $-0.29$ , 0.14 vs. $-0.18,$ , indicating that the surrounding area of the small rPHE group contains more homogeneity, which may decrease the degree of PHE.  

The nomogram model combining BHV and the PHR$5\mathrm{mm}$ radiomics signature demonstrated excellent discrimination in the training and validation cohorts. The mean BHV of large rPHE was larger than that of small rPHE, which is consistent with previous studies [6]. RodriguezLuna et al. found that the volume of hematoma is significantly related to the formation of PHE, and it can independently predict the development of PHE [23]. Studies have shown that retraction of clots and change of local hydrostatic pressure result in the formation of early PHE. The mass effect of hematoma causes damage to surrounding brain tissue, leading to ischemia and hypoxia, and eventually edema and necrosis around the hematoma [6, 33]. Therefore, interventions aimed at limiting the extent of the primary injury can lead to the lower early formation of PHE and downstream secondary injury by reducing hematoma volume or hematoma expansion. The nomogram model is superior to a single clinical feature while slightly higher in predicting performance compared to the radiomics signature on the validation cohorts. This finding indicated that the radiomics features have an overwhelming weight in the nomogram model for improving the discrimination capability. Furthermore, we proposed SVR-based model with BHV and a subset of radiomics features as the independent variables to predict the change of PHE and overcome the drawbacks of conventional methods that are extremely influenced by outliers.  

This study has a few limitations. First, it is a retrospective study with a relatively small sample. In our research, all the patients underwent CT scans at our institutes within 6 h of onset. Therefore, multicenter studies with a larger sample and prospective research are expected to identify the power of the models with a larger cohort. Secondly, it was challenging to segment edema by an automatic technique. Thirdly, we assessed PHE growth only up to the first $^{241}$ ; however, PHE growth is fastest during the first few days after onset and continues at a slower rate between 2 and 3 weeks; thus, our results are not applicable for delayed PHE formation. Fourthly, only SVR was trained for the second model; other machine learning approaches had not been evaluated, considering this study’s small dataset. Finally, prognostic information such as 90-day mortality were not included. The value of models in predicting outcomes of patients with acute ICH should be further confirmed.  

In conclusion, a new predictive model integrating radiomics signature with BHV based on NCCT images offers a reliable and powerful diagnostic tool for predicting PHE growth at an early stage. Future studies are expected to provide a convincing, objective, and convenient method for clinical practice, thus improving treatment guidelines for patients with ICH.  

Funding This study has received funding by Social Develop Foundation of Yangzhou (No.2017066), Yangzhou City Science and Education Strengthening Leading Talents Project (No.LJRC201810), Yangzhou City Science and Education Strengthening Key Talents Project (No.ZDRC201873) and Jiangsu Province “Six First Project” for High-Level Health Professionals (No.LGY2019032).  

Author Contribution All authors contributed to the study conception and design. Material preparation, data collection and analysis were performed by Jia Wang, Xing Xiong, Jinzhao Zou, and Jianxiong Fu. The first draft of the manuscript was written by Jia Wang and Xing Xiong. All authors commented on previous versions of the manuscript. All authors read and approved the final manuscript.  

Conflict of interest J. Wang, X. Xiong, J. Zou, J. Fu, Y. Yin and J. Ye declare that they have no competing interests.  

# References  

1. Okauchi M, Xi G, Keep RF, Hua Y. Tissue-type transglutaminase and the effects of cystamine on intracerebral hemorrhage-induced brain edema and neurological deficits. Brain Res. 2009;1249:   
229–36.   
2. Zheng H, Chen C, Zhang J, Hu Z. Mechanism and Therapy of Brain Edema after Intracerebral Hemorrhage. Cerebrovasc Dis.   
2016;42:155–69.   
3. Babi MA, James ML. Peri-Hemorrhagic Edema and Secondary Hematoma Expansion after Intracerebral Hemorrhage: From Benchwork to Practical Aspects. Front Neurol. 2017;8:4.   
4. Cao S, Zheng M, Hua Y, Chen G, Keep RF, Xi G. Hematoma Changes During Clot Resolution After Experimental Intracerebral Hemorrhage. Stroke. 2016;47:1626–31.   
5. Keep RF, Hua Y, Xi G. Intracerebral haemorrhage: mechanisms of injury and therapeutic targets. Lancet Neurol. 2012;11:720–31.   
6. Urday S, Kimberly WT, Beslow LA, Vortmeyer AO, Selim MH, Rosand J, Simard JM, Sheth KN. Targeting secondary injury in intracerebral haemorrhage--perihaematomal oedema. Nat Rev Neurol. 2015;11:111–22.   
7. Arima H, Wang JG, Huang Y, Heeley E, Skulina C, Parsons MW, Peng B, Li Q, Su S, Tao QL, Li YC, Jiang JD, Tai LW, Zhang JL, Xu E, Cheng Y, Morgenstern LB, Chalmers J, Anderson CS; INTERACT Investigators. Significance of perihematomal edema in acute intracerebral hemorrhage: the INTERACT trial. Neurology.   
2009;73:1963–8.   
8. Morotti A, Boulouis G, Dowlatshahi D, Li Q, Barras CD, Delcourt C, Yu Z, Zheng J, Zhou Z, Aviv RI, Shoamanesh A, Sporns PB, Rosand J, Greenberg SM, Al-Shahi Salman R, Qureshi AI, Demchuk AM, Anderson CS, Goldstein JN, Charidimou A; International NCCT ICH Study Group. Standards for Detecting, Interpreting, and Reporting Noncontrast Computed Tomographic Markers of Intracerebral Hemorrhage Expansion. Ann Neurol. 2019;86:480–92.   
9. Appelboom G, Bruce SS, Hickman ZL, Zacharia BE, Carpenter AM, Vaughan KA, Duren A, Hwang RY, Piazza M, Lee K, Claassen J, Mayer S, Badjatia N, Connolly ES Jr. Volume-dependent effect of perihaematomal oedema on outcome for spontaneous intracerebral haemorrhages. J Neurol Neurosurg Psychiatry.   
2013;84:488–93.   
10. Volbers B, Staykov D, Wagner I, Dörfler A, Saake M, Schwab S, Bardutzky J. Semi-automatic volumetric assessment of perihemorrhagic edema with computed tomography. Eur J Neurol.   
2011;18:1323–8.   
11. Chen L, Xu M, Yan S, Luo Z, Tong L, Lou M. Insufficient cerebral venous drainage predicts early edema in acute intracerebral hemorrhage. Neurology. 2019;93:e1463–73.   
12. Feng H, Zhang H, He W, Zhou J, Zhao X. Jugular Venous Reflux Is Associated with Perihematomal Edema after Intracerebral Hemorrhage. Biomed Res Int. 2017;2017:7514639.   
13. Yan PF, Yan L, Hu TT, Xiao DD, Zhang Z, Zhao HY, Feng J. The Potential Value of Preoperative MRI Texture and Shape Analysis in Grading Meningiomas: A Preliminary Investigation. Transl Oncol.   
2017;10:570–7.   
14. Xie H, Ma S, Wang X, Zhang X. Noncontrast computer tomography-based radiomics model for predicting intracerebral hemorrhage expansion: preliminary findings and comparison with conventional radiological model. Eur Radiol. 2020;30:87–98.   
15. Lubner MG, Smith AD, Sandrasegaran K, Sahani DV, Pickhardt PJ. CT Texture Analysis: Definitions, Applications, Biologic Correlates, and Challenges. Radiographics. 2017;37:1483–503.   
16. Urday S, Beslow LA, Goldstein DW, Vashkevich A, Ayres AM, Battey TW, Selim MH, Kimberly WT, Rosand J, Sheth KN. Measurement of perihematomal edema in intracerebral hemorrhage. Stroke. 2015;46:1116–9.   
17. Gusdon AM, Gialdini G, Kone G, Baradaran H, Merkler AE, Mangat HS, Navi BB, Iadecola C, Gupta A, Kamel H, Murthy SB. Neutrophil-Lymphocyte Ratio and Perihematomal Edema Growth in Intracerebral Hemorrhage. Stroke. 2017;48:2589–92.   
18. Yang L, Dong D, Fang M, Zhu Y, Zang Y, Liu Z, Zhang H, Ying J, Zhao X, Tian J. Can CT-based radiomics signature predict KRAS/NRAS/BRAF mutations in colorectal cancer? Eur Radiol. 2018;28:2058–67.   
19. Kang D, Park JE, Kim YH, Kim JH, Oh JY, Kim J, Kim Y, Kim ST, Kim HS. Diffusion radiomics as a diagnostic model for atypical manifestation of primary central nervous system lymphoma: development and multicenter external validation. Neuro Oncol. 2018;20:1251–61.   
20. Li Y, Liu X, Qian Z, Sun Z, Xu K, Wang K, Fan X, Zhang Z, Li S, Wang Y, Jiang T. Genotype prediction of ATRX mutation in lower-grade gliomas using an MRI radiomics signature. Eur Radiol. 2018;28:2960–8.   
21. Zhang Y, Zhang B, Liang F, Liang S, Zhang Y, Yan P, Ma C, Liu A, Guo F, Jiang C. Radiomics features on non-contrast-enhanced CT scan can precisely classify AVM-related hematomas from other spontaneous intraparenchymal hematoma types. Eur Radiol. 2019;29:2157–65.   
22. Xu W, Ding Z, Shan Y, Chen W, Feng Z, Pang P, Shen Q. A Nomogram Model of Radiomics and Satellite Sign Number as Imaging Predictor for Intracranial Hematoma Expansion. Front Neurosci. 2020;14:491.   
23. Gebel JM Jr, Jauch EC, Brott TG, Khoury J, Sauerbeck L, Salisbury S, Spilker J, Tomsick TA, Duldner J, Broderick JP. Relative edema volume is a predictor of outcome in patients with hyperacute spontaneous intracerebral hemorrhage. Stroke. 2002;33:2636–41.   
24. Jauch E, Gebel J, Salisbury S, Broderick J, Brott T, Kothari R, Tomsick T, Pancioli A, Barsan W. Lack of association between early edema and outcome in spontaneous intracerebral hemorrhage. Conference Proceedings. Stroke. 1999;30:249.   
25. Rodriguez-Luna D, Stewart T, Dowlatshahi D, Kosior JC, Aviv RI, Molina CA, Silva Y, Dzialowski I, Lum C, Czlonkowska A, Boulanger JM, Kase CS, Gubitz G, Bhatia R, Padma V, Roy J, Subramaniam S, Hill MD, Demchuk AM; PREDICT/Sunnybrook ICH CTA Study Group. Perihematomal Edema Is Greater in the Presence of a Spot Sign but Does Not Predict Intracerebral Hematoma Expansion. Stroke. 2016;47:350–5.   
26. Oeinck M, Neunhoeffer F, Buttler KJ, Meckel S, Schmidt B, Czosnyka M, Weiller C, Reinhard M. Dynamic cerebral autoregulation in acute intracerebral hemorrhage. Stroke. 2013;44:2722–8.   
27. Su X, Zheng K, Ma Q, Huang J, He X, Chen G, Wang W, Su F, Tang H, Wu H, Tong S. Effect of local mild hypothermia on regional cerebral blood flow in patients with acute intracerebral hemorrhage assessed by 99mTc-ECD SPECT imaging. J Xray Sci Technol. 2015;23:101–9.   
28. McCourt R, Gould B, Kate M, Asdaghi N, Kosior JC, Coutts S, Hill MD, Demchuk A, Jeerakathil T, Emery D, Butcher KS. Bloodbrain barrier compromise does not predict perihematoma edema growth in intracerebral hemorrhage. Stroke. 2015;46:954–60.   
29. Xu H, Li R, Duan Y, Wang J, Liu S, Zhang Y, He W, Qin X, Cao G, Yang Y, Zhuge Q, Yang J, Chen W. Quantitative assessment on blood-brain barrier permeability of acute spontaneous intracerebral hemorrhage in basal ganglia: a CT perfusion study. Neuroradiology. 2017;59:677–84.   
30. Liu Y, Saleh Z, Song Y, Chan M, Li X, Shi C, Qian X, Tang X. Novel Wavelet-Based Segmentation of Prostate CBCT Images with Implanted Calypso Transponders. Int J Med Phys Clin Eng Radiat Oncol. 2017;6:336–43.   
31. Said M, Nilsson P, Ceberg C. Analysis of dose heterogeneity using a subvolume-DVH. Phys Med Biol. 2017;62:N517–24.   
32. Amadasun M, King R. Textural features corresponding to textural properties. IEEE Trans Syst Man Cybern A Syst Hum. 1989;19:1264–74.   
33. Gould B, McCourt R, Gioia LC, Kate M, Hill MD, Asdaghi N, Dowlatshahi D, Jeerakathil T, Coutts SB, Demchuk AM, Emery D, Shuaib A, Butcher K; ICH ADAPT Investigators. Acute blood pressure reduction in patients with intracerebral hemorrhage does not result in borderzone region hypoperfusion. Stroke. 2014;45:2894–9.  