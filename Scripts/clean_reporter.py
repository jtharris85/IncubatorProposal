rom collections import OrderedDict
import re

all_reporter.drop(columns=['ADMINISTERING_IC',
                           'ARRA_FUNDED',
                           'ED_INST_TYPE',
                           'FUNDING_ICs',
                           'FUNDING_Ics',
                           'ORG_CITY',
                           'ORG_COUNTRY',
                           'ORG_DEPT',
                           'ORG_DUNS',
                           'ORG_FIPS',
                           'ORG_IPF_CODE',
                           'ORG_ZIPCODE',
                           'PHR',
                           'SUBPROJECT_ID'], inplace = True)

all_reporter = all_reporter.replace({np.nan:'XXX'})

cause_search_library = OrderedDict({r'.*HIV.*':'HIV/AIDS',
                        r'.*AIDS.*':'HIV/AIDS',
                        r'.*(?i)motor\sneuron.*':'Motor neuron disease',
                        r'.*(?i)tuberculosis.*':'Tuberculosis',
                        r'.*(?i)syphilis.*':'Sexually transmitted infections excluding HIV',
                        r'.*(?i)chlamydia.*':'Sexually transmitted infections excluding HIV',
                        r'.*(?i)(gonococc|gonorrhea).*':'Sexually transmitted infections excluding HIV',
                        r'.*(?i)trichomon.*':'Sexually transmitted infections excluding HIV',
                        r'.*(?i)(varicella|herpes.zoster).*':'Varicella and herpes zoster',
                        r'.*(?i)herpes.*':'Sexually transmitted infections excluding HIV',
                        r'.*(?i)lower\srespiratory\sinfection.*':'Lower respiratory infections',
                        r'.*(?i)(influenza|pneumonia|respiratory\ssyncytial).*':'Lower respiratory infections',
                        r'.*(?i)upper\srespiratory\sinfection.*':'Upper respiratory infections',
                        r'.*(?i)otitis.*':'Otitis media',
                        r'.*(?i)diarrhea.*':'Diarrheal diseases',
                        r'.*(?i)(cholera|shigella|enteropathogenic\se\scoli|enterotoxigenic\se\scoli|campylobacter|entamoeba|cryptosporidium|rotavirus|aeromonas|clostridium\sdifficile|norovirus|adenovirus).*':'Diarrheal diseases',
                        r'.*(?i)typhoid.*':'Typhoid and paratyphoid',
                        r'.*[iI]NTS.*':'Invasive Non-typhoidal Salmonella (iNTS)',
                        r'.*(?i)salmonella.*':'Invasive Non-typhoidal Salmonella (iNTS)',
                        r'.*(?i)non\-typhoidal.*':'Invasive Non-typhoidal Salmonella (iNTS)',
                        r'.*(?i)malaria.*':'Malaria',
                        r'.*(?i)chagas.*':'Chagas disease',
                        r'.*(?i)leishmaniasis':'Leishmaniasis',
                        r'.*(?i)trypanosomiasis.*':'African trypanosomiasis',
                        r'.*(?i)schistosomiasis.*':'Schistosomiasis',
                        r'.*(?i)cysticercosis.*':'Cysticercosis',
                        r'.*(?i)echinococcosis.*':'Cystic echinococcosis',
                        r'.*(?i)filariasis.*':'Lymphatic filariasis',
                        r'.*(?i)onchocerciasis.*':'Onchocerciasis',
                        r'.*(?i)trachoma.*':'Trachoma',
                        r'.*(?i)dengue.*':'Dengue',
                        r'.*(?i)yellow\sfever.*':'Yellow fever',
                        r'.*(?i)rabies.*': 'Rabies',
                        r'.*(?i)(ascariasis|trichuriasis|hookworm|nematode).*':'Intestinal nematode infections',
                        r'.*(?i)trematodias.*':'Food-borne trematodiases',
                        r'.*(?i)leprosy.*':'Leprosy',
                        r'.*(?i)ebola.*':'Ebola',
                        r'.*(?i)zika.*':'Zika virus',
                        r'.*(?i)guinea\sworm.*':'Guinea worm disease',
                        r'.*(?i)tropical\sdisease.*':'Other neglected tropical diseases',
                        r'.*(?i)meningitis.*':'Meningitis',
                        r'.*(?i)encephalitis.*':'Encephalitis',
                        r'.*(?i)diphtheria.*':'Diphtheria',
                        r'.*(?i)whooping\scough.*':'Whooping cough',
                        r'.*(?i)tetanus.*':'Tetanus',
                        r'.*(?i)measle.*':'Measles',
                        r'.*(?i)hepatitis.*':'Acute hepatitis',
                        r'.*(?i)maternal.*':'Maternal disorders',
                        r'.*(?i)neonatal.*':'Neonatal disorders',
                        r'.*(?i)protein.energy.*':'Protein-energy malnutrition',
                        r'.*PEM':'Protein-energy malnutrition',
                        r'.*(?i)iodine.deficien.*':'Iodine deficiency',
                        r'.*(?i)vitamin.a.*':'Vitamin A deficiency',
                        r'.*(?i)iron.deficien.*':'Dietary iron deficiency',
                        r'.*(?i)(lip|oral|mouth)\s(cancer|neoplasm).*':'Lip and oral cavity cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(lip|oral|mouth).*':'Lip and oral cavity cancer',
                        r'.*(?i)nasopharynx.*':'Nasopharynx cancer',
                        r'.*(?i)pharnyx.*':'Other pharynx cancer',
                        r'.*(?i)(esophageal|esophagus).*\s(cancer|neoplasm).*':'Esophageal cancer',
                        r'.*(?i)stomach\s.*(cancer|neoplasm).*':'Stomach cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*stomach.*':'Stomach cancer',
                        r'.*(?i)(colorectal|colon|rectum)\s(cancer|neoplasm).*':'Colon and rectum cancer',
                        r'.*(?i)(cancer|neoplasm)\s(colorectal|colon|rectum).*':'Colon and rectum cancer',
                        r'.*(?i)liver\s.*(cancer|neoplasm).*':'Liver cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*liver.*':'Liver cancer',
                        r'.*(?i)(gallbladder|biliary)\s.*(cancer|neoplasm).*':'Gallbladder and biliary tract cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(gallbladder|biliary).*':'Gallbaldder and biliary tract cancer',
                        r'.*(?i)(pancreatic|pancreas).*':'Pancreatic cancer',
                        r'.*(?i)larynx\s.*(cancer|neoplasm).*':'Larynx cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*larynx.*':'Larynx cancer',
                        r'.*(?i)(trachea|bronchus|lung)\s.*(cancer|neoplasm).*':'Tracheal, bronchus, and lung cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(trachea|bronchus|lung).*':'Tracheal, bronchus, and lung cancer',
                        r'.*(?i)(non.melanoma|squamous.cell|basal.cell)\s.*(cancer|neoplasm|carcinoma).*':'Non-melanoma skin cancer',
                        r'.*(?i)melanoma.*':'Malignant skin melanoma',
                        r'.*(?i)skin\s.*(cancer|neoplasm).*':'Malignant skin melanoma',
                        r'.*(?i)breast\s.*(cancer|neoplasm).*':'Breast cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*breast.*':'Breast cancer',
                        r'.*(?i)(cervical|cervix)\s.*(cancer|neoplasm).*':'Cervical cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(cervical|cervix).*':'Cervical cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(uterine|uterus).*':'Uterine cancer',
                        r'.*(?i)(uterine|uterus)\s.*(cancer|neoplasm).*':'Uterine cancer',
                        r'.*(?i)(ovarian|ovary)\s.*(cancer|neoplasm).*':'Ovarian cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(ovarian|ovary).*':'Ovarian cancer',
                        r'.*(?i)prostate\s.*(cancer|neoplasm).*':'Prostate cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*prostate.*':'Prostate cancer',
                        r'.*(?i)(testicular|testes|testicle).*(cancer|neoplasm)':'Testicular cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(testicular|testes|testicle)':'Testicular cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*kidney':'Kidney cancer',
                        r'.*(?i)kidney\s.*(cancer|neoplasm)':'Kidney cancer',
                        r'.*(?i)bladder\s.*(cancer|neoplasm)':'Bladder cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*bladder.*':'Bladder cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*(brain|nervous).*':'Brain and nervous system cancer',
                        r'.*(?i)(cancer|neoplasm)\s.*thyroid.*':'Thyroid cancer',
                        r'.*(?i)(brain|nervous)\s.*(cancer|neoplasm)':'Brain and nervous system cancer',
                        r'.*(?i)thyroid\s.*(cancer|neoplasm)':'Thyroid cancer',
                        r'.*(?i)mesothelioma.*':'Mesothelioma',
                        r'.*(?i)non\-hodgkin.*':'Non-Hodgkin lymphoma',
                        r'.*(?i)hodgkin.*':'Hodgkin lymphoma',
                        r'.*(?i)leukemia.*':'Leukemia',
                        r'.*(?i)myeloma.*':'Multiple myeloma',
                        r'.*(?i)(rheumat|valvular).*heart.*':'Rheumatic heart disease',
                        r'.*RHD.*':'Rheumatic heart disease',
                        r'.*(?i)(non.?rheumatic|calcific.aort|degenerative.mitr).*':'Non-rheumatic valvular heart disease',
                        r'.*(?i)ischem.*heart.*':'Ischemic heart disease',
                        r'.*IHD.*':'Ischemic heart disease',
                        r'.*(?i)heart.*ischem.*':'Ischemic heart disease',
                        r'.*(?i)(stroke|intracerebral.hemorrhage|subarachnoid.hemorrhage).*':'Stroke',
                        r'.*(?i)hypertensive.*':'Hypertensive heart disease',
                        r'.*(?i)cardiomyopathy.*':'Cardiomyopathy and myocarditis',
                        r'.*(?i)myocarditis.*':'Cardiomyopathy and myocarditis',
                        r'.*(?i)fibrillation.*':'Atrial fibrillation and flutter',
                        r'.*(?i)aort.*aneurysm.*':'Aortic aneurysm',
                        r'.*(?i)peripheral\sart.*':'Peripheral artery disease',
                        r'.*(?i)endocarditis.*':'Endocarditis',
                        r'.*COPD.*':'Chronic obstructive pulmonary disease',
                        r'.*(?i)obstruct.*pulmonary.*':'Chronic obstructive pulmonary disease',
                        r'.*(?i)pneumoconiosis.*':'Pneumoconiosis',
                        r'.*(?i)silicosis.*':'Pneumoconiosis',
                        r'.*(?i)asbestosis.*':'Pneumoconiosis',
                        r'.*(?i)\scoal\s.*':'Pneumoconiosis',
                        r'.*(?i)asthma.*':'Asthma',
                        r'.*(?i)interstitial\slung.*':'Interstitial lung disease and pulmonary sarcoidosis',
                        r'.*(?i)sarcoidosis.*':'Interstitial lung disease and pulmonary sarcoidosis',
                        r'.*(?i)cirrhos.*':'Cirrhosis and other chronic liver diseases',
                        r'.*(?i)chronic.*liver.*':'Cirrhosis and other chronic liver diseases',
                        r'.*(?i)peptic\sulcer.*':'Upper digestive system diseases',
                        r'.*(?i)gastritis.*':'Upper digestive system diseases',
                        r'.*(?i)duodenitis.*':'Upper digestive system diseases',
                        r'.*(?i)reflux.*':'Upper digestive system diseases',
                        r'.*(?i)gastroesophageal.*':'Upper digestive system diseases',
                        r'.*(?i)appendi.*':'Appendicitis',
                        r'.*(?i)(ileus|intestinal)\sobstruction.*':'Paralytic ileus and intestinal obstruction',
                        r'.*(?i)hernia.*':'Inguinal, femoral, and abdominal hernia',
                        r'.*(?i)inflam.*bowel.*':'Inflammatory bowel disease',
                        r'.*(IBS|IBD).*':'Inflammatory bowel disease',
                        r'.*(?i)(vascular.intestin|mesenteric.vasc|intestinal.ischem).*':'Vascular intestinal disorders',
                        r'.*(?i)pancreatitis.*':'Pancreatitis',
                        r'.*(?i)alzheimer.*':'Alzheimer\'s disease and other dementias',
                        r'.*(?i)dementia.*':'Alzheimer\'s disease and other dementias',
                        r'.*(?i)parkinson.*':'Parkinson\'s disease',
                        r'.*(?i)epilep(sy|tic).*':'Epilepsy',
                        r'.*(?i)multiple\ssclero(sis|tic).*':'Multiple sclerosis',
                        r'.*(?i)motor.neuron.*':'Motor neuron disease',
                        r'.*(?i)gehrig.*':'Motor neuron disease',
                        r'.*lateral\ssclero(sy|tic).*':'Motor neuron disease',
                        r'.*(?i)(migraine|tension|cluster).*(headache)?.*':'Headache disorders',
                        r'.*(?i)conduct\sdisorder.*':'Conduct disorder',
                        r'.*(?i)schizo.*':'Schizophrenia',
                        r'.*(?i)(depressi|dysthymia).*':'Depressive disorders',
                        r'.*(?i)bipolar.*':'Bipolar disorder',
                        r'.*(?i)anxi.*':'Anxiety disorders',
                        r'.*(?i)(anorex|bulim).*':'Eating disorders',
                        r'.*(?i)(asperger|autis(tic|m)).*':'Autism spectrum disorders',
                        r'.*(ADHD|(?i)attention.deficit|hyperactiv).*':'Attention-deficit/hyperactivity disorder',
                        r'.*(?i)idiopath.*':'Idiopathic developmental intellectual disability',
                        r'.*(?i)alcohol.*':'Alcohol use disorders',
                        r'.*(?i)(opioid|cocaine|amphetamine|cannabis|marijuana|drug).*\sabuse.*':'Drug use disorders',
                        r'.*(CKD|(?i)chronic\skidney).*':'Chronic kidney disease',
                        r'.*(?i)(diabetes|diabetic).*':'Diabetes mellitus',
                        r'.*(?i)glomerulonephr.*':'Acute glomerulonephritis',
                        r'.*(?i)dermatit.*':'Dermatitis',
                        r'.*(?i)psoria.*':'Psoriasis',
                        r'.*(?i)(cellulitis|pyoderma|bacterial\sskin).*':'Bacterial skin diseases',
                        r'.*(?i)scabies.*':'Scabies',
                        r'.*(?i)fungal.*':'Fungal skin diseases',
                        r'.*(?i)viral\sskin.*':'Viral skin diseases',
                        r'.*(?i)acne.*':'Acne vulgaris',
                        r'.*(?i)alopecia.*':'Alopecia areata',
                        r'.*(?i)pruritus.*':'Pruritus',
                        r'.*(?i)urticari.*':'Urticaria',
                        r'.*(?i)decubit.*':'Decubitus ulcer',
                        r'.*(?i)(glaucoma|cataract|macular.degener|refraction|vision.loss).*':'Blindness and vision impairment',
                        r'.*(?i)hearing.*loss.*':'Age-related and other hearing loss',
                        r'.*(?i)rheumat.*arthrit.*':'Rheumatoid arthritis',
                        r'.*(?i)osteoarthritis.*':'Osteoarthritis',
                        r'.*(?i)back.*pain.*':'Low back pain',
                        r'.*(?i)neck.*pain.*':'Neck pain',
                        r'.*(?i)gout.*':'Gout',
                        r'.*(?i)(neural.tube|congenital.heart|cleft|down.syndrome|turner.syndrome|klinefelter.syndrome|congenital).*':'Congenital birth defects',
                        r'.*(?i)(urolithiasis|urinary.tract.infect|prostatic.hyperplasia|male.infertility).*':'Urinary diseases and male infertility',
                        r'.*(PMS|(?i)uterine.fibroid|polycystic|female.infertil|endometrios|genital.prolapse|premenstrual|gynecol).*':'Gynecological diseases',
                        r'.*(?i)(thalassemi|sickle.cell|g6pd|hemoglobinopath|hemolytic.anemia).*':'Hemoglobinopathies and hemolytic anemias',
                        r'.*(?i)(endocrine|metabolic|blood|immune).*disorder.*':'Endocrine, metabolic, blood, and immune disorders',
                        r'.*(?i)caries.*(deciduous|permanent).*':'Oral disorders',
                        r'.*(?i)periodontal.*diseas.*':'Oral disorders',
                        r'.*(?i)(edentulis|tooth.loss|oral.disorder).*':'Oral disorders',
                        r'.*(SIDS|(?i)sudden.infant.death).*':'Sudden infant death syndrome',
                        r'.*(?i)gallbladder.*':'Gallbladder and biliary diseases',
                        r'.*(?i)bil(e|iary).*':'Gallbladder and biliary diseases',
                        r'.*(?i)digest.*':'Other digestive diseases',
                        r'.*(?i)sense.organ.dis.*':'Other sense organ diseases',
                        f'.*(?i)intestinal.infect.*':'Other intestinal infectious diseases',
                        r'.*(?i)(cardiovascular|heart).*':'Other cardiovascular and circulatory diseases',
                        r'.*(?i)neurol.*':'Other neurological disorders',
                        r'.*(?i)mental.*':'Other mental disorders',
                        r'.*(?i)respiratory.*':'Other chronic respiratory diseases',
                        r'.*(?i)malignant.*':'Other malignant neoplasms',
                        r'.*(?i)(benign|in.situ|myelodysplat|myeloproliferat|hematopoietic).*(cancer|neoplasm).*':'Other neoplasms',
                        r'.*(?i)cancer.*':'Other malignant neoplasms',
                        r'.*(?i)infectio.*':'Other unspecified infectious diseases',
                        r'.*(?i)sexually.*':'Sexually transmitted infections excluding HIV',
                        r'.*(?i)nutritional.deficien.*':'Other nutritional deficiencies',
                        r'.*ALS.*':'Motor neuron disease',
                        r'.*(?i)(skin|subcutaneous).*disease.*':'Other skin and subcutaneous diseases',
                        r'.*(?i)musculoskel.*':'Other musculoskeletal disorders',
                        r'.*':'Other'})

#Create search column and dummy for CauseFamily
all_reporter['SearchTerms'] = all_reporter['PROJECT_TITLE'] + all_reporter['PROJECT_TERMS']
all_reporter['CauseFamily'] = 'XXX'

#Search searchterms and categorize CauseFamily based on cause_search_library
pd.set_option('mode.chained_assignment', None)
for row in range(len(all_reporter)):
    for key in cause_search_library:
        if all_reporter['CauseFamily'][row] != 'XXX':
            break
        else:
            matching_key = re.match(key, all_reporter['SearchTerms'][row])
            if matching_key:
                all_reporter['CauseFamily'][row] = cause_search_library[key]

#Clean up remaining for joins
all_reporter = all_reporter.replace({'XXX':None})
all_reporter['AWARD_NOTICE_DATE'] = pd.to_datetime(all_reporter['AWARD_NOTICE_DATE'], infer_datetime_format = True)
all_reporter['BUDGET_END'] = pd.to_datetime(all_reporter['BUDGET_END'], infer_datetime_format = True)
all_reporter['BUDGET_START'] = pd.to_datetime(all_reporter['BUDGET_START'], infer_datetime_format = True)
all_reporter['PROJECT_START'] = pd.to_datetime(all_reporter['PROJECT_START'], infer_datetime_format = True)
all_reporter['APPLICATION_ID'] = all_reporter['APPLICATION_ID'].astype('object')

#Save prepped RePORTER data
all_reporter.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\all_reporter.csv')

#Join with hierarchy table and clean to create new master
reporter_cause = all_reporter.join(trim_cause_hierarchy.set_index('Cat C - Full'), on = 'CauseFamily')
reporter_cause_only = reporter_cause.drop(columns = ['ACTIVITY',
                                                    'APPLICATION_ID',
                                                    'APPLICATION_TYPE',
                                                    'BUDGET_END',
                                                    'BUDGET_START',
                                                    'CFDA_CODE',
                                                    'CORE_PROJECT_NUM',
                                                    'FOA_NUMBER',
                                                    'SUPPORT_YEAR',
                                                    'Cat A - Med',
                                                    'Cat B - Med',
                                                    'Cat C - Med',
                                                    'Cat D - Full'])
reporter_cause_only.drop(columns = ['FULL_PROJECT_NUM',
                                    'FUNDING_MECHANISM',
                                    'ORG_DISTRICT',
                                    'ORG_NAME',
                                    'SERIAL_NUMBER',
                                    'STUDY_SECTION',
                                    'STUDY_SECTION_NAME',
                                    'SUFFIX'],
                        inplace=True)

reporter_cause_year.to_csv('C:\\Users\\Justin\\Documents\\GitHub\\IncubatorProposal\\Data\\reporter_cause_year.csv')
